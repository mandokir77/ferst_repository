from heroes_battle.game import Game
from heroes_battle.hero import Hero


def main() -> None:
    player_name = input("Введите имя вашего героя: ").strip() or "Игрок"
    computer_name = "Компьютер"

    player = Hero(name=player_name)
    computer = Hero(name=computer_name)

    game = Game(player=player, computer=computer)
    game.start()


if __name__ == "__main__":
    main()
