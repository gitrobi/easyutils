import pytest
from easyutils.timeutils import is_holiday


def test_is_holiday():
    cases = [
        ("20190501", False),
        ("20190524", False),
        ("20190525", True),
        ("20190526", True),
    ]
    for day, result in cases:
        assert is_holiday(day) == result
