"""Tests for the referrals REST API."""

from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from referrals.models import Referral
from referrals.tests.factories import create_referral


class ReferralAPITests(APITestCase):
    """Integration tests for referral CRUD endpoints."""

    list_url = reverse("referral-list")

    def _payload(self, **overrides):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
        }
        data.update(overrides)
        return data

    @patch("referrals.views.time.sleep")
    def test_create_referral_succeeds_with_expected_defaults(self, mock_sleep) -> None:
        response = self.client.post(self.list_url, self._payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Referral.Status.INVITATION_SENT)
        self.assertIsNotNone(response.data["last_sent_at"])
        self.assertEqual(response.data["email"], "jane@example.com")

        referral = Referral.objects.get(pk=response.data["id"])
        self.assertTrue(referral.token)
        mock_sleep.assert_called_once()

    @patch("referrals.views.time.sleep")
    def test_duplicate_email_is_rejected_case_insensitively(self, mock_sleep) -> None:
        create_referral(email="test@example.com")

        response = self.client.post(
            self.list_url,
            self._payload(email="TEST@EXAMPLE.COM"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data,
            {"error": "A referral with this email already exists."},
        )
        mock_sleep.assert_not_called()

    @patch("referrals.views.time.sleep")
    def test_list_returns_created_referrals(self, mock_sleep) -> None:
        create_referral(email="alice@example.com", first_name="Alice")
        create_referral(email="bob@example.com", first_name="Bob", last_name="Smith")

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        emails = {item["email"] for item in response.data["results"]}
        self.assertEqual(emails, {"alice@example.com", "bob@example.com"})

    def test_resend_rejected_within_cooldown(self) -> None:
        referral = create_referral(email="cooldown@example.com")

        response = self.client.post(reverse("referral-resend", args=[referral.pk]))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Cannot resend within 30 seconds"})

    @patch("referrals.views.time.sleep")
    def test_resend_allowed_after_cooldown(self, mock_sleep) -> None:
        referral = create_referral(email="resend@example.com")
        referral.last_sent_at = timezone.now() - timedelta(seconds=31)
        referral.save(update_fields=["last_sent_at"])

        response = self.client.post(reverse("referral-resend", args=[referral.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_sleep.assert_called_once()

    @patch("referrals.views.time.sleep")
    def test_resend_rotates_token(self, mock_sleep) -> None:
        referral = create_referral(email="rotate@example.com")
        old_token = referral.token
        referral.last_sent_at = timezone.now() - timedelta(seconds=31)
        referral.save(update_fields=["last_sent_at"])

        response = self.client.post(reverse("referral-resend", args=[referral.pk]))
        referral.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(referral.token, old_token)

        lookup_url = reverse("referral-lookup")
        old_lookup = self.client.get(lookup_url, {"token": old_token})
        new_lookup = self.client.get(lookup_url, {"token": referral.token})

        self.assertEqual(old_lookup.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(new_lookup.status_code, status.HTTP_200_OK)

    def test_resend_rejected_when_status_is_not_invitation_sent(self) -> None:
        referral = create_referral(
            email="joined@example.com",
            status=Referral.Status.JOINED,
        )

        response = self.client.post(reverse("referral-resend", args=[referral.pk]))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_lookup_returns_referral_for_valid_token(self) -> None:
        referral = create_referral(email="lookup@example.com")

        response = self.client.get(
            reverse("referral-lookup"),
            {"token": referral.token},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "lookup@example.com")
        self.assertNotIn("id", response.data)
        self.assertNotIn("status", response.data)

    def test_lookup_rejects_invalid_token(self) -> None:
        response = self.client.get(
            reverse("referral-lookup"),
            {"token": "invalid-token"},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lookup_rejects_token_after_status_advances(self) -> None:
        referral = create_referral(
            email="used@example.com",
            status=Referral.Status.JOINED,
        )

        response = self.client.get(
            reverse("referral-lookup"),
            {"token": referral.token},
        )

        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        self.assertEqual(response.data, {"error": "Invitation already used."})

    def test_analytics_returns_zero_for_empty_database(self) -> None:
        response = self.client.get(reverse("referral-analytics"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "total_invited": 0,
                "invitations_sent": 0,
                "joined": 0,
                "conversion_rate": 0.0,
            },
        )

    def test_analytics_returns_correct_counts(self) -> None:
        create_referral(email="sent1@example.com", status=Referral.Status.INVITATION_SENT)
        create_referral(email="sent2@example.com", status=Referral.Status.INVITATION_SENT)
        create_referral(email="joined@example.com", status=Referral.Status.JOINED)
        create_referral(email="declined@example.com", status=Referral.Status.DECLINED)
        create_referral(
            email="received@example.com",
            status=Referral.Status.APPLICATION_RECEIVED,
        )

        response = self.client.get(reverse("referral-analytics"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_invited"], 5)
        self.assertEqual(response.data["invitations_sent"], 2)
        self.assertEqual(response.data["joined"], 1)
        self.assertEqual(response.data["conversion_rate"], 20.0)

