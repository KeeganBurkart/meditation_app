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

