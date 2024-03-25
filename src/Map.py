import pygame
import pytmx
from src.Player import Player
from src.settings import *
import math
import os
from src.Tile import Wall
import random

from typing import Dict, List, Any

ROOM = 1
PATH = 2
WALL = 0


class Map:
    def __init__(self, obstacle, width, height):
        self.width = width
        self.height = height

        self.chunks: List[List[ChunkMap]] = [[None for x in range(width)] for y in range(height)]
        self.chunkTypes = [[None for x in range(width)] for y in range(height)]
        self.closed_chunk = [[[None for k in range(4)] for i in range(width)] for y in range(height)]
        self.baseMaps: Dict[str, MapObject] = {}
        

        self.room_type_chooser = random.randint(1, 3)

        if True:
            self.baseMaps["Room1"] = MapObject(r"Maps/Sillydog's map/First.tmx")
            self.baseMaps["Room2"] = MapObject(r"Maps/Sillydog's map/Second.tmx")
            self.baseMaps["Room3"] = MapObject(r"Maps/the room of maps/YAY.tmx")

            self.baseMaps["Path1"] = MapObject(r"Maps/Sillydog's map/path2.tmx")
            self.baseMaps["Path1-90"] = MapObject(r"Maps/Sillydog's map/path2_90.tmx")
            
            self.baseMaps["WallTop"] = MapObject(r"Maps/WallTop.tmx") # opened , 1 means closed
            self.baseMaps["WallDown"] = MapObject(r"Maps/WallDown.tmx")
            self.baseMaps["WallLeft"] = MapObject(r"Maps/WallLeft.tmx")
            self.baseMaps["WallRight"] = MapObject(r"Maps/WallRight.tmx")
            self.baseMaps["WallTop1"] = MapObject(r"Maps/WallTop1.tmx")
            self.baseMaps["WallDown1"] = MapObject(r"Maps/WallDown1.tmx")
            self.baseMaps["WallLeft1"] = MapObject(r"Maps/WallLeft1.tmx")
            self.baseMaps["WallRight1"] = MapObject(r"Maps/WallRight1.tmx")

        self.createMap(0, 0, ROOM, [0, 0])
        self.generateMap()
        self.checkMap(5)

    def blit(self, surface, player):
        additionalObstacle = {}
        offset = pygame.math.Vector2(player.rect.centerx - SCREEN_WIDTH / 2,
                                     player.rect.centery - SCREEN_HEIGHT / 2)
        playerxChunk = math.ceil(player.rect.topleft[0] / CHUNK_WIDTH)
        playeryChunk = math.ceil(player.rect.topleft[1] / CHUNK_HEIGHT)
        #print(playerxChunk, playeryChunk)
        for x in range(playerxChunk - SHOW_CHUNK_N - 1,
                       playerxChunk + SHOW_CHUNK_N, 1):
            if x >= len(self.chunks) or x < 0:
                continue
            for y in range(playeryChunk - SHOW_CHUNK_N - 1,
                           playeryChunk + SHOW_CHUNK_N, 1):
                if y >= len(self.chunks[x]) or y < 0:
                    continue
                chunk = self.chunks[x][y]
                if chunk:
                    for tile in chunk.tileLayer:
                        if tile[2]:
                            surface.blit(tile[2], (tile[0] - offset.x, tile[1] - offset.y))
                    for obj in chunk.objectLayer:
                        additionalObstacle[(obj[0], obj[1])] = obj[2]
        return additionalObstacle

    def choose_room_type_randomly(self,x,y,add):
        if self.room_type_chooser == 1:
            self.chunks[x][y] = self.baseMaps["Room1"].getMap(
                [x * CHUNK_WIDTH, y * CHUNK_HEIGHT], add)
        elif self.room_type_chooser == 2:
            self.chunks[x][y] = self.baseMaps["Room2"].getMap(
                [x * CHUNK_WIDTH, y * CHUNK_HEIGHT], add)
        elif self.room_type_chooser == 3:
            self.chunks[x][y] = self.baseMaps["Room3"].getMap(
                [x *CHUNK_WIDTH, y * CHUNK_HEIGHT], add)

    def createMap(self, x, y, Type, dir):
        if self.chunkTypes[x][y]:
            if Type == ROOM:
                if dir == [1, 0]:
                    self.chunkTypes[x][y].left = 1
                if dir == [-1, 0]:
                    self.chunkTypes[x][y].right = 1
                if dir == [0, 1]:
                    self.chunkTypes[x][y].top = 1
                if dir == [0, -1]:
                    self.chunkTypes[x][y].down = 1
            return
        # self.chunks[x][y] = self.baseMaps[("Room1" if Type == ROOM else "Path1")].getMap([
        #     x * self.CHUNK_WIDTH, y * self.CHUNK_HEIGHT], (0 if dir[0] else 90))
        if Type == PATH:
            self.chunkTypes[x][y] = PathInf((x, y), dir)
            if dir == [1, 0]:
                if x + 1 < self.width:
                    self.createMap(x + 1, y, ROOM, [1, 0])
                else:
                    self.chunkTypes[x][y] = None
                    self.chunkTypes[x - 1][y].right = 0
            if dir == [-1, 0]:
                if x - 1 >= 0:
                    self.createMap(x - 1, y, ROOM, [-1, 0])
                else:
                    self.chunkTypes[x][y] = None
                    self.chunkTypes[x + 1][y].left = 0
            if dir == [0, 1]:
                if y + 1 < self.height:
                    self.createMap(x, y + 1, ROOM, [0, 1])
                else:
                    self.chunkTypes[x][y] = None
                    self.chunkTypes[x][y - 1].top = 0
            if dir == [0, -1]:
                if y - 1 >= 0:
                    self.createMap(x, y - 1, ROOM, [0, -1])
                else:
                    self.chunkTypes[x][y] = None
                    self.chunkTypes[x][y + 1].down = 0
        else:
            rand = [0, 1, 1]
            right = random.choice(rand) if dir[0] != -1 else 1
            left = random.choice(rand) if dir[0] != 1 else 1
            top = random.choice(rand) if dir[1] != 1 else 1
            down = random.choice(rand) if dir[1] != -1 else 1
            if not right and not left and not top and not down:
                i = random.randint(1, 4)
                if i == 1:
                    right = 1
                elif i == 2:
                    left = 1
                elif i == 3:
                    top = 1
                else:
                    down = 1
            if right and x + 1 >= self.width:
                right = 0
            if left and x - 1 < 0:
                left = 0
            if top and y - 1 < 0:
                top = 0
            if down and y + 1 >= self.height:
                down = 0

            self.chunkTypes[x][y] = RoomInf((x, y), (top, down, right, left))

            if right and x + 1 < self.width:
                self.createMap(x + 1, y, PATH, [1, 0])
            if left and x - 1 >= 0:
                self.createMap(x - 1, y, PATH, [-1, 0])
            if top and y - 1 >= 0:
                self.createMap(x, y - 1, PATH, [0, -1])
            if down and y + 1 < self.height:
                self.createMap(x, y + 1, PATH, [0, 1])

    def checkMap(self, min):
        rooms = 0
        for x in range(len(self.chunkTypes)):
            for y in range(len(self.chunkTypes[x])):
                if self.chunkTypes[x][y]:
                    rooms += 1
        # if rooms < min:
        #     self.createMap(0, 0, ROOM, [0, 0])
        #     self.checkMap(min)

    def generateMap(self):
        if True:
            tileWidth = self.baseMaps["Room1"].tileWidth
            tileHeight = self.baseMaps["Room1"].tileHeight
            width = self.baseMaps["Room1"].width
            height = self.baseMaps["Room1"].height
        
        chunkWidthN = len(self.chunks)
        chunkHeightN = len(self.chunks[0])
        for x in range(len(self.chunkTypes)):
            for y in range(len(self.chunkTypes[x])):
                
                if isinstance(self.chunkTypes[x][y], RoomInf):
                    add = []
                    coordX = x * CHUNK_WIDTH
                    coordY = y * CHUNK_HEIGHT

                    if True: #Top
                        closed_wall = self.baseMaps["WallTop1"].getMap([
                            coordX + 6 * tileWidth, coordY
                        ])
                        opened_wall = self.baseMaps["WallTop"].getMap([
                            coordX + 6 * tileWidth, coordY
                        ])

                        if self.chunkTypes[x][y].top:
                            if y - 1 < 0 or (y - 1 >= 0 and not self.chunkTypes[x][y - 1]):
                                self.chunkTypes[x][y].top = 0
                                add.append(closed_wall)
                            else:
                                add.append(opened_wall)
                            self.closed_chunk[x][y][0] = closed_wall
                            
                        else:
                            if y - 1 >= 0 and self.chunkTypes[x][y - 1]:
                                self.chunkTypes[x][y].top = 1
                                add.append(opened_wall)
                            else:
                                add.append(closed_wall)
                            self.closed_chunk[x][y][0] = closed_wall

                    if True: #Down
                        closed_wall = self.baseMaps["WallDown1"].getMap([
                            coordX + 6 * tileWidth, coordY + height - tileHeight
                        ])
                        opened_wall = self.baseMaps["WallDown"].getMap([
                            coordX + 6 * tileWidth, coordY + height - tileHeight
                        ])

                        if self.chunkTypes[x][y].down:
                            if y + 1 >= chunkHeightN or (
                                    y + 1 < chunkHeightN
                                    and not self.chunkTypes[x][y + 1]):
                                self.chunkTypes[x][y].down = 0
                                add.append(closed_wall)
                            else:
                                add.append(opened_wall)
                            self.closed_chunk[x][y][1] = closed_wall
                        else:
                            if y + 1 < chunkHeightN and self.chunkTypes[x][y + 1]:
                                self.chunkTypes[x][y].down = 1
                                add.append(opened_wall)
                            else:
                                add.append(closed_wall)
                            self.closed_chunk[x][y][1] = closed_wall

                    if True: #Left
                        closed_wall = self.baseMaps["WallLeft1"].getMap([
                            coordX , coordY + 6 * tileHeight
                        ])
                        opened_wall = self.baseMaps["WallLeft"].getMap([
                            coordX , coordY + 6 * tileHeight
                        ])

                        if self.chunkTypes[x][y].left:
                            if x - 1 < 0 or (x - 1 >= 0
                                            and not self.chunkTypes[x - 1][y]):
                                self.chunkTypes[x][y].left = 0
                                add.append(closed_wall)
                            else:
                                add.append(opened_wall)
                            self.closed_chunk[x][y][2] = closed_wall
                        else:
                            if x - 1 >= 0 and self.chunkTypes[x - 1][y]:
                                self.chunkTypes[x][y].left = 0
                                add.append(opened_wall)
                            else:
                                add.append(closed_wall)
                            self.closed_chunk[x][y][2] = closed_wall

                    if True: #Right
                        closed_wall = self.baseMaps["WallRight1"].getMap([
                            coordX + width - tileWidth, coordY + 6 * tileHeight
                        ])
                        opened_wall = self.baseMaps["WallRight"].getMap([
                            coordX + width - tileWidth , coordY + 6 * tileHeight
                        ])

                        if self.chunkTypes[x][y].right:
                            if x + 1 >= chunkWidthN or (
                                    x + 1 < chunkWidthN
                                    and not self.chunkTypes[x + 1][y]):
                                self.chunkTypes[x][y].right = 0
                                add.append(closed_wall)
                            else:
                                add.append(opened_wall)
                            self.closed_chunk[x][y][3] = closed_wall

                        else:
                            if x + 1 < chunkWidthN and self.chunkTypes[x + 1][y]:
                                self.chunkTypes[x][y].right = 1
                                add.append(opened_wall)
                            else:
                                add.append(closed_wall)
                            self.closed_chunk[x][y][3] = closed_wall

                    self.room_type_chooser = random.randint(1, 3)
                    self.choose_room_type_randomly(x,y,add)

    
                elif isinstance(self.chunkTypes[x][y], PathInf):
                    self.chunks[x][y] = self.baseMaps[
                        ("Path1" if self.chunkTypes[x][y].dir[0] else "Path1-90")
                        ].getMap([x * CHUNK_WIDTH, y * CHUNK_HEIGHT])


