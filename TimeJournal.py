#11
import pandas as pd
from datetime import datetime

class TimeJournal:
    def __init__(self):
        self.records = []

    def add_record(self, task_name: str, minutes: int, date: str):

        if not task_name:
            raise ValueError("task_name не может быть пустым")
        if minutes <= 0:
            raise ValueError("minutes должно быть больше 0")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date должно быть в формате YYYY-MM-DD")
        self.records.append({
            "task_name": task_name,
            "minutes": minutes,
            "date": date
        })

    def to_dataframe(self):
        df = pd.DataFrame(self.records)
        if df.empty:
            return df
        df["task_name"] = df["task_name"].astype(str)
        df["minutes"] = df["minutes"].astype(int)
        df["date"] = pd.to_datetime(df["date"])

        df = df.sort_values(by="date").reset_index(drop=True)

        return df

if __name__ == "__main__":
    journal = TimeJournal()

