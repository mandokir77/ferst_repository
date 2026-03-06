"""
Пример использования системы управления учётными записями.
"""

from user_management import User, Admin


def main():
    # Создаём обычных сотрудников
    worker1 = User(1, "Иван Петров")
    worker2 = User(2, "Мария Сидорова")

    # Создаём администратора
    admin = Admin(100, "Алексей Администратор")

    # Администратор добавляет пользователей
    admin.add_user(worker1)
    admin.add_user(worker2)

    # Доступ к данным через геттеры (инкапсуляция)
    print(f"Сотрудник: {worker1.get_name()}, ID: {worker1.get_id()}, доступ: {worker1.get_access_level()}")
    print(f"Администратор: {admin.get_name()}, ID: {admin.get_id()}, доступ: {admin.get_access_level()}")

    print(f"\nПользователей в системе: {len(admin.get_users())}")

    # Удаление пользователя
    admin.remove_user(1)
    print(f"После удаления: {len(admin.get_users())} пользователь(ей)")


if __name__ == "__main__":
    main()
