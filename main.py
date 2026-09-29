from datetime import datetime

from data_loader import create_system


def ask_int(prompt):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit():
            return int(answer)
        print("Please enter a number.")


def ask_datetime(prompt):
    while True:
        answer = input(prompt).strip()
        try:
            return datetime.strptime(answer, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Please use the format YYYY-MM-DD HH:MM, e.g. 2026-10-05 17:00.")


def book(system):
    customer_id = ask_int("Customer id: ")
    start = ask_datetime("Start (YYYY-MM-DD HH:MM): ")
    duration = ask_int("Duration in minutes (60, 90 or 120): ")
    try:
        customer = system.find_customer(customer_id)
        booking = system.create_booking(customer, system.rinks[0], start, duration)
        print(f"Booked: {booking}")
    except ValueError as error:
        print(f"Could not book: {error}")


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
