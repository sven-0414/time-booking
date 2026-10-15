class Customer:
    """A customer in the time-booking system."""

    def __init__(self, name: str, id: int | None = None):
        name = name.strip()
        if len(name) < 5:
            raise ValueError("Name must be five characters or more.")
        self.name = name
        self.id = id

    def __str__(self):
        id_part = f"{self.id:04d}" if self.id is not None else "----"
        return f"{id_part}, {self.name}"
