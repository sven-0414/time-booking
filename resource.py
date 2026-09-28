from datetime import timedelta


class Resource:
    """Object for bookable resources"""

    def __init__(self, name: str):
        name = name.strip()
        if len(name) >= 5:
            self.name = name
        else:
            raise ValueError("Name must be at least five characters.")

    def __str__(self) -> str:
        return self.name


class Rink(Resource):
    """An ice rink. Occupied exactly during the booked time. Last 10 minutes is used for resurficing."""

    RESURFACE_MINUTES = 10


class LockerRoom(Resource):
    """Object for locker rooms"""

    def occupied_period(self, start, end):
        buffer = timedelta(minutes=30)
        occupied_start = start - buffer
        occupied_end = end + buffer
        return occupied_start, occupied_end
