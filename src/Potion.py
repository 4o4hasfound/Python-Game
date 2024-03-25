import pygame
import random
from math import sqrt
from src.Player import Player
from src.Animation import Animation
from src.settings import *
from src.sound import *

class Potion(pygame.sprite.Sprite):
    def __init__(self,pos):
        self.ani = Animation(r"Tool image/Potion.png",(0, 0, 32, 32),4, 1, -1,True,10)
        self.ani.iter()
        self.image = self.ani.next(0)
        self.rect = self.image.get_rect(topleft=pos)

        self.sound = sound(r"Music/Mario Power Up Sound Effect.wav",0.5)
        self.reach = 30
        self.healing_point = random.randint(200,500)
        # self.pos = (1231,1) #我要知道在哪Chunk 然後那個Chunk的Pos 還有走道是值得還是衡的 才能隨機生成
        self.used = False

    def update(self,player):
        self.image = self.ani.next(0)
        if self.touched(player):
            player.hp += self.healing_point
            self.sound.Go_off()
            self.used = True # To remove the used potion

    def touched (self,player):
        if ( sqrt( (self.rect.centerx - player.rect.centerx)**2 +
                 (self.rect.centery - player.rect.centery)**2) < self.reach ):
            return True
        return False

class PotionManager:
    def __init__(self):
        self.potions = []
        

    def generate_potion(self, count, map, width, height, pos,
                      player, dir):  # pos 是map的左上角那個點
        count = random.randint(1,2)
        width -= 1
        height -= 1
        self.potions.clear()

        for i in range(count):
            overLap = True  # 觀看重疊的情形
            while overLap:
                if (dir[0] == 0):
                    x = random.randint(pos[0] + (7 * 32), pos[0] + width - (8 * 32))
                    y = random.randint(pos[1], pos[1] + height)
                else:
                    x = random.randint(pos[0] , pos[0] + width)
                    y = random.randint(pos[1] + (7 * 32) , pos[1] + height - (8 * 32))
                overLap = False  # 觀看重疊的情形
                rect = pygame.Rect(x, y, 32, 32)
                for obj in map.objectLayer:
                    if rect.colliderect(pygame.Rect(obj[0], obj[1], 32, 32)):
                        overLap = True
                        break
                for potion in self.potions:
                    if rect.colliderect(potion.rect):
                        overLap = True
                        break
                if not overLap:
                    if pygame.Rect(x, y, 32, 32).colliderect(player.rect):
                        overLap = True
                        break
            self.potions.append(Potion([x, y]))

    def update(self, player, obstacles):
        if True: #I don't understand :(
            minx, miny = 0, 0
            for obj in obstacles:
                if minx == 0:
                    minx = obj[0]
                else:
                    minx = min(minx, obj[0])
                if miny == 0:
                    miny = obj[1]
                else:
                    miny = min(miny, obj[1])
            for ind, obj in enumerate(obstacles):
                if (not (obj[0] == minx and miny <= obj[1] <= 29 * 32 + miny)
                        or not (obj[1] == miny
                                and minx <= obj[0] <= 29 * 32 + minx)
                        or not (obj[0] == minx + 29 * 32
                                and miny <= obj[1] <= 29 * 32 + miny)
                        or not (obj[1] == miny + 29 * 32
                                and minx <= obj[0] <= 29 * 32 + minx)):
                    obstacles.pop(ind)

        for potion in self.potions:
            potion.update(player)
            if (potion.used):
                self.potions.remove(potion)
