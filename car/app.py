import random
import pygame
import os

WIDTH, HEIGHT = 650, 667
win = pygame.display.set_mode((WIDTH, HEIGHT))


def load(name):
    return pygame.image.load(os.path.join("assets", name+".png"))


# images
bg_image = load("bg")
player_car = pygame.transform.scale(load("blue_car"), (65, 120))
enemy_car = pygame.transform.scale(load("yellow_car"), (65, 120))

# colors
ROAD = (86, 86, 86)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game variables
FPS = 60
score = 0


class Background():
    y1 = 0
    y2 = -660
    speed = 5

    def draw(self):
        win.blit(bg_image, (0, self.y1))
        win.blit(bg_image, (0, self.y2))
        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= 668:
            self.y1 = -660
        if self.y2 >= 668:
            self.y2 = -660


class Player():
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.crash = False

    def draw(self):
        win.blit(player_car, (self.x, self.y))

    def hit(self):
        self.crash = True


class Enemy():
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.fy = y
        self.width = width
        self.height = height
        self.speed = speed
        self.over = False

    def draw(self):
        win.blit(enemy_car, (self.x, self.y))

    def move(self):
        self.y += self.speed


def draw_window(bg, player, enemies):
    bg.draw()
    player.draw()
    for enemy in enemies:
        enemy.draw()
    pygame.display.update()


def handle_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x >= 130:
        player.x -= player.speed
    if keys_pressed[pygame.K_RIGHT] and player.x + player.width <= WIDTH-130:
        player.x += player.speed


bg = Background()
player = Player(300, 500, 65, 125, 5)
enemies = []
clock = pygame.time.Clock()
run = True


def close():
    pygame.time.delay(5000)


while run:
    clock.tick(FPS)
    score += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if len(enemies) == 0:
        for i in range(7):
            enemy = Enemy(random.choice([130, 195, 260, 325, 260, 325, 390, 455]),
                          random.choice([-1000, -875, -750, -625, -500, -375, -250, -125]), 65, 125, 5)
            enemies.append(enemy)

    for enemy in enemies:
        enemy.move()
        if enemy.y >= 670:
            enemies.remove(enemy)

        if player.y < enemy.y + enemy.height and player.y + player.height > enemy.y:
            if player.x + player.width > enemy.x and player.x < enemy.x + enemy.width:
                player.hit()

    if player.crash:
        close()
        run = False

    keys_pressed = pygame.key.get_pressed()
    handle_movement(keys_pressed, player)
    draw_window(bg, player, enemies)


pygame.quit()
