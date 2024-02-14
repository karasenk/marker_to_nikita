import os
import sys
import pygame
from random import choice


dirs = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]


def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    # если файл не существует, то выходим
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


class Oc:
    def __init__(self, coords):
        self.coords = coords


class Marker(Oc):
    def __init__(self, coords):
        super().__init__(coords)
        self.image = load_image('marker.png')
        self.to_del = False

    def move(self):
        self.coords[1] -= 0.3

    def check_collide(self, nikita, himik):
        x, y = nikita.coords
        if abs(self.coords[0] - x) < 14 and abs(self.coords[1] - y) < 50:
            himik.score += 1
            self.to_del = True


class Nikita(Oc):
    def __init__(self, coords):
        super().__init__(coords)
        self.img = load_image('nikita.png')
        self.dir = [choice(dirs), choice(dirs)]
        self.speed = 0.3
        self.timer = 0

    def change_dir(self):
        if choice([1, 2]) % 2 == 0:
            self.dir[0] = choice(dirs)
        else:
            self.dir[1] = choice(dirs)
        while self.dir[0] == 0 and self.dir[1] == 0:
            self.dir[0] = choice(dirs)
            self.dir[1] = choice(dirs)

    def move(self):
        x = round(self.coords[0] + self.dir[0] * self.speed, 1)
        y = round(self.coords[1] + self.dir[1] * self.speed, 1)

        if x < 50 or x > 700:
            self.dir[0] *= -1
            x = round(self.coords[0] + self.dir[0] * self.speed, 1)
        if y < 50 or y > 700:
            self.dir[1] *= -1
            y = round(self.coords[1] + self.dir[1] * self.speed, 1)
        self.coords = [x, y]


class Himik(Oc):
    def __init__(self, coords):
        super().__init__(coords)
        self.img = load_image('himik.png')
        self.speed = 40
        self.score = 0

    def move(self, d):
        x = round(self.coords[0] + d * self.speed, 1)
        if 50 <= x <= 700:
            self.coords[0] = x
