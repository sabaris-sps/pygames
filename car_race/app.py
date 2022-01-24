from utils import *
import os
import pygame
import time
import math

track = pygame.image.load(os.path.join("imgs", "track.png"))

# window setup
WIDTH, HEIGHT = track.get_width()/1.3, track.get_height()/1.3
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car race")

# load images
track = scale_image(track, 0.779)
red_car = scale_image(pygame.image.load(
    os.path.join("imgs", "red-car.png")), 0.47)
purple_car = scale_image(pygame.image.load(
    os.path.join("imgs", "purple-car.png")), 0.47)
grass = scale_image(pygame.image.load(
    os.path.join("imgs", "grass.jpg")), 2)
track_border = scale_image(pygame.image.load(
    os.path.join("imgs", "track-border.png")), 0.779)
finish = pygame.image.load(os.path.join("imgs", "finish.png"))
# finish = pygame.transform.scale(finish, (60, 25/(100/45)))

# game variables
FPS = 60


class Car:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.x, self.y = self.START_POS
        self.angle = 0
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self):
        blit_rotated_car(window, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal


class Player(Car):
    IMG = purple_car
    START_POS = (150, 150)


def draw_window(player):
    window.blit(grass, (0, 0))
    window.blit(track, (0, 0))
    window.blit(finish, (95, 195))
    window.blit(track_border, (0, 0))
    player.draw()
    pygame.display.update()


def handle_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT]:
        player.rotate(left=True)
    if keys_pressed[pygame.K_RIGHT]:
        player.rotate(right=True)
    if keys_pressed[pygame.K_UP]:
        player.move_forward()


def main():
    player = Player(4, 4)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, player)
        draw_window(player)
    pygame.quit()


if __name__ == "__main__":
    main()
