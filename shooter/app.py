#MADE WITH MY MEMORY
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500

FPS = 60
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 45

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOTER")
YELLOW_SHOOTER = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "spaceship_red.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SHOOTER = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "spaceship_red.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Assets_Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Assets_Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPEED = 7
BULLET_VEL = 15
MAX_BULLETS = 3


def draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SHOOTER, (yellow.x, yellow.y))
    WIN.blit(RED_SHOOTER, (red.x, red.y))

    red_health_text = HEALTH_FONT.render(
        "HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "HEALTH: " + str(yellow_health), 1, WHITE)

    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - SPEED > 0:
        yellow.x -= SPEED
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + SPEED < BORDER.x+10:
        yellow.x += SPEED
    if keys_pressed[pygame.K_w] and yellow.y - SPEED > 0:
        yellow.y -= SPEED
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + SPEED < HEIGHT:
        yellow.y += SPEED


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - SPEED > BORDER.x:
        red.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + SPEED < WIDTH:
        red.x += SPEED
    if keys_pressed[pygame.K_UP] and red.y - SPEED > 0:
        red.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + SPEED < HEIGHT:
        red.y += SPEED


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def handle_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
             2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width - 1, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
        if yellow_health <= 0:
            winner_text = "RED WINS!"
        if winner_text != "":
            handle_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.quit()


if __name__ == "__main__":
    main()
