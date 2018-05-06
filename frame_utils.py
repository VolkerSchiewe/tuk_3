import numpy as np

from models.frame import Frame


def interpolate_missing_frames(previous, following):
    assert (following.id - previous.id) > 1
    missing_ids = range(previous.id + 1, following.id)
    longitudes = np.interp(missing_ids, (previous.id, following.id), (previous.x, following.x))
    latitudes = np.interp(missing_ids, (previous.id, following.id), (previous.y, following.y))
    return [Frame(missing_ids[i], longitudes[i], latitudes[i]) for i in range(len(longitudes))]


def add_padding(frames, n):
    first_id = (frames[0].id % n)
    padded_frames = []
    padded_frames += [Frame(0, 0, 0)] * (first_id - 1)
    padded_frames += frames
    padded_frames += [Frame(0, 0, 0)] * (n - len(padded_frames))
    assert len(padded_frames) == n
    return padded_frames


def group_frames_by_hour(frames):
    grouped_frames = {}

    for frame in frames:
        group_id = int(frame.id / 60) + 1
        if group_id not in grouped_frames:
            grouped_frames[group_id] = list()
        grouped_frames[group_id].append(frame)

    return grouped_frames


def delta_encode(i_frame, frame):
    x = frame.x - i_frame.x
    y = frame.y - i_frame.y
    return Frame(frame.id, x, y)
