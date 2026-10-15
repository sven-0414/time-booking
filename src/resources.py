from datetime import timedelta


class Resource:
    """Base class for bookable resources."""

    def __init__(self, name: str, id: int | None = None):
        name = name.strip()
        if len(name) < 5:
            raise ValueError("Name must be at least five characters.")
        self.name = name
        self.id = id

    def occupied_period(self, start, end):
        """Return the period the resource is actually occupied for a booking
        from start to end. The base resource is busy exactly that period;
        subclasses may widen it."""
        return start, end

    def __str__(self) -> str:
        return self.name


class Rink(Resource):
    """An ice rink. Occupied exactly during the booked time; the last
    10 minutes of the booking are used to resurface the ice."""

    RESURFACE_MINUTES = 10

    def resurface_notice(self) -> str:
        return (
            f"Note: the last {Rink.RESURFACE_MINUTES} minutes of the "
            f"booking are used to resurface the ice."
        )


class LockerRoom(Resource):
    """A locker room. Occupied 30 minutes before and after the booking."""

    BUFFER_MINUTES = 30

    def occupied_period(self, start, end):
        buffer = timedelta(minutes=LockerRoom.BUFFER_MINUTES)
        return start - buffer, end + buffer
