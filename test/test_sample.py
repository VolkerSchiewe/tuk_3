import datetime

from models.sample import Sample


def test_frame_id():
    sample = Sample(datetime.datetime(2018, 1, 1, 0, 0, 0), 0.0, 0.0, 0, 0)
    assert sample.frame_id() == 0
    sample = Sample(datetime.datetime(2018, 1, 1, 0, 0, 30), 0.0, 0.0, 0, 0)
    assert sample.frame_id() == 1
    sample = Sample(datetime.datetime(2018, 1, 1, 0, 1, 29), 0.0, 0.0, 0, 0)
    assert sample.frame_id() == 2
    sample = Sample(datetime.datetime(2018, 1, 1, 1, 0, 0), 0.0, 0.0, 0, 0)
    assert sample.frame_id() == 120
    sample = Sample(datetime.datetime(2018, 1, 1, 1, 0, 30), 0.0, 0.0, 0, 0)
    assert sample.frame_id() == 121
    sample = Sample(datetime.datetime(2018, 1, 1, 23, 59, 59), 0.0, 0.0, 0, 0)
    assert sample.frame_id() == 2879
