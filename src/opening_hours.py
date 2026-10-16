"""Opening hours for the ice arena."""

from datetime import datetime, time


WEEKDAY_OPEN = time(8, 0)
WEEKDAY_CLOSE = time(22, 0)
WEEKEND_OPEN = time(6, 0)
WEEKEND_CLOSE = time(23, 0)


def opening_period(date):
    """Return (open_datetime, close_datetime) for a given date."""
    is_weekend = date.weekday() >= 5
    open_time = WEEKEND_OPEN if is_weekend else WEEKDAY_OPEN
    close_time = WEEKEND_CLOSE if is_weekend else WEEKDAY_CLOSE
    return datetime.combine(date, open_time), datetime.combine(date, close_time)
