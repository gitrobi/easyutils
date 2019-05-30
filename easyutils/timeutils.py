# coding:utf8
import datetime
import time
import requests

from datetime import timedelta
from functools import lru_cache


@lru_cache()
def _is_holiday2(day):
    """
    判断是否节假日
    :param day: 日期， 格式为 '20160404'
    :return: bool
    """
    api = 'http://www.easybots.cn/api/holiday.php'
    params = {'d': day}
    rep = requests.get(api, params)
    res = rep.json()[day if isinstance(day, str) else day[0]]
    return True if res == "1" else False


@lru_cache()
def _is_holiday(day):
    """
    判断是否节假日, api 来自百度 apistore: http://apistore.baidu.com/apiworks/servicedetail/1116.html
    :param day: 日期， 格式为 '20160404'
    :return: bool
    """
    api = "http://tool.bitefu.net/jiari/"
    params = {"d": day, "apiserviceid": 1116}
    rep = requests.get(api, params)
    res = rep.text
    return True if res != "0" else False


def is_holiday(now_time):
    """
    判断是否节假日
    :param now_time: datetime.datetime.now()
    :return:
    """
    day = now_time.strftime("%Y%m%d")
    return _is_holiday(day)


def is_holiday_today():
    """
    判断今天是否时节假日
    :return: bool
    """
    return is_holiday(datetime.date.today())


def is_weekend(now_time):
    """
    判断当前是不是周末
    :param now_time: datetime.datetime.now()
    :return:
    """
    return now_time.weekday() >= 5


def is_trade_date(now_time):
    return not (is_holiday(now_time) or is_weekend(now_time))


OPEN_TIME = (
    (datetime.time(9, 15, 0), datetime.time(11, 30, 0)),
    (datetime.time(13, 0, 0), datetime.time(15, 0, 0)),
)

PAUSE_TIME = (
    (datetime.time(11, 30, 0), datetime.time(12, 59, 30)),
)

CONTINUE_TIME = (
    (datetime.time(12, 59, 30), datetime.time(13, 0, 0)),
)

CLOSE_TIME = (
    (datetime.time(14, 54, 30), datetime.time(15, 0, 0)),
)


def is_trade_time(now_time):
    """
    :param now_time: datetime.time()
    :return:
    """
    now = now_time.time()
    for begin, end in OPEN_TIME:
        if begin <= now < end:
            return True
    else:
        return False


def is_pause(now_time):
    """
    :param now_time:
    :return:
    """
    now = now_time.time()
    for b, e in PAUSE_TIME:
        if b <= now < e:
            return True


def is_continue(now_time):
    now = now_time.time()
    for b, e in CONTINUE_TIME:
        if b <= now < e:
            return True
    return False


def is_closing(now_time):
    now = now_time.time()
    for b, e in CLOSE_TIME:
        if b <= now < e:
            return True
    return False


def is_trade_date_now():
    """
    判断现在是否是交易日
    :return:
    """
    now_time = datetime.datetime.now()
    return is_trade_date(now_time)


def is_trade_time_now():
    """
    判断现在是否是交易日
    :return:
    """
    now_time = datetime.datetime.now()
    #now_time = time.localtime()
    return is_trade_time(now_time)


def get_next_trade_date(now_time):
    """
    :param now_time: datetime.datetime
    :return:
    >>> import datetime
    >>> get_next_trade_date(datetime.date(2016, 5, 5))
    datetime.date(2016, 5, 6)
    """
    now = now_time
    max_days = 365
    days = 0
    while 1:
        days += 1
        now += datetime.timedelta(days=1)
        if is_trade_date(now):
            if isinstance(now, datetime.date):
                return now
            else:
                return now.date()
        if days > max_days:
            raise ValueError('无法确定 %s 下一个交易日' % now_time)


def calc_next_trade_time_delta_seconds():
    now_time = datetime.datetime.now()
    now = (now_time.hour, now_time.minute, now_time.second)
    if now < (9, 15, 0):
        next_trade_start = now_time.replace(
            hour=9, minute=15, second=0, microsecond=0
        )
    elif (12, 0, 0) < now < (13, 0, 0):
        next_trade_start = now_time.replace(
            hour=13, minute=0, second=0, microsecond=0
        )
    elif now > (15, 0, 0):
        distance_next_work_day = 1
        while True:
            target_day = now_time + timedelta(days=distance_next_work_day)
            if is_holiday(target_day):
                distance_next_work_day += 1
            else:
                break

        day_delta = timedelta(days=distance_next_work_day)
        next_trade_start = (now_time + day_delta).replace(
            hour=9, minute=15, second=0, microsecond=0
        )
    else:
        return 0
    time_delta = next_trade_start - now_time
    return time_delta.total_seconds()
