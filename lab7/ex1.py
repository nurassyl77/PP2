import pygame
from datetime import datetime

pygame.init()


screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("Mickey clock")
# Иконкасы

# Суреттер
right_arm = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\mickey_right_arm.png"
)
left_arm = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\mickey_left_arm.png"
)
without_arms = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\mickey_without_arms.png"
)

# Өлшемін дұрыстау
right_arm = pygame.transform.smoothscale(right_arm, (1000, 750))
left_arm = pygame.transform.smoothscale(left_arm, (1000, 750))
without_arms = pygame.transform.smoothscale(without_arms, (1000, 750))

running = True

# Басты бөлік
while running:

    # Қазіргі уақыт
    now = datetime.now()
    angle_min = -now.minute * 6
    angle_sec = -now.second * 6

    # Суреттерді бұрамыз
    rotated_right = pygame.transform.rotate(right_arm, angle_min)
    rotated_left = pygame.transform.rotate(left_arm, angle_sec)

    # Центрін дұрыстаймыз
    right_rect = rotated_right.get_rect(center=(500, 375))
    left_rect = rotated_left.get_rect(center=(500, 375))

    # Суреттерді экранға шығарамыз
    screen.fill((0, 0, 0))  # Ескі беттерін өшіреміз
    screen.blit(without_arms, (0, 0))
    screen.blit(rotated_right, right_rect.topleft)  # Минут көрсететін қолы
    screen.blit(rotated_left, left_rect.topleft)  # Секунд көрсететін қолы

    pygame.display.update()  # Экранды жаңартамыз

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()