from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List
import random


@dataclass
class Ad:
    """Simple text-based advertisement."""

    ad_id: int
    text: str


class AdManager:
    """Database-backed ad rotation for the free tier."""

    def __init__(self, conn: Any) -> None:
        self._conn = conn

    def add_ad(self, text: str, *, is_active: bool = True) -> int:
        """Insert an ad into the ``advertisements`` table and return its ID."""
        cur = self._conn.execute(
            "INSERT INTO advertisements (text, is_active) VALUES (?, ?) RETURNING ad_id",
            (text, int(is_active)),
        )
        ad_id = cur.fetchone()[0]
        self._conn.commit()
        return ad_id

    def get_random_ad(self) -> Ad:
        """Return a random active ad. Raises ``ValueError`` if none exist."""
        cur = self._conn.execute(
            "SELECT ad_id, text FROM advertisements WHERE is_active = 1"
        )
        rows = cur.fetchall()
        if not rows:
            raise ValueError("No ads available")
        ad_id, text = random.choice(rows)
        return Ad(ad_id, text)
