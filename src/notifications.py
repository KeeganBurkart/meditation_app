"""Simple notification preferences management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from typing import Dict, List


@dataclass
class Notification:
    """A user-configurable reminder."""

    notification_id: int
    reminder_time: time
    message: str
    enabled: bool = True


class NotificationManager:
    """In-memory store for notification preferences."""

    def __init__(self) -> None:
        self._store: Dict[int, List[Notification]] = {}
        self._counter = 0

    def add_notification(self, user_id: int, reminder_time: time, message: str) -> int:
        """Create a new notification and return its identifier."""
        self._counter += 1
        note = Notification(self._counter, reminder_time, message, True)
        self._store.setdefault(user_id, []).append(note)
        return note.notification_id

    def remove_notification(self, user_id: int, notification_id: int) -> None:
        """Remove a notification for ``user_id`` by ``notification_id``."""
        if user_id in self._store:
            self._store[user_id] = [n for n in self._store[user_id] if n.notification_id != notification_id]

    def get_notifications(self, user_id: int) -> List[Notification]:
        """Return all notifications for ``user_id``."""
        return list(self._store.get(user_id, []))
