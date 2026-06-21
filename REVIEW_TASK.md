# Code Review Exercise

Another engineer submitted the resend endpoint below as a PR for review. **It runs and
passes their manual test** - treat it as a real PR.

Review it as you would a teammate's: list the bugs, correctness issues, and
design problems you find, **ordered by severity**. Then pick the single most
important one and show how you'd fix it (a few lines or a short description is
fine).

You do **not** need to wire this code into your project, this is only a review
exercise. Add your findings to the bottom of this file.

> Context: requirements say resend must (a) only work for "Invitation Sent"
> referrals, (b) be rejected within 30s of the last send, enforced server-side,
> and (c) rotate the invite token so the old one stops working.

```python
# referrals/views.py
from datetime import datetime, timedelta
import random

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Referral


@api_view(["POST"])
def resend_invitation(request, pk):
    referral = Referral.objects.get(pk=pk)

    last_sent = request.data.get("last_sent_at")
    if last_sent:
        elapsed = datetime.now() - datetime.fromisoformat(last_sent)
        if elapsed < timedelta(seconds=30):
            return Response({"error": "Cannot resend within 30 seconds"})

    # rotate the token
    referral.token = str(random.randint(100000, 999999))
    referral.last_sent_at = datetime.now()
    referral.save()

    return Response({"status": "sent", "token": referral.token})
```

---

## Your review

> List issues, most severe first. Then fix the top one.

### Issues

**1. Cooldown trusts the client, not the database (critical)**

The cooldown reads `last_sent_at` from `request.data`. If the client omits that field, the check never runs and they can resend immediately. They can also send an old timestamp to get around the 30-second rule. The requirements say this has to be enforced on the server, so we should use what's stored on the referral record.

**2. No status guard (critical)**

Nothing checks that the referral is still in `"Invitation Sent"`. You can resend for joined or declined referrals, which shouldn't be allowed and would keep rotating tokens when it doesn't make sense.

**3. Token is guessable (high)**

`random.randint(100000, 999999)` only gives you about 900k possible values. That's easy to brute force and doesn't match the requirement for a secure invite token. Something like `secrets.token_urlsafe(32)` would be a better fit.

**4. Missing referral returns 500 (high)**

`Referral.objects.get(pk=pk)` will blow up with `DoesNotExist` on a bad id and return a 500. That should be a 404 instead.

**5. Error responses use the wrong status code (medium)**

When the cooldown rejects the request, the message in the body is right but the status code defaults to 200. The frontend needs a 400 (or similar) to handle it as an error.

**6. Uses naive `datetime.now()` (medium)**

We're using plain `datetime.now()` here while the rest of Django typically uses timezone-aware datetimes. That can cause awkward comparisons against `last_sent_at` depending on how it's stored.

---

### Fix for #1

Drop the request body from the cooldown logic and use `referral.last_sent_at` from the database instead:

```python
from django.utils import timezone

# After fetching the referral...

if referral.last_sent_at:
    elapsed = timezone.now() - referral.last_sent_at
    if elapsed < timedelta(seconds=30):
        return Response(
            {"error": "Cannot resend within 30 seconds"},
            status=400,
        )
```

The client shouldn't send `last_sent_at` for this at all. The server already has the value it needs.
