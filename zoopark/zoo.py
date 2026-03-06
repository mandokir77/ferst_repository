"""
Система управления зоопарком с демонстрацией ООП концепций:
наследование, полиморфизм и композиция.
"""


# ============== 1. Базовый класс Animal ==============
class Animal:
    """Базовый класс для всех животных."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def make_sound(self) -> str:
        """Издать звук (будет переопределён в подклассах)."""
        return "Неизвестный звук"

    def eat(self, food: str = "еду") -> str:
        """Поесть."""
        return f"{self.name} ест {food}"


# ============== 2. Наследование: подклассы Animal ==============
class Bird(Animal):
    """Класс птиц с характерными атрибутами."""

    def __init__(self, name: str, age: int, wingspan: float):
        super().__init__(name, age)
        self.wingspan = wingspan  # размах крыльев в метрах

    def make_sound(self) -> str:
        return f"Чик-чирик! ({self.name} поёт)"

    def fly(self) -> str:
        return f"{self.name} летит с размахом крыльев {self.wingspan} м"


class Mammal(Animal):
    """Класс млекопитающих."""

    def __init__(self, name: str, age: int, fur_color: str):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self) -> str:
        return f"Рррр! ({self.name} рычит)"

    def run(self) -> str:
        return f"{self.name} бежит"


class Reptile(Animal):
    """Класс рептилий."""

    def __init__(self, name: str, age: int, is_venomous: bool = False):
        super().__init__(name, age)
        self.is_venomous = is_venomous

    def make_sound(self) -> str:
        return f"Шшш... ({self.name} шипит)"

    def bask_in_sun(self) -> str:
        return f"{self.name} греется на солнце"


# ============== 3. Полиморфизм ==============
def animal_sound(animals: list[Animal]) -> None:
    """Вызывает make_sound() для каждого животного в списке (полиморфизм)."""
    for animal in animals:
        print(animal.make_sound())


# ============== 5. Классы сотрудников ==============
class ZooEmployee:
    """Базовый класс для сотрудников зоопарка."""

    def __init__(self, name: str, position: str):
        self.name = name
        self.position = position


class ZooKeeper(ZooEmployee):
    """Смотритель за животными."""

    def __init__(self, name: str):
        super().__init__(name, "Смотритель")

    def feed_animal(self, animal: Animal, food: str) -> str:
        """Покормить животное."""
        return f"{self.name} кормит {animal.name}: {animal.eat(food)}"


class Veterinarian(ZooEmployee):
    """Ветеринар."""

    def __init__(self, name: str):
        super().__init__(name, "Ветеринар")

    def heal_animal(self, animal: Animal, ailment: str = "недомогание") -> str:
        """Вылечить животное."""
        return f"{self.name} лечит {animal.name} от {ailment}"


# ============== 4. Композиция: класс Zoo ==============
class Zoo:
    """Зоопарк, содержащий животных и сотрудников (композиция)."""

    def __init__(self, name: str):
        self.name = name
        self._animals: list[Animal] = []
        self._employees: list[ZooEmployee] = []

    def add_animal(self, animal: Animal) -> None:
        """Добавить животное в зоопарк."""
        self._animals.append(animal)
        print(f"Животное {animal.name} добавлено в {self.name}")

    def add_employee(self, employee: ZooEmployee) -> None:
        """Добавить сотрудника в зоопарк."""
        self._employees.append(employee)
        print(f"Сотрудник {employee.name} ({employee.position}) принят в {self.name}")

    def list_animals(self) -> list[Animal]:
        """Получить список животных."""
        return self._animals.copy()

    def list_employees(self) -> list[ZooEmployee]:
        """Получить список сотрудников."""
        return self._employees.copy()

    def make_all_sounds(self) -> None:
        """Услышать звуки всех животных."""
        print(f"\n--- Звуки животных в {self.name} ---")
        animal_sound(self._animals)


# ============== Демонстрация ==============
if __name__ == "__main__":
    # Создание животных
    parrot = Bird("Кеша", 3, 0.5)
    lion = Mammal("Симба", 5, "золотистый")
    snake = Reptile("Каа", 10, is_venomous=False)

    # Полиморфизм
    print("=== Полиморфизм: animal_sound() ===\n")
    animal_sound([parrot, lion, snake])

    # Создание зоопарка и сотрудников
    zoo = Zoo("Городской зоопарк")

    keeper = ZooKeeper("Иван Петров")
    vet = Veterinarian("Доктор Мария")

    zoo.add_employee(keeper)
    zoo.add_employee(vet)
    zoo.add_animal(parrot)
    zoo.add_animal(lion)
    zoo.add_animal(snake)

    # Звуки животных в зоопарке
    zoo.make_all_sounds()

    # Специфические методы сотрудников
    print("\n=== Действия сотрудников ===")
    print(keeper.feed_animal(lion, "мясо"))
    print(vet.heal_animal(snake, "линька"))
