"""Utility helpers for Mindful Connect.

This module includes a basic math helper used in tests and minimal
database helpers for managing custom meditation types. The database
functions operate on a SQLite connection and rely on the schema in
``scripts/init_db.sql``.
"""

from __future__ import annotations

import sqlite3
from typing import Any
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


def init_postgres_db(conn: Any) -> None:
    """Initialize a PostgreSQL database using ``init_db_postgres.sql``."""
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "init_db_postgres.sql"
    with open(script_path, "r", encoding="utf-8") as f:
        sql = f.read()
    cur = conn.cursor()
    for statement in sql.split(';'):
        stmt = statement.strip()
        if stmt:
            cur.execute(stmt + ';')
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


def create_challenge(
    conn: sqlite3.Connection,
    name: str,
    target_minutes: int,
    start_date: str,
    end_date: str,
) -> int:
    """Create a community challenge and return its ID."""
    cur = conn.execute(
        "INSERT INTO community_challenges (name, target_minutes, start_date, end_date)"
        " VALUES (?, ?, ?, ?)",
        (name, target_minutes, start_date, end_date),
    )
    conn.commit()
    return cur.lastrowid


def join_challenge(conn: sqlite3.Connection, user_id: int, challenge_id: int) -> None:
    """Join a community challenge if not already joined."""
    conn.execute(
        "INSERT OR IGNORE INTO challenge_progress (user_id, challenge_id) VALUES (?, ?)",
        (user_id, challenge_id),
    )
    conn.commit()


def log_challenge_progress(
    conn: sqlite3.Connection, user_id: int, challenge_id: int, minutes: int
) -> None:
    """Increment progress for a user's challenge participation."""
    conn.execute(
        "UPDATE challenge_progress SET minutes = minutes + ? "
        "WHERE user_id = ? AND challenge_id = ?",
        (minutes, user_id, challenge_id),
    )
    conn.commit()


def get_challenge_progress(
    conn: sqlite3.Connection, user_id: int, challenge_id: int
) -> int:
    """Return current progress in minutes for ``user_id`` in ``challenge_id``."""
    cur = conn.execute(
        "SELECT minutes FROM challenge_progress WHERE user_id = ? AND challenge_id = ?",
        (user_id, challenge_id),
    )
    row = cur.fetchone()
    return row[0] if row else 0


def log_session(
    conn: sqlite3.Connection,
    user_id: int,
    duration: int,
    session_type: str,
    session_date: str,
    *,
    notes: str | None = None,
    mood_before: int | None = None,
    mood_after: int | None = None,
) -> int:
    """Insert a session and optional mood data and return the session ID."""

    cur = conn.execute(
        "INSERT INTO sessions (user_id, duration, session_type, session_date, notes) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, duration, session_type, session_date, notes),
    )
    session_id = cur.lastrowid

    if mood_before is not None or mood_after is not None:
        conn.execute(
            "INSERT INTO moods (session_id, mood_before, mood_after) VALUES (?, ?, ?)",
            (session_id, mood_before, mood_after),
        )

    conn.commit()
    return session_id


def get_user_moods(conn: sqlite3.Connection, user_id: int) -> list[tuple[int | None, int | None]]:
    """Return ``(mood_before, mood_after)`` pairs for all of ``user_id``'s sessions."""

    cur = conn.execute(
        "SELECT m.mood_before, m.mood_after FROM moods m "
        "JOIN sessions s ON m.session_id = s.id WHERE s.user_id = ?",
        (user_id,),
    )
    return [(row[0], row[1]) for row in cur.fetchall()]

