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
