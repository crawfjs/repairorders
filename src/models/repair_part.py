class RepairPart:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"<part name=\"{self.name}\" quantity=\"{self.quantity}\"/>"
