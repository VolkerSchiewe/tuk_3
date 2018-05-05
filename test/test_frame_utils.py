import pytest

from frame_utils import interpolate_missing_frames
from models.frame import Frame


def test_interpolate_single_missing_frame():
    previous = Frame(1, 1.00, 3.00)
    following = Frame(3, 2.00, 6.00)
    expected = [Frame(2, 1.5, 4.5)]

    actual = interpolate_missing_frames(previous, following)
    assert expected == actual


def test_interpolate_multiple_missing_frames():
    previous = Frame(1, 1.00, 5.00)
    following = Frame(5, 5.00, 1.00)
    expected = [Frame(2, 2.0, 4.0), Frame(3, 3.0, 3.0), Frame(4, 4.0, 2.0)]

    actual = interpolate_missing_frames(previous, following)
    assert expected == actual


def test_error_on_interpolating_subsequent_frames():
    previous = Frame(1, 1.00, 5.00)
    following = Frame(2, 5.00, 1.00)

    with pytest.raises(AssertionError):
        interpolate_missing_frames(previous, following)
