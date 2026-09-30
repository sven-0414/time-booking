from datetime import timedelta


class Resource:
    """Object for bookable resources"""

    def __init__(self, name: str):
        name = name.strip()
        if len(name) >= 5:
            self.name = name
        else:
            raise ValueError("Name must be at least five characters.")

    def occupied_period(self, start, end):
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
    """Object for locker rooms"""

    BUFFER_MINUTES = 30

    def occupied_period(self, start, end):
        buffer = timedelta(minutes=LockerRoom.BUFFER_MINUTES)
        occupied_start = start - buffer
        occupied_end = end + buffer
        return occupied_start, occupied_end
