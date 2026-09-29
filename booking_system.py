from datetime import datetime, timedelta

from booking import Booking
from resources import LockerRoom, Rink
from customer import Customer


class BookingSystem:
    def __init__(self):
        self.customers = []
        self.rinks = []
        self.locker_rooms = []
        self.bookings = []

    def create_booking(
        self,
        customer: Customer,
        rink: Rink,
        start: datetime,
        duration: int,
    ):
        end = start + timedelta(minutes=duration)
        if not self.is_available(rink, start, end):
            raise ValueError("The rink is already booked at that time.")
        locker_room = self.find_free_locker_room(start, end)
        booking = Booking(customer, rink, locker_room, start, duration)
        self.bookings.append(booking)
        return booking

    def is_available(self, resource, start, end):
        """Return True if resource is free for a booking from start to end."""
        new_start, new_end = resource.occupied_period(start, end)

        for booking in self.bookings:
            if resource is booking.rink or resource is booking.locker_room:
                old_start, old_end = resource.occupied_period(
                    booking.start, booking.end
                )
                if new_start < old_end and old_start < new_end:
                    return False

        return True

    def find_free_locker_room(self, start, end):
        """Return the first locker room that is free from start to end."""
        for locker_room in self.locker_rooms:
            if self.is_available(locker_room, start, end):
                return locker_room
        raise ValueError("No locker room is available at that time.")

    def add_rink(self, name):
        rink = Rink(name)
        self.rinks.append(rink)
        return rink

    def add_locker_room(self, name):
        locker_room = LockerRoom(name)
        self.locker_rooms.append(locker_room)
        return locker_room

    def add_customer(self, name):
        customer = Customer(name)
        self.customers.append(customer)
        return customer

    def cancel_booking(self, booking_id):
        """Remove the booking with the given id."""
        for booking in self.bookings:
            if booking.id == booking_id:
                self.bookings.remove(booking)
                return booking
        raise ValueError(f"No booking with id {booking_id}.")

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        raise ValueError(f"No customer with id {customer_id}.")
