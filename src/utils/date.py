from datetime import datetime
from datetime import date
import calendar
import pytz


def now():
    """get the timestamp of now"""
    now_date = datetime.now()
    now_timestamp = int(datetime.timestamp(now_date))
    return now_timestamp


def today():
    today_date = datetime.now(pytz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_timestamp = int(datetime.timestamp(today_date))
    return today_timestamp


def day_in_sec():
    return 24 * 60 * 60




