import pandas as pd
from datetime import datetime


class TimeJournalSummary:
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

    def get_summary(self) -> pd.DataFrame:
        df = pd.DataFrame(self.records)
        if df.empty:
            return df

        df["minutes"] = df["minutes"].astype(int)

        summary = (
            df.groupby("task_name")["minutes"]
              .sum()
              .reset_index()
              .sort_values(by="minutes", ascending=False)
        )
        return summary

    def save_to_csv(self, filename: str = "tasks_summary.csv") -> None:
        summary = self.get_summary()
        summary.to_csv(filename, index=False)
        print(f"Файл сохранён: {filename}")


