# free_time/strategy.py
from abc import ABC, abstractmethod
from datetime import datetime, date

class FreeTimeStrategy(ABC):
    @abstractmethod
    def get_day_range(self, target_date: date) -> tuple[datetime, datetime]:
        pass
