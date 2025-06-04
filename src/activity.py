from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Set, Optional


@dataclass
class FeedItem:
    """Entry in the social activity feed."""

    item_id: int
    user_id: int
    item_type: str  # 'session', 'comment', 'encouragement'
    message: str
    timestamp: datetime
    target_user_id: Optional[int] = None


class ActivityFeed:
    """In-memory activity feed showing friends' sessions and interactions."""

    def __init__(self) -> None:
        self._items: List[FeedItem] = []
        self._friends: Dict[int, Set[int]] = {}
        self._counter = 0

    def add_friend(self, user_id: int, friend_id: int) -> None:
        """Establish a friendship so ``user_id`` sees ``friend_id`` in their feed."""
        self._friends.setdefault(user_id, set()).add(friend_id)

    def log_session(self, user_id: int, description: str) -> int:
        """Add a meditation session entry."""
        self._counter += 1
        item = FeedItem(self._counter, user_id, "session", description, datetime.utcnow())
        self._items.append(item)
        return item.item_id

    def add_comment(self, user_id: int, target_user_id: int, text: str) -> int:
        """Post a comment directed at ``target_user_id``."""
        self._counter += 1
        item = FeedItem(self._counter, user_id, "comment", text, datetime.utcnow(), target_user_id)
        self._items.append(item)
        return item.item_id

    def add_encouragement(self, user_id: int, target_user_id: int, text: str) -> int:
        """Send encouragement to ``target_user_id``."""
        self._counter += 1
        item = FeedItem(self._counter, user_id, "encouragement", text, datetime.utcnow(), target_user_id)
        self._items.append(item)
        return item.item_id

    def get_feed(self, user_id: int, limit: int = 10) -> List[FeedItem]:
        """Return recent feed items from the user's friends."""
        friends = self._friends.get(user_id, set())
        items = [i for i in self._items if i.user_id in friends]
        return sorted(items, key=lambda i: i.timestamp, reverse=True)[:limit]
