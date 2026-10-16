"""Compute free periods on a rink for a given date."""

from datetime import timedelta

from src.opening_hours import opening_period


MIN_FREE_MINUTES = 60


def find_free_periods(bookings, date):
    """Return a list of (start, end) tuples for periods when the rink is free.

    bookings must be sorted by start time and all belong to the same rink
    on the given date. Only periods of at least MIN_FREE_MINUTES are returned.
    """
    open_time, close_time = opening_period(date)
    free = []
    cursor = open_time

    for booking in bookings:
        if booking.start > cursor:
            free.append((cursor, booking.start))
        if booking.end > cursor:
            cursor = booking.end

    if close_time > cursor:
        free.append((cursor, close_time))

    min_gap = timedelta(minutes=MIN_FREE_MINUTES)
    return [(start, end) for start, end in free if end - start >= min_gap]
