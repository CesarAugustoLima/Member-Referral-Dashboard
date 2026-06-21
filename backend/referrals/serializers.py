"""Serializers for the referrals API."""

from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Referral


class EmailAlreadyExistsError(APIException):
    """Raised when a referral already exists for the given email."""

    status_code = 409

    def __init__(self) -> None:
        super().__init__({"error": "A referral with this email already exists."})


class ReferralSerializer(serializers.ModelSerializer):
    """Serialize referral records for API consumption."""

    class Meta:
        model = Referral
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "status",
            "created_at",
            "last_sent_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "last_sent_at",
        ]

    def validate_email(self, value: str) -> str:
        """Normalize email and enforce case-insensitive uniqueness."""
        email = value.strip().lower()
        if not email:
            raise serializers.ValidationError("Email is required.")

        queryset = Referral.objects.filter(email__iexact=email)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise EmailAlreadyExistsError()

        return email
