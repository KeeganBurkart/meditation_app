import sqlite3
from src import mindful, profiles


def test_update_bio_and_photo():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    user_id = conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("user@example.com", "hash"),
    ).lastrowid
    profiles.update_bio(conn, user_id, "Hello world")
    profiles.update_photo(conn, user_id, "/uploads/pic.jpg")
    cur = conn.execute("SELECT bio, photo_url FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    assert row == ("Hello world", "/uploads/pic.jpg")
