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
3. Initialize the database:
   ```bash
   ./scripts/setup_database.sh
   ```
   Or set the `DATABASE_URL` environment variable to connect to a PostgreSQL instance.
4. Start the server:
   ```bash
   uvicorn backend.main:app --reload
   ```

The API uses an SQLite database at the location specified by `DB_FILE` or `mindful.db` if the variable is not set. The database will be created automatically on first run.
