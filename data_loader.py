from datetime import datetime

from booking_system import BookingSystem
from customer import Customer
from resources import LockerRoom, Rink


def create_system():
    """Create a booking system with sample resources, customers and bookings."""
    system = BookingSystem()

    big_rink = system.add_rink("Stora")
    small_rink = system.add_rink("Lilla")
    for number in range(1, 7):
        system.add_locker_room(f"Locker Room {number}")

    frolunda = system.add_customer("Frölunda HC U16")
    backen = system.add_customer("Bäcken HC")
    gkk = system.add_customer("Göteborgs Konståkningsklubb")

    system.create_booking(frolunda, big_rink, datetime(2026, 10, 5, 16, 0), duration=90)
    system.create_booking(backen, big_rink, datetime(2026, 10, 5, 17, 30), duration=60)
    system.create_booking(gkk, small_rink, datetime(2026, 10, 5, 17, 30), duration=90)
    return system
