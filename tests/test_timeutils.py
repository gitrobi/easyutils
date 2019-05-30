import pytest
from easyutils.timeutils import *


def test_is_holiday():
    cases = [
        (datetime.date(2019,5,28), False),
        (datetime.date(2019,5,29), False),
        (datetime.date(2019,5,30), False),
        (datetime.date(2019,5,31), False),
        (datetime.date(2019,6,1), True),
    ]
    for day, result in cases:
        assert is_holiday(day) == result


def test_is_holiday_today():
    assert is_holiday_today() == False


def test_is_weekend():
    now_time = datetime.datetime.now()
    assert is_weekend(now_time) == False


def test_is_trade_date():
    now_time = datetime.datetime.now()
    assert is_holiday(now_time) == False
    assert is_weekend(now_time) == False
    assert is_trade_date(now_time) == True


def test_is_trade_time():
    #now_time = datetime.datetime.now()
    now_time = datetime.datetime(2019,5,30,9,47,24)
    assert is_trade_time(now_time) == True

    now_time = datetime.datetime(2019, 5, 30, 19, 47, 24)
    assert is_trade_time(now_time) == False


def test_is_trade_now():
    assert is_trade_date_now() == True
    assert is_trade_time_now() == False


def test_get_next_trade_date():
    now_time = datetime.datetime.now()
    next_trade_date = get_next_trade_date(now_time)
    assert next_trade_date.date() == datetime.date(2019,5,31)


def test_calc_next_trade_time_delta_seconds():
    seconds = calc_next_trade_time_delta_seconds()
    hours = int(seconds / 3600)
    minutes = int((seconds - hours * 3600) / 60)
    assert hours == 13 and minutes == 15