"""Simple authentication helpers for Mindful Connect."""

from __future__ import annotations

import sqlite3
from typing import Optional

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a secure hash of ``password`` using bcrypt."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Return ``True`` if ``password`` matches ``hashed``."""
    return pwd_context.verify(password, hashed)


def _insert_user(
    conn: sqlite3.Connection,
    email: Optional[str],
    password_hash: str | None,
    display_name: Optional[str],
    bio: str,
    photo_url: str | None,
    is_public: bool,
) -> int:
    """Insert a user record and return the new ID."""
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
    return cur.fetchone()[0]


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
    user_id = _insert_user(
        conn,
        email,
        password_hash,
        display_name,
        bio,
        photo_url,
        is_public,
    )
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
    user_id = _insert_user(
        conn,
        email,
        None,
        display_name,
        bio,
        photo_url,
        is_public,
    )
    conn.execute(
        "INSERT INTO social_accounts (user_id, provider, provider_user_id) VALUES (?, ?, ?)",
        (user_id, provider, provider_user_id),
    )
    conn.commit()
    return user_id
