"""Command-line menu for the ice arena booking system."""

from datetime import datetime

from src.db import connect
from src.booking_system import BookingSystem
from src.booking_repository import BookingRepository
from src.customer_repository import CustomerRepository
from src.locker_room_repository import LockerRoomRepository
from src.rink_repository import RinkRepository


def ask_int(prompt):
    """Prompt until the user enters a whole number, then return it as int."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit():
            return int(answer)
        print("Please choose a number.")


def ask_datetime(prompt):
    """Prompt until the user enters a date and a time, then return it as datetime."""
    while True:
        answer = input(prompt).strip()
        try:
            return datetime.strptime(answer, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Please use the format YYYY-MM-DD HH:MM, e.g. 2026-10-05 17:00.")


def ask_date(prompt):
    """Prompt until the user enters a date, then return it as date."""
    while True:
        answer = input(prompt).strip()
        try:
            return datetime.strptime(answer, "%Y-%m-%d").date()
        except ValueError:
            print("Please use the format YYYY-MM-DD, e.g. 2026-10-05.")


def choose_rink(system):
    rinks = system.all_rinks()
    for number, rink in enumerate(rinks, start=1):
        print(f"{number}. {rink}")
    while True:
        choice = ask_int("Rink: ")
        if 1 <= choice <= len(rinks):
            return rinks[choice - 1]
        print("Invalid rink.")


def add_customer(system):
    name = input("Customer name: ")
    try:
        customer = system.add_customer(name)
        print(f"Added: {customer}")
    except ValueError as error:
        print(f"Could not add customer: {error}")


def list_customers(system):
    customers = system.all_customers()
    if not customers:
        print("No customers yet.")
        return
    for customer in customers:
        print(customer)


def book(system):
    """Run the booking dialog. The customer id is checked first, so an
    unknown id fails before the rink, time and duration are asked for."""
    customer_id = ask_int("Customer id: ")
    try:
        customer = system.find_customer(customer_id)
    except ValueError as error:
        print(f"Could not book: {error}")
        return

    rink = choose_rink(system)
    start = ask_datetime("Start (YYYY-MM-DD HH:MM): ")
    duration = ask_int("Duration in minutes (60, 90, 120 or 240): ")
    try:
        booking = system.create_booking(customer, rink, start, duration)
        print(f"Booked: {booking}")
        print(booking.rink.resurface_notice())
    except ValueError as error:
        print(f"Could not book: {error}")


def cancel(system):
    booking_id = ask_int("Booking id: ")
    try:
        booking = system.cancel_booking(booking_id)
        print(f"Cancelled: {booking}")
    except ValueError as error:
        print(f"Could not cancel: {error}")


def list_bookings(system):
    bookings = system.all_bookings()
    if not bookings:
        print("No bookings yet.")
        return
    for booking in bookings:
        print(booking)


def list_customer_bookings(system):
    customer_id = ask_int("Customer id: ")
    try:
        customer = system.find_customer(customer_id)
    except ValueError as error:
        print(error)
        return
    bookings = system.bookings_for_customer(customer)
    if not bookings:
        print(f"No bookings for {customer.name}.")
        return
    for booking in bookings:
        print(booking)


def show_free_periods(system):
    rink = choose_rink(system)
    date = ask_date("Date (YYYY-MM-DD): ")
    periods = system.free_periods_on_date(rink, date)
    if not periods:
        print(f"No free periods of at least 60 minutes on {date} for {rink}.")
        return
    print(f"Free periods on {date:%Y-%m-%d} for {rink}:")
    for start, end in periods:
        minutes = int((end - start).total_seconds() / 60)
        print(f"  {start:%H:%M}-{end:%H:%M} ({minutes} min)")


def main():
    with connect() as conn:
        system = BookingSystem(
            customer_repo=CustomerRepository(conn),
            rink_repo=RinkRepository(conn),
            locker_room_repo=LockerRoomRepository(conn),
            booking_repo=BookingRepository(conn),
        )

        while True:
            print("\n1. Add customer")
            print("2. List customers")
            print("3. Book")
            print("4. Cancel booking")
            print("5. List bookings")
            print("6. List a customer's bookings")
            print("7. Show free periods for a rink on a date")
            print("0. Quit")
            choice = input("Choose: ").strip()

            if choice == "1":
                add_customer(system)
            elif choice == "2":
                list_customers(system)
            elif choice == "3":
                book(system)
            elif choice == "4":
                cancel(system)
            elif choice == "5":
                list_bookings(system)
            elif choice == "6":
                list_customer_bookings(system)
            elif choice == "7":
                show_free_periods(system)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
