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

1. …
