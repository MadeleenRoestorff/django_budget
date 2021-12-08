from math import ceil
from datetime import date


def days_in_month(date_in):
    days_in_month = 31

    days_in_month = date(date_in.year, date_in.month, 1) - \
        date(date_in.year, date_in.month + 1, 1)

    return date(date_in.year, date_in.month, days_in_month)


def week_in_month(day_in_week, totalweeks=None):

    if totalweeks:
        day_in_week = days_in_month(day_in_week)

    week_number = ceil(
        (date(day_in_week.year, day_in_week.month,
              1).weekday()+day_in_week.day)/7
    )

    return week_number
