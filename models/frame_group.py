from models.frame import Frame


class FrameGroup:
    def __init__(self, trajectory_id: int, frame_group_id: int, i_frame: Frame, p_frames: [Frame]):
        self.trajectory_id = trajectory_id
        self.frame_group_id = frame_group_id
        self.i_frame = i_frame
        self.p_frames = p_frames

    def delta_encoding(self):
        raw_x = self.i_frame.x
        raw_y = self.i_frame.y
        for frame in self.p_frames:
            frame.x = frame.x - raw_x
            frame.y = frame.y - raw_y
