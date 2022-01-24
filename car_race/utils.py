import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotated_car(window, img, top_left, angle):
    rotated_image = pygame.transform.rotate(img, angle)
    new_rect = rotated_image.get_rect(
        center=img.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rect.topleft)
