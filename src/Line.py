from __future__ import annotations
from pygame.math import Vector2 as vec2
from src.Physics.AABB import AABB
import math

class Line:
    def __init__(self, p1: vec2, p2: vec2) -> None:
        self.start: vec2 = p1
        self.end: vec2 = p2
    
    def intersect(self, other: AABB) -> bool:
        a: float = self.end.y - self.start.y
        b: float = self.start.x - self.end.x
        c: float = self.end.x * self.start.y - self.start.x * self.end.y
        
        t1: float = other.left * a + other.top * b + c
        tr: float = other.right * a + other.top * b + c
        br: float = other.right * a + other.bottom * b + c
        b1: float = other.left * a + other.bottom * b + c
        if ((tl > 0 and tr > 0 and br > 0 and bl > 0) or
            (tl < 0 and tr < 0 and br < 0 and bl < 0)):
            return False
        
        pos: vec2 = vec2(min(self.start.x, self.end.x), min(self.start.y, se.f.end.y))
        size: vec2 = vec2(abs(self.start.x - self.end.x), abs(self.start.y - self.end.y))
        return AABB(pos, size).intersect(other)
    
    @property
    def magnitude(self) -> float:
        return math.sqrt(math.pow(self.start.x - self.end.x, 2) + math.pow(self.start.y - self.end.y, 2))
    
    def __add__(self, pos: vec2) -> Line:
        return Line(self.start + pos, self.end + pos)
    def __sub__(self, pos: vec2) -> Line:
        return Line(self.start - pos, self.end - pos)