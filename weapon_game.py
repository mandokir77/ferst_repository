"""
Простая игра с оружием против монстров.
Применён принцип открытости/закрытости (OCP): новые типы оружия
добавляются без изменения класса Fighter и механизма боя.
"""

from abc import ABC, abstractmethod


# Шаг 1: Абстрактный класс для оружия
class Weapon(ABC):
    """Абстрактный класс оружия."""

    @abstractmethod
    def attack(self) -> str:
        """Выполнить атаку. Возвращает описание удара."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Название оружия."""
        pass


# Шаг 2: Конкретные типы оружия
class Sword(Weapon):
    """Меч."""

    @property
    def name(self) -> str:
        return "меч"

    def attack(self) -> str:
        return "наносит удар мечом"


class Bow(Weapon):
    """Лук."""

    @property
    def name(self) -> str:
        return "лук"

    def attack(self) -> str:
        return "наносит удар из лука"


class Axe(Weapon):
    """Топор - пример легко добавляемого нового оружия."""

    @property
    def name(self) -> str:
        return "топор"

    def attack(self) -> str:
        return "рубит топором"


# Шаг 3: Класс бойца
class Fighter:
    """Боец, управляемый игроком."""

    def __init__(self, name: str = "Боец", weapon: Weapon | None = None):
        self.name = name
        self._weapon = weapon

    def change_weapon(self, weapon: Weapon) -> None:
        """Сменить оружие бойца."""
        self._weapon = weapon
        print(f"{self.name} выбирает {weapon.name}.")

    def perform_attack(self) -> str | None:
        """Выполнить атаку текущим оружием."""
        if self._weapon is None:
            print("Боец не вооружён!")
            return None
        return self._weapon.attack()


# Класс монстра
class Monster:
    """Монстр."""

    def __init__(self, name: str = "Монстр", health: int = 1):
        self.name = name
        self.health = health
        self.alive = True

    def take_damage(self) -> None:
        """Монстр получает урон."""
        self.health -= 1
        if self.health <= 0:
            self.alive = False


# Шаг 4: Механизм боя
def fight(fighter: Fighter, monster: Monster) -> None:
    """
    Демонстрация боя между бойцом и монстром.
    Не зависит от конкретного типа оружия благодаря полиморфизму.
    """
    attack_description = fighter.perform_attack()
    if attack_description:
        print(f"{fighter.name} {attack_description}.")
        monster.take_damage()
        if monster.alive:
            print(f"{monster.name} всё ещё жив! (HP: {monster.health})")
        else:
            print("Монстр побеждён!")
    print()


def main():
    """Демонстрация игры."""
    fighter = Fighter("Боец")
    sword = Sword()
    bow = Bow()
    axe = Axe()

    # Бой с мечом
    monster1 = Monster("Монстр", health=1)
    fighter.change_weapon(sword)
    fight(fighter, monster1)

    # Бой с луком
    monster2 = Monster("Монстр", health=1)
    fighter.change_weapon(bow)
    fight(fighter, monster2)

    # Бой с топором (демонстрация лёгкого добавления нового оружия)
    monster3 = Monster("Монстр", health=1)
    fighter.change_weapon(axe)
    fight(fighter, monster3)


if __name__ == "__main__":
    main()
