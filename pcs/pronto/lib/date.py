import math
import datetime

from .wrapper import *


def get_time_now():
    return datetime.datetime.now()

def get_day():
    return datetime.datetime.now().day

@wrapper_cache
def get_statics_begin():
    return datetime.datetime(2016, 9, 12)


def get_current_week_range():
    day_of_week = datetime.datetime.now().isoweekday()
    now = datetime.datetime.now()
    date_from = get_previous_datetime(now, day_of_week)
    date_to = get_next_datetime(now, 7-day_of_week)
    return date_from, date_to


def get_time_format(date):
    return date.strftime('%Y-%W')


def get_next_datetime(data_from, days):
    return data_from + datetime.timedelta(days=days)


def get_previous_datetime(data_from, days):
    return data_from - datetime.timedelta(days=days)


def get_all_weeks_range():
    date_from = get_statics_begin()
    date_to = datetime.datetime.now()
    week_list = []
    weeks = int(math.ceil((date_to - date_from).days / 7)) + 1
    aligned_monday = False
    for week in range(weeks):
        if not aligned_monday:
            days = date_from.weekday()
            date_from = get_previous_datetime(date_from, days)
            this_sunday = get_next_datetime(date_from, 7)
            week_list.append((date_from, this_sunday, get_time_format(date_from)))
            aligned_monday = True
        else:
            this_sunday = get_next_datetime(date_from, 7)
            week_list.append((date_from, this_sunday, get_time_format(date_from)))
        date_from = this_sunday
    return week_list

