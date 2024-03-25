from turtle import speed
import pygame
import sys
from math import *
import random
from src.Player import Player
from src.Animation import *
from src.sound import *
from src.words import *
from src.settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.Ani = Animation(r"Boss image/Boss_ani.png", (0, 0, 64, 64),
                                   4, 1, -1, True, 10)
        self.Ani.iter()

        self.hurted_ani = Animation(r"Boss image/Boss hurted.png", (0, 0, 64, 64),1 ,0.85, -1, False, 10)
        self.hurt_sound = sound(r"Music/Minecraft Steve Hurt.wav", 0.5)
        self.is_hurted=False
        
        self.died_ani = Animation(r"Boss image/Boss_died.png", (0, 0, 64, 64),
                                  5, 1, -1, False, 20)
        self.died_ani.iter()
        self.die = 0
        self.died_pos = (0, 0)

        self.atk_sound = sound(r"Music/Hit by pan.wav", 0.5)
        self.attack = random.randrange(50, 150)  # 攻擊力 (蝦
        self.attackspeed = random.randrange(1, 600)
        self.attack_ani = Animation(r"Boss image/Boss attack.png",
                                    (0, 0, 64, 64), 4, 1, -1, False, 5)
        self.attack_ani.iter()
        self.attack_or_not = 0
        self.atk_cooldown = 300
        # self.cooldown = 60//(self.attackspeed)
        self.cooldown = 120
        self.reach = 50

        self.where_to_face = 1
        self.image = self.Ani.next(self.where_to_face)
        
       
        self.rect = self.image.get_rect(topleft=pos)
        self.rect = self.rect.inflate(0, -10)
        self.health = random.randrange(100, 500)  # 生命數值
        self.health_display = words(
            str(self.health), 20, (205, 0, 0),
            (self.rect.centerx, self.rect.centery - 50))
        self.speed_times = random.randrange(1, 3)  # 速度等級
        self.direction = pygame.math.Vector2()
        self.lastTouchPlayer = 0
        # self.ouch = 10
        # self.ani = Animation(r"Boss appearing animation.png", (0, 0, 32, 32), 7, 1, None, True, 6)
        # self.ani.iter()

    def update(self, player, obstacles):
        self.atk_cooldown += 1
        self.choose_image()
       
        if self.lastTouchPlayer:
            self.lastTouchPlayer -= 1
        if ((player.rect.x - self.rect.x)**2 +
            (player.rect.y - self.rect.y)**2)**0.5 < self.reach:
            self.attacking(player)

        see = self.seePlayer(player, obstacles)
        if (see):
            self.move(player, obstacles)


    def attacking(self, player):
        if self.atk_cooldown > self.cooldown:  # 休息時間小於冷卻時間
            # 圖片改變 攻擊
            self.atk_cooldown = 0
            self.attack_or_not = 1
            self.atk_sound.Go_off()
            player.hp = player.hp - self.attack
            if player.hp <= 0:
                player.died_pos = player.rect.topleft
            player.is_hurted=True
            player.hurt_sound.Go_off()

    def choose_image(self):
        if self.is_hurted:
            self.image=self.hurted_ani.next(self.where_to_face)
            if self.hurted_ani.now_picture_index==self.hurted_ani.count:
                self.is_hurted=False
                self.hurted_ani.iter()

        elif self.attack_or_not:
            self.image = self.attack_ani.next(self.where_to_face)
            if self.attack_ani.now_picture_index==self.attack_ani.count:
                self.attack_or_not=False
                self.atk_cooldown = 0
                self.attack_ani.iter()

        else:
            self.image=self.Ani.next(self.where_to_face)

    def move(self, player, obstacles):
        if self.rect.centerx - player.rect.centerx > 0 and self.rect.centerx - player.rect.centerx > self.speed_times + 1:
            self.direction.x = -1
            self.where_to_face = -1
        elif self.rect.centerx - player.rect.centerx < 0 and player.rect.centerx - self.rect.centerx > self.speed_times + 1:
            self.direction.x = 1
            self.where_to_face = 1
        else:
            self.direction.x = 0

        if self.rect.centery - player.rect.centery > 0 and self.rect.centery - player.rect.centery > self.speed_times + 1:
            self.direction.y = -1
        elif self.rect.centery - player.rect.centery < 0 and player.rect.centery - self.rect.centery > self.speed_times + 1:
            self.direction.y = 1
        else:
            self.direction.y = 0
        self.rect = self.rect.move(
            self.direction.x * self.speed_times,
            self.direction.y * self.speed_times
        )
        '''Huzuni's
        # self.direction = pygame.math.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        # if self.direction.magnitude() != 0:
        #     # Eat dinner
        #     l = sqrt(pow(self.direction.x, 2) + pow(self.direction.y, 2))
        #     # self.direction /= l
        #     # self.direction = self.direction.normalize()
            
        #     #l = sqrt(pow(self.direction.x,2)+pow(self.direction.y, 2))
        #     if self.lastTouchPlayer:
        #         return
        #     if l <= 1:
        #         self.rect.center = player.rect.center
        #         self.lastTouchPlayer = 10
        #     else:
        #         self.rect.centerx += self.direction.x / l * self.speed_times
        #         self.collision_horizontal(obstacles)
        #         self.rect.centery += self.direction.y / l * self.speed_times
        #         self.collision_vertical(obstacles)
        Huzuni's'''
        self.collision(obstacles)
        self.health_display = words(
            str(self.health), 20, (205, 0, 0),
            (self.rect.centerx, self.rect.centery - 50))


    def collision(self, obstacle):
        for sprite in obstacle:
            if self.rect.colliderect(pygame.Rect(sprite[0], sprite[1], 32,
                                                   32)):
                deltax1 = self.rect.right - sprite[0] # self -- intersect -- wall
                deltax2 = sprite[0] - self.rect.left + 32 # wall -- intersect -- self
                deltay1 = self.rect.bottom - sprite[1]
                deltay2 = sprite[1] - self.rect.top + 32

                if min(deltay1, deltay2) < min(deltax1, deltax2) and deltay2 <= deltay1:
                    self.rect.top = sprite[1] + 32
                elif min(deltay1, deltay2) < min(deltax1, deltax2) and deltay2 > deltay1:
                    self.rect.bottom = sprite[1] 

                if min(deltax1, deltax2) < min(deltay1, deltay2) and deltax2 <= deltax1:
                    self.rect.left = sprite[0] + 32
                elif min(deltax1, deltax2) < min(deltay1, deltay2) and deltax2 > deltax1:
                    self.rect.right = sprite[0]

    def collision_vertical(self, obstacle):
        for sprite in obstacle:
            if self.rect.colliderect(pygame.Rect(sprite[0], sprite[1], 32,
                                                 32)):
                if self.direction.y < 0:
                    self.rect.top = sprite[1] + 32
                elif self.direction.y > 0:
                    self.rect.bottom = sprite[1] 

    def collision_horizontal(self, obstacle):
        for sprite in obstacle:
            if self.rect.colliderect(pygame.Rect(sprite[0], sprite[1], 32,
                                                 32)):
                if self.direction.x < 0:
                    self.rect.left = sprite[0] + 32
                elif self.direction.x > 0:
                    self.rect.right = sprite[0]

    

    def ccw(self, Ax, Ay, Bx, By, Cx, Cy):
        return (Cy - Ay) * (Bx - Ax) > (By - Ay) * (Cx - Ax)

