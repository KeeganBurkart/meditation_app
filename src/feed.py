from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .sessions import MeditationSession


@dataclass
class FeedEntry:
    """A single activity feed entry."""

    user_id: int
    session: MeditationSession


def build_feed(
    viewer_id: int,
    sessions: Dict[int, Iterable[MeditationSession]],
    privacy_settings: Dict[int, bool],
) -> List[FeedEntry]:
    """Return feed entries visible to ``viewer_id``.

    Sessions from other users are included only if that user has opted in via
    ``privacy_settings``. A user's own sessions are always visible to them.
    Entries are returned in reverse chronological order.
    """
    entries: List[FeedEntry] = []
    for user_id, sess_list in sessions.items():
        if user_id != viewer_id and not privacy_settings.get(user_id, False):
            # Skip sessions from users who have not opted in
            continue
        for session in sess_list:
            entries.append(FeedEntry(user_id, session))

    entries.sort(
        key=lambda e: (
            e.session.session_date,
            e.session.time_of_day,
        ),
        reverse=True,
    )
    return entries
