class Frame:
    def __init__(self, id: int, x: float, y: float, occupancy: int):
        self.id = id
        self.x = x
        self.y = y
        self.occupancy = occupancy

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
