from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import sqlite3


@dataclass
class Subscription:
    """Represents a user's subscription tier."""

    user_id: int
    tier: str  # "free" or "premium"
    start_date: str
    end_date: Optional[str] = None


def subscribe_user(
    conn: sqlite3.Connection,
    user_id: int,
    tier: str,
    start_date: str,
    end_date: Optional[str] = None,
) -> None:
    """Create or update a subscription for ``user_id``."""
    conn.execute(
        """
        INSERT INTO subscriptions (user_id, tier, start_date, end_date)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            tier=excluded.tier,
            start_date=excluded.start_date,
            end_date=excluded.end_date
        """,
        (user_id, tier, start_date, end_date),
    )
    conn.commit()


def get_user_tier(conn: sqlite3.Connection, user_id: int) -> str:
    """Return the subscription tier for ``user_id`` or ``"free"`` if none."""
    cur = conn.execute(
        "SELECT tier FROM subscriptions WHERE user_id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    return row[0] if row else "free"


def is_premium(conn: sqlite3.Connection, user_id: int) -> bool:
    """Return ``True`` if the user has a premium subscription."""
    return get_user_tier(conn, user_id) == "premium"


PREMIUM_FEATURES = {
    "advanced_stats",
    "unlimited_friends",
    "private_challenges",
}


def has_feature_access(conn: sqlite3.Connection, user_id: int, feature: str) -> bool:
    """Return ``True`` if ``user_id`` may access ``feature``."""
    if feature in PREMIUM_FEATURES:
        return is_premium(conn, user_id)
    return True

