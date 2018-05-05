from models.frame import Frame


class Sample:
    def __init__(self, timestamp, x, y, speed, occupancy):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.speed = speed
        self.occupancy = occupancy

    def to_frame(self):
        return Frame(self.frame_id(), self.x, self.y)

    def frame_id(self):
        return self.timestamp.hour * 60 + self.timestamp.minute

    @classmethod
    def from_tuple(cls, tuple):
        return Sample(tuple[1], tuple[2], tuple[3], tuple[4], tuple[5])

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
