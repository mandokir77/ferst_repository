class Hero:
    """Герой с именем, здоровьем и силой удара."""

    def __init__(self, name: str, health: int = 100, attack_power: int = 20) -> None:
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other: "Hero") -> None:
        """Наносит урон другому герою в размере своей силы удара."""
        other.health -= self.attack_power
        if other.health < 0:
            other.health = 0

    def is_alive(self) -> bool:
        """Возвращает True, если здоровье героя больше 0."""
        return self.health > 0
