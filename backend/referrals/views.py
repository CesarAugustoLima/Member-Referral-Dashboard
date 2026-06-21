"""REST API views for referrals."""

import time

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .analytics import get_referral_analytics
from .models import Referral
from .serializers import ReferralPublicSerializer, ReferralSerializer


class ReferralViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for member referrals."""

    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

    def perform_create(self, serializer) -> None:
        """Simulate sending an invitation email before persisting."""
        time.sleep(0.5)
        serializer.save()

    @action(detail=True, methods=["post"])
    def resend(self, request, pk=None) -> Response:
        """Resend an invitation for a referral in 'Invitation Sent' status."""
        referral = self.get_object()
        error = referral.resend_error()
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        time.sleep(0.5)
        referral.resend()
        serializer = self.get_serializer(referral)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="lookup")
    def lookup(self, request) -> Response:
        """Look up a referral by invite token (public endpoint)."""
        token = request.query_params.get("token")
        if not token:
            return Response(
                {"error": "Token query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            referral = Referral.objects.get(token=token)
        except Referral.DoesNotExist:
            return Response(
                {"error": "Invalid invitation token."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if referral.status != Referral.Status.INVITATION_SENT:
            return Response(
                {"error": "Invitation already used."},
                status=status.HTTP_410_GONE,
            )

        serializer = ReferralPublicSerializer(referral)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def analytics(self, request) -> Response:
        """Return aggregate referral metrics."""
        return Response(get_referral_analytics())
