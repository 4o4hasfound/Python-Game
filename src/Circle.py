from __future__ import annotations
from pygame.math import Vector2 as vec2
from src.Physics.AABB import AABB
import math

class Circle:
    def __init__(self, pos: vec2, radius: float) -> None:
        self.position: vec2 = pos
        self.radius: float = radius
    
    def intersect(self, other: AABB) -> bool:
        testX: float = self.position.x
        testY: float = self.position.y

        if (self.position.x < other.left):		    testX = other.left
        elif (self.position.x > other.right):		testX = other.right
        if (self.position.y < other.top):			testY = other.top
        elif (self.position.y > other.bottom):		testY = other.bottom

        distX: float = self.position.x - testX
        distY: float = self.position.y - testY
        distanceSquare: float = (distX * distX) + (distY * distY)

        return distanceSquare <= self.radius * self.radius
    
    def __add__(self, pos: vec2) -> Circle:
        return Circle(self.position + pos, self.radius)
    def __sub__(self, pos: vec2) -> Circle:
        return Circle(self.position - pos, self.radius)