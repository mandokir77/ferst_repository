"""
Игра «Змейка» на Pygame.

Управление: стрелки или WASD.
Перезапуск после проигрыша: пробел или Enter.
Выход: Esc или закрытие окна.
"""

import random
import sys

import pygame

# --- Настройки окна и сетки ---
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20  # размер одной клетки в пикселях

# Количество клеток по горизонтали и вертикали
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Скорость игры (кадров в секунду)
FPS = 10

# Цвета (R, G, B)
COLOR_BG = (20, 25, 35)
COLOR_GRID = (35, 42, 55)
COLOR_SNAKE_HEAD = (80, 220, 120)
COLOR_SNAKE_BODY = (50, 180, 90)
COLOR_FOOD = (240, 80, 80)
COLOR_TEXT = (230, 230, 230)
COLOR_GAME_OVER = (255, 200, 80)


# Направления движения: (смещение по X, смещение по Y)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_food_position(snake_body: list[tuple[int, int]]) -> tuple[int, int]:
    """Возвращает координаты еды на свободной клетке (не на змейке)."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake_body:
            return pos


def draw_grid(surface: pygame.Surface) -> None:
    """Рисует лёгкую сетку для наглядности."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))


def draw_cell(
    surface: pygame.Surface,
    grid_pos: tuple[int, int],
    color: tuple[int, int, int],
    inset: int = 2,
) -> None:
    """Рисует закрашенный квадрат в координатах сетки."""
    x, y = grid_pos
    rect = pygame.Rect(
        x * CELL_SIZE + inset,
        y * CELL_SIZE + inset,
        CELL_SIZE - 2 * inset,
        CELL_SIZE - 2 * inset,
    )
    pygame.draw.rect(surface, color, rect, border_radius=4)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Змейка")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)
    big_font = pygame.font.SysFont("consolas", 36)

    # Начальное состояние змейки: три сегмента по центру, движение вправо
    snake: list[tuple[int, int]] = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
    ]
    direction = RIGHT
    next_direction = RIGHT  # буфер: направление применится на следующем шаге

    food = random_food_position(snake)
    score = 0
    game_over = False

    while True:
        # --- Обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Перезапуск после проигрыша
                if game_over and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    snake = [
                        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
                        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
                    ]
                    direction = RIGHT
                    next_direction = RIGHT
                    food = random_food_position(snake)
                    score = 0
                    game_over = False
                    continue

                # Смена направления (нельзя развернуться на 180°)
                key_dirs = {
                    pygame.K_UP: UP,
                    pygame.K_w: UP,
                    pygame.K_DOWN: DOWN,
                    pygame.K_s: DOWN,
                    pygame.K_LEFT: LEFT,
                    pygame.K_a: LEFT,
                    pygame.K_RIGHT: RIGHT,
                    pygame.K_d: RIGHT,
                }
                if not game_over and event.key in key_dirs:
                    new_dir = key_dirs[event.key]
                    # Запрещаем движение в противоположную сторону
                    if (new_dir[0] + direction[0], new_dir[1] + direction[1]) != (0, 0):
                        next_direction = new_dir

        if not game_over:
            direction = next_direction

            # Новая позиция головы
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Столкновение со стеной
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                game_over = True
            # Столкновение с собой
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)

                # Съели еду — растём и добавляем очки
                if new_head == food:
                    score += 10
                    food = random_food_position(snake)
                else:
                    # Иначе хвост укорачивается (змейка «движется»)
                    snake.pop()

        # --- Отрисовка ---
        screen.fill(COLOR_BG)
        draw_grid(screen)

        draw_cell(screen, food, COLOR_FOOD)

        for i, segment in enumerate(snake):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            draw_cell(screen, segment, color)

        score_text = font.render(f"Счёт: {score}", True, COLOR_TEXT)
        screen.blit(score_text, (10, 10))

        if game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            lines = [
                big_font.render("Игра окончена!", True, COLOR_GAME_OVER),
                font.render(f"Итоговый счёт: {score}", True, COLOR_TEXT),
                font.render("Пробел — новая игра", True, COLOR_TEXT),
            ]
            y = WINDOW_HEIGHT // 2 - 60
            for line in lines:
                rect = line.get_rect(center=(WINDOW_WIDTH // 2, y))
                screen.blit(line, rect)
                y += 40

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
