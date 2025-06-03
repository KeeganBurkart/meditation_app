import sys
from pathlib import Path
from datetime import time

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from notifications import NotificationManager


def test_add_and_get_notifications():
    manager = NotificationManager()
    note_id = manager.add_notification(1, time(7, 0), "Morning practice")
    notes = manager.get_notifications(1)
    assert len(notes) == 1
    assert notes[0].notification_id == note_id
    assert notes[0].message == "Morning practice"
