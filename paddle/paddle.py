import random
import pygame
import time
import os
os.environ['MATPLOTLIBDATA'] = '/usr/local/lib64/python3.6/site-packages/matplotlib/mpl-data'
pygame.font.init()

WIDTH = 1000
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

LEFT_PADDLE = pygame.Rect(0, 220, 30, 120)
RIGHT_PADDLE = pygame.Rect(970, 220, 30, 120)
BALL = pygame.Rect(WIDTH/2, HEIGHT/2, 50, 50)
VEL = 8
BALL_VEL = [random.randint(2, 4), random.randint(2, 4)]
FPS = 60
SCORE = 0
LEVEL = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 177, 235)
RED = (245, 66, 66)
WINNER_FONT = pygame.font.SysFont("comicsans", 150)
LOSER_FONT = pygame.font.SysFont("comicsans", 100)
SCORE_FONT = pygame.font.SysFont("comicsans", 45)


def draw_window():
    window.fill("#03fcb6")
    pygame.draw.rect(window, WHITE, LEFT_PADDLE)
    pygame.draw.rect(window, WHITE, RIGHT_PADDLE)
    pygame.draw.rect(window, BLUE, BALL, border_radius=25)
    draw_text = SCORE_FONT.render(f"Score: {SCORE}", 1, BLACK)
    window.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 0))
    pygame.display.update()


def handle_left_paddle(keys_pressed):
    if keys_pressed[pygame.K_w] and LEFT_PADDLE.y - VEL > 0:
        LEFT_PADDLE.y -= VEL
    if keys_pressed[pygame.K_s] and LEFT_PADDLE.y + VEL < HEIGHT-LEFT_PADDLE.height:
        LEFT_PADDLE.y += VEL


def handle_right_paddle(keys_pressed):
    if keys_pressed[pygame.K_UP] and RIGHT_PADDLE.y - VEL > 0:
        RIGHT_PADDLE.y -= VEL
    if keys_pressed[pygame.K_DOWN] and RIGHT_PADDLE.y + VEL < HEIGHT-RIGHT_PADDLE.height:
        RIGHT_PADDLE.y += VEL


def draw_win(text):
    draw_text = WINNER_FONT.render(text, 1, RED)
    window.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
                            2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_lose(text):
    draw_text = LOSER_FONT.render(text, 1, RED)
    draw_text2 = LOSER_FONT.render(f"Score: {SCORE}", 1, RED)
    window.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
                            2, HEIGHT//2 - draw_text.get_height()//2))
    window.blit(draw_text2, (WIDTH//2 - draw_text2.get_width() //
                             2, HEIGHT//2 - draw_text2.get_height()//2 + 90))
    pygame.display.update()
    pygame.time.delay(5000)


def update_ball():
    BALL.x += BALL_VEL[0]
    BALL.y += BALL_VEL[1]
    if BALL.y + BALL_VEL[1] + 50 > HEIGHT or BALL.y + BALL_VEL[1] < 0:
        BALL_VEL[1] = -BALL_VEL[1]
    if BALL.x + BALL_VEL[0] + 100 > WIDTH or BALL.x + BALL_VEL[0] < 50:
        if LEFT_PADDLE.colliderect(BALL) or RIGHT_PADDLE.colliderect(BALL):
            BALL_VEL[0] = -BALL_VEL[0]
        elif BALL.x + BALL_VEL[0] + 50 > WIDTH or BALL.x + BALL_VEL[0] < 0:
            return False
    return True


clock = pygame.time.Clock()
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    SCORE += 1
    if SCORE >= 1000:
        LEVEL += 1
    if SCORE >= 2000:
        LEVEL += 1
    if SCORE >= 3000:
        LEVEL += 1
    if SCORE >= 4000:
        LEVEL += 1
    if SCORE >= 5000:
        draw_win("You win!")
        run = False
    keys_pressed = pygame.key.get_pressed()
    handle_left_paddle(keys_pressed)
    handle_right_paddle(keys_pressed)
    out = update_ball()
    if not out:
        draw_lose("You lose!")
        run = False
    draw_window()

pygame.quit()
