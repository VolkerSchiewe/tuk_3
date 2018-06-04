from models.frame import Frame


class FrameGroup:
    def __init__(self, trajectory_id: int, frame_group_id: int, trip_id: int, occupancy: int, i_frame: Frame,
                 p_frames: [Frame]):
        self.trajectory_id = trajectory_id
        self.frame_group_id = frame_group_id
        self.trip_id = trip_id
        self.occupancy = bool(occupancy)
        self.i_frame = i_frame
        self.p_frames = p_frames

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
