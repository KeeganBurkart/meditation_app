from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class MeditationSession:
    """Data model for a meditation session."""

    duration_minutes: int
    meditation_type: str
    time_of_day: time
    session_date: date
    location: str
    mood_before: Optional[int] = None
    mood_after: Optional[int] = None
