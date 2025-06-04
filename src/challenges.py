"""Simple challenge and badge helpers."""

from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from typing import Iterable


def create_challenge(
    conn: sqlite3.Connection,
    name: str,
    created_by: int,
    *,
    is_private: bool = False,
    target_minutes: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    description: str | None = None,
) -> int:
    """Insert a challenge and return its ID."""
    cur = conn.execute(
        "INSERT INTO challenges (name, created_by, is_private, target_minutes, start_date, end_date, description)"
        " VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING id",
        (
            name,
            created_by,
            int(is_private),
            target_minutes,
            start_date,
            end_date,
            description,
        ),
    )
    challenge_id = cur.fetchone()[0]
    conn.commit()
    return challenge_id


def award_badge(conn: sqlite3.Connection, user_id: int, badge_name: str) -> None:
    """Award a badge to the given user."""
    conn.execute(
        "INSERT INTO badges (user_id, badge_name) VALUES (?, ?)",
        (user_id, badge_name),
    )
    conn.commit()


def get_user_badges(conn: sqlite3.Connection, user_id: int) -> list[tuple[str, str]]:
    """Return ``(badge_name, awarded_at)`` tuples for ``user_id``."""
    cur = conn.execute(
        "SELECT badge_name, awarded_at FROM badges WHERE user_id = ? ORDER BY awarded_at",
        (user_id,),
    )
    return [(row[0], row[1]) for row in cur.fetchall()]


def get_private_challenges(conn: sqlite3.Connection, user_id: int) -> list[tuple]:
    """Return all private challenges created by ``user_id``."""
    cur = conn.execute(
        "SELECT id, name, target_minutes, start_date, end_date, description FROM challenges"
        " WHERE created_by = ? AND is_private = 1",
        (user_id,),
    )
    return [tuple(row) for row in cur.fetchall()]


def update_private_challenge(
    conn: sqlite3.Connection,
    user_id: int,
    challenge_id: int,
    name: str,
    target_minutes: int,
    start_date: str,
    end_date: str,
    description: str | None = None,
) -> None:
    """Update a private challenge owned by ``user_id``."""
    conn.execute(
        "UPDATE challenges SET name = ?, target_minutes = ?, start_date = ?, end_date = ?, description = ?"
        " WHERE id = ? AND created_by = ? AND is_private = 1",
        (
            name,
            target_minutes,
            start_date,
            end_date,
            description,
            challenge_id,
            user_id,
        ),
    )
    conn.commit()


def delete_private_challenge(conn: sqlite3.Connection, user_id: int, challenge_id: int) -> None:
    """Delete a private challenge owned by ``user_id``."""
    conn.execute(
        "DELETE FROM challenges WHERE id = ? AND created_by = ? AND is_private = 1",
        (challenge_id, user_id),
    )
    conn.commit()


def current_streak(dates: Iterable[date]) -> int:
    """Return the current streak length given a collection of ``date`` objects."""
    unique_dates = sorted(set(dates), reverse=True)
    if not unique_dates:
        return 0

    streak = 1
    for prev, curr in zip(unique_dates, unique_dates[1:]):
        if prev - curr == timedelta(days=1):
            streak += 1
        else:
            break
    return streak


class StreakChallenge:
    """Challenge based on maintaining a daily streak."""

    def __init__(self, target_days: int) -> None:
        self.target_days = target_days

    def is_completed(self, dates: Iterable[date]) -> bool:
        """Return ``True`` if ``dates`` achieve the required streak."""
        return current_streak(dates) >= self.target_days


class DurationChallenge:
    """Challenge based on accumulating a total number of minutes."""

    def __init__(self, target_minutes: int) -> None:
        self.target_minutes = target_minutes

    def is_completed(self, durations: Iterable[int]) -> bool:
        """Return ``True`` if total minutes meets or exceeds the target."""
        return sum(durations) >= self.target_minutes
