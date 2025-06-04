from __future__ import annotations

from pydantic import BaseModel
from typing import List


class DateValuePoint(BaseModel):
    """Data point representing a value on a specific date."""

    date_str: str  # e.g. "YYYY-MM-DD"
    value: int


class ConsistencyDataResponse(BaseModel):
    """Response model for consistency over time charts."""

    points: List[DateValuePoint]


class MoodCorrelationPoint(BaseModel):
    """Single mood before/after pair."""

    mood_before: int
    mood_after: int


class MoodCorrelationResponse(BaseModel):
    """Response model containing mood correlation points."""

    points: List[MoodCorrelationPoint]


class HourValuePoint(BaseModel):
    """Value aggregated by hour of day."""

    hour: int
    value: int


class TimeOfDayResponse(BaseModel):
    """Response model for time of day distribution."""

    points: List[HourValuePoint]


class StringValuePoint(BaseModel):
    """Generic name/value pair for categorical data."""

    name: str
    value: int


class LocationFrequencyResponse(BaseModel):
    """Response model for location frequency charts."""

    points: List[StringValuePoint]


class AdResponse(BaseModel):
    """API representation of an advertisement."""

    ad_id: int
    text: str


class CustomTypeInput(BaseModel):
    """Input model for creating or updating a custom meditation type."""

    type_name: str


class CustomTypeResponse(BaseModel):
    """Representation of a custom meditation type."""

    id: str
    type_name: str


class ProfileVisibilityInput(BaseModel):
    """Input payload for updating profile visibility."""

    is_public: bool


class BadgeResponse(BaseModel):
    """Representation of an earned badge."""

    badge_name: str
    awarded_at: str


class PrivateChallengeInput(BaseModel):
    """Input for creating or updating a private challenge."""

    name: str
    target_minutes: int
    start_date: str
    end_date: str
    description: str | None = None


class PrivateChallengeResponse(BaseModel):
    """Representation of a private challenge."""

    id: int
    name: str
    target_minutes: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    created_by: int | None = None
    is_private: bool | None = None
    description: str | None = None


class PublicProfileResponse(BaseModel):
    """Public profile information with aggregated statistics."""

    user_id: int
    display_name: str | None = None
    bio: str | None = None
    photo_url: str | None = None
    total_minutes: int
    session_count: int
