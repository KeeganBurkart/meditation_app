"""Dashboard statistics utilities for Mindful Connect."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Iterable

from .sessions import MeditationSession


def calculate_total_time(sessions: Iterable[MeditationSession]) -> int:
    """Return the total meditation time in minutes for all ``sessions``."""
    return sum(session.duration_minutes for session in sessions)


def calculate_session_count(sessions: Iterable[MeditationSession]) -> int:
    """Return the total number of sessions."""
    return sum(1 for _ in sessions)


def calculate_current_streak(sessions: Iterable[MeditationSession]) -> int:
    """Return the current daily streak length.

    Streaks are computed by looking at unique session dates sorted in
    descending order. Starting from the most recent date, consecutive
    days with at least one session count toward the streak.
    """
    # Get unique dates from sessions
    unique_dates = sorted({s.session_date for s in sessions}, reverse=True)

    if not unique_dates:
        return 0

    streak = 1
    for prev, curr in zip(unique_dates, unique_dates[1:]):
        if prev - curr == timedelta(days=1):
            streak += 1
        else:
            break
    return streak
