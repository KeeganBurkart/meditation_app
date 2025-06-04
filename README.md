# Mindful Connect

Mindful Connect is a meditation tracking and social platform consisting of an iOS app and a companion website.

## Features

- Track meditation sessions and moods
- Earn badges for completing challenges
- Create challenges with optional private visibility
- Personalized activity feed that respects user privacy settings
- Follow other users and manage your network
- Activity feed to view friends' sessions and send encouragement
- Sign up with email or social login providers

## Community Challenges
Mindful Connect supports community meditation challenges where users can join and log their progress toward a shared goal. The helper functions in `src/mindful.py` manage challenge creation, participation, and minute tracking.

## Technology Stack

The following tools and frameworks will be used for the project:

### iOS App
- **Language**: Swift 5
- **UI Framework**: SwiftUI
- **State Management**: Combine

### Web App
- **Framework**: React with TypeScript
- **Routing**: React Router
- **Styling**: CSS Modules or styled-components
- The web frontend lives under `web/frontend`.

### Backend
- **Language**: Python 3.10
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **API Style**: RESTful endpoints

These technologies were chosen for their strong community support, modern feature sets, and the ability to scale both the mobile and web experiences consistently.

## Dashboard Analytics

The `src/dashboard.py` module provides helper functions to calculate total meditation time, session count, and current streaks from a list of `MeditationSession` objects.

## Running the Web App

Install Node dependencies inside `web/frontend` and run the Vite dev server:

```bash
cd web/frontend
npm install
# copy the example environment file and set your backend URL if needed
cp .env.example .env
npm run dev
```

The `.env` file contains a `VITE_API_URL` variable that should point to your backend API. By default it targets `http://localhost:8000`.

The backend API can be started with:

```bash
uvicorn backend.main:app --reload
```

Install the backend Python dependencies before running the API or tests:

```bash
python -m pip install -r requirements.txt
# passlib is required for password hashing
```

With the requirements installed, the test suite can be executed using:

```bash
pytest
```

Additional details on environment variables and deployment scripts are available in [docs/deployment.md](docs/deployment.md).

## Monetization

Mindful Connect includes a Premium tier that unlocks advanced statistics,
unlimited friends, and private challenges. The `subscriptions` module tracks a
user's tier so the app can gate these features. Free tier users may see small
text advertisements served via the `ads` module.

