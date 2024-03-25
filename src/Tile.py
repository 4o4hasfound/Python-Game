# 剛剛的每一格東西是幾乘幾!?

import pygame
import pytmx


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, length, img):
        super().__init__(group)
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        # self.hitbox = self.rect.inflate(?, ?)
        self.hitbox = self.rect.inflate(0, -10)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, group, length, img):
        # super().__init__(group)
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group, length, img):
        super().__init__(group)
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        # self.hitbox = rect.inflate(?, ?)
        self.hitbox = self.rect.inflate(0, -10)
