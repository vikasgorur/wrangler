from unittest.mock import Mock
from freezegun import freeze_time

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
