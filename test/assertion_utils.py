def frame_list_equals(frames, other_frame):
    if len(frames) != len(other_frame):
        return False

    for i, frame in enumerate(frames):
        if not frame_equals(frame, other_frame[i]):
            return False

    return True


def frame_equals(frame, other_frame):
    return frame.id == other_frame.id \
           and frame.x == other_frame.x \
           and frame.y == other_frame.y
