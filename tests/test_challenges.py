import sys
from pathlib import Path
import sqlite3

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import mindful
from challenges import create_challenge, award_badge, get_user_badges


def test_private_challenge_and_badges():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )
    # Create a private challenge
    challenge_id = create_challenge(conn, "7 Day Streak", 1, is_private=True)
    assert challenge_id == 1
    # Award a badge upon completion
    award_badge(conn, 1, "7 Day Streak")
    assert get_user_badges(conn, 1) == ["7 Day Streak"]
