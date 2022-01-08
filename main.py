import pygame.sprite
import os
import sys
import pygame
from pygame.locals import *
import sqlite3
from pygame.math import Vector2
import random


pygame.init()
size = width, height = 750, 550
screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
GRAVITY = 1

all_sprites = pygame.sprite.Group()
mouse = pygame.sprite.Group()
fon = pygame.sprite.Group()
platform_ground = pygame.sprite.Group()
ground_im = pygame.sprite.Group()
playerfirst = pygame.sprite.Group()
playersecond = pygame.sprite.Group()
cris_group = pygame.sprite.Group()
cris_group2 = pygame.sprite.Group()
gates_group = pygame.sprite.Group()
gates_group2 = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
ship_group = pygame.sprite.Group()
ladder_group = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
disk_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()

pygame.mixer.music.load("fon.wav")
pygame.mixer.music.play(-1)

button_sound = pygame.mixer.Sound("button.wav")
cris_sound = pygame.mixer.Sound("cris.mp3")
level_sound = pygame.mixer.Sound("level.mp3")
winner_sound = pygame.mixer.Sound("winner.mp3")
fall_sound = pygame.mixer.Sound("fall.mp3")
dragon_sound = pygame.mixer.Sound("dragon.mp3")
dragon_sound.set_volume(0.5)
jump_sound = pygame.mixer.Sound("jump.mp3")

con = sqlite3.connect('players.db')
cur = con.cursor()

LEVEL_COUNT = 0
SCORE = 0
SCORE2 = 0
SCORE_UP = 0
SCORE2_UP = 0
SCORE_ALL = 0
DISK_LEFT = 0
DISK_RIGHT = 1

need_input = False
need_input2 = False
text = ''
text2 = ''


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


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 1
    # возможные скорости
    numbers = range(-1, 3)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png", -1)]
    for scale in (5, 10, 10):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(star_group, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


boys_left = [load_image('left.png'), load_image('left2.png'), load_image('left.png'),
             load_image('left2.png')]
boys_right = [load_image('right.png'), load_image('right2.png'), load_image('right.png'),
             load_image('right3.png')]
girl_left = [load_image('left_g.png'), load_image('left2_g.png'), load_image('left_g.png'),
             load_image('left2_g.png')]
girl_right = [load_image('right_g.png'), load_image('right2_g.png'), load_image('right_g.png'),
             load_image('right3_g.png')]
boys_up = [load_image('up_2.png'), load_image('up_1.png'), load_image('up_2.png'),
             load_image('up_3.png')]
girl_up = [load_image('up.png'), load_image('up3.png'), load_image('up.png'),
             load_image('up2.png')]
cris_img = [load_image('cris.png'), load_image('cris2.png'), load_image('cris3.png'),
             load_image('cris4.png'), load_image('cris5.png'), load_image('cris6.png'),
            load_image('cris7.png'), load_image('cris8.png')]
cris2_img = [load_image('cris_2.png'), load_image('cris22.png'), load_image('cris23.png'),
             load_image('cris24.png'), load_image('cris25.png'), load_image('cris26.png'),
            load_image('cris27.png'), load_image('cris28.png')]
water_img = [load_image('water.png'), load_image('water2.png'), load_image('water3.png'), load_image('water4.png'),
             load_image('water5.png'), load_image('water4.png'), load_image('water3.png'), load_image('water2.png'),
             load_image('water.png')]
fire_img = [load_image('fire.png'), load_image('fire2.png'), load_image('fire3.png'), load_image('fire4.png'),
            load_image('fire5.png'), load_image('fire6.png'), load_image('fire7.png'), load_image('fire8.png'),
            load_image('fire9.png'), load_image('fire10.png'), load_image('fire11.png'), load_image('fire12.png'),
            load_image('fire13.png'), load_image('fire14.png'), load_image('fire15.png'), load_image('fire16.png')]
dragon_left = [load_image('dragon.png', -1), load_image('dragon2.png', -1), load_image('dragon3.png', -1),
             load_image('dragon4.png', -1), load_image('dragon5.png', -1), load_image('dragon6.png', -1),
               load_image('dragon5.png', -1), load_image('dragon4.png', -1), load_image('dragon3.png', -1),
               load_image('dragon2.png', -1)]


class Mouse(pygame.sprite.Sprite):
    image = load_image("cursor.png")

    def __init__(self):
        super().__init__(mouse, all_sprites)
        self.image = Mouse.image
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def update(self, *args):
        if args[0].pos[1] == 0 or args[0].pos[0] == 0:
            self.rect = (-100, -100)
        else:
            self.rect = args[0].pos


def print_text(message, x, y, shr, color=(0, 0, 0)):
    pygame.font.init()
    font_type = pygame.font.Font('Modo.ttf', shr)
    text = font_type.render(str(message), True, color)
    screen.blit(text, (x, y))


def input_text():
    global need_input, text, need_input2, text2
    intro_text = ['', 'Игрок 1', '', '', '', '', 'Игрок 2']
    text_coord = 10
    font = pygame.font.Font(None, 30)
    input_rect = pygame.Rect(220, 100, 300, 50)
    pygame.draw.rect(screen, (255, 255, 255), input_rect)

    input_rect2 = pygame.Rect(220, 250, 300, 50)
    pygame.draw.rect(screen, (255, 255, 255), input_rect2)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input = True
        need_input2 = False
    if input_rect2.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input2 = True
        need_input = False
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(128, 0, 128))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 220
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    if need_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if need_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 20:
                        text += event.unicode
    if need_input2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if need_input2 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text2 = text2[:-1]
                else:
                    if len(text2) < 10:
                        text2 += event.unicode
    if len(text) or len(text2):
        print_text(text, input_rect.x + 10, input_rect.y + 10, 30)
        print_text(text2, input_rect2.x + 10, input_rect2.y + 10, 30)


