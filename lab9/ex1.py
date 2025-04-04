import pygame
import sys
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint 2")
clock = pygame.time.Clock()

# Цвета
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
color_index = 0
current_color = COLORS[color_index]

# Инструменты:
# 0-карандаш, 1-прямоугольник, 2-круг, 3-ластик,
# 4-квадрат, 5-прямоугольный треугольник, 6-равносторонний треугольник, 7-ромб
current_tool = 0
drawing = False
start_pos = None
radius = 5  # Толщина линии


# Холст
canvas = pygame.Surface((800, 600))
canvas.fill((255, 255, 255))


# Шрифт для информации
font = pygame.font.SysFont(None, 24)


def draw_equilateral_triangle(surface, color, start, end, width):
    """Рисует равносторонний треугольник"""
    height = end[1] - start[1]
    side_length = abs(height * 2 / math.sqrt(3))
    points = [
        (start[0], start[1]),
        (start[0] + side_length, start[1]),
        (start[0] + side_length / 2, end[1]),
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_right_triangle(surface, color, start, end, width):
    """Рисует прямоугольный треугольник (гипотенуза от start до end)"""
    points = [(start[0], start[1]), (end[0], start[1]), (start[0], end[1])]
    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width):
    """Рисует ромб"""
    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    width_rhomb = abs(end[0] - start[0]) // 2
    height_rhomb = abs(end[1] - start[1]) // 2
    points = [
        (center_x, center_y - height_rhomb),  # Верх
        (center_x + width_rhomb, center_y),  # Право
        (center_x, center_y + height_rhomb),  # Низ
        (center_x - width_rhomb, center_y),  # Лево
    ]
    pygame.draw.polygon(surface, color, points, width)


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

        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            canvas.fill((255, 255, 255))

        # Смена инструмента цифрами 1-8
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_8:
                current_tool = (
                    event.key - pygame.K_1
                )  # Конвертируем клавишу в номер инструмента 0-7

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

            elif current_tool == 4:  # Квадрат
                size = max(
                    abs(mouse_pos[0] - start_pos[0]), abs(mouse_pos[1] - start_pos[1])
                )
                x = start_pos[0] if mouse_pos[0] > start_pos[0] else start_pos[0] - size
                y = start_pos[1] if mouse_pos[1] > start_pos[1] else start_pos[1] - size
                pygame.draw.rect(canvas, current_color, (x, y, size, size), radius)

            elif current_tool == 5:  # Прямоугольный треугольник
                draw_right_triangle(canvas, current_color, start_pos, mouse_pos, radius)

            elif current_tool == 6:  # Равносторонний треугольник
                draw_equilateral_triangle(
                    canvas, current_color, start_pos, mouse_pos, radius
                )

            elif current_tool == 7:  # Ромб
                draw_rhombus(canvas, current_color, start_pos, mouse_pos, radius)

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
    tools = [
        "1-Карандаш",
        "2-Прямоуг.",
        "3-Круг",
        "4-Ластик",
        "5-Квадрат",
        "6-Треуг. прямоуг.",
        "7-Треуг. равност.",
        "8-Ромб",
    ]
    info = (
        f"Инструмент: {tools[current_tool]} | Цвет: {current_color} (Пробел - сменить)"
    )
    text = font.render(info, True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()