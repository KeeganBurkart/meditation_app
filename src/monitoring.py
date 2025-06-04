import logging

logger = logging.getLogger("analytics")


def log_event(event: str, payload: dict | None = None) -> None:
    """Log a usage analytics event."""
    logger.info("EVENT %s %s", event, payload or {})
