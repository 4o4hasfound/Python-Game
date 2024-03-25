from __future__ import annotations
import pygame as pg
from pygame.math import Vector2 as vec2


class AABB:
    def __init__(self, pos: vec2, size: vec2):
        # top left
        self.tl = pos

        # top right
        self.tr = pos + vec2(size.x, 0)

        # bottom left
        self.bl = pos + vec2(0, size.y)

        # bottom right
        self.br = pos + size

        self.width = size.x

        self.height = size.y

        self.minX = pos.x
        self.maxX = pos.x + size.x
        self.minY = pos.y
        self.maxY = pos.y + size.y

    def intersect(self, other: AABB) -> bool:
        return self.maxX > other.minX and other.maxX > self.minX and self.maxY > other.minY and other.maxX > self.minY
