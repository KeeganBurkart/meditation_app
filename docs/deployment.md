# Deployment Guide

This document outlines how to run the FastAPI backend and PostgreSQL database in
production using Docker as well as the steps to build the web interface.

## Backend and Database

1. Ensure Docker is installed.
2. Run the deployment script:

```bash
./scripts/deploy_backend.sh
```

This uses `docker-compose.yml` to start a PostgreSQL container and build the
backend image defined by the `Dockerfile`. The database is automatically
initialized from `scripts/init_db_postgres.sql`. The backend listens on port
`8000` and connects to the database using the `DATABASE_URL` environment
variable.

## Web Application

To prepare the web frontend for production:

```bash
cd web/frontend
npm install
npm run build
```

The `dist/` directory contains static files that can be served by any web host
or CDN alongside the backend API.
