import numpy as np
from datetime import datetime

class TimeTracker:
    def __init__(self):
        self.records = []
    def add_record(self, name: str, minutes: int, date: str):

        if not name:
            raise ValueError("name не может быть пустым")
        if minutes <= 0:
            raise ValueError("minutes должно быть больше 0")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date должно быть в формате YYYY-MM-DD")

        record = {"name": name, "minutes": minutes, "date": date}
        self.records.append(record)

    def total_minutes(self):
        minutes_array = np.array([rec["minutes"] for rec in self.records])
        return np.sum(minutes_array)

if __name__ == "__main__":
    tracker = TimeTracker()

    tracker.add_record("Учёба", 50, "2026-04-01")
    tracker.add_record("Спорт", 30, "2026-04-01")
    tracker.add_record("Проект", 120, "2026-04-02")

    print("Общая сумма минут:", tracker.total_minutes())