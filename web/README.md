# Web App

This folder now contains a small React + TypeScript project built with Vite.
The original HTML pages remain for reference, but the new application lives in
`frontend/` and communicates with the FastAPI backend under `backend/`.

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

Open the printed local URL to use the timer, session form and other pages.
