from __future__ import annotations
import pygame as pg
from pygame.math import Vector2 as vec2
from src.Physics.AABB import AABB
from src.Physics.Collider import CollidePoint, Collider, SphereCollider
from typing import List


class PhysicsWorld:
    def __init__(self):
        self.objects: List[SphereCollider] = list()
        # ...
        # O..
        # OXX
        # .O.
        # .OX

    def TestCollision(self):
        # O(n^2) broad phase
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                collidePoint: CollidePoint = self.objects[
                    i].testCollisionSphereToSphere(self.objects[j])
                if collidePoint.hasCollide:
                    self.objects[i].Position -= 0.5 * \
                        collidePoint.Normal * collidePoint.Depth
                    self.objects[j].Position += 0.5 * \
                        collidePoint.Normal * collidePoint.Depth

    def AddObject(self, object) -> int:
        self.objects.append(object)
        return len(self.objects) - 1
