"""Notification preference helpers backed by the database."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time, datetime
from typing import Any, List


@dataclass
class Notification:
    """A user-configurable reminder."""

    notification_id: int
    reminder_time: time
    message: str
    enabled: bool = True


class NotificationManager:
    """Database-backed notification preference manager."""

    def __init__(self, conn: Any) -> None:
        self._conn = conn

    def _to_time(self, value: Any) -> time:
        if isinstance(value, time):
            return value
        if isinstance(value, datetime):
            return value.time()
        value_str = str(value)
        if " " in value_str:
            value_str = value_str.split(" ")[-1]
        return time.fromisoformat(value_str)

    def add_notification(self, user_id: int, reminder_time: time, message: str, enabled: bool = True) -> int:
        """Create a new notification and return its identifier."""
        cur = self._conn.execute(
            "INSERT INTO user_notifications (user_id, reminder_time, message, is_enabled) "
            "VALUES (?, ?, ?, ?) RETURNING id",
            (user_id, reminder_time.isoformat(), message, int(enabled)),
        )
        note_id = cur.fetchone()[0]
        self._conn.commit()
        return note_id

    def remove_notification(self, user_id: int, notification_id: int) -> None:
        """Remove a notification for ``user_id`` by ``notification_id``."""
        self._conn.execute(
            "DELETE FROM user_notifications WHERE user_id = ? AND id = ?",
            (user_id, notification_id),
        )
        self._conn.commit()

    def get_notifications(self, user_id: int) -> List[Notification]:
        """Return all notifications for ``user_id``."""
        cur = self._conn.execute(
            "SELECT id, reminder_time, message, is_enabled FROM user_notifications WHERE user_id = ? ORDER BY id",
            (user_id,),
        )
        rows = cur.fetchall()
        return [
            Notification(r[0], self._to_time(r[1]), r[2], bool(r[3]))
            for r in rows
        ]
