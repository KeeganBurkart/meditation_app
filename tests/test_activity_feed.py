import sqlite3

from src import mindful
from src.activity import ActivityFeed


def setup_db():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    for idx in range(1, 5):
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (f'user{idx}@example.com', 'pw'),
        )
    conn.commit()
    return conn


def test_activity_feed():
    conn = setup_db()
    feed = ActivityFeed(conn)
    feed.add_friend(1, 2)
    feed.add_friend(1, 3)

    feed.log_session(2, "Morning meditation")
    feed.add_comment(3, 2, "Great job!")
    feed.add_encouragement(3, 2, "Keep it up!")
    feed.log_session(4, "Not visible")

    items = feed.get_feed(1)
    assert len(items) == 3
    assert [i.item_type for i in items] == ["encouragement", "comment", "session"]
