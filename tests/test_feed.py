from datetime import date, time

from src.sessions import MeditationSession
from src.feed import build_feed


def sample_sessions() -> dict[int, list[MeditationSession]]:
    return {
        1: [MeditationSession(10, "Zen", time(6, 0), date(2023, 1, 1), "Home")],
        2: [MeditationSession(15, "Guided", time(7, 0), date(2023, 1, 1), "Home")],
    }


def test_feed_includes_public_users():
    sessions = sample_sessions()
    privacy = {1: False, 2: True}
    feed = build_feed(1, sessions, privacy)
    assert any(entry.user_id == 2 for entry in feed)


def test_feed_excludes_private_users():
    sessions = sample_sessions()
    privacy = {1: False, 2: False}
    feed = build_feed(1, sessions, privacy)
    assert all(entry.user_id == 1 for entry in feed)


def test_feed_shows_own_sessions():
    sessions = sample_sessions()
    privacy = {1: False, 2: False}
    feed = build_feed(1, sessions, privacy)
    assert any(entry.user_id == 1 for entry in feed)
