import sys
from pathlib import Path
from datetime import date

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from challenges import (
    current_streak,
    StreakChallenge,
    DurationChallenge,
)


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
