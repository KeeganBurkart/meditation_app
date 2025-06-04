import sqlite3

from src import mindful


def test_log_and_retrieve_moods():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    )

    session_id = mindful.log_session(
        conn,
        user_id=1,
        duration=10,
        session_type="Guided",
        session_date="2023-01-01",
        session_time="06:00",
        location="Home",
        mood_before=3,
        mood_after=7,
    )
    assert isinstance(session_id, int)

    moods = mindful.get_user_moods(conn, 1)
    assert moods == [(3, 7)]
