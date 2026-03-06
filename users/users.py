"""
Система управления учётными записями пользователей для небольшой компании.
Поддерживает обычных сотрудников (User) и администраторов (Admin).
"""


class User:
    """Класс обычного пользователя (сотрудника)."""

    def __init__(self, user_id: int, name: str, access_level: str = "user"):
        self.__id = user_id
        self.__name = name
        self.__access_level = access_level if access_level else "user"

    # Методы доступа (getters)
    def get_id(self) -> int:
        """Возвращает уникальный идентификатор пользователя."""
        return self.__id

    def get_name(self) -> str:
        """Возвращает имя пользователя."""
        return self.__name

    def get_access_level(self) -> str:
        """Возвращает уровень доступа пользователя."""
        return self.__access_level

    # Методы изменения (setters)
    def set_id(self, user_id: int) -> None:
        """Устанавливает идентификатор пользователя."""
        self.__id = user_id

    def set_name(self, name: str) -> None:
        """Устанавливает имя пользователя."""
        self.__name = name

    def set_access_level(self, access_level: str) -> None:
        """Устанавливает уровень доступа пользователя."""
        self.__access_level = access_level

    def __str__(self) -> str:
        return f"User(id={self.__id}, name='{self.__name}', access_level='{self.__access_level}')"


class Admin(User):
    """Класс администратора. Наследуется от User. Может управлять пользователями."""

    def __init__(self, user_id: int, name: str):
        super().__init__(user_id, name, access_level="admin")
        self.__users: list[User] = []

    def get_access_level(self) -> str:
        """Возвращает уровень доступа администратора ('admin')."""
        return "admin"

    def add_user(self, user: User) -> bool:
        """Добавляет пользователя в список. Возвращает True при успехе."""
        if not isinstance(user, User):
            return False
        if any(u.get_id() == user.get_id() for u in self.__users):
            return False  # Пользователь с таким ID уже существует
        self.__users.append(user)
        return True

    def remove_user(self, user_id: int) -> bool:
        """Удаляет пользователя по ID из списка. Возвращает True при успехе."""
        for i, user in enumerate(self.__users):
            if user.get_id() == user_id:
                self.__users.pop(i)
                return True
        return False

    def get_users(self) -> list[User]:
        """Возвращает копию списка пользователей (только для чтения)."""
        return list(self.__users)

    def __str__(self) -> str:
        return f"Admin(id={self.get_id()}, name='{self.get_name()}', access_level='admin', users_count={len(self.__users)})"

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