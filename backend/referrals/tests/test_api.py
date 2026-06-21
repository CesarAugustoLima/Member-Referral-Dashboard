"""Tests for the referrals REST API."""

from unittest.mock import patch

from django.urls import reverse
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
