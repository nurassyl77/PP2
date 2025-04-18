import pygame
import pygame.gfxdraw
from datetime import datetime

grey = (128, 128, 128)
white = (255, 255, 255)

pygame.init()

size = 500
center = (size // 2, size // 2)
window = pygame.display.set_mode((size, size))
clock = pygame.time.Clock()

def draw_seconds(surface, second):
    hand_length = size * 0.4
    angle = second * 6
    end_x = center[0] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).x
    end_y = center[1] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).y
    pygame.draw.line(surface, grey, center, (end_x, end_y), 5)

def draw_hours(surface, hour):
    hand_length = size * 0.2
    angle = hour * 0.1
    end_x = center[0] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).x
    end_y = center[1] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).y
    pygame.draw.line(surface, grey, center, (end_x, end_y), 5)

def draw_minute(surface, minut):
    hand_length = size * 0.3
    angle = minut * 0.1
    end_x = center[0] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).x
    end_y = center[1] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).y
    pygame.draw.line(surface, grey, center, (end_x, end_y), 5)

def main():

    running = True
    while running:
        window.fill(white)
        now = datetime.now()
        draw_seconds(window, now.second)
        draw_hours(window, now.hour)
        draw_minute(window, now.minute)
        pygame.display.flip()
        clock.tick(1)
        
        for event  in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
main()