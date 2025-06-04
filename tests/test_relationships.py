import sqlite3

from src import mindful
from src.relationships import (
    follow_user,
    unfollow_user,
    get_followers,
    get_following,
)


def setup_db():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("alice@example.com", "h1"),
    )
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("bob@example.com", "h2"),
    )
    return conn


def test_follow_and_unfollow():
    conn = setup_db()
    follow_user(conn, 1, 2)
    assert get_following(conn, 1) == [2]
    assert get_followers(conn, 2) == [1]

    unfollow_user(conn, 1, 2)
    assert get_following(conn, 1) == []
    assert get_followers(conn, 2) == []


def test_follow_idempotent():
    conn = setup_db()
    follow_user(conn, 1, 2)
    follow_user(conn, 1, 2)
    assert get_following(conn, 1) == [2]
    assert get_followers(conn, 2) == [1]
