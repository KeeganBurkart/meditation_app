from __future__ import annotations

from dataclasses import dataclass
from typing import List
import random


@dataclass
class Ad:
    """Simple text-based advertisement."""

    ad_id: int
    text: str


class AdManager:
    """In-memory ad rotation for the free tier."""

    def __init__(self) -> None:
        self._ads: List[Ad] = []
        self._counter = 0

    def add_ad(self, text: str) -> int:
        """Add an ad and return its identifier."""
        self._counter += 1
        ad = Ad(self._counter, text)
        self._ads.append(ad)
        return ad.ad_id

    def get_random_ad(self) -> Ad:
        """Return a random ad. Raises ``ValueError`` if none exist."""
        if not self._ads:
            raise ValueError("No ads available")
        return random.choice(self._ads)
