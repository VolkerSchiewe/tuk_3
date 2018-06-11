import numpy as np

from models.frame import Frame


def interpolate_missing_frames(previous, following):
    # assert (following.id - previous.id) > 1
    missing_ids = range(previous.id + 1, following.id)
    longitudes = np.interp(missing_ids, (previous.id, following.id), (previous.x, following.x))
    latitudes = np.interp(missing_ids, (previous.id, following.id), (previous.y, following.y))
    return [Frame(missing_ids[i], longitudes[i], latitudes[i], previous.occupancy) for i in range(len(longitudes))]


def add_padding(frames, n):
    first_id = (frames[0].id % 15) if len(frames) > 0 else 0
    padded_frames = []
    padded_frames += [Frame(0, None, None, 0)] * first_id
    padded_frames += frames
    padded_frames += [Frame(0, None, None, 0)] * (n - len(padded_frames))
    assert len(padded_frames) == n
    return padded_frames


def group_frames(frames, group_size):
    grouped_frames = {}
    trip_id = -1
    last_occupancy = -1
    last_group_id = -1

    for frame in frames:
        group_id = int(frame.id / group_size) + 1

        if last_occupancy != frame.occupancy or last_group_id != group_id:
            trip_id += 1
            last_occupancy = frame.occupancy
            last_group_id = group_id

        key = (group_id, trip_id, frame.occupancy)

        if key not in grouped_frames:
            grouped_frames[key] = list()
        grouped_frames[key].append(frame)

    return grouped_frames


def delta_encode(i_frame, frame):
    if any(frame.x is None for frame in [i_frame, frame]):
        return frame
    x = frame.x - i_frame.x
    y = frame.y - i_frame.y
    return Frame(frame.id, x, y, frame.occupancy)
