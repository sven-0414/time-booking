# Time Booking

A command-line booking system for an ice arena, built as the final project for Python Fundamentals.

Customers book ice time on a rink. The system checks that the rink is free and automatically assigns a free locker room. Locker rooms are occupied 30 minutes before and after the ice time, so two bookings can share a rink back to back but still need different locker rooms.

## Features

- Add and list customers
- Book a rink for 60, 90 or 120 minutes
- Automatic assignment of a free locker room
- Conflict checks for both rinks and locker rooms
- Cancel bookings by id
- List all bookings sorted by start time
- Validation of names, dates, durations and menu input
- Sample data (two rinks, six locker rooms, three customers and three bookings) loaded at start

## Requirements

Python 3.10 or later. No external dependencies. Tested with Python 3.14.

## How to run

From the project folder:

```
python main.py
```

Dates are entered as `YYYY-MM-DD HH:MM`, for example `2026-10-05 17:00`.

## Project structure

| File | Responsibility |
|---|---|
| `main.py` | Menu and user input |
| `data_loader.py` | Creates the system with sample data |
| `booking_system.py` | Holds all data and handles booking, conflict checks and cancellation |
| `booking.py` | A single booking |
| `customer.py` | A customer |
| `resources.py` | `Resource` base class with `Rink` and `LockerRoom` |

`Rink` and `LockerRoom` share the method `occupied_period`, but each returns its own period. The conflict check calls the same method for both, without knowing which type it is dealing with.

The locker room rules are based on the City of Gothenburg's rules for booking ice arenas.