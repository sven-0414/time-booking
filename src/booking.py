from datetime import timedelta


class Booking:
    """A booking of a rink and a locker room for a customer."""

    ALLOWED_DURATIONS = (60, 90, 120, 240)

    def __init__(self, customer, rink, locker_room, time, duration, id=None):
        Booking.validate_duration(duration)
        self.customer = customer
        self.rink = rink
        self.locker_room = locker_room
        self.start = time
        self.end = time + timedelta(minutes=duration)
        self.duration = duration
        self.id = id

    @staticmethod
    def validate_duration(duration: int) -> None:
        if duration not in Booking.ALLOWED_DURATIONS:
            raise ValueError(
                f"Duration must be one of {Booking.ALLOWED_DURATIONS} minutes."
            )

    def __str__(self) -> str:
        id_part = f"{self.id:04d}" if self.id is not None else "----"
        return (
            f"{id_part} {self.start:%Y-%m-%d %H:%M}-{self.end:%H:%M} "
            f"{self.rink}, {self.locker_room}, {self.customer.name}"
        )
