import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class TimeJournalChart:
    def __init__(self):
        self.records = []

    def add_record(self, task_name: str, minutes: int, date: str):
        if not task_name:
            raise ValueError("task_name не может быть пустым")

        if minutes <= 0:
            raise ValueError("minutes должно быть > 0")

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date должен быть YYYY-MM-DD")

        self.records.append({
            "task_name": task_name,
            "minutes": minutes,
            "date": date
        })

    def get_top5(self):
        df = pd.DataFrame(self.records)

        if df.empty:
            return df

        summary = (
            df.groupby("task_name")["minutes"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        return summary

    def plot_top5(self, filename="top5_tasks.png"):
        df = self.get_top5()

        if df.empty:
            print("Нет данных для графика")
            return

        plt.figure()

        plt.barh(df["task_name"], df["minutes"])
        plt.xlabel("Minutes")
        plt.ylabel("Task Name")
        plt.title("Top 5 Tasks by Time")
        plt.gca().invert_yaxis()

        plt.tight_layout()
        plt.savefig(filename)

        print(f"График сохранён: {filename}")
        plt.show()

