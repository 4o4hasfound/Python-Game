from __future__ import annotations
import pygame as pg
from pygame.math import Vector2 as vec2
from AABB import AABB
from Line import Line
from Circle import Circle
from Body import Body, BodyType
from typing import List, Dict, Tuple
from FreeList import FreeList
from enum import Enum, auto
import copy
import math


class PhysicsWorld:
    chunkSize: vec2 = vec2(256, 256)
    gravity: float = 0.006
    
    def __init__(self) -> None:
        self.__bodies: List[Body] = list()
        # old aabb
        self.__aabbs: List[AABB] = list()
        self.__globalBound: AABB = AABB(-self.chunkSize, self.chunkSize * 2.0)
        self.__chunks: List[List[FreeList[int]]] = [
            [
                FreeList() for x in range(int(self.__globalBound.width / self.chunkSize.x))
            ] for y in range(int(self.__globalBound.height / self.chunkSize.y))
        ]
        
    def addBody(self, body: Body) -> None:
        self.__addObjectInChunk(len(self.__bodies), body)
        self.__bodies.append(body)
        self.__aabbs.append(body.aabb)
        
    def update(self) -> None:
        self.__UpdateGrid()
        self.__globalCollisionDetection()
        
    def applyGravity(self) -> None:
        for body in self.__bodies:
            body.status.velocity.y += self.gravity
            
    def query(self, toQuery: AABB | Circle | Line, queryType: BodyType = BodyType.Any) -> List[Body]:
        inVector: Dict[Body, bool] = dict()
        ret: List[Body] = list()
        
        x1: int = 0
        x2: int = 0
        y1: int = 0
        y2: int = 0
        
        if type(toQuery) == AABB:
            x1 = int((toQuery.left - self.__globalBound.left) / self.chunkSize.x)
            x2 = int((toQuery.right - self.__globalBound.left) / self.chunkSize.x)
            y1 = int((toQuery.top - self.__globalBound.top) / self.chunkSize.y)
            y2 = int((toQuery.bottom - self.__globalBound.top) / self.chunkSize.y)
        elif type(toQuery) == Circle:
            x1 = int((toQuery.position.x - toQuery.radius - self.__globalBound.left) / self.chunkSize.x)
            x2 = int((toQuery.position.x + toQuery.radius - self.__globalBound.left) / self.chunkSize.x)
            y1 = int((toQuery.position.y - toQuery.radius - self.__globalBound.top) / self.chunkSize.y)
            y2 = int((toQuery.position.y + toQuery.radius - self.__globalBound.top) / self.chunkSize.y)
        elif type(toQuery) == Line:
            x1 = int((toQuery.start.x - self.__globalBound.left) / self.chunkSize.x)
            x2 = int((toQuery.end.x - self.__globalBound.left) / self.chunkSize.x)
            y1 = int((toQuery.start.y - self.__globalBound.top) / self.chunkSize.y)
            y2 = int((toQuery.end.y - self.__globalBound.top) / self.chunkSize.y)
        
        x1 = max(0, x1)
        x2 = min(len(self.__chunks[0])-1, x2)
        y1 = max(0, y1)
        y2 = min(len(self.__chunks)-1, y2)
    
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                for ind in self.__chunks[y][x]:
                    if not toQuery.intersect(self.__bodies[ind].aabb):
                        continue
                    if queryType != BodyType.Any and self.__bodies[ind].type != queryType:
                        continue
                    if inVector[self.__bodies[ind]]:
                        continue
                    inVector[self.__bodies[ind]] = 1
                    ret.append(self.__bodies[ind])
        return ret
        
    def __globalCollisionDetection(self) -> None:
        solved: Dict[Tuple[int, int], bool] = dict()
        for i in range(len(self.__bodies)):
            if self.__bodies[i].type == BodyType.Static:
                continue
            
            x1: int = int((self.__bodies[i].aabb.left - self.__globalBound.left) / self.chunkSize.x)
            x2: int = int((self.__bodies[i].aabb.right - self.__globalBound.left) / self.chunkSize.x)
            y1: int = int((self.__bodies[i].aabb.top - self.__globalBound.top) / self.chunkSize.y)
            y2: int = int((self.__bodies[i].aabb.bottom - self.__globalBound.top) / self.chunkSize.y)
                
            for y in range(y1, y2+1):
                for x in range(x1, x2+1):
                    self.__localCollisionDetection(i, self.__chunks[y][x], solved)
                    
    def __localCollisionDetcetion(self, bodyIndex: int, chunk: FreeList[int], solved: Dict[Tuple[int, int], bool]) -> None:
        for i in chunk:
            if bodyIndex == i or solved[(bodyIndex, i)] or solved[(i, bodyIndex)]:
                continue
            solved[(bodyIndex, i)] = solved[(i, bodyIndex)] = True

            body: Body = self.__bodies[bodyIndex]
            other: Body = self.__bodies[i]
            
            if not body.aabb.intersect(other.aabb):
                continue
            
            # body at right of other
            deltax1: float = other.aabb.right - body.aabb.left
            # body at left of other
            deltax2: float = body.aabb.right - other.aabb.left
            
            # body at bottom of other
            deltay1: float = other.aabb.bottom - body.aabb.top
            # body at top of other
            deltay2: float = body.aabb.bottom - other.aabb.top
            
            if min(deltax1, deltax2) < min(deltay1, deltay2):
                if abs(deltax1) < abs(deltax2):
                    direction: vec2 = vec2(1, 0)
                    if other.type == BodyType.Static:
                        body.move(deltax1, 0)
                        body.onCollide(other, CollisionDetail(direction, deltax1))
                        continue
                    body.onCollide(other, CollisionDetail(direction, deltax1))
                    other.onCollide(body, CollisionDetail(-direction, deltax1))
                    continue
                else:
                    direction: vec2 = vec2(-1, 0)
                    if other.type == BodyType.Static:
                        body.move(-deltax2, 0)
                        body.onCollide(other, CollisionDetail(direction, -deltax2))
                        continue
                    body.onCollide(other, CollisionDetail(direction, deltax2))
                    other.onCollide(body, CollisionDetail(-direction, deltax2))
                    continue
            else:
                if abs(deltay1) < abs(deltay2):
                    direction: vec2 = vec2(0, 1)
                    if other.type == BodyType.Static:
                        body.move(0, deltay1)
                        body.onCollide(other, CollisionDetail(direction, deltay1))
                        continue
                    body.onCollide(other, CollisionDetail(direction, deltay1))
                    other.onCollide(body, CollisionDetail(-direction, deltay1))
                    continue
                else:
                    direction: vec2 = vec2(0, -1)
                    if other.type == BodyType.Static:
                        body.move(0, -deltay2)
                        body.onCollide(other, CollisionDetail(direction, deltay2))
                        continue
                    body.onCollide(other, CollisionDetail(direction, deltay2))
                    other.onCollide(body, CollisionDetail(-direction, deltay2))
                    continue
            
                
    def __UpdateGrid(self) -> None:
        for i in range(len(self.__bodies)):
            if self.__bodies[i].type == BodyType.Static or self.__bodies[i].aabb == self.__aabbs[i]:
                continue
            self.__removeObjectInGrid(i, self.__aabbs[i])
            self.__addObjectInGrid(i, self.__bodies[i].aabb)
            self.__aabbs[i] = self.__bodies[i].aabb
        
    def __addObjectInChunk(self, index: int, aabb: AABB) -> None:
        if not self.__globalBound.contain(aabb):
            self.__expandGrid(aabb)
            
        x1: int = int((aabb.left - self.__globalBound.left) / self.chunkSize.x)
        x2: int = int((aabb.right - self.__globalBound.left) / self.chunkSize.x)
        y1: int = int((aabb.top - self.__globalBound.top) / self.chunkSize.y)
        y2: int = int((aabb.bottom - self.__globalBound.top) / self.chunkSize.y)
        
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                self.__chunks[y][x].push(index)
                
    def __removeObjectInGrid(self, index: int, aabb: AABB) -> None:
        if not self.__globalBound.contain(aabb):
            self.__expandGrid(aabb)
            
        x1: int = int((aabb.left - self.__globalBound.left) / self.chunkSize.x)
        x2: int = int((aabb.right - self.__globalBound.left) / self.chunkSize.x)
        y1: int = int((aabb.top - self.__globalBound.top) / self.chunkSize.y)
        y2: int = int((aabb.bottom - self.__globalBound.top) / self.chunkSize.y)
        
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                ind: int = self.__chunks[y][x].find(index)
                if ind == -1:
                    continue
                self.__chunks[y][x].remove(ind)
            
    def __expandGrid(self, aabb: AABB) -> None:
        self.__expandChunkVertical(aabb)
        self.__expandChunkHorizontal(aabb)
    
    def __expandChunkVertical(self, aabb: AABB) -> None:
        class ExpandDirection(Enum):
            Up = auto(),
            Down = auto(),
            Left = auto(),
            Right = auto(),
            UpDown = auto(),
            LeftRight = auto(),
            NoExpansion = auto()
            
        oldBound: AABB = copy.copy(self.__globalBound)
        vertical: ExpandDirection = ExpandDirection.NoExpansion
        
        if aabb.top <= self.__globalBound.top:
            vertical = ExpandDirection.Up
        if aabb.bottom >= self.__globalBound.bottom:
            vertical = ExpandDirection.Down if vertical == ExpandDirection.NoExpansion else ExpandDirection.UpDown
        
        if vertical == ExpandDirection.Up or vertical == ExpandDirection.UpDown:
            factor: int = math.floor((aabb.top - self.__globalBound.top) / self.chunkSize.y) + 1
            self.__globalBound.top = self.__globalBound.top - self.chunkSize.y * factor
            
        if vertical == ExpandDirection.Down or vertical == ExpandDirection.UpDown:
            factor: int = math.floor((aabb.bottom - self.__globalBound.bottom) / self.chunkSize.y) + 1
            self.__globalBound.bottom = self.__globalBound.bottom + self.chunkSize.y * factor
        
        if self.__globalBound != oldBound:
            newWidth: float = self.__globalBound.width / self.chunkSize.x
            newHeight: float = self.__globalBound.height / self.chunkSize.y
            for i in range(int(newHeight) - len(self.__chunks)):
                self.__chunks.append(list())
            for y in range(len(self.__chunks)):
                for i in range(int(newWidth) - len(self.__chunks[y])):
                    self.__chunks[y].append(FreeList())
                    
            delta: int = int((oldBound.top - self.__globalBound.top) / self.chunkSize.y)
            for y in range(int(oldBound.height / self.chunkSize.y - 1), -1, -1):
                self.__chunks[y + delta], self.__chunks[y] = self.__chunks[y], self.__chunks[y + delta]
        
    def __expandChunkHorizontal(self, aabb: AABB) -> None:
        class ExpandDirection(Enum):
            Up = auto(),
            Down = auto(),
            Left = auto(),
            Right = auto(),
            UpDown = auto(),
            LeftRight = auto(),
            NoExpansion = auto()
            
        oldBound: AABB = copy.copy(self.__globalBound)
        horizontal: ExpandDirection = ExpandDirection.NoExpansion
        
        if aabb.left <= self.__globalBound.left:
            horizontal = ExpandDirection.Left
        if aabb.right >= self.__globalBound.right:
            horizontal = ExpandDirection.Right if horizontal == ExpandDirection.NoExpansion else ExpandDirection.LeftRight
        
        if horizontal == ExpandDirection.Left or horizontal == ExpandDirection.LeftRight:
            factor: int = math.floor((aabb.left - self.__globalBound.left) / self.chunkSize.x) + 1
            self.__globalBound.left = self.__globalBound.left - self.chunkSize.x * factor
            
        if horizontal == ExpandDirection.Right or horizontal == ExpandDirection.LeftRight:
            factor: int = math.floor((aabb.right - self.__globalBound.right) / self.chunkSize.x) + 1
            self.__globalBound.right = self.__globalBound.right + self.chunkSize.y * factor
        
        if self.__globalBound != oldBound:
            newWidth: float = self.__globalBound.width / self.chunkSize.x
            newHeight: float = self.__globalBound.height / self.chunkSize.y
            for i in range(int(newHeight) - len(self.__chunks)):
                self.__chunks.append(list())
            for y in range(len(self.__chunks)):
                for i in range(int(newWidth) - len(self.__chunks[y])):
                    self.__chunks[y].append(FreeList())
                    
            delta: int = int((oldBound.left - self.__globalBound.left) / self.chunkSize.y)
            for y in range(len(self.__chunks)):
                for x in range(int(oldBound.height / self.chunkSize.y - 1), -1, -1):
                    self.__chunks[y][x + delta], self.__chunks[y][x] = self.__chunks[y][x], self.__chunks[y][x + delta]