class Customer:
    """A Class representing the customer in the time-booking system"""

    _next_id = 1

    def __init__(self, name: str):
        name = name.strip()
        if len(name) <= 5:
            raise ValueError("Name must be five characters or more.")
        self.name = name
        self.id = Customer._next_id
        Customer._next_id += 1

    def __str__(self):
        return f"{self.id:04d}, {self.name}"
