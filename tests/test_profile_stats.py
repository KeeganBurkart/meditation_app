import sqlite3
from src import mindful
from src import profiles


def test_get_profile_with_stats():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    user_id = conn.execute(
        "INSERT INTO users (email, password_hash, display_name) VALUES (?, ?, ?)",
        ("user@example.com", "hash", "User"),
    ).lastrowid
    conn.execute(
        "INSERT INTO sessions (user_id, duration, session_type, session_date) VALUES (?, ?, ?, ?)",
        (user_id, 10, "Guided", "2023-01-01"),
    )
    conn.execute(
        "INSERT INTO sessions (user_id, duration, session_type, session_date) VALUES (?, ?, ?, ?)",
        (user_id, 15, "Guided", "2023-01-02"),
    )
    conn.commit()

    profile = profiles.get_profile_with_stats(conn, user_id)
    assert profile["display_name"] == "User"
    assert profile["total_minutes"] == 25
    assert profile["session_count"] == 2