class Button:
    def __init__(self, wight, height, base, light):
        self.wight = wight
        self.height = height
        self.base = base
        self.light = light

    def draw(self, x, y, message, shr, action=None, color=(0, 0, 0)):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.wight and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.light, (x, y, self.wight, self.height))
            pygame.mixer.Sound.play(button_sound)
            if click[0] == 1:
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.base, (x, y, self.wight, self.height))

        print_text(message, x + 60, y + 5, shr, color)


class Fon(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__(fon, all_sprites)
        image = load_image(image)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


def information():
    Mouse()
    OK_btn = Button(150, 50, (95, 158, 160), (0, 206, 209))
    intro_text = ["ПРАВИЛА ИГРЫ:", "",
                  "Во время прохождения вам предстоит управлять двумя персонажами.",
                  "Используйте стрелочки, чтобы управлять девочкой",
                  "Используйте A, W, D, S, чтобы управлять мальчиком.",
                  "Не пробуйте переместить персонажа в жидкость",
                  "не предназначенную для него:",
                  "для девочки - вода, для мальчика - огонь,",
                  "шипы убивают их обоих. Не забывайте собирать алмазы!",
                  "Дойдите до ворот, чтобы перейти на следующий уровень.",
                  "Желаем удачи!"]
    play = True
    while play:
        screen.fill(pygame.Color("black"))
        fon = pygame.transform.scale(load_image('inf.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 10
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(72, 61, 139))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
            if event.type == pygame.MOUSEMOTION:
                create_particles(pygame.mouse.get_pos())
        OK_btn.draw(280, 400, 'OK', 36, start_screen)
        mouse.draw(screen)
        star_group.update()
        star_group.draw(screen)
        pygame.display.flip()
        clock.tick(30)


def event_name():
    Mouse()
    ok_btn = Button(150, 50, (105, 105, 105), (186, 85, 211))
    play = True
    while True:
        screen.fill(pygame.Color("black"))
        fon = pygame.transform.scale(load_image('name.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        input_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(True)
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
            if event.type == pygame.MOUSEMOTION:
                create_particles(pygame.mouse.get_pos())
        ok_btn.draw(280, 350, 'OK', 36, base_data)
        pygame.display.flip()
        clock.tick(30)


def start_screen():
    global LEVEL_COUNT, SCORE, SCORE2, SCORE_UP, SCORE2_UP, SCORE_ALL
    LEVEL_COUNT = 0
    SCORE = 0
    SCORE2 = 0
    SCORE_UP = 0
    SCORE2_UP = 0
    SCORE_ALL = 0
    Mouse()
    pygame.mixer.music.unpause()
    start_btn = Button(200, 50, (105, 105, 105), (154, 205, 50))
    info_btn = Button(200, 50, (105, 105, 105), (72, 209, 204))
    exit_btn = Button(200, 50, (105, 105, 105), (178, 34, 34))
    play = True
    while True:
        screen.fill(pygame.Color("black"))
        fon = pygame.transform.scale(load_image('start_window.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
            if event.type == pygame.MOUSEMOTION:
                create_particles(pygame.mouse.get_pos())
        start_btn.draw(20, 450, 'Start', 36, level)
        info_btn.draw(260, 450, 'Info', 36, information)
        exit_btn.draw(500, 450, 'Exit', 36, terminate)
        mouse.draw(screen)
        star_group.update()
        star_group.draw(screen)
        pygame.display.flip()
        clock.tick(30)


def finish_screen():
    intro_text = ["", "", "", "Поздравляем!", "",
                  "Очки первого игрока составили:", str(SCORE_UP),
                  "Очки второго игрока составили:", str(SCORE2_UP),
                  "Всего очков:", str(SCORE_ALL),
                  "Чтобы сохранить достижение, необходимо сохраниться"]
    Mouse()
    pygame.mixer.music.unpause()
    again_btn = Button(200, 50, (105, 105, 105), (154, 205, 50))
    save_btn = Button(200, 50, (105, 105, 105), (186, 85, 211))
    exit_btn = Button(200, 50, (105, 105, 105), (178, 34, 34))
    play = True
    while True:
        screen.fill(pygame.Color("black"))
        fon = pygame.transform.scale(load_image('finish.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 10
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(25, 25, 112))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
            if event.type == pygame.MOUSEMOTION:
                create_particles(pygame.mouse.get_pos())
        again_btn.draw(20, 25, 'Again', 36, start_screen)
        save_btn.draw(260, 25, 'Save', 36, event_name)
        exit_btn.draw(500, 25, 'Exit', 36, terminate)
        mouse.draw(screen)
        star_group.update()
        star_group.draw(screen)
        pygame.display.flip()
        clock.tick(30)


def died_screen(level_count):
    global SCORE, SCORE2, LEVEL_COUNT, DISK_LEFT, DISK_RIGHT
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(fall_sound)
    platform_ground.empty()
    ground_im.empty()
    playerfirst.empty()
    playersecond.empty()
    cris_group.empty()
    cris_group2.empty()
    gates_group.empty()
    gates_group2.empty()
    fire_group.empty()
    water_group.empty()
    ship_group.empty()
    disk_group.empty()
    projectiles.empty()
    enemy_sprites.empty()
    SCORE = 0
    SCORE2 = 0
    DISK_RIGHT = 1
    DISK_LEFT = 0
    Mouse()
    return_btn = Button(200, 50, (25, 25, 112), (255, 140, 0))
    start_btn = Button(200, 50, (25, 25, 112), (50, 205, 50))
    finish_btn = Button(200, 50, (25, 25, 112), (255, 215, 0))
    exit_btn = Button(200, 50, (25, 25, 112), (178, 34, 34))
    play = True
    while True:
        screen.fill(pygame.Color("black"))
        fon = pygame.transform.scale(load_image('died.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
            if event.type == pygame.MOUSEMOTION:
                create_particles(pygame.mouse.get_pos())
        if level_count == 2 or level_count == 3:
            LEVEL_COUNT = 2
            return_btn.draw(120, 220, 'Again', 36, level_2, (255, 255, 255))
        if level_count == 4 or level_count == 5:
            LEVEL_COUNT = 4
            return_btn.draw(120, 220, 'Again', 36, level_3, (255, 255, 255))
        if level_count == 6 or level_count == 7:
            LEVEL_COUNT = 6
            return_btn.draw(120, 220, 'Again', 36, level_4, (255, 255, 255))
        if level_count == 8 or level_count == 9:
            LEVEL_COUNT = 8
            return_btn.draw(120, 220, 'Again', 36, level_5, (255, 255, 255))
        start_btn.draw(380, 220, 'Start', 36, start_screen, (255, 255, 255))
        finish_btn.draw(120, 300, 'Finish', 36, finish_screen, (255, 255, 255))
        exit_btn.draw(380, 300, 'Exit', 36, terminate, (255, 255, 255))
        mouse.draw(screen)
        star_group.update()
        star_group.draw(screen)
        pygame.display.flip()
        clock.tick(30)


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
            pygame.mixer.Sound.play(cris_sound)
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
        if pressed_keys[K_UP]:
            if pygame.sprite.spritecollide(self, ladder_group, False):
                self.isJump = False
                self.rect.y -= 2
                self.animated(girl_up)
        if pressed_keys[K_DOWN]:
            if pygame.sprite.spritecollide(self, ladder_group, False):
                self.isJump = False
                if self.rect.y < self.pol:
                    self.rect.y += 2
                self.animated(girl_up)
        if self.isJump:
            if self.jumpCount > 0:
                self.rect.y -= self.jumpCount
                self.jumpCount -= 1
            else:
                self.down()
        else:
            if not pygame.sprite.spritecollide(self, platform_ground, False):
                if not pygame.sprite.spritecollide(self, ground_im, False):
                    if not pygame.sprite.spritecollide(self, ladder_group, False):
                        self.isdown()
                    else:
                        if pressed_keys[K_UP]:
                            self.rect.y -= 2
                        if pressed_keys[K_DOWN]:
                            if self.rect.y < self.pol:
                                self.rect.y += 2

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
            pygame.mixer.Sound.play(cris_sound)
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
        if pressed_keys[K_w]:
            if pygame.sprite.spritecollide(self, ladder_group, False):
                self.isJump = False
                self.rect.y -= 2
                self.animated(boys_up)
        if pressed_keys[K_s]:
            if pygame.sprite.spritecollide(self, ladder_group, False):
                self.isJump = False
                if self.rect.y < self.pol:
                    self.rect.y += 2
                self.animated(boys_up)
        if self.isJump:
            if self.jumpCount > 0:
                self.rect.y -= self.jumpCount
                self.jumpCount -= 1
            else:
                self.down()
        else:
            if not pygame.sprite.spritecollide(self, platform_ground, False):
                if not pygame.sprite.spritecollide(self, ground_im, False):
                    if not pygame.sprite.spritecollide(self, ladder_group, False):
                        self.isdown()
                    else:
                        if pressed_keys[K_w]:
                            self.rect.y -= 2
                        if pressed_keys[K_s]:
                            if self.rect.y < self.pol:
                                self.rect.y += 2

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


class Enemy(pygame.sprite.Sprite):
    image = load_image("dragon.png", colorkey=-1)

    def __init__(self, x, y, projectiles):
        super().__init__()
        self.image = Enemy.image
        self.count = 0
        self.rect = self.image.get_rect(topleft=(x, y))
        self.previous_time = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.speed = -20
        self.projectiles = projectiles
        self.mask = pygame.mask.from_surface(self.image)

    def animated(self, img):
        if self.count == 20:
            self.count = 0

        self.image = img[self.count // 5]
        self.count += 1

    def update(self):
        self.animated(dragon_left)
        now = pygame.time.get_ticks()
        if now - self.previous_time > self.shoot_delay:
            pygame.mixer.Sound.play(dragon_sound)
            self.image = load_image("dragon7.png", colorkey=-1)
            self.previous_time = now
            vel = Vector2(self.speed, 0)
            self.projectiles.add(Projectile(self.rect.x, self.rect.y, vel))


class Projectile(pygame.sprite.Sprite):
    image = load_image("sun.png")

    def __init__(self, x, y, vel):
        super().__init__()
        self.image = Projectile.image
        self.rect = self.image.get_rect(topleft=(x, y + 100))
        self.vel = Vector2(vel)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pl1, pl2):
        global LEVEL_COUNT
        self.rect.move_ip(self.vel)
        if pygame.sprite.collide_mask(self, pl1):
            playerfirst.empty()
            playersecond.empty()
            died_screen(LEVEL_COUNT)
        if pygame.sprite.collide_mask(self, pl2):
            playerfirst.empty()
            playersecond.empty()
            died_screen(LEVEL_COUNT)


class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(platform_ground, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Ship(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(ship_group, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self, pl, pl2):
        if pygame.sprite.collide_mask(self, pl):
            playerfirst.empty()
            died_screen(LEVEL_COUNT)
        if pygame.sprite.collide_mask(self, pl2):
            playersecond.empty()
            died_screen(LEVEL_COUNT)


class Disk(pygame.sprite.Sprite):
    def __init__(self, image, x, y, left=None, right=None):
        super().__init__(disk_group, all_sprites)
        image = load_image(image)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.left = left
        self.right = right
        self.rect.x = x
        self.rect.y = y

    def update(self, pl, pl2):
        self.rect.x -= 60
        if not pygame.sprite.spritecollideany(self, platform_ground) or self.rect.x <= 0:
            self.left = 0
            self.right = 1
        self.rect.x += 120
        if not pygame.sprite.spritecollideany(self, platform_ground) or self.rect.x >= width:
            self.left = 1
            self.right = 0
        self.rect.x -= 60
        if self.left:
            self.rect.x -= 5
        if self.right:
            self.rect.x += 5
        if pygame.sprite.collide_mask(self, pl):
            playerfirst.empty()
            died_screen(LEVEL_COUNT)
        if pygame.sprite.collide_mask(self, pl2):
            playersecond.empty()
            died_screen(LEVEL_COUNT)


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(ground_im, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


def base_data():
    global text, text2
    c = False
    result = cur.execute("""SELECT * FROM participants""").fetchall()
    for i in result:
        if (i[1] == text and i[2] == text2) or (i[1] == text2 and i[2] == text):
            c = True
            if i[5] < SCORE_ALL:
                up_date = cur.execute("""UPDATE participants 
                SET score = ?, score2 = ?, score_all = ? 
                WHERE id = ?""", (SCORE_UP, SCORE2_UP, SCORE_ALL, i[0])).fetchall()
                con.commit()
    if not c:
        up_date = cur.execute("""INSERT INTO participants(name, name2, score, score2, score_all)
        VALUES(?, ?, ?, ?, ?)""", (text, text2, SCORE_UP, SCORE2_UP, SCORE_ALL))
        con.commit()
    text = ''
    text2 = ''
    finish_screen()


class Fire(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(fire_group, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.count = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def animated(self):
        if self.count == 80:
            self.count = 0

        self.image = fire_img[self.count // 5]
        self.count += 1

    def update(self, pl):
        global LEVEL_COUNT
        if pygame.sprite.collide_mask(self, pl):
            playerfirst.empty()
            died_screen(LEVEL_COUNT)


class Water(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(water_group, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.count = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def animated(self):
        if self.count == 45:
            self.count = 0

        self.image = water_img[self.count // 5]
        self.count += 1

    def update(self, pl):
        global LEVEL_COUNT
        if pygame.sprite.collide_mask(self, pl):
            playersecond.empty()
            died_screen(LEVEL_COUNT)


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


class Gates(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(gates_group, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global LEVEL_COUNT
        if pygame.sprite.spritecollide(self, playerfirst, True):
            LEVEL_COUNT += 1


class Gates2(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(gates_group2, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global LEVEL_COUNT
        if pygame.sprite.spritecollide(self, playersecond, True):
            LEVEL_COUNT += 1


class Ladder(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(ladder_group, all_sprites)
        image = load_image(image, -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


def level():
    global SCORE, SCORE2, SCORE_ALL, SCORE_UP, SCORE2_UP
    pygame.mixer.music.unpause()
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
    Mouse()
    play = True
    while running:
        if LEVEL_COUNT == 2:
            pygame.mixer.Sound.play(level_sound)
            fon.empty()
            platform_ground.empty()
            ground_im.empty()
            playerfirst.empty()
            playersecond.empty()
            cris_group.empty()
            cris_group2.empty()
            gates_group.empty()
            gates_group2.empty()
            SCORE_ALL += SCORE
            SCORE_ALL += SCORE2
            SCORE_UP += SCORE
            SCORE2_UP += SCORE2
            SCORE = 0
            SCORE2 = 0
            level_2()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(jump_sound)
                    first.isJump = True
                if event.key == pygame.K_w:
                    pygame.mixer.Sound.play(jump_sound)
                    second.isJump = True
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
        pressed_keys = pygame.key.get_pressed()
        first.move(pressed_keys)
        second.move(pressed_keys)
        screen.fill(pygame.Color("black"))
        fon.draw(screen)
        print_text(SCORE, 40, 5, 30, (255, 255, 255))
        print_text(SCORE2, 700, 5, 30, (255, 255, 255))
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
        mouse.draw(screen)
        playerfirst.draw(screen)
        playersecond.draw(screen)
        gates_group.update()
        gates_group2.update()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


def level_2():
    global SCORE, SCORE2, SCORE_ALL, SCORE_UP, SCORE2_UP
    pygame.mixer.music.unpause()
    Fon("montain.png")
    Gates("gates2.png", 560, 30)
    Gates2("gates.png", 640, 30)
    cris = []
    cris2 = []
    water = []
    fire = []
    first = PlayerFirst(40, 461)
    second = PlayerSecond(0, 463)
    fire_list = [[155, 450], [160, 290]]
    for i in fire_list:
        fire.append(Fire("fire.png", i[0], i[1]))
    water_list = [[355, 445], [355, 215]]
    list_cr_gl = [[5, 5], [160, 400], [190, 400], [20, 310], [430, 120]]
    for i in water_list:
        water.append(Water("water.png", i[0], i[1]))
    for i in list_cr_gl:
        cris.append(Cris("cris.png", i[0], i[1]))
    list_cr_mn = [[660, 5], [360, 400], [390, 400], [20, 170], [280, 170]]
    for i in list_cr_mn:
        cris2.append(Cris2("cris2.png", i[0], i[1]))
    list_platforms = [[150, 430], [350, 430], [-2, 340], [80, 340], [158, 340], [236, 340], [314, 340], [392, 340],
                      [470, 340], [150, 270], [350, 270], [-2, 200], [250, 200], [400, 150], [550, 90], [628, 90],
                      [635, 370], [550, 440]]
    for i in list_platforms:
        Platform("platform.png", i[0], i[1])
    running = True
    Mouse()
    play = True
    while running:
        if LEVEL_COUNT == 4:
            pygame.mixer.Sound.play(level_sound)
            fon.empty()
            platform_ground.empty()
            ground_im.empty()
            playerfirst.empty()
            playersecond.empty()
            cris_group.empty()
            cris_group2.empty()
            gates_group.empty()
            gates_group2.empty()
            fire_group.empty()
            water_group.empty()
            SCORE_ALL += SCORE
            SCORE_ALL += SCORE2
            SCORE_UP += SCORE
            SCORE2_UP += SCORE2
            SCORE = 0
            SCORE2 = 0
            level_3()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(jump_sound)
                    first.isJump = True
                if event.key == pygame.K_w:
                    pygame.mixer.Sound.play(jump_sound)
                    second.isJump = True
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
        pressed_keys = pygame.key.get_pressed()
        first.move(pressed_keys)
        second.move(pressed_keys)
        screen.fill(pygame.Color("black"))
        fon.draw(screen)
        print_text(SCORE, 40, 5, 30, (255, 255, 255))
        print_text(SCORE2, 700, 5, 30, (255, 255, 255))
        for i in cris:
            i.animated()
        for i in cris2:
            i.animated()
        for i in fire:
            i.animated()
        for i in water:
            i.animated()
        fire_group.draw(screen)
        water_group.draw(screen)
        cris_group.draw(screen)
        cris_group2.draw(screen)
        gates_group.draw(screen)
        gates_group2.draw(screen)
        platform_ground.draw(screen)
        playerfirst.draw(screen)
        playersecond.draw(screen)
        gates_group.update()
        gates_group2.update()
        fire_group.update(first)
        water_group.update(second)
        mouse.draw(screen)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


def level_3():
    global SCORE, SCORE2, SCORE_ALL, SCORE_UP, SCORE2_UP
    pygame.mixer.music.unpause()
    Fon("village.jpg")
    Gates("gates2.png", 0, 450)
    Gates2("gates.png", 650, 450)
    cris = []
    cris2 = []
    water = []
    fire = []
    ship = []
    first = PlayerFirst(660, 468)
    second = PlayerSecond(20, 468)
    fire_list = [[500, 465], [420, 465], [185, 395], [490, 102]]
    for i in fire_list:
        fire.append(Fire("fire.png", i[0], i[1]))
    water_list = [[150, 455], [220, 455], [455, 390], [140, 95]]
    list_cr_gl = [[5, 5], [480, 410], [360, 340], [210, 265], [330, 195], [165, 115]]
    for i in water_list:
        water.append(Water("water.png", i[0], i[1]))
    for i in list_cr_gl:
        cris.append(Cris("cris.png", i[0], i[1]))
    list_cr_mn = [[660, 5], [210, 410], [330, 340], [470, 265], [365, 195], [515, 115]]
    for i in list_cr_mn:
        cris2.append(Cris2("cris2.png", i[0], i[1]))
    list_platforms = [[180, 445], [450, 445], [180, 300], [100, 300], [450, 300], [530, 300], [320, 230],
                      [180, 150], [100, 150], [450, 150], [530, 150], [315, 375]]
    for i in list_platforms:
        Platform("platform.png", i[0], i[1])
    ship_list = [[535, 285], [105, 285]]
    for i in ship_list:
        ship.append(Ship("ship.png", i[0], i[1]))
    running = True
    Mouse()
    play = True
    while running:
        if LEVEL_COUNT == 6:
            pygame.mixer.Sound.play(level_sound)
            fon.empty()
            platform_ground.empty()
            ground_im.empty()
            playerfirst.empty()
            playersecond.empty()
            cris_group.empty()
            cris_group2.empty()
            gates_group.empty()
            gates_group2.empty()
            fire_group.empty()
            water_group.empty()
            ship_group.empty()
            SCORE_ALL += SCORE
            SCORE_ALL += SCORE2
            SCORE_UP += SCORE
            SCORE2_UP += SCORE2
            SCORE = 0
            SCORE2 = 0
            level_4()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(jump_sound)
                    first.isJump = True
                if event.key == pygame.K_w:
                    pygame.mixer.Sound.play(jump_sound)
                    second.isJump = True
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
        pressed_keys = pygame.key.get_pressed()
        first.move(pressed_keys)
        second.move(pressed_keys)
        screen.fill(pygame.Color("black"))
        fon.draw(screen)
        print_text(SCORE, 40, 5, 30)
        print_text(SCORE2, 700, 5, 30)
        for i in cris:
            i.animated()
        for i in cris2:
            i.animated()
        for i in fire:
            i.animated()
        for i in water:
            i.animated()
        fire_group.draw(screen)
        water_group.draw(screen)
        cris_group.draw(screen)
        cris_group2.draw(screen)
        gates_group.draw(screen)
        gates_group2.draw(screen)
        ship_group.draw(screen)
        platform_ground.draw(screen)
        playerfirst.draw(screen)
        playersecond.draw(screen)
        gates_group.update()
        gates_group2.update()
        fire_group.update(first)
        water_group.update(second)
        ship_group.update(first, second)
        mouse.draw(screen)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


def level_4():
    global SCORE, SCORE2, SCORE_ALL, SCORE_UP, SCORE2_UP
    enemy = Enemy(600, 60, projectiles)
    enemy_sprites.add(enemy)
    enemy = Enemy(600, 380, projectiles)
    enemy_sprites.add(enemy)
    pygame.mixer.music.unpause()
    Fon("gorge.jpg")
    Gates("gates2.png", 100, 10)
    Gates2("gates.png", 200, 10)
    cris = []
    cris2 = []
    first = PlayerFirst(10, 465)
    second = PlayerSecond(40, 468)
    list_cr_gl = [[5, 5], [150, 420], [300, 280], [150, 120], [400, 30]]
    for i in list_cr_gl:
        cris.append(Cris("cris.png", i[0], i[1]))
    list_cr_mn = [[660, 5], [200, 420], [50, 280], [600, 120], [300, 30]]
    for i in list_cr_mn:
        cris2.append(Cris2("cris2.png", i[0], i[1]))
    list_platforms = [[0, 370], [80, 370], [160, 370], [240, 370], [320, 370], [400, 370], [480, 370], [560, 370],
                      [640, 370], [720, 370], [0, 220], [160, 220], [240, 220], [320, 220], [400, 220],
                      [480, 220], [560, 220], [640, 220], [720, 220], [0, 70], [80, 70], [160, 70], [240, 70],
                      [320, 70], [400, 70], [480, 70], [560, 70], [640, 70], [720, 70], [100, 300]]
    for i in list_platforms:
        Platform("gr.png", i[0], i[1])
    list_ladder = [[400, 370], [400, 70]]
    for i in list_ladder:
        Ladder("lest1.png", i[0], i[1])
    running = True
    Mouse()
    play = True
    while running:
        if LEVEL_COUNT == 8:
            pygame.mixer.Sound.play(level_sound)
            fon.empty()
            platform_ground.empty()
            ground_im.empty()
            playerfirst.empty()
            playersecond.empty()
            cris_group.empty()
            cris_group2.empty()
            gates_group.empty()
            gates_group2.empty()
            projectiles.empty()
            enemy_sprites.empty()
            ladder_group.empty()
            SCORE_ALL += SCORE
            SCORE_ALL += SCORE2
            SCORE_UP += SCORE
            SCORE2_UP += SCORE2
            SCORE = 0
            SCORE2 = 0
            level_5()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(jump_sound)
                    first.isJump = True
                if event.key == pygame.K_w:
                    pygame.mixer.Sound.play(jump_sound)
                    second.isJump = True
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
        pressed_keys = pygame.key.get_pressed()
        first.move(pressed_keys)
        second.move(pressed_keys)
        screen.fill(pygame.Color("black"))
        fon.draw(screen)
        print_text(SCORE, 40, 5, 30, (255, 255, 255))
        print_text(SCORE2, 700, 5, 30, (255, 255, 255))
        for i in cris:
            i.animated()
        for i in cris2:
            i.animated()
        cris_group.draw(screen)
        cris_group2.draw(screen)
        gates_group.draw(screen)
        gates_group2.draw(screen)
        ship_group.draw(screen)
        platform_ground.draw(screen)
        ladder_group.draw(screen)
        playerfirst.draw(screen)
        playersecond.draw(screen)
        gates_group.update()
        gates_group2.update()
        mouse.draw(screen)
        projectiles.update(first, second)
        enemy_sprites.update()
        projectiles.draw(screen)
        enemy_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(40)
    pygame.quit()


def level_5():
    global SCORE, SCORE2, SCORE_ALL, SCORE_UP, SCORE2_UP
    enemy = Enemy(600, 60, projectiles)
    enemy_sprites.add(enemy)
    enemy = Enemy(600, 360, projectiles)
    enemy_sprites.add(enemy)
    pygame.mixer.music.unpause()
    Fon("home.jpg")
    Gates("gates2.png", 100, 15)
    Gates2("gates.png", 200, 15)
    cris = []
    cris2 = []
    disk = []
    ship = []
    disk_list = [[600, 490], [600, 345]]
    for i in disk_list:
        disk.append(Disk("disk.png", i[0], i[1], 1, 0))
    first = PlayerFirst(10, 465)
    second = PlayerSecond(40, 468)
    list_cr_gl = [[5, 5], [170, 420], [650, 290], [530, 100], [400, 30]]
    for i in list_cr_gl:
        cris.append(Cris("cris.png", i[0], i[1]))
    list_cr_mn = [[660, 5], [300, 420], [60, 180], [400, 180], [350, 30]]
    for i in list_cr_mn:
        cris2.append(Cris2("cris2.png", i[0], i[1]))
    list_platforms = [[0, 365], [80, 365], [160, 365], [240, 365], [320, 365], [420, 425], [510, 365], [590, 365],
                      [670, 365],  [0, 510], [80, 510], [160, 510], [240, 510], [320, 510], [400, 510],
                      [480, 510], [560, 510], [640, 510], [720, 510], [320, 220], [400, 220], [480, 220],
                      [560, 220], [640, 220], [720, 220], [0, 70], [80, 70], [160, 70], [240, 70], [320, 70], [400, 70],
                      [500, 140], [170, 290], [30, 220]]
    for i in list_platforms:
        Platform("platform.png", i[0], i[1])
    ship_list = [[0, 350], [80, 350], [160, 350], [230, 350]]
    for i in ship_list:
        ship.append(Ship("ship.png", i[0], i[1]))
    running = True
    Mouse()
    play = True
    while running:
        if LEVEL_COUNT == 10:
            pygame.mixer.Sound.play(winner_sound)
            fon.empty()
            platform_ground.empty()
            ground_im.empty()
            playerfirst.empty()
            playersecond.empty()
            cris_group.empty()
            cris_group2.empty()
            gates_group.empty()
            gates_group2.empty()
            projectiles.empty()
            enemy_sprites.empty()
            disk_group.empty()
            ship_group.empty()
            SCORE_ALL += SCORE
            SCORE_ALL += SCORE2
            SCORE_UP += SCORE
            SCORE2_UP += SCORE2
            SCORE = 0
            SCORE2 = 0
            finish_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    first.isJump = True
                    pygame.mixer.Sound.play(jump_sound)
                if event.key == pygame.K_w:
                    second.isJump = True
                    pygame.mixer.Sound.play(jump_sound)
            if event.type == pygame.MOUSEMOTION:
                if play:
                    pygame.mouse.set_visible(False)
                    mouse.update(event)
                    mouse.draw(screen)
                else:
                    pygame.mouse.set_visible(True)
                    screen.fill(pygame.Color("black"))
            if pygame.mouse.get_focused():
                play = True
            else:
                play = False
        pressed_keys = pygame.key.get_pressed()
        first.move(pressed_keys)
        second.move(pressed_keys)
        screen.fill(pygame.Color("black"))
        fon.draw(screen)
        print_text(SCORE, 40, 5, 30, (255, 255, 255))
        print_text(SCORE2, 700, 5, 30, (255, 255, 255))
        for i in cris:
            i.animated()
        for i in cris2:
            i.animated()
        disk_group.draw(screen)
        cris_group.draw(screen)
        cris_group2.draw(screen)
        gates_group.draw(screen)
        gates_group2.draw(screen)
        ship_group.draw(screen)
        ship_group.draw(screen)
        platform_ground.draw(screen)
        playerfirst.draw(screen)
        playersecond.draw(screen)
        gates_group.update()
        gates_group2.update()
        disk_group.update(first, second)
        mouse.draw(screen)
        projectiles.update(first, second)
        ship_group.update(first, second)
        enemy_sprites.update()
        projectiles.draw(screen)
        enemy_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(40)
    pygame.quit()


def terminate():
    pygame.quit()
    sys.exit()


start_screen()
