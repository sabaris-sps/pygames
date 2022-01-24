import pygame
import os
pygame.font.init()
pygame.mixer.init()


def load(name):
    return pygame.image.load(os.path.join("assets", name + ".png"))


WIDTH = 852
HEIGHT = 480

window = pygame.display.set_mode((WIDTH, HEIGHT))

# load images
LEFT = [load("L1"), load("L2"), load("L3"), load("L4"), load(
    "L5"), load("L6"), load("L7"), load("L8"), load("L9")]
RIGHT = [load("R1"), load("R2"), load("R3"), load("R4"), load(
    "R5"), load("R6"), load("R7"), load("R8"), load("R9")]
BG = pygame.image.load(
    os.path.join("assets", "bg.jpg"))
CHAR = load("standing")
MUSIC = pygame.mixer.music.load(os.path.join("assets", "music.mp3"))
BULLET_FIRE = pygame.mixer.Sound(os.path.join("assets", "bullet.mp3"))
BULLET_HIT = pygame.mixer.Sound(os.path.join("assets", "hit.mp3"))
pygame.mixer.music.play(-1)

# game variables
FPS = 30
MAX_BULLETS = 3
SCORE = 0
FONT = pygame.font.SysFont("calibri", 30, True)
BIG_FONT = pygame.font.SysFont("calibri", 70, True)
# colors
RED = (235, 64, 52)
GREEN = (52, 235, 156)
BLUE = (52, 137, 235)
BLACK = (0, 0, 0)


class Player(object):
    def __init__(self, x, y, width, height):
        self.VEL = 5
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump = False
        self.jump_count = 10
        self.standing = True
        self.hitbox = (self.x+17, self.y+12, 27, 50)

    def draw(self):
        if self.walk_count >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                window.blit(LEFT[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                window.blit(RIGHT[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                window.blit(RIGHT[0], (self.x, self.y))
            else:
                window.blit(LEFT[0], (self.x, self.y))
        self.hitbox = (self.x+17, self.y+12, 27, 50)

    def hit(self):
        self.jump = False
        self.jump_count = 10
        self.x = 10
        self.y = 400
        self.walk_count = 0

        text = BIG_FONT.render("-5", 1, RED)
        window.blit(text, (WIDTH//2 - text.get_width() //
                    2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
            except:
                pass


class Projectile(object):
    def __init__(self, x, y, color, width, direction):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.direction = direction
        self.vel = 10 * direction

    def draw(self):
        rectangle = pygame.Rect(self.x, self.y, self.width, 10)
        pygame.draw.rect(window, self.color, rectangle, self.width, 3)


class Enemy(object):
    LEFT = [load("L1E"), load("L2E"), load("L3E"), load("L4E"), load(
        "L5E"), load("L6E"), load("L7E"), load("L8E"), load("L9E"), load("L10E"), load("L11E")]
    RIGHT = [load("R1E"), load("R2E"), load("R3E"), load("R4E"), load(
        "R5E"), load("R6E"), load("R7E"), load("R8E"), load("R9E"), load("R10E"), load("R11E")]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walk_count = 0
        self.vel = 8
        self.path = [self.x, self.end]
        self.hitbox = (self.x+17, self.y+2, 30, 58)
        # self.health = 100
        self.visible = True

    def draw(self):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.vel > 0:
                window.blit(self.RIGHT[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            else:
                window.blit(self.LEFT[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            self.hitbox = (self.x+17, self.y+2, 30, 60)
            # pygame.draw.rect(
            #     window, RED, (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            # pygame.draw.rect(
            #     window, BLUE, (self.hitbox[0], self.hitbox[1] - 20, self.health * 0.5, 10))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0

    def hit(self):
        if SCORE >= 50:
            self.visible = False


def draw_window(bullets):
    window.blit(BG, (0, 0))
    player.draw()
    enemy.draw()
    for bullet in bullets:
        bullet.draw()
    draw_text = FONT.render(f"Score: {SCORE}", 1, BLACK)
    window.blit(draw_text, (WIDTH - draw_text.get_width() - 10, 10))
    pygame.display.update()


def handle_movement(player):
    if keys_pressed[pygame.K_LEFT] and player.x > 0:
        player.x -= player.VEL
        player.left = True
        player.right = False
        player.standing = False
    elif keys_pressed[pygame.K_RIGHT] and player.x + CHAR.get_width() < WIDTH:
        player.x += player.VEL
        player.right = True
        player.left = False
        player.standing = False
    else:
        player.standing = True
        player.walk_count = 0
    if not player.jump:
        if keys_pressed[pygame.K_UP]:
            player.jump = True
            player.standing = True
            player.walk_count = 0
    else:
        if player.jump_count >= -10:
            neg = 1
            if player.jump_count < 0:
                neg = -1
            player.y -= neg * player.jump_count**2 * 0.5
            player.jump_count -= 1
        else:
            player.jump = False
            player.jump_count = 10


player = Player(425, 400, 64, 64)
enemy = Enemy(50, 400, 64, 64, 800)
clock = pygame.time.Clock()
bullets = []
run = True
while run:
    clock.tick(FPS)

    if enemy.visible:
        if player.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and player.hitbox[1] + player.hitbox[3] > enemy.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > enemy.hitbox[0] and player.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                player.hit()
                SCORE -= 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(bullets) <= MAX_BULLETS:
                if player.right:
                    dir = 1
                else:
                    dir = -1
                bullet = Projectile(
                    round(player.x + player.width//2), round(player.y + player.height//2), RED, 20, dir)
                bullets.append(bullet)
                BULLET_FIRE.play()

    for bullet in bullets:
        if enemy.visible:
            if bullet.y - bullet.width < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.width > enemy.hitbox[1]:
                if bullet.x + bullet.width > enemy.hitbox[0] and bullet.x - bullet.width < enemy.hitbox[0] + enemy.hitbox[2]:
                    BULLET_HIT.play()
                    bullets.remove(bullet)
                    SCORE += 1
                    enemy.hit()

        if bullet.x < WIDTH and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)

    if not enemy.visible:
        text = BIG_FONT.render("You win!", 1, BLUE)
        window.blit(text, (WIDTH//2 - text.get_width() //
                    2, HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        run = False

    keys_pressed = pygame.key.get_pressed()
    handle_movement(player)
    draw_window(bullets)

pygame.quit()
