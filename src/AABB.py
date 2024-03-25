from __future__ import annotations
from pygame.math import Vector2 as vec2

class AABB:
    def __init__(self, pos: vec2, size: vec2) -> None:
        self.__position: vec2 = pos
        self.__size: vec2 = size
        
    @classmethod
    def fromTwoPoints(cls, p1: vec2, p2: vec2) -> AABB:
        topLeft: vec2 = vec2(
            min(p1.x, p2.x),
            min(p1.y, p2.y)
        )
        bottomRight: vec2 = vec2(
            max(p1.x, p2.x),
            max(p1.y, p2.y)
        )
        return cls(topLeft, bottomRight - topLeft)
    
    def intersect(self, other: AABB) -> bool:
        return (
            self.right > other.left and 
            other.right > self.left and 
            self.bottom > other.top and 
            other.bottmo > self.top
        )
        
    def contain(self, other: AABB) -> bool:
        return (
            self.left < other.left and 
            self.right > other.right and 
            self.top < other.top and 
            self.bottom > other.bottom
        )
    
    # Other property functions
    @property
    def size(self) -> vec2:
        return self.__size
    @size.setter
    def size(self, size: vec2) -> None:
        self.__size = size
        
    @property
    def position(self) -> vec2:
        return self.__position
    @position.setter
    def position(self, pos: vec2) -> None:
        self.__position = pos
    
    @property
    def left(self) -> float:
        return self.__position.x
    @left.setter
    def left(self, newLeft: float) -> None:
        newWidth: float = self.right - newLeft
        self.__size.x = newWidth
        self.__position.x = newLeft
        
    @property
    def right(self) -> float:
        return self.__position.x + self.__size.x
    @right.setter
    def right(self, newRight: float) -> None:
        self.__size.x = newRight - self.__position.x

    @property
    def top(self) -> float:
        return self.__position.y
    @top.setter
    def top(self, newTop: float) -> None:
        newHeight: float = self.bottom - newTop
        self.__size.y = newHeight
        self.__position.y = newTop
    
    @property
    def bottom(self) -> float:
        return self.__position.y + self.__size.y
    @bottom.setter
    def bottom(self, newBottom: float) -> None:
        self.__size.y = newBottom - self.__position.y
        
    @property
    def width(self) -> float:
        return self.__size.x
    @width.setter
    def width(self, newWidth: float) -> None:
        self.__size.x = newWidth
        
    @property
    def height(self) -> float:
        return self.__size.y
    @height.setter
    def height(self, newHeight: float) -> None:
        self.__size.y = newHeight
        
    def __add__(self, pos: vec2) -> AABB:
        return AABB(self.__position + pos, self.__size)
    
    def __sub__(self, pos: vec2) -> AABB:
        return AABB(self.__position - pos, self.__size)