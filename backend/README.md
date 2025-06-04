# Backend Services

A small FastAPI application is provided to experiment with the web frontend.

## Running Locally

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt fastapi uvicorn pydantic
   ```
3. (Optional) specify a custom database path using the `DB_FILE` environment variable.
4. Start the server:
   ```bash
   uvicorn backend.main:app --reload
   ```

The API uses an SQLite database defined by `DB_FILE` (default `mindful.db`). It will be created automatically on first run.
