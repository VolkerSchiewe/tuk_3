import numpy as np

from models.frame import Frame


def interpolate_missing_frames(previous, following):
    assert (following.id - previous.id) > 1
    missing_ids = range(previous.id + 1, following.id)
    longitudes = np.interp(missing_ids, (previous.id, following.id), (previous.x, following.x))
    latitudes = np.interp(missing_ids, (previous.id, following.id), (previous.y, following.y))
    return [Frame(missing_ids[i], longitudes[i], latitudes[i]) for i in range(len(longitudes))]
