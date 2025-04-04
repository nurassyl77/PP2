import pygame
import random
import time

pygame.init()

# Окно
WIDTH = 800
HEIGHT = 600
cell_size = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake 2")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Шрифт
font = pygame.font.SysFont("Arial", 40)
total = 0
score = font.render(f"Score: {total}", True, WHITE)

# Местоположение змейки
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
clock = pygame.time.Clock()
fps = 10

# Время жизни еды
food_lifetime = 5

# 3 вида еды
food_types = {
    "small": {"color": RED, "points": 1},  # +1
    "medium": {"color": BLUE, "points": 3},  # +3
    "large": {"color": YELLOW, "points": 5},  # +5
}


# Функция для отрисовки змейки
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], cell_size, cell_size))


# Функция для появления еды
def random_food():
    x = random.randint(0, (WIDTH - cell_size) // cell_size) * cell_size
    y = random.randint(0, (HEIGHT - cell_size) // cell_size) * cell_size
    food_type = random.choice(list(food_types.keys()))  # Выбираем случайный тип еды
    return (x, y, food_type)


# Функция для проверки таймера еды
def check_food_timer(start_time, food_time):
    return time.time() - start_time > food_time


# Переменные для еды
food = random_food()
food_start_time = time.time()

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)
    draw_snake()

    # Проверяем, не истёк ли таймер еды
    if check_food_timer(food_start_time, food_lifetime):
        food = random_food()  # Генерация новой еды
        food_start_time = time.time()  # Сброс таймера для новой еды

    pygame.draw.rect(
        screen, food_types[food[2]]["color"], (food[0], food[1], cell_size, cell_size)
    )

    screen.blit(score, (10, 10))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # Управление змейкой
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    head_x = snake[0][0]
    head_y = snake[0][1]

    # Движение змейки
    if direction == "RIGHT":
        new_head = (head_x + cell_size, head_y)
    elif direction == "LEFT":
        new_head = (head_x - cell_size, head_y)
    elif direction == "UP":
        new_head = (head_x, head_y - cell_size)
    elif direction == "DOWN":
        new_head = (head_x, head_y + cell_size)

    # Проверка столкновений с границами
    if (
        new_head[0] < 0
        or new_head[0] >= WIDTH
        or new_head[1] < 0
        or new_head[1] > HEIGHT
    ):
        running = False

    if new_head in snake:
        running = False  # Если змейка съела себя

    snake.insert(0, new_head)

    # Проверяем, съела ли змейка еду
    if new_head[:2] == food[:2]:
        total += food_types[food[2]]["points"]
        food = random_food()  # Генерация новой еды
        food_start_time = time.time()  # Сброс таймера
        score = font.render(f"Score: {total}", True, WHITE)  # Обновляем счёт
    else:
        snake.pop()

    clock.tick(fps)

# Финальный экран с результатом
screen.fill(BLACK)
screen.blit(score, (325, 250))
pygame.display.update()
pygame.time.delay(3000)  # Финальный экран с результатом. После 3 секунд закроется

pygame.quit()