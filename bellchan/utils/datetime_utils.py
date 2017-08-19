from datetime import datetime


def get_now_datetime():
    return datetime.now()


def get_now_day():
    dt = get_now_datetime()
    return dt.day
