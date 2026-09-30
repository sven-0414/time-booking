from datetime import datetime

from data_loader import create_system


def ask_int(prompt):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit():
            return int(answer)
        print("Please choose a number: ")


def ask_datetime(prompt):
    while True:
        answer = input(prompt).strip()
        try:
            return datetime.strptime(answer, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Please use the format YYYY-MM-DD HH:MM, e.g. 2026-10-05 17:00.")


def book(system):
    customer_id = ask_int("Customer id: ")
    try:
        customer = system.find_customer(customer_id)
    except ValueError as error:
        print(f"Could not book: {error}")
        return

    rink = choose_rink(system)
    start = ask_datetime("Start (YYYY-MM-DD HH:MM): ")
    duration = ask_int("Duration in minutes (60, 90 or 120): ")
    try:
        booking = system.create_booking(customer, rink, start, duration)
        print(f"Booked: {booking}")
        # ... din resurface_notice-rad ligger kvar här om du lagt den
    except ValueError as error:
        print(f"Could not book: {error}")


def add_customer(system):
    name = input("Customer name: ")
    try:
        customer = system.add_customer(name)
        print(f"Added: {customer}")
    except ValueError as error:
        print(f"Could not add customer: {error}")


def list_customers(system):
    if not system.customers:
        print("No customers yet.")
        return
    for customer in system.customers:
        print(customer)


def choose_rink(system):
    for number, rink in enumerate(system.rinks, start=1):
        print(f"{number}. {rink}")
    while True:
        choice = ask_int("Rink: ")
        if 1 <= choice <= len(system.rinks):
            return system.rinks[choice - 1]
        print("Invalid rink.")


def cancel(system):
    booking_id = ask_int("Booking id: ")
    try:
        booking = system.cancel_booking(booking_id)
        print(f"Cancelled: {booking}")
    except ValueError as error:
        print(f"Could not cancel: {error}")


def list_bookings(system):
    if not system.bookings:
        print("No bookings yet.")
        return
    for booking in sorted(system.bookings, key=lambda booking: booking.start):
        print(booking)


def main():
    system = create_system()
    while True:
        print("\n1. Add customer")
        print("2. List customers")
        print("3. Book")
        print("4. Cancel booking")
        print("5. List bookings")
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
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
