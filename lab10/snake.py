import pygame
import sys
import random
import psycopg2
from datetime import datetime

# Database connection
try:
    conn = psycopg2.connect(
        dbname="snake_score",
        user="postgres",
        password="Nurassyl1948",
        host="localhost",
        client_encoding='UTF8'
    )
    cur = conn.cursor()
except psycopg2.OperationalError as e:
    print(f"Failed to connect to database: {e}")
    sys.exit(1)

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_progress (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        current_level INTEGER DEFAULT 1,
        high_score INTEGER DEFAULT 0,
        last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Game setup
pygame.init()
WIDTH, HEIGHT = 600, 500
BLOCK_SIZE = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

LEVELS = {
    1: {"speed": 5, "walls": []},
    2: {"speed": 7, "walls": [pygame.Rect(150, 150, 300, 25)]},
    3: {"speed": 9, "walls": [pygame.Rect(150, 150, 300, 25), pygame.Rect(75, 100, 25, 300)]},
    4: {"speed": 11, "walls": [pygame.Rect(150, 150, 300, 25), pygame.Rect(75, 100, 25, 300), pygame.Rect(200, 250, 150, 25)]}
}

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.head = pygame.Rect(100, 100, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(75, 100, BLOCK_SIZE, BLOCK_SIZE)]
        self.direction = (1, 0)

    def move(self):
        self.body.append(pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        self.head.x += self.direction[0] * BLOCK_SIZE
        self.head.y += self.direction[1] * BLOCK_SIZE
        self.body.pop(0)

    def check_collision(self, walls):
        if self.head.x < 0 or self.head.x >= WIDTH or self.head.y < 0 or self.head.y >= HEIGHT:
            return True
        for wall in walls:
            if self.head.colliderect(wall):
                return True
        for segment in self.body:
            if self.head.colliderect(segment):
                return True
        return False

class Game:
    def __init__(self):
        self.snake = Snake()
        self.apple = pygame.Rect(300, 300, BLOCK_SIZE, BLOCK_SIZE)
        self.score = 0
        self.level = 1
        self.username = ""
        self.paused = False
        self.loaded_level = 1

    def get_username(self):
        username = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username:
                        return username
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
            screen.fill((0, 0, 0))
            text = font.render(f"Enter username: {username}", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()

    def save_progress(self):
        try:
            cur.execute("""
                INSERT INTO user_progress (username, current_level, high_score)
                VALUES (%s, %s, %s)
                ON CONFLICT (username)
                DO UPDATE SET
                    current_level = EXCLUDED.current_level,
                    high_score = GREATEST(user_progress.high_score, EXCLUDED.high_score),
                    last_played = CURRENT_TIMESTAMP
            """, (self.username, self.level, self.score))
            conn.commit()
        except Exception as e:
            print(f"Error saving progress: {e}")

    def load_progress(self):
        try:
            cur.execute("SELECT current_level, high_score FROM user_progress WHERE username = %s", (self.username,))
            result = cur.fetchone()
            if result:
                self.loaded_level = result[0]
                return result[0], result[1]
        except Exception as e:
            print(f"Error loading progress: {e}")
        return 1, 0

    def game_over(self):
        self.save_progress()
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER! Press SPACE to continue", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 10))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_progress()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

        self.snake.reset()
        self.score = 0
        self.level = self.loaded_level
        self.apple.x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.apple.y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

    def run(self):
        self.username = self.get_username()
        self.level, high_score = self.load_progress()

        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.save_progress()
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.paused = not self.paused
                            if self.paused:
                                self.save_progress()
                        if not self.paused:
                            if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                                self.snake.direction = (0, -1)
                            elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                                self.snake.direction = (0, 1)
                            elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                                self.snake.direction = (-1, 0)
                            elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                                self.snake.direction = (1, 0)

                if self.paused:
                    continue

                self.snake.move()

                if self.snake.check_collision(LEVELS[self.level]["walls"]):
                    self.game_over()
                    continue

                if self.snake.head.colliderect(self.apple):
                    self.score += 1
                    self.apple.x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                    self.apple.y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                    self.snake.body.append(pygame.Rect(self.snake.body[-1].x, self.snake.body[-1].y, BLOCK_SIZE, BLOCK_SIZE))

                    if self.score % 5 == 0 and self.level < len(LEVELS):
                        self.level += 1

                screen.fill((0, 0, 0))
                for wall in LEVELS[self.level]["walls"]:
                    pygame.draw.rect(screen, (0, 0, 255), wall)

                pygame.draw.rect(screen, (0, 255, 0), self.snake.head)
                for segment in self.snake.body:
                    pygame.draw.rect(screen, (0, 200, 0), segment)

                pygame.draw.rect(screen, (255, 0, 0), self.apple)

                score_text = font.render(f"Score: {self.score} (High: {high_score})", True, (255, 255, 255))
                level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
                user_text = font.render(f"Player: {self.username}", True, (255, 255, 255))

                screen.blit(score_text, (10, 10))
                screen.blit(level_text, (10, 40))
                screen.blit(user_text, (WIDTH - 150, 10))

                pygame.display.flip()
                clock.tick(LEVELS[self.level]["speed"])

        except (KeyboardInterrupt, SystemExit):
            self.save_progress()
            pygame.quit()
            sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
    conn.close()