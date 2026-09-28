import datetime

from customer import Customer
from resource import Rink


class Booking:
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
        self.time = time
        self.duration = duration