class ChunkMap:
    def __init__(self, tileLayer, objectLayer, obstacles):
        self.tileLayer = tileLayer
        self.objectLayer = objectLayer
        self.obstacles = obstacles


class MapObject:
    def __init__(self, filename):
        self.tileLayer = [] # x,y,gid
        self.objectLayer = []
        self.obstacles = []
        #(x, y, image)

        map = pytmx.load_pygame(filename)
        self.tileWidth = map.tilewidth
        self.tileHeight = map.tileheight
        self.width = (map.width) * self.tileWidth
        self.height = (map.height) * self.tileHeight
        # self.width = (map.width - 1) * self.tileWidth
        # self.height = (map.height - 1) * self.tileHeight
        
        for layer in map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    self.tileLayer.append(
                        (x * map.tilewidth, y * map.tileheight,
                         map.get_tile_image_by_gid(gid)))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    self.objectLayer.append((obj.x, obj.y, obj.image))
                    self.obstacles.append((obj.x, obj.y, obj.image))

    def getMap(self, pos, add=None): #回傳tilelayer[] objectlayer[] obstacles[]
        toReturn = ChunkMap(
            [[tile[0] + pos[0], tile[1] + pos[1], tile[2]] for tile in self.tileLayer],
            [[object[0] + pos[0], object[1] + pos[1], object[2]] for object in self.objectLayer], 
            [Wall((obj[0] + pos[0], obj[1] + pos[1]), [], 0, obj[2]) for obj in self.obstacles]
            )
        if not add:
            return toReturn
        else:
            for element in add:
                toReturn.tileLayer.extend(element.tileLayer)
                toReturn.objectLayer.extend(element.objectLayer)
                toReturn.obstacles.extend(element.obstacles)
            return toReturn


class RoomInf:
    def __init__(self, pos, doors):
        self.pos = pos
        self.top, self.down, self.right, self.left = doors

    def __str__(self): 
        print(self.pos, (self.top, self.down, self.right, self.left), end="")

class PathInf:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir

    def __str__(self):
        print(self.pos, self.dir, end="")
