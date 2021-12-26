import pygame.sprite
import pygame
import os
import sys
from pygame.locals import *


pygame.init()
size = width, height = 750, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
fon = pygame.sprite.Group()
playerfirst = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Fon(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__(fon, all_sprites)
        image = load_image(image)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


Fon("forest.png")
running = True
play = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed_keys = pygame.key.get_pressed()
    screen.fill(pygame.Color("black"))
    fon.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()