"""Seed the time_booking database with sample data."""

from datetime import datetime, timedelta

from src.db import connect


def seed():
    with connect() as conn:
        with conn.cursor() as cur:
            # Clear everything. Order matters because of foreign keys.
            cur.execute("DELETE FROM bookings")
            cur.execute("DELETE FROM customers")
            cur.execute("DELETE FROM rinks")
            cur.execute("DELETE FROM locker_rooms")

            # Reset identity sequences so ids start at 1 again.
            cur.execute("ALTER TABLE bookings ALTER COLUMN id RESTART WITH 1")
            cur.execute("ALTER TABLE customers ALTER COLUMN id RESTART WITH 1")
            cur.execute("ALTER TABLE rinks ALTER COLUMN id RESTART WITH 1")
            cur.execute("ALTER TABLE locker_rooms ALTER COLUMN id RESTART WITH 1")

            # Rinks
            cur.execute("INSERT INTO rinks (name) VALUES (%s) RETURNING id", ("Stora",))
            big_rink_id = cur.fetchone()[0]
            cur.execute("INSERT INTO rinks (name) VALUES (%s) RETURNING id", ("Lilla",))
            small_rink_id = cur.fetchone()[0]

            # Locker rooms
            for number in range(1, 7):
                cur.execute(
                    "INSERT INTO locker_rooms (name) VALUES (%s)",
                    (f"Locker Room {number}",),
                )

            # Pick two locker rooms for the sample bookings.
            cur.execute("SELECT id FROM locker_rooms ORDER BY id LIMIT 2")
            locker_a, locker_b = (row[0] for row in cur.fetchall())

            # Customers
            customer_ids = {}
            for name in ("Frölunda HC U16", "Bäcken HC", "Göteborgs Konståkningsklubb"):
                cur.execute(
                    "INSERT INTO customers (name) VALUES (%s) RETURNING id", (name,)
                )
                customer_ids[name] = cur.fetchone()[0]

            # Bäcken HC: every other Wednesday 18:00 and Sunday 16:00 for 12 weeks
            first_wednesday = datetime(2026, 10, 21, 18, 0)
            first_sunday = datetime(2026, 10, 18, 16, 0)
            for week in range(0, 12, 2):
                for base_time in (first_wednesday, first_sunday):
                    cur.execute(
                        """
                        INSERT INTO bookings
                            (customer_id, rink_id, locker_room_id,
                             start_time, duration)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            customer_ids["Bäcken HC"],
                            big_rink_id,
                            locker_a,
                            base_time + timedelta(weeks=week),
                            240,
                        ),
                    )

            # Three bookings on 2026-11-05
            extra_bookings = [
                (
                    "Frölunda HC U16",
                    big_rink_id,
                    locker_b,
                    datetime(2026, 11, 5, 16, 0),
                    90,
                ),
                ("Bäcken HC", big_rink_id, locker_a, datetime(2026, 11, 5, 17, 30), 60),
                (
                    "Göteborgs Konståkningsklubb",
                    small_rink_id,
                    locker_b,
                    datetime(2026, 11, 5, 17, 30),
                    90,
                ),
            ]
            for name, rink_id, locker_id, start, duration in extra_bookings:
                cur.execute(
                    """
                    INSERT INTO bookings
                        (customer_id, rink_id, locker_room_id,
                         start_time, duration)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (customer_ids[name], rink_id, locker_id, start, duration),
                )

        conn.commit()
    print("Database seeded.")


if __name__ == "__main__":
    seed()
