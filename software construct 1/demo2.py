# pylint: disable=missing-module-docstring
import datetime


def NextDate(year, month, day):
    try:
        current_date = datetime.date(year, month, day)
        next_date = current_date + datetime.timedelta(days=1)
        return next_date.strftime("%Y-%m-%d")
    except ValueError:
        return "Invalid date"


print(NextDate(2025, 6, 1))
print(NextDate(2025, 12, 31))
print(NextDate(2025, 2, 28))
print(NextDate(2024, 2, 28))
