import pygame
import os

pygame.init()


# Экран
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music")
icon = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\m_lab_7.png"
)
pygame.display.set_icon(icon)

screen.fill((255, 255, 255))


# Плейлист өлеңдермен
playlist = [
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\mp3\cc4a1e3e297ab7f.mp3",
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\mp3\lab7_musics_Bylygyp.mp3 "
]

# Кнопкалардың суреттері
image = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\m_lab_7.png"
)
play_button = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\play_button.png"
)
pause_button = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\pause_button.png"
)
next_button = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\next_button.png"
)
prev_button = pygame.image.load(
    r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab7\images\prev_button.png"
)

# Өлшемдерін дұрыстау
image = pygame.transform.smoothscale(image, (270, 270))
play_button = pygame.transform.smoothscale(play_button, (100, 100))
pause_button = pygame.transform.smoothscale(pause_button, (100, 100))
next_button = pygame.transform.smoothscale(next_button, (100, 100))
prev_button = pygame.transform.smoothscale(prev_button, (100, 100))

# Текст
font = pygame.font.Font(None, 40)
txt1 = font.render("Press P", True, (0, 0, 0))
txt2 = font.render("Press S", True, (0, 0, 0))
txt3 = font.render("Press <-", True, (0, 0, 0))
txt4 = font.render("Press ->", True, (0, 0, 0))


# Музыканы басқару функциясы
current_music = 0
paused = False


def play_music():
    pygame.mixer.music.load(playlist[current_music])
    pygame.mixer.music.play()


# Алдыңғы өлең
def prev_music():
    global current_music
    current_music = (current_music - 1) % len(playlist)
    play_music()


# Келесі өлең
def next_music():
    global current_music
    current_music = (current_music + 1) % len(playlist)
    play_music()


running = True

while running:
    # Экранды тазарту
    screen.fill((255, 255, 255))

    # Кнопкалардың суреттерін орналастыру
    screen.blit(image, (250, 50))
    screen.blit(play_button, (80, 400))
    screen.blit(pause_button, (260, 400))
    screen.blit(prev_button, (440, 400))
    screen.blit(next_button, (620, 400))

    # Кнопкалардың атауы
    screen.blit(txt1, (80, 500))
    screen.blit(txt2, (260, 500))
    screen.blit(txt3, (440, 500))
    screen.blit(txt4, (620, 500))

    # Ойнап жатқан музыканың атын шығару
    music_name = os.path.basename(playlist[current_music])
    m_name = font.render(music_name, True, (0, 0, 0))
    screen.blit(m_name, (300, 350))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # Музыканы басқару
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    play_music()
            elif event.key == pygame.K_s:
                pygame.mixer.music.pause()
                paused = True
            elif event.key == pygame.K_LEFT:
                prev_music()
            elif event.key == pygame.K_RIGHT:
                next_music()