# free_time/weekend.py
from datetime import datetime, time, date
from .strategy import FreeTimeStrategy

class WeekendStrategy(FreeTimeStrategy):
    def get_day_range(self, target_date: date):
        start = datetime.combine(target_date, time(10, 0))
        end = datetime.combine(target_date, time(23, 59))
        return start, end
