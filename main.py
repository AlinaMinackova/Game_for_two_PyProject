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
playerfirst = pygame.sprite.Group()
playersecond = pygame.sprite.Group()
cris_group = pygame.sprite.Group()
cris_group2 = pygame.sprite.Group()


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


girl_left = [load_image('left_g.png'), load_image('left2_g.png'), load_image('left_g.png'),
             load_image('left2_g.png')]
girl_right = [load_image('right_g.png'), load_image('right2_g.png'), load_image('right_g.png'),
             load_image('right3_g.png')]
cris_img = [load_image('cris.png'), load_image('cris2.png'), load_image('cris3.png'),
             load_image('cris4.png'), load_image('cris5.png'), load_image('cris6.png'),
            load_image('cris7.png'), load_image('cris8.png')]


class PlayerFirst(pygame.sprite.Sprite):
    image = load_image("girl.png", colorkey=-1)

    def __init__(self, x, y):
        super().__init__(playerfirst, all_sprites)
        self.image = PlayerFirst.image
        self.pol = y
        self.count = 0
        self.isJump = False
        self.jumpCount = 12
        self.jumpCount1 = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = self.pol

    def move(self, pressed_keys):
        global SCORE
        self.image = load_image("girl.png", colorkey=-1)
        if pygame.sprite.spritecollide(self, cris_group, True):
            SCORE += 10
        if pressed_keys[K_RIGHT]:
            self.rect.x += 4
            if self.rect.x > 700:
                self.rect.x -= 4
            self.animated(girl_right)
            if pygame.sprite.spritecollide(self, ground_im, False):
                if 459 <= self.rect.y <= 465:
                    self.rect.x -= 4
        if pressed_keys[K_LEFT]:
            self.rect.x -= 4
            if self.rect.x < -10:
                self.rect.x += 4
            self.animated(girl_left)
            if pygame.sprite.spritecollide(self, ground_im, False):
                if 459 <= self.rect.y <= 465:
                    self.rect.x -= 4
        if self.isJump:
            if self.jumpCount > 0:
                self.rect.y -= self.jumpCount
                self.jumpCount -= 1
            else:
                self.down()
        else:
            if not pygame.sprite.spritecollide(self, platform_ground, False):
                if not pygame.sprite.spritecollide(self, ground_im, False):
                    self.isdown()

    def down(self):
        if pygame.sprite.spritecollide(self, platform_ground, False):
            self.rect.y += 5
            self.isJump = False
            self.jumpCount = 12
            self.jumpCount1 = 0

        elif pygame.sprite.spritecollide(self, ground_im, False):
            self.rect.y += 2
            self.isJump = False
            self.jumpCount = 12
            self.jumpCount1 = 0

        else:
            if self.jumpCount1 <= 12:
                self.rect.y += self.jumpCount1
                self.jumpCount1 += 1
            else:
                self.isJump = False
                self.jumpCount = 12
                self.jumpCount1 = 0

    def isdown(self):
        if self.rect.y < self.pol:
            self.rect.y += 5

    def animated(self, img):
        if self.count == 20:
            self.count = 0

        self.image = img[self.count // 5]
        self.count += 1


class Cris(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(cris_group, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.count = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def animated(self):
        if self.count == 40:
            self.count = 0

        self.image = cris_img[self.count // 5]
        self.count += 1


cris = []
list_cr_gl = []
for i in list_cr_gl:
    cris.append(Cris("cris.png", i[0], i[1]))
first = PlayerFirst(40, 461)
running = True
play = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                first.isJump = True
    pressed_keys = pygame.key.get_pressed()
    first.move(pressed_keys)
    screen.fill(pygame.Color("black"))
    playerfirst.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()