"""Utility functions for the referrals app."""

import secrets


def generate_token() -> str:
    """Return a cryptographically secure, non-guessable invite token."""
    return secrets.token_urlsafe(32)
