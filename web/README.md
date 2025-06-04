# Web App

This folder contains a React + TypeScript project built with Vite.
The application lives in `frontend/` and communicates with the FastAPI backend under `backend/`.

## Getting Started

Install Node dependencies and start the development server:

```bash
cd web/frontend
npm install
npm run dev
```

Start the backend API in another terminal:

```bash
uvicorn backend.main:app --reload
```

Open the printed local URL to access the app.

## Deployment

To create a production build of the web app, run:

```bash
cd web/frontend
npm install
npm run build
```

The compiled files are placed in `web/frontend/dist`. Copy this folder to any
static web host or serve it with a CDN alongside the backend API.
