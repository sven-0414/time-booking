"""Database access for bookings."""

from src.booking import Booking
from src.customer import Customer
from src.resources import Rink, LockerRoom


SELECT_WITH_JOINS = """
    SELECT
        b.id, b.start_time, b.duration,
        c.id, c.name,
        r.id, r.name,
        lr.id, lr.name
    FROM bookings b
    JOIN customers c    ON c.id  = b.customer_id
    JOIN rinks r        ON r.id  = b.rink_id
    JOIN locker_rooms lr ON lr.id = b.locker_room_id
"""


def _row_to_booking(row) -> Booking:
    """Build a Booking from a row returned by SELECT_WITH_JOINS."""
    (
        booking_id,
        start_time,
        duration,
        customer_id,
        customer_name,
        rink_id,
        rink_name,
        locker_id,
        locker_name,
    ) = row
    return Booking(
        customer=Customer(name=customer_name, id=customer_id),
        rink=Rink(name=rink_name, id=rink_id),
        locker_room=LockerRoom(name=locker_name, id=locker_id),
        time=start_time,
        duration=duration,
        id=booking_id,
    )


class BookingRepository:
    """Reads and writes bookings to the database."""

    def __init__(self, conn):
        self.conn = conn

    def add(self, booking: Booking) -> Booking:
        """Insert a booking and set its id. Returns the same booking."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO bookings
                    (customer_id, rink_id, locker_room_id, start_time, duration)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    booking.customer.id,
                    booking.rink.id,
                    booking.locker_room.id,
                    booking.start,
                    booking.duration,
                ),
            )
            booking.id = cur.fetchone()[0]
        self.conn.commit()
        return booking

    def delete(self, booking_id: int) -> Booking:
        """Delete and return the booking with the given id."""
        booking = self.find_by_id(booking_id)
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        self.conn.commit()
        return booking

    def find_by_id(self, booking_id: int) -> Booking:
        with self.conn.cursor() as cur:
            cur.execute(SELECT_WITH_JOINS + " WHERE b.id = %s", (booking_id,))
            row = cur.fetchone()
        if row is None:
            raise ValueError(f"No booking with id {booking_id}.")
        return _row_to_booking(row)

    def find_all(self) -> list[Booking]:
        with self.conn.cursor() as cur:
            cur.execute(SELECT_WITH_JOINS + " ORDER BY b.start_time")
            rows = cur.fetchall()
        return [_row_to_booking(row) for row in rows]

    def find_by_customer_id(self, customer_id: int) -> list[Booking]:
        with self.conn.cursor() as cur:
            cur.execute(
                SELECT_WITH_JOINS + " WHERE b.customer_id = %s ORDER BY b.start_time",
                (customer_id,),
            )
            rows = cur.fetchall()
        return [_row_to_booking(row) for row in rows]

    def find_by_rink_on_date(self, rink_id: int, date) -> list[Booking]:
        """Return all bookings for a rink on a given date, ordered by start time."""
        with self.conn.cursor() as cur:
            cur.execute(
                SELECT_WITH_JOINS
                + " WHERE b.rink_id = %s"
                + " AND b.start_time::date = %s"
                + " ORDER BY b.start_time",
                (rink_id, date),
            )
            rows = cur.fetchall()
        return [_row_to_booking(row) for row in rows]
