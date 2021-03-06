import datetime

from frame.__main__ import create_frames, create_frame_groups
from frame.frame_utils import add_padding, delta_encode
from frame.models.frame import Frame
from frame.models.frame_group import FrameGroup


def test_create_frames_groups_sample_in_same_minute():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 0, 0), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 0, 30), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 0, 59), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 1, 0), 105.0, 105.5, 0, 0)]
    expected_frames = [Frame(0, 100.0, 100.5), Frame(1, 100.0, 100.5), Frame(2, 105.0, 105.5)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_interpolates_missing_frame():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 0, 0), 100.0, 100.0, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 1, 0), 200.0, 200.0, 0, 0)]
    expected_frames = [Frame(0, 100.0, 100.0), Frame(1, 150.0, 150.0), Frame(2, 200.0, 200.0)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_does_not_interpolate_first_missing_frames():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 3, 0), 100.0, 100.0, 0, 0)]
    expected_frames = [Frame(6, 100.0, 100.0)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frames_does_not_interpolate_last_missing_frames():
    trajectory = [(1, datetime.datetime(2017, 1, 1, 0, 57, 0), 100.0, 100.0, 0, 0)]
    expected_frames = [Frame(114, 100.0, 100.0)]
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
                  (1, datetime.datetime(2017, 1, 1, 0, 1, 30), 100.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 1, 40), 200.0, 100.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 1, 59), 149.0, 104.5, 0, 0),
                  (1, datetime.datetime(2017, 1, 1, 0, 2, 0), 150.0, 105.5, 0, 0)]
    expected_frames = [Frame(2, 100.0, 100.0), Frame(3, 200.0, 100.5), Frame(4, 150.0, 105.5)]
    actual_frames = create_frames(trajectory)
    assert actual_frames == expected_frames


def test_create_frame_groups():
    trajectory_id = 1
    frames = [Frame(1, 100.0, 100.0), Frame(2, 200.0, 100.0), Frame(3, 150.0, 150.0)]
    i_frame = Frame(1, 100.0, 100.0)
    p_frames = [Frame(0, 0.0, 0.0), Frame(2, 100.0, 0.0), Frame(3, 50.0, 50.0)]
    p_frames += [Frame(0, 0.0, 0.0)] * 56
    expected_frame_groups = [FrameGroup(trajectory_id, 1, i_frame, p_frames)]
    actual_frame_groups = create_frame_groups(trajectory_id, frames)
    assert actual_frame_groups == expected_frame_groups


def test_add_padding_fills_missing_frames_for_n_minutes_at_beginning_and_end():
    frames = [Frame(2, 200.0, 100.0), Frame(3, 150.0, 150.0)]
    expected_frames = [Frame(0, 0.0, 0.0), Frame(2, 200.0, 100.0), Frame(3, 150.0, 150.0)]
    expected_frames += [Frame(0, 0.0, 0.0)] * 56
    actual_frames = add_padding(frames, 59)
    assert actual_frames == expected_frames


def test_add_no_padding_if_frame_is_full():
    frames = [Frame(1, 200.0, 100.0)] * 59
    actual_frames = add_padding(frames, 59)
    assert actual_frames == frames


def test_add_full_padding_frame():
    frames = []
    expected_frames = [Frame(0, 0, 0)] * 59
    actual_frames = add_padding(frames, 59)
    assert actual_frames == expected_frames


def test_delta_encoding():
    i_frame = Frame(1, 100.0, 100.0)
    frame = Frame(1, 150.0, 50.0)
    expected_p_frame = Frame(1, 50.0, -50.0)
    actual_p_frame = delta_encode(i_frame, frame)
    assert actual_p_frame == expected_p_frame