# Return true if line segments AB and CD intersect

    def intersect(self, Ax, Ay, Bx, By, Cx, Cy, Dx, Dy):
        return self.ccw(Ax, Ay, Cx, Cy, Dx, Dy) != self.ccw(
            Bx, By, Cx, Cy, Dx, Dy) and self.ccw(
                Ax, Ay, Bx, By, Cx, Cy) != self.ccw(Ax, Ay, Bx, By, Dx, Dy)

    def seePlayer(self, player, obstacles) -> bool:
        for obj in obstacles:
            if (self.intersect(player.rect.centerx, player.rect.centery,
                               self.rect.centerx, self.rect.centery, obj[0],
                               obj[1], obj[0] + 32, obj[1])
                    or self.intersect(
                        player.rect.centerx, player.rect.centery,
                        self.rect.centerx, self.rect.centery, obj[0] + 32,
                        obj[1], obj[0] + 32, obj[1] + 32) or self.intersect(
                            player.rect.centerx, player.rect.centery,
                            self.rect.centerx, self.rect.centery, obj[0] + 32,
                            obj[1] + 32, obj[0], obj[1] + 32)
                    or self.intersect(player.rect.centerx, player.rect.centery,
                                      self.rect.centerx, self.rect.centery,
                                      obj[0], obj[1] + 32, obj[0], obj[1])):
                return False
        return True


class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.appearing_ani = Animation(r"Boss image/Boss appearing animation.png",
                             (0, 0, 32, 32), 7, 1, (0, 0, 0), True, 10)
        self.appearing_ani.iter()
        # self.image = pygame.image.load("Boss.png").convert_alpha()
        # self.image = pygame.transform.scale(
        #     self.image, (64,64 / self.image.get_width() * self.image.get_height()))
        # self.image_damaged = pygame.image.load("Boss_damaged.png").convert_alpha()
        # self.image_damaged = pygame.transform.scale(
        #     self.image_damaged, (64,64 / self.image.get_width() * self.image.get_height()))

    def generateEnemy(self, count, map, width, height, pos,
                      player):  # pos 是map的左上角那個點
        width -= 1
        height -= 1
        self.enemies.clear()
        for i in range(count):
            overLap = True  # 觀看重疊的情形
            while overLap:
                x = random.randint(pos[0], pos[0] + width)
                y = random.randint(pos[1], pos[1] + height)
                overLap = False  # 觀看重疊的情形
                rect = pygame.Rect(x, y, 32, 32)
                for obj in map.objectLayer:
                    # if x == obj[0] and y == obj[1]:
                    #   overLap = True
                    #   break
                    if rect.colliderect(pygame.Rect(obj[0], obj[1], 32, 32)):
                        overLap = True
                        break
                for enemy in self.enemies:
                    if rect.colliderect(enemy.rect):
                        overLap = True
                        break
                if not overLap:
                    if pygame.Rect(x, y, 32, 32).colliderect(player.rect):
                        overLap = True
                        break
            self.enemies.append(Enemy([x, y]))

    def update(self, player, obstacles):
        if self.appearing_ani.times == 3:
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

            for enemy in self.enemies:
                if enemy.health > 0:
                    enemy.update(player, obstacles)
                elif enemy.health <= 0:
                    enemy.health_display = words(
                        "0", 20, (205, 0, 0),
                        (enemy.rect.centerx, enemy.rect.centery - 50))
                    enemy.die = 1
                    enemy.died_pos = enemy.rect.topleft
