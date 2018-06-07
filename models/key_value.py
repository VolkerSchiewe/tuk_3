class KeyValue:
    def __init__(self, id: int, obj: [], start: float, end: float, mbr: []):
        self.id = id
        self.obj = obj
        self.start = start
        self.end = end
        self.mbr = mbr

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
