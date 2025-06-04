from dataclasses import dataclass
from typing import Dict
import sqlite3


@dataclass
class Profile:
    """Basic user profile with visibility flag."""

    user_id: int
    username: str
    bio: str = ""
    is_public: bool = True


class ProfileManager:
    """In-memory profile storage and privacy controls."""

    def __init__(self) -> None:
        self._store: Dict[int, Profile] = {}

    def create_profile(
        self, user_id: int, username: str, bio: str = "", *, is_public: bool = True
    ) -> Profile:
        """Create a profile for ``user_id``."""
        profile = Profile(user_id, username, bio, is_public)
        self._store[user_id] = profile
        return profile

    def set_visibility(self, user_id: int, is_public: bool) -> None:
        """Update whether ``user_id``'s profile is public."""
        if user_id in self._store:
            self._store[user_id].is_public = is_public

    def can_view(self, requester_id: int, profile_user_id: int) -> bool:
        """Return ``True`` if ``requester_id`` may view ``profile_user_id``."""
        profile = self._store.get(profile_user_id)
        if profile is None:
            return False
        return profile.is_public or requester_id == profile_user_id


def update_bio(conn: sqlite3.Connection, user_id: int, bio: str) -> None:
    """Persist a new bio for ``user_id`` in the database."""
    conn.execute("UPDATE users SET bio = ? WHERE id = ?", (bio, user_id))
    conn.commit()


def update_photo(conn: sqlite3.Connection, user_id: int, photo_url: str) -> None:
    """Persist a new profile photo path for ``user_id``."""
    conn.execute("UPDATE users SET photo_url = ? WHERE id = ?", (photo_url, user_id))
    conn.commit()

def update_visibility(conn: sqlite3.Connection, user_id: int, is_public: bool) -> None:
    """Update profile visibility flag for a user."""
    conn.execute(
        "UPDATE users SET is_public = ? WHERE id = ?",
        (int(is_public), user_id),
    )
    conn.commit()
