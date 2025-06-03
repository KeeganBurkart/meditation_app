import sys
from pathlib import Path
from datetime import date, time

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from sessions import MeditationSession
import dashboard


def sample_sessions():
    return [
        MeditationSession(
            duration_minutes=20,
            meditation_type="Guided",
            time_of_day=time(6, 0),
            session_date=date(2023, 1, 1),
            location="Home",
        ),
        MeditationSession(
            duration_minutes=25,
            meditation_type="Guided",
            time_of_day=time(6, 30),
            session_date=date(2023, 1, 2),
            location="Home",
        ),
        MeditationSession(
            duration_minutes=30,
            meditation_type="Guided",
            time_of_day=time(7, 0),
            session_date=date(2023, 1, 3),
            location="Home",
        ),
    ]


def test_total_time():
    sessions = sample_sessions()
    assert dashboard.calculate_total_time(sessions) == 75


def test_session_count():
    sessions = sample_sessions()
    assert dashboard.calculate_session_count(sessions) == 3


def test_current_streak():
    sessions = sample_sessions()
    assert dashboard.calculate_current_streak(sessions) == 3
