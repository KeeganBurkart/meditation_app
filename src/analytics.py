from __future__ import annotations

from collections import Counter
from datetime import date
from typing import Iterable, Dict, Tuple, List

from .sessions import MeditationSession


def consistency_over_time(sessions: Iterable[MeditationSession]) -> Dict[date, int]:
    """Return a mapping of session dates to number of sessions."""
    counts = Counter(s.session_date for s in sessions)
    return dict(sorted(counts.items()))


def mood_correlation_points(sessions: Iterable[MeditationSession]) -> List[Tuple[int, int]]:
    """Return pairs of mood before/after for sessions that include mood data."""
    return [
        (s.mood_before, s.mood_after)
        for s in sessions
        if s.mood_before is not None and s.mood_after is not None
    ]


def time_of_day_distribution(sessions: Iterable[MeditationSession]) -> Dict[int, int]:
    """Return a count of sessions by hour of day."""
    counts = Counter(s.time_of_day.hour for s in sessions)
    return dict(sorted(counts.items()))


def location_frequency(sessions: Iterable[MeditationSession]) -> Dict[str, int]:
    """Return a count of sessions by location."""
    counts = Counter(s.location for s in sessions)
    return dict(sorted(counts.items()))


def plot_consistency_over_time(sessions: Iterable[MeditationSession], output_path: str) -> None:
    """Plot a line chart of sessions per date."""
    try:
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - matplotlib optional
        return
    data = consistency_over_time(sessions)
    if not data:
        return
    dates = list(data.keys())
    counts = list(data.values())
    plt.figure()
    plt.plot(dates, counts, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Sessions")
    plt.title("Consistency Over Time")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_mood_correlation(sessions: Iterable[MeditationSession], output_path: str) -> None:
    """Plot a scatter chart of mood before vs. mood after."""
    try:
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - matplotlib optional
        return
    points = mood_correlation_points(sessions)
    if not points:
        return
    before, after = zip(*points)
    plt.figure()
    plt.scatter(before, after)
    plt.xlabel("Mood Before")
    plt.ylabel("Mood After")
    plt.title("Mood Correlation")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_time_of_day_distribution(sessions: Iterable[MeditationSession], output_path: str) -> None:
    """Plot a bar chart showing sessions by hour of day."""
    try:
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - matplotlib optional
        return
    data = time_of_day_distribution(sessions)
    if not data:
        return
    hours = list(data.keys())
    counts = list(data.values())
    plt.figure()
    plt.bar(hours, counts)
    plt.xlabel("Hour")
    plt.ylabel("Sessions")
    plt.title("Sessions by Time of Day")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_location_frequency(sessions: Iterable[MeditationSession], output_path: str) -> None:
    """Plot a bar chart showing sessions per location."""
    try:
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - matplotlib optional
        return
    data = location_frequency(sessions)
    if not data:
        return
    names = list(data.keys())
    counts = list(data.values())
    plt.figure()
    plt.bar(names, counts)
    plt.xlabel("Location")
    plt.ylabel("Sessions")
    plt.title("Sessions by Location")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
