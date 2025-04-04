import pygame
import sys
import math

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# Цвета
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
color_index = 0
current_color = COLORS[color_index]

# Инструменты: 0-карандаш, 1-прямоугольник, 2-круг, 3-ластик
current_tool = 0
drawing = False
start_pos = None
radius = 5

# Холст
canvas = pygame.Surface((800, 600))
canvas.fill((255, 255, 255))

# Шрифт
font = pygame.font.SysFont(None, 24)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Смена цвета на пробел
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            color_index = (color_index + 1) % len(COLORS)
            current_color = COLORS[color_index]

        # Смена инструмента цифрами 1-4
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = 0
            elif event.key == pygame.K_2:
                current_tool = 1
            elif event.key == pygame.K_3:
                current_tool = 2
            elif event.key == pygame.K_4:
                current_tool = 3

        # Начало рисования
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True
            start_pos = mouse_pos

        # Окончание рисования (для фигур)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            if current_tool == 1:  # Прямоугольник
                x = min(start_pos[0], mouse_pos[0])
                y = min(start_pos[1], mouse_pos[1])
                w = abs(mouse_pos[0] - start_pos[0])
                h = abs(mouse_pos[1] - start_pos[1])
                pygame.draw.rect(canvas, current_color, (x, y, w, h), radius)
            elif current_tool == 2:  # Круг
                r = math.sqrt(
                    (mouse_pos[0] - start_pos[0]) ** 2
                    + (mouse_pos[1] - start_pos[1]) ** 2
                )
                pygame.draw.circle(canvas, current_color, start_pos, int(r), radius)
            drawing = False

    # Рисование карандашом/ластиком
    if pygame.mouse.get_pressed()[0] and drawing:
        if current_tool == 0:  # Карандаш
            if start_pos:
                pygame.draw.line(canvas, current_color, start_pos, mouse_pos, radius)
            start_pos = mouse_pos
        elif current_tool == 3:  # Ластик
            pygame.draw.circle(canvas, (255, 255, 255), mouse_pos, radius)

    # Отрисовка
    screen.blit(canvas, (0, 0))

    # Текстовая информация
    tools = ["1-Карандаш", "2-Прямоуг.", "3-Круг", "4-Ластик"]
    info = (
        f"Инструмент: {tools[current_tool]} | Цвет: {current_color} (Пробел - сменить)"
    )
    text = font.render(info, True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()