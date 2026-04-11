from TaskManager import TaskManager
from TimeTracker import TimeTracker
from TimeJournal import TimeJournal
import numpy as np

if __name__ == "__main__":

    print("\n==== TaskManager =====")
    t1 = TaskManager()
    t1.add_task("Учёба", 50, "2026-04-02")
    t1.add_task("Спорт", 30, "2026-04-01")
    print("Total (9):", t1.total_minutes())

    print("\n===== TimeTracker =====")
    t2 = TimeTracker()
    t2.add_record("Учёба", 50, "2026-04-02")
    t2.add_record("Спорт", 30, "2026-04-01")
    t2.add_record("Проект", 120, "2026-04-03")

    print("Array:", np.array([r["minutes"] for r in t2.records]))
    print("Total (10):", t2.total_minutes())

    print("\n===== TimeJournal =====")
    t3 = TimeJournal()
    t3.add_record("Учёба", 50, "2026-04-02")
    t3.add_record("Спорт", 30, "2026-04-01")
    t3.add_record("Проект", 120, "2026-04-03")

    print(t3.to_dataframe())