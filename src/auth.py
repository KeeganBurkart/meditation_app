"""Simple authentication helpers for Mindful Connect."""

from __future__ import annotations

import hashlib
import sqlite3
from typing import Optional


def hash_password(password: str) -> str:
    """Return a SHA-256 hash of ``password``."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(
    conn: sqlite3.Connection,
    email: str,
    password: str,
    *,
    display_name: Optional[str] = None,
    bio: str = "",
    photo_url: str | None = None,
    is_public: bool = True,
) -> int:
    """Register a user with an email and password and return the new user id."""
    password_hash = hash_password(password)
    cur = conn.execute(
        "INSERT INTO users (email, password_hash, display_name, bio, photo_url, is_public) "
        "VALUES (?, ?, ?, ?, ?, ?) RETURNING id",
        (
            email,
            password_hash,
            display_name,
            bio,
            photo_url,
            int(is_public),
        ),
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    return user_id


def register_social_user(
    conn: sqlite3.Connection,
    provider: str,
    provider_user_id: str,
    *,
    email: Optional[str] = None,
    display_name: Optional[str] = None,
    bio: str = "",
    photo_url: str | None = None,
    is_public: bool = True,
) -> int:
    """Register a user using a social login provider."""
    cur = conn.execute(
        "INSERT INTO users (email, password_hash, display_name, bio, photo_url, is_public) "
        "VALUES (?, ?, ?, ?, ?, ?) RETURNING id",
        (
            email,
            None,
            display_name,
            bio,
            photo_url,
            int(is_public),
        ),
    )
    user_id = cur.fetchone()[0]
    conn.execute(
        "INSERT INTO social_accounts (user_id, provider, provider_user_id) VALUES (?, ?, ?)",
        (user_id, provider, provider_user_id),
    )
    conn.commit()
    return user_id
