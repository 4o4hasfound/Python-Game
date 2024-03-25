from __future__ import annotations
import pygame as pg
from pygame.math import Vector2 as vec2
from src.Physics.AABB import AABB


class CollidePoint:
    def __init__(self, a: Collider, b: Collider, normal: vec2, depth: float, hasCollide: bool):
        self.a = a
        self.b = b
        self.Normal = normal
        self.Depth = depth
        self.hasCollide = hasCollide


class Collider:
    def __init__(self, aabb: AABB, pos: vec2):
        self.Position = pos
        self.aabb = AABB


class SphereCollider(Collider):
    def __init__(self, radius: int, aabb: AABB, pos: vec2):
        self.radius = radius
        Collider.__init__(self, aabb, pos)

    def testCollisionSphereToSphere(self, other: SphereCollider) -> CollidePoint:
        normal: vec2 = self.Position - other.Position
        dist: float = normal.length()
        hasCollide: bool = dist < self.radius + other.radius
        normal = normal.normalize()
        depth: float = self.radius + other.radius - dist
        return CollidePoint(a=self, b=other, normal=normal, depth=depth, hasCollide=hasCollide)


# PhysicsWorld -> List[Object]
# Object -> Collider
# Collider -> AABB

# AABB 大致上
