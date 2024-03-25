import pygame
from math import sqrt
import random
from src.Player import *
from src.Animation import Animation
from src.sound import sound
from src.words import words

class Atk_thing:
    def __init__(self,pos, atk_type, where_to_face, direction = pygame.math.Vector2(1,0), low_power =0, high_power = 100 , reach =50, enemy = None):
        self.where_to_face = where_to_face
        self.direction = pygame.math.Vector2()
        self.direction = direction
        self.atk_type=atk_type
        self.display=False
        self.reach = reach
        self.low_power = low_power
        self.high_power = high_power
        self.atk_num = random.randint(self.low_power,self.high_power)
        self.exist = True
        self.touch_enemies = []
        for i in range(len(enemy.enemies)):
            self.touch_enemies.append(0)

        if self.atk_type=="explosion":
            self.atk_thing_ani=Animation(r"Character image/Somebody/somebody_atk_thing.png",
                                 (0,0,32,32), 5, 3, -1, False, 10)
            self.atk_thing_pos = pos
            self.image=self.atk_thing_ani.next(where_to_face)
            self.rect = self.image.get_rect(center=self.atk_thing_pos)
            # self.rect = pygame.Rect(0,0,32,32)
            # self.rect.center = pos
            # print(self.atk_thing_pos)
            # print(type(self.rect))
            self.atk_sound = sound(r"Music/Crash.wav",0.3)


        elif self.atk_type=="shooting":
            self.atk_thing_ani=Animation(r"Character image/Blueduck/Blueduck atk thing.png",
                                         (0,0,32,32), 5,1,-1,True,10)
            self.atk_thing_pos = pos
            self.image=self.atk_thing_ani.next(where_to_face)
            self.rect = self.image.get_rect(center=self.atk_thing_pos)
            # print(self.rect)
            self.atk_sound = sound(r"Music/Crash.wav",0.3)

    def update(self,enemies,obstacles):
        if self.atk_type == "explosion":
            pass
            # self.rect.width += 2
            # self.rect.height += 2
            # self.rect.topleft = self.atk_thing_pos

        if self.atk_type=="shooting":
            #  if self.direction.magnitude() != 0:
            #     self.direction.normalize()
            #     # self.rect.x += self.direction.x * 10
            #     self.rect.centerx += self.direction.x 
            #     self.rect.centery += self.direction.y 
            self.rect.centerx +=  self.where_to_face * 2
        
        self.attack(enemies)
        self.check_for_vanishing(obstacles)
        if self.exist:
            self.image = self.atk_thing_ani.next(self.where_to_face)
    
    def attack(self,enemies):
        i=0
        for enemy in enemies.enemies:
            if (not self.touch_enemies[i]) and (sqrt((enemy.rect.centerx - self.rect.centerx)**2 +
                      (enemy.rect.centery - self.rect.centery)**2) <= self.reach ):
                self.touch_enemies[i] = 1
                self.atk_num = random.randint(self.low_power, self.high_power)
                enemy.health -= self.atk_num
                enemy.hurt_sound.Go_off()
                enemy.is_hurted = True
            i+=1
        # for enemy in enemies.enemies:
        #     if self.rect.colliderect(enemy.hitbox):
        #         enemy.health -= self.atk_num
        #         enemy.hurt_sound.Go_off()
        #         enemy.is_hurted = True

    def check_for_vanishing(self,obstacles):
        if self.atk_type == "explosion":
            if self.atk_thing_ani.now_picture_index == self.atk_thing_ani.count:
                self.exist = False
        elif self.atk_type == "shooting":
            for obj in obstacles:
                if self.rect.colliderect(obj.hitbox):
                    self.exist = False
        
                


    # def start_attacking(self,direction,pos):
    #     self.atk_thing_ani.iter()
    #     self.direction.x = 1 if direction == 1 else -1
    #     self.rect = self.image.get_rect(center=pos)

    


class ATK_thing_manager:
    def __init__(self):
        self.things = []
        self.atk_sound = sound(r"Music/Crash.wav",0.3)

    def generate_thing(self,pos,atk_type,where_to_face,direction,low_power,high_power,reach,enemy):
        self.things.append(Atk_thing(pos,atk_type,where_to_face,direction,low_power,high_power,reach,enemy))
        self.atk_sound.Go_off()

    def use_skill(self,skill,player,enemies):
        if skill == "All_kill":
            for enemy in enemies.enemies:
                enemy.health -= 500
                enemy.hurt_sound.Go_off()
                enemy.is_hurted = True
        elif skill == "Healthy":
            player.hp += 500


    def update(self,enemy,obstacles):
        for ATK_thing in self.things:
            ATK_thing.update(enemy,obstacles)
            if not ATK_thing.exist:
                self.things.remove(ATK_thing)


