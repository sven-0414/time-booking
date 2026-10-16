"""Database access for rinks."""

from src.resources import Rink


class RinkRepository:
    """Reads and writes rinks to the database."""

    def __init__(self, conn):
        self.conn = conn

    def add(self, rink: Rink) -> Rink:
        """Insert a rink and set its id. Returns the same rink."""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO rinks (name) VALUES (%s) RETURNING id", (rink.name,)
            )
            rink.id = cur.fetchone()[0]
        self.conn.commit()
        return rink

    def find_by_id(self, rink_id: int) -> Rink:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM rinks WHERE id = %s", (rink_id,))
            row = cur.fetchone()
        if row is None:
            raise ValueError(f"No rink with id {rink_id}.")
        return Rink(name=row[1], id=row[0])

    def find_all(self) -> list[Rink]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM rinks ORDER BY id")
            rows = cur.fetchall()
        return [Rink(name=row[1], id=row[0]) for row in rows]
