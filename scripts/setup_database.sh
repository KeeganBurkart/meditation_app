#!/bin/sh
# Simple setup script to create the SQLite database using init_db.sql

DB_FILE="mindful_connect.db"
SCRIPT_DIR="$(dirname "$0")"

sqlite3 "$DB_FILE" < "$SCRIPT_DIR/init_db.sql"

echo "Database initialized: $DB_FILE"
