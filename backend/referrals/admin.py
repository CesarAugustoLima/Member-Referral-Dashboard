"""Django admin configuration for referrals."""

from django.contrib import admin

from .models import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Admin UI for inspecting and updating referral records."""

    list_display = ("email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("first_name", "last_name", "email")
    readonly_fields = ("token", "created_at", "last_sent_at")
