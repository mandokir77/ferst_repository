"""
Модуль для управления задачами (делами).
"""

from datetime import date
from typing import Optional


class Task:
    """Класс для управления задачами."""

    def __init__(self, description: str, deadline: date, status: bool = False):
        """
        Инициализация задачи.

        Args:
            description: описание задачи
            deadline: срок выполнения
            status: статус (False - не выполнено, True - выполнено)
        """
        self.description = description
        self.deadline = deadline
        self.status = status


# Список для хранения всех задач
tasks: list[Task] = []


def add_task(description: str, deadline: date) -> Task:
    """
    Добавить новую задачу.

    Args:
        description: описание задачи
        deadline: срок выполнения

    Returns:
        Созданная задача
    """
    task = Task(description=description, deadline=deadline, status=False)
    tasks.append(task)
    return task


def mark_task_done(index: int) -> bool:
    """
    Отметить задачу как выполненную по индексу в общем списке.

    Args:
        index: индекс задачи (0-based)

    Returns:
        True если задача найдена и отмечена, иначе False
    """
    if 0 <= index < len(tasks):
        tasks[index].status = True
        return True
    return False


def get_current_tasks() -> list[Task]:
    """
    Получить список текущих (не выполненных) задач.

    Returns:
        Список невыполненных задач
    """
    return [task for task in tasks if not task.status]


def print_current_tasks() -> None:
    """Вывести список текущих (не выполненных) задач в консоль."""
    current = get_current_tasks()
    if not current:
        print("Нет текущих задач.")
        return
    print("\n--- Текущие задачи ---")
    for i, task in enumerate(current, 1):
        print(f"{i}. {task.description} | Срок: {task.deadline}")
    print()


# Пример использования
if __name__ == "__main__":
    from datetime import date

    # Добавление задач
    add_task("Купить продукты", date(2025, 3, 10))
    add_task("Сдать отчёт", date(2025, 3, 8))
    add_task("Позвонить маме", date(2025, 3, 7))

    # Отмечаем одну задачу выполненной
    mark_task_done(1)

    # Вывод текущих задач
    print_current_tasks()
