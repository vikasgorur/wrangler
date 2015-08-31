from datetime import datetime
from freezegun import freeze_time
from unittest.mock import Mock

import wrangler.wrangler as w

def test_validate_run_times():
    valid_run_times = [
        [(11, 23), (0, 0)],
        [(1, 2), (23, 59)],
        [(0, 60)]
    ]
    for rt in valid_run_times:
        conf = Mock(RUN_AT=rt)
        assert w.validate_run_times(conf)

    invalid_run_times = [
        [],
        [(12, 61)],
        [(24, 5)]
    ]
    for rt in invalid_run_times:
        conf = Mock(RUN_AT=rt)
        assert not w.validate_run_times(conf)

def test_next_run_time():
    conf = Mock(RUN_AT=[(11, 15), (20, 45)])

    with freeze_time("2015-08-30 9:46"):
        assert w.next_run_time(conf) == datetime(2015, 8, 30, 11, 15)
    with freeze_time("2015-08-30 19:05"):
        assert w.next_run_time(conf) == datetime(2015, 8, 30, 20, 45)
    with freeze_time("2015-08-30 20:46"):
        assert w.next_run_time(conf) == datetime(2015, 8, 31, 11, 15)
