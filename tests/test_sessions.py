from datetime import date, time

from src.sessions import MeditationSession

def test_session_creation():
    session = MeditationSession(
        duration_minutes=30,
        meditation_type="Guided",
        time_of_day=time(6, 30),
        session_date=date(2023, 1, 1),
        location="Home",
        mood_before=5,
        mood_after=8,
    )
    assert session.duration_minutes == 30
    assert session.meditation_type == "Guided"
    assert session.time_of_day == time(6, 30)
    assert session.session_date == date(2023, 1, 1)
    assert session.location == "Home"
    assert session.mood_before == 5
    assert session.mood_after == 8
