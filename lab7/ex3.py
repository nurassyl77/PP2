import pygame

pygame.init()

# Экран
screen = pygame.display.set_mode((800, 600))

# Шардың бастапқы орны мен параметрлері
x, y = 400, 300
radius = 25
speed = 40

running = True

while running:
    screen.fill((255, 255, 255))

    # Шарды салу
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    pygame.display.update()

    # Оқиғаларды өңдеу
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Кілтті басуды тексеру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y - radius - speed >= 0:
                y -= speed
            if event.key == pygame.K_DOWN and y + radius + speed <= 600:
                y += speed
            if event.key == pygame.K_LEFT and x - radius - speed >= 0:
                x -= speed
            if event.key == pygame.K_RIGHT and x + radius + speed <= 800:
                x += speed

pygame.quit()