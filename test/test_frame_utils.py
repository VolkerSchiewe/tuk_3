import unittest

from frame_utils import interpolate_missing_frames, _euclidean_distance
from models.frame import Frame
from test.assertion_utils import frame_list_equals


class TestFrameUtils(unittest.TestCase):
    def test_interpolate_single_missing_frame(self):
        previous = Frame(1, 1.00, 3.00)
        following = Frame(3, 2.00, 6.00)
        expected = [Frame(2, 1.5, 4.5)]

        actual = interpolate_missing_frames(previous, following)
        assert frame_list_equals(expected, actual)

    def test_interpolate_multiple_missing_frames(self):
        previous = Frame(1, 1.00, 5.00)
        following = Frame(5, 5.00, 1.00)
        expected = [Frame(2, 2.0, 4.0), Frame(3, 3.0, 3.0), Frame(4, 4.0, 2.0)]

        actual = interpolate_missing_frames(previous, following)
        assert frame_list_equals(expected, actual)

    def test_error_on_interpolating_subsequent_frames(self):
        previous = Frame(1, 1.00, 5.00)
        following = Frame(2, 5.00, 1.00)

        with self.assertRaises(AssertionError):
            interpolate_missing_frames(previous, following)


if __name__ == '__main__':
    unittest.main()
