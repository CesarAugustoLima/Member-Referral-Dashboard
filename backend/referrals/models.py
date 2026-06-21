"""Database models for member referrals."""

from datetime import timedelta

from django.db import models
from django.utils import timezone

from .services import generate_token

RESEND_COOLDOWN_SECONDS = 30


class Referral(models.Model):
    """A member referral invitation and its lifecycle status."""

    class Status(models.TextChoices):
        INVITATION_SENT = "invitation_sent", "Invitation Sent"
        APPLICATION_RECEIVED = "application_received", "Application Received"
        JOINED = "joined", "Joined"
        DECLINED = "declined", "Declined"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.INVITATION_SENT,
    )
    token = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} <{self.email}>"

    def normalize_email(self) -> None:
        """Trim whitespace and lowercase the email address."""
        if self.email:
            self.email = self.email.strip().lower()

    def clean(self) -> None:
        super().clean()
        self.normalize_email()

    def save(self, *args, **kwargs) -> None:
        self.normalize_email()
        if not self.token:
            self.token = generate_token()
        if self.last_sent_at is None:
            self.last_sent_at = timezone.now()
        super().save(*args, **kwargs)

    def resend_error(self) -> str | None:
        """Return an error message if resend is not allowed, otherwise None."""
        if self.status != self.Status.INVITATION_SENT:
            return "Invitation can only be resent while status is 'Invitation Sent'."

        if self.last_sent_at is not None:
            elapsed = timezone.now() - self.last_sent_at
            if elapsed < timedelta(seconds=RESEND_COOLDOWN_SECONDS):
                return "Cannot resend within 30 seconds"

        return None

    def resend(self) -> None:
        """Rotate the invite token and update the last sent timestamp."""
        error = self.resend_error()
        if error:
            raise ValueError(error)

        self.token = generate_token()
        self.last_sent_at = timezone.now()
        self.save(update_fields=["token", "last_sent_at"])
