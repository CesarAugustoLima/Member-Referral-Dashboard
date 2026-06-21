# Member Referral Dashboard - Take-Home Assessment

## Overview

Build a member referral system where users can invite others, track invitation status, and view analytics.

**Note**: You don't need to actually send emails - assume the invitation is "sent" by creating an Invitation database record.

**Estimated Time**: 2-3 hours at most

Use whatever tools, libraries, and references you'd normally reach for while building.

## What You'll Build

- **Invitation Form**: Create referrals with name and email
- **Referrals List**: View all referrals with status indicators
- **Status Tracking**: Track referrals through their lifecycle
- **Resend Functionality**: Ability to resend invitations with business logic
- **Invite Token**: A non-guessable token per invite (see `REQUIREMENTS.md`)
- **Analytics API Endpoint**: Display basic metrics about referrals

You'll also complete **`REVIEW_TASK.md`** (a quick code-review exercise). Include tests - see `REQUIREMENTS.md` for details.

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Node.js** (v18+) and **npm** installed
- **Git** for version control
- Basic knowledge of Vue 3 or a similar frontend framework, TypeScript, Django, and REST APIs

## Project Structure

```
assessment/
├── frontend/          # Vue 3 + TypeScript + Vite
│   ├── src/
│   │   ├── components/   # Build your components here
│   │   ├── stores/       # Pinia stores (if used)
│   │   ├── types/        # TypeScript interfaces
│   │   └── App.vue       # Main app component
│   └── package.json
├── backend/           # Django + DRF
│   ├── config/           # Django settings
│   ├── referrals/        # Referrals app (add your code here)
│   └── requirements.txt
├── docker-compose.yml # PostgreSQL + backend setup
└── REQUIREMENTS.md    # Detailed feature requirements
```

## Setup Instructions

### 1. Download/clone and Navigate

```bash
cd assessment
```

### 2. Start Database and Backend

```bash
# Start PostgreSQL and Django backend
docker compose up -d

# Run initial migrations
docker compose exec backend python manage.py migrate

# Verify backend is running (Django welcome page until you wire up routes)
curl http://localhost:8000/
```

The backend will be available at `http://localhost:8000`

### 3. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Development Workflow

### Backend Development

```bash
# Create migrations after model changes
docker compose exec backend python manage.py makemigrations

# Run migrations
docker compose exec backend python manage.py migrate

# Access Django shell
docker compose exec backend python manage.py shell

# View logs
docker compose logs -f backend

# Restart backend after code changes
docker compose restart backend
```

### Frontend Development

The Vite dev server has hot reload enabled - changes will appear automatically.

```bash
# Run from frontend/ directory
npm run dev

# Build for production (helpful to check typescript errors!)
npm run build
```

### Database Access

```bash
# Access PostgreSQL directly
docker compose exec db psql -U postgres -d referrals
```

## Key Requirements

See `REQUIREMENTS.md` for detailed feature specifications.

## Technology Stack

### Frontend

- **Vue 3** with Composition API
- **TypeScript** (no vanilla JavaScript please)
- **Vite** for build tooling/serving frontend
- **Pinia** for state management (if needed)
- **Tailwind CSS** for styling
- **Axios** for API calls (if not using `fetch`)

### Backend

- **Django 5.1**
- **Django REST Framework**
- **PostgreSQL** via Docker
- **CORS** configured for local development

## Troubleshooting

### Backend won't start

```bash
# Check logs
docker compose logs backend

# Rebuild containers
docker compose down
docker compose up --build
```

### Database connection errors

```bash
# Ensure database is healthy
docker compose ps

# Reset database (caution: deletes all data)
docker compose down -v
docker compose up -d
```

### Frontend can't connect to backend

- Verify backend is running: `curl http://localhost:8000/`
- Check `.env` file has correct `VITE_API_URL=http://localhost:8000/api`
- Check CORS settings in Django `settings.py`


## Questions or Issues?

If you encounter any setup issues or have questions about requirements:

1. Check the troubleshooting section above
2. Review `REQUIREMENTS.md` for detailed specifications
3. Contact your interviewer for clarification

Good luck! We're excited to see what you build.
