"""Orchestrates bookings against the database.

Holds references to the repositories and contains the booking logic:
duration validation, past-check, conflict detection and automatic
assignment of a free locker room.
"""

from datetime import datetime, timedelta

from src.booking import Booking
from src.free_periods import find_free_periods


class BookingSystem:
    """Business logic for creating, cancelling and querying bookings."""

    def __init__(self, customer_repo, rink_repo, locker_room_repo, booking_repo):
        self.customer_repo = customer_repo
        self.rink_repo = rink_repo
        self.locker_room_repo = locker_room_repo
        self.booking_repo = booking_repo

    # --- Create ---

    def create_booking(self, customer, rink, start, duration):
        """Create and store a booking, assigning a free locker room.

        Raises ValueError if the duration is invalid, the start is in the
        past, the rink is already booked, or no locker room is free.
        """
        Booking.validate_duration(duration)
        if start < datetime.now():
            raise ValueError("Cannot book a time in the past.")

        end = start + timedelta(minutes=duration)

        conflict = self._find_rink_conflict(rink, start, end)
        if conflict is not None:
            raise ValueError(
                f"{rink} is already booked {conflict.start:%H:%M}-{conflict.end:%H:%M}."
            )

        locker_room = self._find_free_locker_room(start, end)

        booking = Booking(customer, rink, locker_room, start, duration)
        return self.booking_repo.add(booking)

    # --- Cancel ---

    def cancel_booking(self, booking_id):
        """Delete the booking with the given id and return it."""
        return self.booking_repo.delete(booking_id)

    # --- Queries ---

    def all_customers(self):
        return self.customer_repo.find_all()

    def all_rinks(self):
        return self.rink_repo.find_all()

    def all_bookings(self):
        return self.booking_repo.find_all()

    def find_customer(self, customer_id):
        return self.customer_repo.find_by_id(customer_id)

    def bookings_for_customer(self, customer):
        return self.booking_repo.find_by_customer_id(customer.id)

    def free_periods_on_date(self, rink, date):
        """Return (start, end) tuples for periods when the rink is free."""
        bookings = self.booking_repo.find_by_rink_on_date(rink.id, date)
        return find_free_periods(bookings, date)

    # --- Add resources ---

    def add_customer(self, name):
        from src.customer import Customer

        return self.customer_repo.add(Customer(name))

    def add_rink(self, name):
        from src.resources import Rink

        return self.rink_repo.add(Rink(name))

    def add_locker_room(self, name):
        from src.resources import LockerRoom

        return self.locker_room_repo.add(LockerRoom(name))

    # --- Internal: conflict and locker-room assignment ---

    def _find_rink_conflict(self, rink, start, end):
        """Return the first booking on this rink that overlaps start–end."""
        for booking in self.booking_repo.find_by_rink_on_date(rink.id, start.date()):
            if start < booking.end and booking.start < end:
                return booking
        return None

    def _find_free_locker_room(self, start, end):
        """Return the first locker room free from start to end, with buffer."""
        for locker_room in self.locker_room_repo.find_all():
            if self._locker_room_is_free(locker_room, start, end):
                return locker_room
        raise ValueError("No locker room is available at that time.")

    def _locker_room_is_free(self, locker_room, start, end):
        new_start, new_end = locker_room.occupied_period(start, end)
        bookings = self.booking_repo.find_by_locker_room_on_date(
            locker_room.id, start.date()
        )
        for booking in bookings:
            old_start, old_end = locker_room.occupied_period(booking.start, booking.end)
            if new_start < old_end and old_start < new_end:
                return False
        return True
