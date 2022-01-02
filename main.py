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
platform_ground = pygame.sprite.Group()
ground_im = pygame.sprite.Group()
gates_group = pygame.sprite.Group()
gates_group2 = pygame.sprite.Group()
playerfirst = pygame.sprite.Group()
playersecond = pygame.sprite.Group()
cris_group = pygame.sprite.Group()
cris_group2 = pygame.sprite.Group()

SCORE = 0
SCORE2 = 0


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
boys_left = [load_image('left.png'), load_image('left2.png'), load_image('left.png'),
             load_image('left2.png')]
boys_right = [load_image('right.png'), load_image('right2.png'), load_image('right.png'),
             load_image('right3.png')]
cris2_img = [load_image('cris_2.png'), load_image('cris22.png'), load_image('cris23.png'),
             load_image('cris24.png'), load_image('cris25.png'), load_image('cris26.png'),
            load_image('cris27.png'), load_image('cris28.png')]


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


class PlayerSecond(pygame.sprite.Sprite):
    image = load_image("boy.png", colorkey=-1)

    def __init__(self, x, y):
        super().__init__(playersecond, all_sprites)
        self.image = PlayerSecond.image
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
        global SCORE2
        self.image = load_image("boy.png", colorkey=-1)
        if pygame.sprite.spritecollide(self, cris_group2, True):
            SCORE2 += 10
        if pressed_keys[K_d]:
            self.rect.x += 4
            if self.rect.x > 700:
                self.rect.x -= 4
            self.animated(boys_right)
            if pygame.sprite.spritecollide(self, ground_im, False):
                if 458 <= self.rect.y <= 463:
                    self.rect.x -= 4
        if pressed_keys[K_a]:
            self.rect.x -= 4
            if self.rect.x < -10:
                self.rect.x += 4
            self.animated(boys_left)
            if pygame.sprite.spritecollide(self, ground_im, False):
                if 458 <= self.rect.y <= 465:
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


class Cris2(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(cris_group2, all_sprites)
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

        self.image = cris2_img[self.count // 5]
        self.count += 1


class Fon(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__(fon, all_sprites)
        image = load_image(image)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(platform_ground, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(ground_im, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Gates(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(gates_group, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Gates2(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(gates_group2, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


def terminate():
    pygame.quit()
    sys.exit()


Fon("forest.png")
Gates("gates2.png", 500, 30)
Gates2("gates.png", 580, 30)
cris = []
cris2 = []
first = PlayerFirst(40, 461)
second = PlayerSecond(0, 463)
list_cr_gl = [[5, 5], [580, 460], [110, 120]]
for i in list_cr_gl:
    cris.append(Cris("cris.png", i[0], i[1]))
list_cr_mn = [[660, 5], [245, 190], [400, 115]]
for i in list_cr_mn:
    cris2.append(Cris2("cris2.png", i[0], i[1]))
list_platforms = [[500, 375], [365, 300], [225, 230], [85, 160], [370, 160], [500, 90], [570, 90]]
for i in list_platforms:
    Platform("platform.png", i[0], i[1])
Ground("ground.png", 635, 450)
running = True
play = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                first.isJump = True
            if event.key == pygame.K_w:
                second.isJump = True
    pressed_keys = pygame.key.get_pressed()
    first.move(pressed_keys)
    second.move(pressed_keys)
    screen.fill(pygame.Color("black"))
    fon.draw(screen)
    for i in cris:
        i.animated()
    for i in cris2:
        i.animated()
    cris_group.draw(screen)
    cris_group2.draw(screen)
    gates_group.draw(screen)
    gates_group2.draw(screen)
    platform_ground.draw(screen)
    ground_im.draw(screen)
    playerfirst.draw(screen)
    playersecond.draw(screen)
    gates_group.update()
    gates_group2.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()