"""Referral analytics metric definitions and computation.

Metrics:
- total_invited: all referral records ever created
- invitations_sent: referrals still pending with status ``invitation_sent``
- joined: referrals with status ``joined``
- conversion_rate: joined / total_invited * 100 (0.0 when total_invited is 0)
"""

from django.db.models import Count, Q

from .models import Referral


def get_referral_analytics() -> dict[str, float | int]:
    """Return referral counts and conversion rate in a single query."""
    stats = Referral.objects.aggregate(
        total_invited=Count("id"),
        invitations_sent=Count(
            "id",
            filter=Q(status=Referral.Status.INVITATION_SENT),
        ),
        joined=Count("id", filter=Q(status=Referral.Status.JOINED)),
    )

    total_invited = stats["total_invited"]
    joined = stats["joined"]
    conversion_rate = (joined / total_invited * 100) if total_invited else 0.0

    return {
        "total_invited": total_invited,
        "invitations_sent": stats["invitations_sent"],
        "joined": joined,
        "conversion_rate": round(conversion_rate, 1),
    }
