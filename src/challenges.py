"""Simple challenge and badge helpers."""

from __future__ import annotations

import sqlite3


def create_challenge(
    conn: sqlite3.Connection,
    name: str,
    created_by: int,
    *,
    is_private: bool = False,
) -> int:
    """Insert a challenge and return its ID."""
    cur = conn.execute(
        "INSERT INTO challenges (name, created_by, is_private) VALUES (?, ?, ?)",
        (name, created_by, int(is_private)),
    )
    conn.commit()
    return cur.lastrowid


def award_badge(conn: sqlite3.Connection, user_id: int, badge_name: str) -> None:
    """Award a badge to the given user."""
    conn.execute(
        "INSERT INTO badges (user_id, badge_name) VALUES (?, ?)",
        (user_id, badge_name),
    )
    conn.commit()


def get_user_badges(conn: sqlite3.Connection, user_id: int) -> list[str]:
    """Return a list of badge names for ``user_id``."""
    cur = conn.execute(
        "SELECT badge_name FROM badges WHERE user_id = ? ORDER BY awarded_at",
        (user_id,),
    )
    return [row[0] for row in cur.fetchall()]

