import datetime

from frame.models.frame import Frame


class Sample:
    def __init__(self, timestamp: datetime.datetime, x: float, y: float, speed: int, occupancy: int):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.speed = speed
        self.occupancy = occupancy

    @classmethod
    def from_row(cls, row):
        return Sample(row[1], row[2], row[3], row[5], row[4])

    def to_frame(self):
        return Frame(self.frame_id(), self.x, self.y, self.occupancy)

    def frame_id(self):
        return self.timestamp.hour * 120 + self.timestamp.minute * 2 + int(self.timestamp.second / 30)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
