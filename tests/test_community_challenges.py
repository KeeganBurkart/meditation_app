import sys
from pathlib import Path
import sqlite3

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import mindful


def test_create_join_and_progress():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )

    challenge_id = mindful.create_challenge(
        conn,
        name="30 Day Challenge",
        target_minutes=300,
        start_date="2023-01-01",
        end_date="2023-01-30",
    )
    assert challenge_id == 1

    mindful.join_challenge(conn, 1, challenge_id)
    cur = conn.execute(
        "SELECT minutes FROM challenge_progress WHERE user_id = ? AND challenge_id = ?",
        (1, challenge_id),
    )
    row = cur.fetchone()
    assert row is not None and row[0] == 0

    mindful.log_challenge_progress(conn, 1, challenge_id, minutes=15)
    assert mindful.get_challenge_progress(conn, 1, challenge_id) == 15
