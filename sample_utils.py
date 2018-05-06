import numpy as np


def sample_with_highest_sed(samples, previous_frame, following_frame):
    time_in_frame = [sample.timestamp.second for sample in samples]
    predicted_longitudes = np.interp(time_in_frame, (0, 60), (previous_frame.x, following_frame.x))
    predicted_latitudes = np.interp(time_in_frame, (0, 60), (previous_frame.y, following_frame.y))
    highest_sed = -1
    highest_sed_sample = None

    for i, sample in enumerate(samples):
        sed = _euclidean_distance(predicted_latitudes[i], predicted_longitudes[i], sample.x, sample.y)
        if sed > highest_sed:
            highest_sed = sed
            highest_sed_sample = sample
    return highest_sed_sample


def _euclidean_distance(px, py, qx, qy):
    return np.sqrt(np.square(qx - px) + np.square(qy - py))
