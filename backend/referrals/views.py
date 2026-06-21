"""REST API views for referrals."""

import time

from rest_framework import viewsets

from .models import Referral
from .serializers import ReferralSerializer


class ReferralViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for member referrals."""

    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

    def perform_create(self, serializer) -> None:
        """Simulate sending an invitation email before persisting."""
        time.sleep(0.5)
        serializer.save()
