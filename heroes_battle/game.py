from heroes_battle.hero import Hero


class Game:
    """Консольная игра «Битва героев» между игроком и компьютером."""

    def __init__(self, player: Hero, computer: Hero) -> None:
        self.player = player
        self.computer = computer

    def _print_turn(self, attacker: Hero, defender: Hero, round_num: int) -> None:
        print(f"--- Раунд {round_num} ---")
        print(f"{attacker.name} атакует {defender.name}!")
        print(f"У {defender.name} осталось здоровья: {defender.health}")

    def start(self) -> None:
        """Запускает игру: чередует ходы, пока один из героев не погибнет."""
        print("=" * 40)
        print("       БИТВА ГЕРОЕВ")
        print("=" * 40)
        print(f"{self.player.name}  vs  {self.computer.name}")
        print(
            f"Здоровье: {self.player.health} HP | "
            f"Сила удара: {self.player.attack_power}"
        )
        print(
            f"Здоровье: {self.computer.health} HP | "
            f"Сила удара: {self.computer.attack_power}"
        )
        print()

        round_num = 1

        while self.player.is_alive() and self.computer.is_alive():
            self.player.attack(self.computer)
            self._print_turn(self.player, self.computer, round_num)

            if not self.computer.is_alive():
                break

            self.computer.attack(self.player)
            self._print_turn(self.computer, self.player, round_num)
            print()

            round_num += 1

        winner = self.player if self.player.is_alive() else self.computer
        print("=" * 40)
        print(f"Победитель: {winner.name}!")
        print("=" * 40)
