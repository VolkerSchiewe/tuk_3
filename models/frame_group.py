class FrameGroup:
    def __init__(self, trajectory_id, frame_group_id, i_frame):
        self.trajectory_id = trajectory_id
        self.frame_group_id = frame_group_id
        self.i_frame = i_frame
        self.p_frames = []

    def delta_encoding(self):
        pass