from datetime import time
import sqlite3

from src import mindful
from src.notifications import NotificationManager


def setup_db():
    conn = sqlite3.connect(":memory:")
    mindful.init_db(conn)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        ("test@example.com", "hash"),
    )
    return conn


def test_add_and_get_notifications():
    conn = setup_db()
    manager = NotificationManager(conn)
    note_id = manager.add_notification(1, time(7, 0), "Morning practice")
    notes = manager.get_notifications(1)
    assert len(notes) == 1
    assert notes[0].notification_id == note_id
    assert notes[0].message == "Morning practice"
    assert notes[0].enabled is True


def test_add_disabled_notification():
    conn = setup_db()
    manager = NotificationManager(conn)
    note_id = manager.add_notification(1, time(20, 0), "Evening", enabled=False)
    notes = manager.get_notifications(1)
    assert len(notes) == 1
    assert notes[0].notification_id == note_id
    assert notes[0].enabled is False
