from TaskManager import TaskManager
from TimeTracker import TimeTracker
from TimeJournal import TimeJournal
from TimeJournalSummary import TimeJournalSummary
from TimeJournalChart import TimeJournalChart
import numpy as np

if __name__ == "__main__":
#9
    print("\n==== TaskManager =====")
    t1 = TaskManager()
    t1.add_task("Учёба", 50, "2026-04-02")
    t1.add_task("Спорт", 30, "2026-04-01")
    print("Total (9):", t1.total_minutes())
#10
    print("\n===== TimeTracker =====")
    t2 = TimeTracker()
    t2.add_record("Учёба", 50, "2026-04-02")
    t2.add_record("Спорт", 30, "2026-04-01")
    t2.add_record("Проект", 120, "2026-04-03")

    print("Array:", np.array([r["minutes"] for r in t2.records]))
    print("Total (10):", t2.total_minutes())
#11
    print("\n===== TimeJournal =====")
    t3 = TimeJournal()
    t3.add_record("Учёба", 50, "2026-04-02")
    t3.add_record("Спорт", 30, "2026-04-01")
    t3.add_record("Проект", 120, "2026-04-03")

    print(t3.to_dataframe())
#12
    print("\n===== Summary =====")
    t4 = TimeJournalSummary()
    t4.add_record("Учёба", 50, "2026-04-02")
    t4.add_record("Учёба", 40, "2026-04-03")
    t4.add_record("Спорт", 30, "2026-04-01")

    print(t4.get_summary())
    t4.save_to_csv()
#13
    print("\n===== Chart =====")
    c = TimeJournalChart()
    c.add_record("Учёба", 50, "2026-04-02")
    c.add_record("Учёба", 40, "2026-04-03")
    c.add_record("Спорт", 30, "2026-04-01")
    c.add_record("Проект", 120, "2026-04-03")
    c.add_record("Кодинг", 70, "2026-04-04")
    c.plot_top5()