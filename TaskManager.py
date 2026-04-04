#9
from datetime import datetime
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name: str, minutes: int, date: str):
        if not task_name or not isinstance(task_name, str):
            print("Ошибка: название задачи пустое или некорректное")
            return
        if not isinstance(minutes, int) or minutes <= 0:
            print("Ошибка: минуты должны быть > 0")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Ошибка: дата должна быть в формате YYYY-MM-DD")
            return
        self.tasks.append({
            "task_name": task_name,
            "minutes": minutes,
            "date": date
        })
        print(f"Задача добавлена: {task_name}, {minutes} мин, {date}")

    def show_tasks(self):
        if not self.tasks:
            print("Задач пока нет.")
            return
        for t in self.tasks:
            print(f"{t['task_name']} — {t['minutes']} мин — {t['date']}")
if __name__ == "__main__":
    manager = TaskManager()

    manager.add_task("Math homework", 40, "2026-04-04")
    manager.add_task("Python practice", 50, "2026-04-04")

    print("\nСписок всех задач:")
    manager.show_tasks()