from datetime import datetime, timedelta

from customer import Customer
from resource import LockerRoom, Rink


class Booking:
    """A booking of a rink and a locker room for a customer."""

    ALLOWED_DURATIONS = (60, 90, 120)
    _next_id = 1

    def __init__(
        self,
        customer: Customer,
        rink: Rink,
        locker_room: LockerRoom,
        time: datetime,
        duration: int,
    ):
        self.customer = customer
        self.rink = rink
        self.locker_room = locker_room
        self.start = time
        self.end = time + timedelta(minutes=duration)
        self.duration = duration

    def __str__(self) -> str:
        return (
            f"{self.id:04d} {self.start:%Y-%m-%d %H:%M}-{self.end:%H:%M} "
            f"{self.rink}, {self.locker_room}, {self.customer.name}"
        )
