from datetime import datetime


def today():
    """get the timestamp of now"""
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    return timestamp