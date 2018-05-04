def frame_list_equals(frames, other_frames):
    if len(frames) != len(other_frames):
        return False

    for frame, other_frame in zip(frames, other_frames):
        if not frame_equals(frame, other_frame):
            return False

    return True


def frame_equals(frame, other_frame):
    return frame.id == other_frame.id \
           and frame.x == other_frame.x \
           and frame.y == other_frame.y


def sample_equals(sample, other_sample):
    return sample.timestamp == other_sample.timestamp \
           and sample.x == other_sample.x \
           and sample.y == other_sample.y \
           and sample.speed == other_sample.speed \
           and sample.occupancy == other_sample.occupancy
