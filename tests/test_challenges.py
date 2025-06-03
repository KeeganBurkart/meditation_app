import sys
from pathlib import Path
import sqlite3

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import mindful


def test_challenge_progress():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )
    challenge_id = mindful.create_challenge(
        conn,
        "January Challenge",
        100,
        "2023-01-01",
        "2023-01-31",
    )
    mindful.join_challenge(conn, 1, challenge_id)
    mindful.log_challenge_progress(conn, 1, challenge_id, 30)
    assert mindful.get_challenge_progress(conn, 1, challenge_id) == 30
