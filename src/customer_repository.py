"""Database access for customers."""

from src.customer import Customer


class CustomerRepository:
    """Reads and writes customers to the database."""

    def __init__(self, conn):
        self.conn = conn

    def add(self, customer: Customer) -> Customer:
        """Insert a customer and set its id. Returns the same customer."""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO customers (name) VALUES (%s) RETURNING id",
                (customer.name,),
            )
            customer.id = cur.fetchone()[0]
        self.conn.commit()
        return customer

    def find_by_id(self, customer_id: int) -> Customer:
        """Return the customer with the given id, or raise ValueError."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM customers WHERE id = %s", (customer_id,))
            row = cur.fetchone()
        if row is None:
            raise ValueError(f"No customer with id {customer_id}.")
        return Customer(name=row[1], id=row[0])

    def find_all(self) -> list[Customer]:
        """Return all customers, ordered by id."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM customers ORDER BY id")
            rows = cur.fetchall()
        return [Customer(name=row[1], id=row[0]) for row in rows]
