"""Utility helpers for Mindful Connect.

This module includes a basic math helper used in tests and minimal
database helpers for managing custom meditation types. The database
functions operate on a SQLite connection and rely on the schema in
``scripts/init_db.sql``.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def add_numbers(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def init_db(conn: sqlite3.Connection) -> None:
    """Initialize the database schema using ``init_db.sql``."""
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "init_db.sql"
    with open(script_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()


def add_custom_meditation_type(
    conn: sqlite3.Connection, user_id: int, type_name: str
) -> None:
    """Insert a custom meditation type for the given user."""
    conn.execute(
        "INSERT INTO custom_meditation_types (user_id, type_name) VALUES (?, ?)",
        (user_id, type_name),
    )
    conn.commit()


def get_custom_meditation_types(conn: sqlite3.Connection, user_id: int) -> list[str]:
    """Return a list of custom meditation type names for ``user_id``."""
    cur = conn.execute(
        "SELECT type_name FROM custom_meditation_types WHERE user_id = ?",
        (user_id,),
    )
    return [row[0] for row in cur.fetchall()]
