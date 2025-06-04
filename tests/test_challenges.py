import sqlite3
from datetime import date # Keep from main

from src import mindful
from src.challenges import (
    create_challenge,
    award_badge,
    get_user_badges,
    current_streak,
    StreakChallenge,
    DurationChallenge,
)


def test_private_challenge_and_badges():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )
    # Keep this section from codex/add-badges-for-challenge-completion
    # Create a private challenge
    challenge_id = create_challenge(conn, "7 Day Streak", 1, is_private=True)
    assert challenge_id == 1
    # Award a badge upon completion
    award_badge(conn, 1, "7 Day Streak")
    assert get_user_badges(conn, 1) == ["7 Day Streak"]

# Keep all these new tests from main
def test_current_streak_simple():
    dates = [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)]
    assert current_streak(dates) == 3


def test_current_streak_with_gap():
    dates = [date(2023, 1, 1), date(2023, 1, 3), date(2023, 1, 4)]
    assert current_streak(dates) == 2


def test_streak_challenge_completed():
    challenge = StreakChallenge(target_days=3)
    dates = [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)]
    assert challenge.is_completed(dates)


def test_duration_challenge_completed():
    challenge = DurationChallenge(target_minutes=60)
    durations = [15, 20, 25]
    assert challenge.is_completed(durations)


def test_duration_challenge_not_completed():
    challenge = DurationChallenge(target_minutes=100)
    durations = [15, 20, 25]
    assert not challenge.is_completed(durations)