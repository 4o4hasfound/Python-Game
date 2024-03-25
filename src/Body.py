from AABB import AABB
from enum import Enum, auto

class BodyType(Enum):
    Static = auto()
    Character = auto()
    Enemy = auto()
    Any = auto()
    
class CollisionDetail:
    def __init__(self, direction: vec2, delta: float) -> None:
        self.direction: vec2 = direction
        self.delta: float = delta
        
class BodyStatus:
    def __init__(self):
        self.velocity: vec2 = vec2(0, 0)
        self.health = 100
        self.doorClosed: bool = False
    
# class Character(Body):
#     def __init__(self):
#         Body.__init__(BodyType.Character, aabb)
        
#     def onCollide(self, other: Body, detail: CollisionDetail):
#         if skill:
#             if other.type == BodyType.Enemy:
#                 other.status.health -= 100

class Body:
    def __init__(self, bodyType: BodyType, aabb: AABB) -> None:
        self._type: BodyType = bodyType
        self._aabb: AABB = aabb
        self._position: vec2 = vec2(0, 0)
        self.status: BodyStatus = BodyStatus()
    
    @property
    def type(self) -> BodyType:
        return self._type
    
    @property
    def aabb(self) -> vec2:
        return self._aabb
    
    @property
    def position(self) -> vec2:
        return self._position
    @position.setter
    def position(self, pos: vec2) -> None:
        self._position += pos - self._aabb.position
        self._aabb.position = pos
    
    def move(self, x: float, y: float) -> None:
        self._aabb.position += vec2(x, y)
        self._position += vec2(x, y)
        
    def onCollide(self, other: Body, detail: CollisionDetail):
        pass