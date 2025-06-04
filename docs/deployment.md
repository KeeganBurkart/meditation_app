# Deployment and Local Setup

This guide explains how to run the FastAPI server locally and how to initialize the database.

## Environment Variables

- `DB_FILE` – path to the SQLite database file. Both the server and `scripts/setup_database.sh` use this variable. It defaults to `mindful.db` if not set.

## Running the FastAPI Server

1. Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt fastapi uvicorn pydantic
   ```
2. Optionally set a custom database location:
   ```bash
   export DB_FILE=/path/to/mindful.db
   ```
3. Start the server with uvicorn:
   ```bash
   uvicorn backend.main:app --reload
   ```

## Deployment Scripts

The repository includes a simple script to create the SQLite database schema:

```bash
./scripts/setup_database.sh
```

The script respects the `DB_FILE` variable so you can create the database in a custom location:

```bash
DB_FILE=data.db ./scripts/setup_database.sh
```
