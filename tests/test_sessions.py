import sys
from pathlib import Path
from datetime import date, time

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from sessions import MeditationSession


def test_session_creation():
    session = MeditationSession(
        duration_minutes=30,
        meditation_type="Guided",
        time_of_day=time(6, 30),
        session_date=date(2023, 1, 1),
        location="Home",
    )
    assert session.duration_minutes == 30
    assert session.meditation_type == "Guided"
    assert session.time_of_day == time(6, 30)
    assert session.session_date == date(2023, 1, 1)
    assert session.location == "Home"

