import datetime

from main import create_frames
from models.frame import Frame


def test_create_frames_groups_sample_in_same_minute():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 0, 0), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 0, 30), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 0, 59), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 1, 0), 105.0, 105.5, 0, 0)]
    expected_frames = [Frame(0, 100.0, 100.5), Frame(1, 105.0, 105.5)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_interpolates_missing_frame():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 0, 0), 100.0, 100.0, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 0), 200.0, 200.0, 0, 0)]
    expected_frames = [Frame(0, 100.0, 100.0), Frame(1, 150.0, 150.0), Frame(2, 200.0, 200.0)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_does_not_interpolate_first_missing_frames():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 3, 0), 100.0, 100.0, 0, 0)]
    expected_frames = [Frame(3, 100.0, 100.0)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_does_not_interpolate_last_missing_frames():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 57, 0), 100.0, 100.0, 0, 0)]
    expected_frames = [Frame(57, 100.0, 100.0)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_performs_sed_to_select_samples_in_same_frame():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 1, 0), 100.0, 100.0, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 0), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 30), 200.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 59), 149.0, 104.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 3, 0), 150.0, 105.5, 0, 0)]
    expected_frames = [Frame(1, 100.0, 100.0), Frame(2, 200.0, 100.5), Frame(3, 150.0, 105.5)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_performs_sed_to_select_samples_in_same_frame():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 1, 0), 100.0, 100.0, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 0), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 30), 200.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 59), 149.0, 104.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 3, 0), 150.0, 105.5, 0, 0)]
    expected_frames = [Frame(1, 100.0, 100.0), Frame(2, 200.0, 100.5), Frame(3, 150.0, 105.5)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames
