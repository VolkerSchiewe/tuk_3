import datetime
import unittest

from models.sample import Sample
from sample_utils import _euclidean_distance, sample_with_highest_sed
from test.assertion_utils import sample_equals


class TestFrameUtils(unittest.TestCase):
    def test_euclidean_distance(self):
        assert _euclidean_distance(0, 0, 5, 0) == 5
        assert _euclidean_distance(4, 0, 0, 0) == 4
        assert _euclidean_distance(0, 0, 4, 3) == 5
        assert _euclidean_distance(0, 0, -4, -3) == 5

    def test_sample_with_highest_sed(self):
        previous = Sample(datetime.time(0, 0, 0), 0, 0, 0, 0)
        following = Sample(datetime.time(0, 2, 0), 5, 5, 0, 0)
        expected = Sample(datetime.time(0, 1, 10), 1, 10, 0, 0)
        samples_in_same_frame = [expected,
                                 Sample(datetime.time(0, 1, 30), 2.5, 2.5, 0, 0),
                                 Sample(datetime.time(0, 1, 45), 3, 3, 0, 0)]

        actual = sample_with_highest_sed(samples_in_same_frame, previous, following)
        assert sample_equals(actual, expected)

    def test_sample_with_highest_sed_single_sample(self):
        previous = Sample(datetime.time(0, 0, 0), 0, 0, 0, 0)
        following = Sample(datetime.time(0, 2, 0), 5, 5, 0, 0)
        expected = Sample(datetime.time(0, 1, 10), 1, 10, 0, 0)
        samples_in_same_frame = [expected]

        actual = sample_with_highest_sed(samples_in_same_frame, previous, following)
        assert sample_equals(actual, expected)


if __name__ == '__main__':
    unittest.main()
