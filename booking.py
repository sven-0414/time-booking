from datetime import datetime, timedelta

from customer import Customer
from resources import LockerRoom, Rink


class Booking:
    """A booking of a rink and a locker room for a customer."""

    ALLOWED_DURATIONS = (60, 90, 120)
    _next_id = 1

    @staticmethod
    def validate_duration(duration: int) -> None:
        if duration not in Booking.ALLOWED_DURATIONS:
            raise ValueError(
                f"Duration must be one of {Booking.ALLOWED_DURATIONS} minutes."
            )

    def __init__(self, customer, rink, locker_room, time, duration):
        Booking.validate_duration(duration)
        self.customer = customer
        self.rink = rink
        self.locker_room = locker_room
        self.start = time
        self.end = time + timedelta(minutes=duration)
        self.duration = duration
        self.id = Booking._next_id
        Booking._next_id += 1

    def __str__(self) -> str:
        return (
            f"{self.id:04d} {self.start:%Y-%m-%d %H:%M}-{self.end:%H:%M} "
            f"{self.rink}, {self.locker_room}, {self.customer.name}"
        )
