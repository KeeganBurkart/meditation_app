from dataclasses import dataclass
from typing import Dict

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
