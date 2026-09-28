class Resource:
    """Object for bookable resources"""

    def __init__(self, name: str):
        name = name.strip()
        if len(name) >= 5:
            self.name = name
        else:
            raise ValueError("Name must be at least five characters.")

    def __str__(self) -> str:
        return self.name
