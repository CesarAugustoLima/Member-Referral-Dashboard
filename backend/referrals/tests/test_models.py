"""Tests for Referral model behavior."""

from django.test import TestCase
from django.utils import timezone

from referrals.models import Referral


class ReferralModelTests(TestCase):
    """Unit tests for Referral persistence and normalization."""

    def test_email_is_trimmed_and_lowercased_on_save(self) -> None:
        referral = Referral.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="  Test@Example.com  ",
        )

        referral.refresh_from_db()
        self.assertEqual(referral.email, "test@example.com")

    def test_token_and_last_sent_at_set_on_first_save(self) -> None:
        before = timezone.now()
        referral = Referral.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
        )
        after = timezone.now()

        self.assertTrue(referral.token)
        self.assertGreaterEqual(len(referral.token), 32)
        self.assertIsNotNone(referral.last_sent_at)
        self.assertGreaterEqual(referral.last_sent_at, before)
        self.assertLessEqual(referral.last_sent_at, after)
        self.assertEqual(referral.status, Referral.Status.INVITATION_SENT)
