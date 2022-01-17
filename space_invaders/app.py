from turtle import width
import wave
import pygame
import os
import time
import random
pygame.init()
pygame.font.init()

WIDTH = 650
HEIGHT = 650

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load Images
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
BLUE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))

RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))

YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)
BIG_FONT = pygame.font.SysFont("comicsans", 80)
NORMAL_FONT = pygame.font.SysFont("comicsans", 50)


class Ship:
    COOL_DOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.width = 50
        self.height = 50
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offscreen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 5
                self.lasers.remove(laser)

    def img(self):
        return self.ship_img

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACESHIP_IMAGE
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offscreen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y +
                         self.get_height()+10, self.get_width(), 10))
        pygame.draw.rect(window, GREEN, (self.x, self.y +
                         self.get_height()+10, self.get_width() * (self.health/self.max_health), 10))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def offscreen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Enemy(Ship):
    COLOR_MAP = {"red": (RED_SPACESHIP_IMAGE, RED_LASER), "green": (
        GREEN_SPACESHIP_IMAGE, GREEN_LASER), "blue": (BLUE_SPACESHIP_IMAGE, BLUE_LASER)}

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, enemy_vel):
        self.y += enemy_vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def draw_window(level, lives, player, enemies):
    WIN.blit(BG, (0, 0))
    lives_text = FONT.render(f"Lives: {lives}", 1, WHITE)
    level_text = FONT.render(f"Level: {level}", 1, WHITE)
    WIN.blit(lives_text, (10, 10))
    WIN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    for enemy in enemies:
        enemy.draw(WIN)

    player.draw(WIN)

    pygame.display.update()


def show_lost(lost):
    if lost:
        lost_label = BIG_FONT.render("You lost", 1, WHITE)
        WIN.blit(lost_label, (WIDTH//2 - lost_label.get_width() //
                 2, HEIGHT//2 - lost_label.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)


def handle_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x - VEL > 0:
        player.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and player.x + VEL < WIDTH - player.get_width():
        player.x += VEL
    if keys_pressed[pygame.K_UP] and player.y - VEL > 0:
        player.y -= VEL
    if keys_pressed[pygame.K_DOWN] and player.y + VEL + 10 < HEIGHT - player.get_width():
        player.y += VEL
    if keys_pressed[pygame.K_SPACE]:
        player.shoot()


def main():
    clock = pygame.time.Clock()
    run = True
    level = 0
    lives = 5

    player = Player(100, 540)
    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 7

    while run:
        clock.tick(FPS)
        lost = False
        if lives <= 0 or player.health <= 0:
            lost = True
            show_lost(lost)
            break

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, player)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        draw_window(level, lives, player, enemies)
    pygame.quit()


def main_menu():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = NORMAL_FONT.render(
            "Press your mouse to begin...", 1, WHITE)
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width() /
                 2, HEIGHT/2 - title_label.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
