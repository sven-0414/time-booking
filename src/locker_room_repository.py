"""Database access for locker rooms."""

from src.resources import LockerRoom


class LockerRoomRepository:
    """Reads and writes locker rooms to the database."""

    def __init__(self, conn):
        self.conn = conn

    def add(self, locker_room: LockerRoom) -> LockerRoom:
        """Insert a locker room and set its id. Returns the same object."""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO locker_rooms (name) VALUES (%s) RETURNING id",
                (locker_room.name,),
            )
            locker_room.id = cur.fetchone()[0]
        self.conn.commit()
        return locker_room

    def find_by_id(self, locker_room_id: int) -> LockerRoom:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, name FROM locker_rooms WHERE id = %s",
                (locker_room_id,),
            )
            row = cur.fetchone()
        if row is None:
            raise ValueError(f"No locker room with id {locker_room_id}.")
        return LockerRoom(name=row[1], id=row[0])

    def find_all(self) -> list[LockerRoom]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM locker_rooms ORDER BY id")
            rows = cur.fetchall()
        return [LockerRoom(name=row[1], id=row[0]) for row in rows]
