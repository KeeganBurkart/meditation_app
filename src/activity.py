from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Set, Optional
import sqlite3


@dataclass
class FeedItem:
    """Entry in the social activity feed."""

    item_id: int
    user_id: int
    item_type: str  # 'session', 'comment', 'encouragement'
    message: str
    timestamp: datetime
    target_user_id: Optional[int] = None
    related_feed_item_id: Optional[int] = None


class ActivityFeed:
    """Database-backed activity feed for social interactions."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._friends: Dict[int, Set[int]] = {}
        self._has_related_column = self._detect_related_column()

    def _detect_related_column(self) -> bool:
        """Return ``True`` if ``related_feed_item_id`` exists on ``activity_feed``."""
        try:
            self._conn.execute(
                "SELECT related_feed_item_id FROM activity_feed LIMIT 1"
            )
            return True
        except Exception:
            return False

    def add_friend(self, user_id: int, friend_id: int) -> None:
        """Establish a friendship so ``user_id`` sees ``friend_id`` in their feed."""
        self._friends.setdefault(user_id, set()).add(friend_id)

    def log_session(self, user_id: int, description: str) -> int:
        """Add a meditation session entry."""
        cur = self._conn.execute(
            "INSERT INTO activity_feed (user_id, item_type, message, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, "session", description, datetime.utcnow()),
        )
        self._conn.commit()
        return cur.lastrowid

    def add_comment(
        self,
        user_id: int,
        target_user_id: int,
        text: str,
        *,
        related_feed_item_id: int | None = None,
    ) -> int:
        """Post a comment directed at ``target_user_id``."""
        cur = self._conn.execute(
            "INSERT INTO activity_feed (user_id, item_type, message, timestamp, target_user_id, related_feed_item_id) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, "comment", text, datetime.utcnow(), target_user_id, related_feed_item_id),
        )
        self._conn.commit()
        return cur.lastrowid

    def add_encouragement(
        self,
        user_id: int,
        target_user_id: int,
        text: str,
        *,
        related_feed_item_id: int | None = None,
    ) -> int:
        """Send encouragement to ``target_user_id``."""
        cur = self._conn.execute(
            "INSERT INTO activity_feed (user_id, item_type, message, timestamp, target_user_id, related_feed_item_id) VALUES (?, ?, ?, ?, ?, ?)",
            (
                user_id,
                "encouragement",
                text,
                datetime.utcnow(),
                target_user_id,
                related_feed_item_id,
            ),
        )
        self._conn.commit()
        return cur.lastrowid

    def get_feed(self, user_id: int, limit: int = 10) -> List[FeedItem]:
        """Return recent feed items from the user's friends."""
        friends = self._friends.get(user_id, set())
        if not friends:
            return []
        placeholders = ",".join("?" for _ in friends)
        columns = "id, user_id, item_type, message, timestamp, target_user_id"
        if self._has_related_column:
            columns += ", related_feed_item_id"
        query = (
            f"SELECT {columns} FROM activity_feed WHERE user_id IN ({placeholders}) "
            f"ORDER BY timestamp DESC, id DESC LIMIT ?"
        )
        cur = self._conn.execute(query, (*friends, limit))
        rows = cur.fetchall()
        items: List[FeedItem] = []
        for r in rows:
            timestamp = datetime.fromisoformat(r[4]) if isinstance(r[4], str) else r[4]
            target_user_id = r[5]
            related_id = r[6] if self._has_related_column else None
            items.append(
                FeedItem(
                    r[0],
                    r[1],
                    r[2],
                    r[3],
                    timestamp,
                    target_user_id,
                    related_id,
                )
            )
        return items
