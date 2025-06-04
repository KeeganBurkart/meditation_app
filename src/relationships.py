"""User following relationships management."""

from __future__ import annotations

import sqlite3
from typing import List

from fastapi import HTTPException
from .subscriptions import is_premium, FREE_TIER_FRIEND_LIMIT


def follow_user(conn: sqlite3.Connection, follower_id: int, followed_id: int) -> None:
    """Create a follow relationship from ``follower_id`` to ``followed_id``."""

    if not is_premium(conn, follower_id):
        cur = conn.execute(
            "SELECT COUNT(*) FROM follows WHERE follower_id = ?",
            (follower_id,),
        )
        count = cur.fetchone()[0]
        if count >= FREE_TIER_FRIEND_LIMIT:
            raise HTTPException(
                status_code=403,
                detail="Upgrade to premium for unlimited friends.",
            )

    conn.execute(
        "INSERT INTO follows (follower_id, followed_id) VALUES (?, ?)"
        " ON CONFLICT(follower_id, followed_id) DO NOTHING",
        (follower_id, followed_id),
    )
    conn.commit()


def unfollow_user(conn: sqlite3.Connection, follower_id: int, followed_id: int) -> None:
    """Remove a follow relationship."""
    conn.execute(
        "DELETE FROM follows WHERE follower_id = ? AND followed_id = ?",
        (follower_id, followed_id),
    )
    conn.commit()


def get_followers(conn: sqlite3.Connection, user_id: int) -> List[int]:
    """Return a list of user IDs following ``user_id``."""
    cur = conn.execute(
        "SELECT follower_id FROM follows WHERE followed_id = ? ORDER BY follower_id",
        (user_id,),
    )
    return [row[0] for row in cur.fetchall()]


def get_following(conn: sqlite3.Connection, user_id: int) -> List[int]:
    """Return a list of user IDs that ``user_id`` is following."""
    cur = conn.execute(
        "SELECT followed_id FROM follows WHERE follower_id = ? ORDER BY followed_id",
        (user_id,),
    )
    return [row[0] for row in cur.fetchall()]
