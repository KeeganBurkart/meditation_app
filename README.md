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
A small HTML/JavaScript timer is included under the `web/` folder so the basic timing functionality can also be used in the browser. Open `web/index.html` to try it locally. A simple profile page is available at `web/profile.html` to view user stats stored in the browser.

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
- A simple HTML form for logging meditation sessions is available at
  `web/session_form.html`.

### Backend
- **Language**: Python 3.10
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **API Style**: RESTful endpoints

These technologies were chosen for their strong community support, modern feature sets, and the ability to scale both the mobile and web experiences consistently.

## Dashboard Analytics

The `src/dashboard.py` module provides helper functions to calculate total meditation time, session count, and current streaks from a list of `MeditationSession` objects.

## Monetization

Mindful Connect includes a Premium tier that unlocks advanced statistics,
unlimited friends, and private challenges. The `subscriptions` module tracks a
user's tier so the app can gate these features. Free tier users may see small
text advertisements served via the `ads` module.

