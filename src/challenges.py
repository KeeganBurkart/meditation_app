"""Challenge logic for Mindful Connect.

This module provides simple utility classes and functions for evaluating
streak and duration based challenges.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable


def current_streak(dates: Iterable[date]) -> int:
    """Return the current consecutive-day streak from ``dates``.

    The streak is calculated using the most recent date in the list and
    counts backward until a gap is encountered. Duplicate dates are ignored.
    """
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


def total_duration(durations: Iterable[int]) -> int:
    """Return the sum of ``durations`` in minutes."""
    return sum(durations)


@dataclass
class StreakChallenge:
    """Challenge requiring a consecutive-day streak."""

    target_days: int

    def is_completed(self, session_dates: Iterable[date]) -> bool:
        """Return ``True`` if ``session_dates`` meet the target streak."""
        return current_streak(session_dates) >= self.target_days


@dataclass
class DurationChallenge:
    """Challenge requiring a total duration."""

    target_minutes: int

    def is_completed(self, durations: Iterable[int]) -> bool:
        """Return ``True`` if the total duration meets ``target_minutes``."""
        return total_duration(durations) >= self.target_minutes
