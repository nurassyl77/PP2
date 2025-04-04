import pygame
import random
import sys
from pygame.locals import *


pygame.init()
pygame.mixer.init()

# Настройки экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Шрифты
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 40)


background = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\Road.png"
).convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
player_img = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\Player.png"
).convert_alpha()
enemy_img = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\Enemy.png"
).convert_alpha()
coin_img = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\coin.png"
).convert_alpha()
coin_img = pygame.transform.scale(coin_img, (40, 40))

# Звук столкновения
crash_sound = pygame.mixer.Sound(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\lab8_img_Lab8_pictures_crash.wav"
)


# Параметры игры
SPEED = 5
SCORE = 0
COINS = 0
SPEED_INCREASE_COINS = 5  # Увеличивать скорость врага каждые 5 монет
road_y = 0  # Позиция дороги для эффекта движения


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = SPEED

    def reset_position(self):
        """Случайное появление врага сверху экрана"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    def move(self):
        """Движение врага вниз"""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 5])  # Случайный вес монеты
        self.set_coin_color()
        self.rect = self.image.get_rect()
        self.reset_position()

    def set_coin_color(self):
        """Изменение цвета монеты в зависимости от веса"""
        if self.weight == 1:
            self.image = pygame.transform.scale(coin_img, (40, 40))
        elif self.weight == 2:
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (20, 20), 20)
        else:  # 5 очков
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.image, BLUE, (25, 25), 25)

    def reset_position(self):
        """Случайное появление монеты сверху"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -300)

    def move(self):
        """Движение монеты вниз"""
        self.rect.y += SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)  # Для точных столкновений

    def move(self):
        """Управление игроком с клавиатуры"""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed


# Создание объектов
player = Player()
enemy = Enemy()
coin = Coin()

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Движение дороги (эффект бесконечной дороги)
    road_y += SPEED
    if road_y >= SCREEN_HEIGHT:
        road_y = 0

    # Обновление объектов
    player.move()
    enemy.move()
    coin.move()

    # Увеличение счета
    SCORE += 0.1

    # Проверка столкновения с монетой
    if pygame.sprite.collide_mask(player, coin):
        COINS += coin.weight
        coin = Coin()  # Создаем новую монету
        # Увеличиваем скорость врага каждые SPEED_INCREASE_COINS монет
        if COINS % SPEED_INCREASE_COINS == 0:
            enemy.speed += 0.5

    # Проверка столкновения с врагом
    if pygame.sprite.collide_mask(player, enemy):
        crash_sound.play()
        pygame.time.delay(500)  # Пауза перед Game Over

        # Экран Game Over
        SCREEN.fill(RED)
        game_over_text = font_large.render("GAME OVER", True, BLACK)
        score_text = font.render(f"Score: {int(SCORE)}", True, BLACK)
        coins_text = font.render(f"Coins: {COINS}", True, BLACK)

        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        SCREEN.blit(coins_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 40))

        pygame.display.update()
        pygame.time.delay(2000)  # Пауза перед выходом
        running = False

    # Отрисовка
    SCREEN.blit(background, (0, road_y - SCREEN_HEIGHT))
    SCREEN.blit(background, (0, road_y))
    SCREEN.blit(enemy.image, enemy.rect)
    SCREEN.blit(coin.image, coin.rect)
    SCREEN.blit(player.image, player.rect)

    # Отображение счета и монет
    score_text = font.render(f"Score: {int(SCORE)}", True, BLACK)
    coins_text = font.render(f"Coins: {COINS}", True, YELLOW)
    speed_text = font.render(f"Speed: {enemy.speed:.1f}", True, BLACK)

    SCREEN.blit(score_text, (10, 10))
    SCREEN.blit(coins_text, (10, 40))
    SCREEN.blit(speed_text, (10, 70))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()