"""Test helpers for creating referral records."""

from referrals.models import Referral


def create_referral(**kwargs) -> Referral:
    """Create a Referral with sensible defaults for tests."""
    defaults = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
    }
    defaults.update(kwargs)
    return Referral.objects.create(**defaults)
