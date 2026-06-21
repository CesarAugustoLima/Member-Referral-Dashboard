"""URL routing for the referrals API."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReferralViewSet

router = DefaultRouter()
router.register(r"", ReferralViewSet, basename="referral")

urlpatterns = [
    path("", include(router.urls)),
]
