# Take-Home Assessment: Member Referral Dashboard

**Time Estimate**: 2-3 hours at most

Build a member referral system where users can invite others, track invitation status, and view analytics. Use whatever tools, libraries, and references you'd normally reach for.

**Note**: You don't need to actually send emails - assume the invitation is "sent" by creating an Invitation database record.

---

## What You'll Build

### 1. Invitation Form
Create a form to invite new members:
- First name and last name (required)
- Email address (required)

### 2. Referrals List
Display all referrals with:
- Name and email
- Date referred
- Status indicator (color-coded)
- Resend action (when applicable)

### 3. Resend Functionality
Allow users to resend invitations with appropriate restrictions.

### 4. Referrals API
A referral API for creating, reading, updating, and deleting invites.

### 5. Invite Token
Every invitation carries a token that an invitee would use to accept it (via a link like `/accept?token=...`). You don't need to build the accept page, but the token does need to work correctly on the backend:
- A token is generated when the invitation is created.
- A token must not be guessable or enumerable (don't use the row id or a short sequential value).
- Resending rotates the token - the previous token stops working.
- A token is single-purpose - it stops working once the referral has progressed past "Invitation Sent" (e.g. already joined or declined).
- Provide an endpoint that, given a token, returns the referral it belongs to (or an appropriate error). Treat this endpoint as if it were public - decide what it should return for a bad / expired / already-used token, and whether tokens expire at all.

### 6. Analytics API Endpoint
An endpoint for referral analytics.

---

## Design Reference

Match our website's visual style - some styles are included in the `tailwind.config.js` file.

**Style**:
- Use Tailwind CSS throughout
- Serif font for headings, sans-serif for body (or as similar as you can get)
- Rounded corners, proper spacing
- Status pills: fully rounded with appropriate colors
- Responsive layout
- As the icons are not provided, feel free to use something similar!

A screenshot reference is provided in the `assets/` folder.

---

## Technical Stack

### Backend: Django + Django REST Framework
- Create a `Referral` model with appropriate fields
- Implement RESTful API endpoints
- Handle validation on the server side
- No need to add real email sends - just add a small delay, then return your API response.
- Use PostgreSQL (via Docker)

### Frontend: Vue 3 + TypeScript
- Proper TypeScript types throughout (avoid `any`)
- Use Tailwind CSS for styling
- Fetch or axios for API calls

You may assume a single logged-in user - no need for real auth. (The token lookup in #5 should still be reasoned about as if public.)

---

## Feature Details

### Invitation Form

**Fields**:
- First Name (required)
- Last Name (required)
- Email (required)

**Important Validation**:
- **Email must be case-insensitive unique**: `test@example.com` and `TEST@EXAMPLE.COM` are the same person
- Show clear, helpful error messages

After successful submission, clear the form and update the referrals list.

---

### Referrals List

Display a table or card layout with:
- Full name (first + last)
- Email address
- Date referred
- Status with visual indicator

**Status Options**:
- Invitation Sent (gray)
- Application Received (blue)
- Joined (green)
- Declined (red)

Show an empty state when there are no referrals yet.

---

### Resend Invitation

Allow users to "resend" an invitation (simulated - just updates the database record).

**Business Rules**:
- Only show "Resend" button for referrals with status "Invitation Sent"
- **Cannot resend within 30 seconds** of the last send time
- When resend succeeds, update the `last_sent_at` timestamp to current time, and rotate the invite token (see #5)
- Show clear error message if cooldown period hasn't passed

No actual email needs to be sent - just add a delay, update the timestamp and return success.

---

### Analytics API

Return these metrics via an API endpoint:
- Total Invited
- Invitations Sent (count)
- Joined (count)
- Conversion Rate (%)

These aren't all spelled out for you - decide what "Total Invited" vs "Invitations Sent" mean, and what the numerator/denominator of "Conversion Rate" is. Pick sensible definitions and make the code match them.

If you're feeling up to it, you can display these nicely in some UI =)

---

## Critical Implementation Details

These requirements are important to get right:

### Email Handling
```
Store email in lowercase in the database
Validate uniqueness case-insensitively
Trim whitespace before saving

Example: "  Test@Example.com  " → "test@example.com"
```

### Resend Cooldown
```
Calculate time since last_sent_at
Reject resend if < 30 seconds
Return clear error message: "Cannot resend within 30 seconds"
Enforce on the server - the client may reflect it, but the server is the source of truth
```

### Status Workflow
```
New referrals start as "Invitation Sent"
Only "Invitation Sent" status allows resend
Status can progress forward but not backward
```

There's no required UI for changing a referral's status - advance it via the Django admin or shell when you need to (e.g. to check that a token stops working once the referral has joined). Whether and how to expose status changes is your call.

---

## Verification

Include tests. We're not looking for exhaustive coverage - we're looking for judgment about what's worth testing. At minimum, cover the parts most likely to break:
- Case-insensitive email uniqueness (including the `Test@Example.com` example)
- The 30-second resend cooldown (both the rejection and the allow path)
- Token rotation on resend (old token stops working) and the token no longer working once status has advanced

Backend tests can use Django's test runner (`manage.py test`). Frontend tests are welcome but not required.

---

## Code Review Exercise (~15 min)

`REVIEW_TASK.md` contains a sample resend endpoint written by another engineer. Review it as you would a teammate's PR: list the bugs and issues you find, ordered by severity, and show how you'd fix the most important one. Put your review in `REVIEW_TASK.md`.

---

## What We're Looking For

**Code Quality**:
- Clean, readable code with clear naming
- Proper component organization
- DRY principles (don't repeat yourself)
- TypeScript used effectively

**User Experience**:
- Intuitive interface that's easy to use and matches the design
- Works well on different screen sizes
- Clear feedback for user actions
- Thoughtful error handling

**Completeness**:
- All core features working
- Edge cases considered and handled
- Sensible defaults and validation

Think through what a real user would need and how they might use (or misuse) this feature.

---

## API Design

Design your API endpoints however makes sense to you. Here's an example structure:

```
GET    /api/referrals/          # List all referrals
POST   /api/referrals/          # Create new referral
POST   /api/referrals/{id}/resend/  # Resend invitation
GET    /api/referrals/lookup/?token=...  # Look up a referral by token
```

Use appropriate HTTP status codes (200, 201, 400, 404, 409) and return structured error responses.

---

## Setup

See `README.md` for complete setup instructions.

**Quick Start**:
```bash
# Backend
docker compose up -d
docker compose exec backend python manage.py migrate

# Frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

Backend runs on `http://localhost:8000`, frontend on `http://localhost:5173`.

---

## Submission

**Commit your work frequently** as you develop. We want to see your process, not just the final result.

**What to submit**:
- Link to your Git repository
- Keep your commit history (don't squash commits)
- `REVIEW_TASK.md` - your code review

---

## Evaluation

We'll evaluate based on:
- **Functionality** (25%): Do all features work correctly?
- **Verification & Testing** (25%): Did you convince yourself it works, and test the things most likely to break?
- **Code Quality** (15%): Is the code clean, organized, and maintainable?
- **API Design** (10%): Is the API well-structured and properly validated?
- **Code Review** (15%): Did the review catch the real issues, in order of importance?
- **User Experience** (10%): Is it intuitive, responsive, and polished?

---

## Tips

- Read through all requirements before starting
- Test your work — try to break it
- Commit small, logical changes as you go
- Focus on getting core features working first
- If you're unsure about something, document your assumptions

We're excited to see what you build. Good luck!
