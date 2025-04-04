import pygame
import random

pygame.init()

# Экранның параметрлері
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Змейка")

# Ойынға қажетті түстер
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Тексттерге қажет шрифт
font = pygame.font.Font(None, 36)

# Ойынның параметрлері
clock = pygame.time.Clock()
initial_speed = 10
level = 1
score = 0


# ---------Алманың функциясы----------
def generate_apple(snake):
    while True:
        x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        if (x, y) not in snake:
            return x, y


# ----------Негізгі ойынның функциясы-----------
def main():
    global score, level

    running = True
    snake = [(300, 300), (280, 300), (260, 300)]  # Змейканың бастапқы координаталары
    direction = "RIGHT"
    food = generate_apple(snake)
    speed = initial_speed

    while running:
        screen.fill(BLACK)

        # Жасаған іс-әрекеттерді тексеру:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        elif keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"
        elif keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        elif keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"

        # Змейканың қозғалысы
        head_x = snake[0][0]
        head_y = snake[0][1]
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        # Экранның қабырғаларына немесе өзіне тигендігін тексереміз
        if (
            head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= HEIGHT
            or (head_x, head_y) in snake
        ):
            running = False

        # Змейканың тұрған орнын ауыстырамыз (яғни snake дейтін массивтін алдына жаңадан координатасын қосамыз)
        snake.insert(0, (head_x, head_y))

        # Алманы жеу
        if (head_x, head_y) == food:
            score += 1

            # Әрбір 4 ұпай сайын жылдамдығын арттырамыз
            if score != 0 and score % 4 == 0:
                level += 1
                speed += 2

            food = generate_apple(snake)  # Келесі алманың координатасы
        else:
            snake.pop()

        # Алма мен змейканың суретін саламыз

        # Змейка:
        for part_of_snake in snake:
            pygame.draw.rect(
                screen,
                GREEN,
                (part_of_snake[0], part_of_snake[1], BLOCK_SIZE, BLOCK_SIZE),
            )
        # Алма:
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

        # Ұпай мен деңгей көрсеткіші
        score_txt = font.render(f"Score: {score} Level: {level}", True, WHITE)
        screen.blit(score_txt, (10, 10))

        # ---Экранды обновить етеміз---
        pygame.display.flip()
        clock.tick(speed)

    # ---Ойын біткеннен кейінгі хабарлама---
    final_score = font.render(
        f"Your score: {score}    Your level: {level}", True, WHITE
    )
    game_over_text = font.render("Game Over! Press any key to exit", True, WHITE)
    screen.fill(BLACK)
    screen.blit(final_score, (240, 200))
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                pygame.quit()


# Ойын
main()