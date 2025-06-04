from datetime import date, time

from src import analytics
from src.sessions import MeditationSession


def sample_sessions():
    return [
        MeditationSession(
            duration_minutes=10,
            meditation_type="Zen",
            time_of_day=time(6, 0),
            session_date=date(2023, 1, 1),
            location="Home",
            mood_before=3,
            mood_after=6,
        ),
        MeditationSession(
            duration_minutes=15,
            meditation_type="Guided",
            time_of_day=time(7, 0),
            session_date=date(2023, 1, 1),
            location="Home",
            mood_before=4,
            mood_after=7,
        ),
        MeditationSession(
            duration_minutes=20,
            meditation_type="Mantra",
            time_of_day=time(20, 0),
            session_date=date(2023, 1, 2),
            location="Park",
            mood_before=5,
            mood_after=8,
        ),
    ]


def test_consistency_over_time():
    sessions = sample_sessions()
    result = analytics.consistency_over_time(sessions)
    assert result == {date(2023, 1, 1): 2, date(2023, 1, 2): 1}


def test_mood_correlation_points():
    sessions = sample_sessions()
    result = analytics.mood_correlation_points(sessions)
    assert result == [(3, 6), (4, 7), (5, 8)]


def test_time_of_day_distribution():
    sessions = sample_sessions()
    result = analytics.time_of_day_distribution(sessions)
    assert result == {6: 1, 7: 1, 20: 1}


def test_location_frequency():
    sessions = sample_sessions()
    result = analytics.location_frequency(sessions)
    assert result == {"Home": 2, "Park": 1}
