# free_time/weekday.py
from datetime import datetime, time, date
from .strategy import FreeTimeStrategy

class WeekdayStrategy(FreeTimeStrategy):
    def get_day_range(self, target_date: date):
        start = datetime.combine(target_date, time(8, 0))
        end = datetime.combine(target_date, time(22, 0))
        return start, end
