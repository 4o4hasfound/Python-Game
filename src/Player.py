
from src.settings import *
import random
import pygame  # (⁎⁍̴̛ᴗ⁍̴̛⁎)
from math import *  # sqrt()
import pytmx
from src.Atk_things import ATK_thing_manager
from src.Atk_things import Atk_thing
from src.Animation import Animation
from src.sound import sound
from src.words import words


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,obstacle_sprites,
                 basic_dict,ani_dict): 
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites

        # 一般動畫
        self.Ani = Animation(ani_dict["ani"],
                             basic_dict["square"], ani_dict["ani_frames"], basic_dict["enlargement"], -1, True, 10) #Picture,frames,size,back_ground_color,loop,Change_frames_speed
        self.Ani.iter()
        self.image = self.Ani.next(0)
        self.rect = self.image.get_rect(topleft=pos)
        # print (self.rect)

        # 死亡動畫
        self.died_ani = Animation(ani_dict["died_ani"],
                                  basic_dict["square"], ani_dict["died_frames"], 6, -1, False, 20)
        self.died_pos = (0, 0)

        #勝利動畫
        self.win_ani = Animation(ani_dict["win_ani"],  
                                 basic_dict["square"], ani_dict["win_frames"], 6, -1, False, 20)
        self.win_pos = (0, 0)

        # 攻擊動畫
        self.atk_ani = Animation(ani_dict["atk_ani"],
                                 basic_dict["square"], ani_dict["atk_frames"], basic_dict["enlargement"], -1, False, 10)
        self.atk_cooldown = 0
        self.is_attacking=False
        # self.atk_ani.now_picture_index = 60
        
        # 受傷動畫
        self.hurt_ani=Animation(ani_dict["hurt_ani"],
                                basic_dict["square"], ani_dict["hurt_frames"], basic_dict["enlargement"],-1, False, 10)
        self.hurt_sound = sound(r"Music/Punch.wav", 0.5)
        self.is_hurted=False
        # self.hurted_time = 20

        # 閒置動畫
        self.idle_ani=Animation(ani_dict["idle_ani"],
                                basic_dict["square"], ani_dict["idle_frames"], basic_dict["enlargement"], -1, True, 10)
        self.is_idle = False
        # self.animation = 0 


        # 基本東西
        self.clock = pygame.time.Clock()
        self.clock.tick()

        # self.lastAnimation = pygame.time.get_ticks()
        self.skill = basic_dict["skill"]
        self.skill_effect = Animation(basic_dict["skill_image"],(0,0,800,600),6,1,-1,False,10)
        self.using_skill = False
        self.skill_cooldown_counter = 0
        self.skill_cooldown = basic_dict["skill_cooldown"] * 60#暫定
        self.skill_sound = sound(basic_dict["skill_sound"],0.3)

        self.direction = pygame.math.Vector2()
        self.where_to_face = 1
        self.atk_type = basic_dict["atk_type"]
        self.hp = basic_dict["health_point"]
        self.cooldown = basic_dict["cooldown"] * 60
        self.speed = basic_dict["speed"] # 腳色移動
        self.reach = basic_dict["reach"]  # 攻擊距離
        self.low_power = basic_dict["low_power"]  # 最低輸出
        self.high_power = basic_dict["high_power"]  # 最高輸出
        self.power = 0  # 攻擊力暫時為0

        self.hp_display = words(str(self.hp), 20, (205, 0, 0),
                                (self.rect.centerx, self.rect.centery + 50))
        self.atk_cooldown_display=words(str(self.atk_cooldown),35,RED,(50,50))   
        self.skill_cooldown_display=words(str(self.skill_cooldown),35,GREEN,(50,50))

        # 攻擊後的物體
        # self.atk_thing = Atk_thing((0,0),basic_dict["atk_type"],0,self.low_power,self.high_power,None)
        # self.atk_thing_appear_pos = ((0,0)) # self.atk_thing_appear_pos = self.image.get_rect(center=pos)
        self.atk_things = ATK_thing_manager()     
        '''
        # self.image_damagedR = pygame.image.load(
        #     self.hurt_ani).convert_alpha()
        # self.image_damagedR = pygame.transform.scale(
        #     self.image_damagedR, (30, 37 / self.image_damagedR.get_width() *
        #                           self.image_damagedR.get_height()))
        # self.image_damagedL = pygame.transform.flip(self.image_damagedR, 1, 0)
        '''
        

    def press(self, enemy):
        key = pygame.key.get_pressed()
        
        # x軸移動
        if key[pygame.K_a]:
            self.is_idle=False
            self.direction.x = -1
            self.where_to_face = -1
        elif key[pygame.K_d]:
            self.is_idle=False
            self.direction.x = 1
            self.where_to_face = 1
        else:
            self.direction.x = 0

        # y軸移動
        if key[pygame.K_w]:
            self.is_idle=False
            # idle = False
            self.direction.y = -1
        elif key[pygame.K_s]:
            self.is_idle=False
            # idle = False
            self.direction.y = 1
        else:
            self.direction.y = 0


        if key[pygame.K_SPACE]:
            if self.atk_cooldown == 0:  # 休息時間小於冷卻時間
                # self.atk_thing.atk_thing_ani.iter()
                # self.atk_thing.atk_sound.Go_off()
                self.attack(enemy)
                # self.atk_thing.atk_thing_pos= self.image.get_rect(bottomright=self.rect.topleft)
                # self.atk_num = words(self.power, 20, (0, 255, 0),
                #                      (self.atk_thing.atk_thing_pos.x + 1,
                #                       self.atk_thing.atk_thing_pos.y + 1))
        if key[pygame.K_f]:
            if self.skill_cooldown_counter == 0:
                self.skill_sound.Go_off()
                self.using_skill = True
                self.skill_cooldown_counter = self.skill_cooldown
                self.atk_things.use_skill(self.skill,self,enemy)
                self.skill_effect.iter()

    def move(self, obstacle):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
            self.rect.x += self.direction.x * self.speed
            # print(type(self.rect))
            self.collision_horizontal(obstacle)
            self.rect.y += self.direction.y * self.speed
            self.collision_vertical(obstacle)

    # 腳色攻擊

    def attack(self, enemy):
        self.is_attacking=True
        self.atk_cooldown = self.cooldown
        self.atk_things.generate_thing(self.rect.center,
                                       self.atk_type,self.where_to_face,self.direction,
                                       self.low_power,self.high_power,self.reach,enemy)
        # self.power = random.randint(self.low_power, self.high_power)
        self.atk_ani.iter()
        # self.atk_thing.start_attacking(self.direction,(self.rect.centerx,self.rect.centery))
        # self.atk_thing.rect=self.rect.topleft
        # if ((sqrt((enemy.rect.x-self.rect.x)**2+(enemy.rect.y-self.rect.y)**2)) <= self.reach):  # 敵人與腳色的距離小於一定的距離
        # for e in enemy.enemies:
        #     if ((sqrt((e.rect.centerx - self.rect.centerx)**2 +
        #               (e.rect.centery - self.rect.centery)**2)) <=
        #             self.reach):  # 敵人與腳色的距離小於一定的距離
        #         e.is_hurted = True
        #         e.health -= self.power  # 敵人扣血
        #         e.hurt_sound.Go_off()

    # 腳色碰撞

    def collision_vertical(self, obstacle):
        for sprite in obstacle:
            if self.rect.colliderect(sprite.hitbox):
                if self.direction.y < 0:
                    self.rect.top = sprite.hitbox.bottom
                elif self.direction.y > 0:
                    self.rect.bottom = sprite.hitbox.top

    def collision_horizontal(self, obstacle):
        for sprite in obstacle:
            if self.rect.colliderect(sprite.hitbox):
                if self.direction.x < 0:
                    self.rect.left = sprite.hitbox.right
                elif self.direction.x > 0:
                    self.rect.right = sprite.hitbox.left

    def collision(self, level):
        obstacles = []
        playerxChunk = ceil(self.rect.topleft[0] / level.CHUNK_WIDTH)
        playeryChunk = ceil(self.rect.topleft[1] / level.CHUNK_HEIGHT)
        for x in range(playerxChunk - 1, playerxChunk + 2, 1):
            if x >= len(level.chunks):
                break
            for y in range(playeryChunk - 1, playeryChunk + 2, 1):
                if y >= len(level.chunks[x]):
                    break
                obstacles += level.chunks[x][y].obstacles
        self.collision_horizontal(obstacles)
        self.collision_vertical(obstacles)

    # 選擇圖片
    def choose_image(self):
        if self.is_hurted:
            self.image=self.hurt_ani.next(self.where_to_face)
            if self.hurt_ani.now_picture_index==self.hurt_ani.count:
                self.is_hurted=False
                self.hurt_ani.iter()

        elif self.is_attacking:
            self.image=self.atk_ani.next(self.where_to_face)
            if self.atk_ani.now_picture_index==self.atk_ani.count:
                self.is_attacking=False
                self.atk_ani.iter()

        elif self.is_idle:
            self.image=self.idle_ani.next(self.where_to_face)
        
        else:
            self.image=self.Ani.next(self.where_to_face)

    def update(self, obstacles, enemy):
        self.is_idle=True
        self.press(enemy)
        
        # if (self.atk_thing.atk_thing_ani.now_picture_index < self.atk_thing.atk_thing_ani.count):
        #     self.atk_thing.update()
        # self.atk_thing.update()
        if self.using_skill:
            if self.skill_effect.now_picture_index == self.skill_effect.count:
                self.using_skill= False
        
        

        self.hp_display.word_update ((str(self.hp)))
        self.hp_display.pos_update((self.rect.centerx, self.rect.centery + 30))

        self.atk_cooldown = self.atk_cooldown -1 if self.atk_cooldown >= 1 else 0
        self.atk_cooldown_display.color = RED if self.atk_cooldown !=0 else GREEN
        self.atk_cooldown_display.word_update("atk_CD:" + str(self.atk_cooldown))
        # self.atk_cooldown_display.pos_update((self.rect.centerx, self.rect.centery + 60))
        
        self.skill_cooldown_counter = self.skill_cooldown_counter - 1 if self.skill_cooldown_counter >= 1 else 0
        self.skill_cooldown_display.color = RED if self.skill_cooldown_counter !=0 else GREEN
        self.skill_cooldown_display.word_update("skill_CD:" + str(self.skill_cooldown_counter))
        # self.skill_cooldown_display.pos_update((self.rect.centerx, self.rect.centery + 90))
        
        
        self.move(obstacles)
        self.atk_things.update(enemy,obstacles)
        self.choose_image()

        # print (self.rect)

class Cat(Player):
    def __init__(self,pos,groups,obstacles_sprites):
        self.ani_dictionary={} #xx_ani:picture xx_frames:動畫的張數
        if True:
            self.ani_dictionary["ani"]=r"Character image/Somebody/Somebody jump.png"
            self.ani_dictionary["ani_frames"]=6
            self.ani_dictionary["atk_ani"]=r"Character image/Somebody/Somebody atk.png"
            self.ani_dictionary["atk_frames"]=5
            self.ani_dictionary["hurt_ani"]=r"Character image/Somebody/Somebody hurt.png"
            self.ani_dictionary["hurt_frames"]=1
            self.ani_dictionary["died_ani"]=r"Character image/Somebody/Somebody died.png"
            self.ani_dictionary["died_frames"]=6
            self.ani_dictionary["idle_ani"]=r"Character image/Somebody/Somebody idle.png"
            self.ani_dictionary["idle_frames"]=2
            self.ani_dictionary["win_ani"]=r"Character image/Somebody/Somebody win.png"
            self.ani_dictionary["win_frames"]=8
            # self.atk_thing_ani=r"Character image/SomeBody/somebody_atk_thing.png"
        self.basic_status_dictionary={}
        if True:
            self.basic_status_dictionary["atk_type"] ="explosion"
            self.basic_status_dictionary["speed"]=5
            self.basic_status_dictionary["health_point"]=1200
            self.basic_status_dictionary["low_power"]=100
            self.basic_status_dictionary["high_power"]=250
            self.basic_status_dictionary["reach"]=48
            self.basic_status_dictionary["cooldown"]=2 #seconds
            self.basic_status_dictionary["square"]=(0, 0, 40, 50)
            self.basic_status_dictionary["enlargement"]=0.75
            self.basic_status_dictionary["skill"] = "Healthy"
            self.basic_status_dictionary["skill_image"] = r"Character image/Somebody/Somebody Skill.png"
            self.basic_status_dictionary["skill_cooldown"] = 5
            self.basic_status_dictionary["skill_sound"] = r"Music/Mario Power Up Sound Effect.wav"
            # self.basic_status_dictionary[]=

        super().__init__(pos,groups,obstacles_sprites,
                         self.basic_status_dictionary,
                         self.ani_dictionary)
        # self.idle_ani=Animation(r"Character image/Somebody/somebody_idle.png",(0,0,40,50),2,0.75,-1,True,10)

        
class Duck(Player):
    def __init__(self,pos,groups,obstacles_sprites):
        self.ani_dictionary={} #xx_ani:picture xx_frames:動畫的張數
        if True:
            self.ani_dictionary["ani"]=r"Character image/Blueduck/Blueduck walking.png"
            self.ani_dictionary["ani_frames"]=3
            self.ani_dictionary["atk_ani"]=r"Character image/Blueduck/Blueduck attacking.png"
            self.ani_dictionary["atk_frames"]=3
            self.ani_dictionary["hurt_ani"]=r"Character image/Blueduck/Blueduck hurt.png"
            self.ani_dictionary["hurt_frames"]=1
            self.ani_dictionary["died_ani"]=r"Character image/Blueduck/Blueduck dying.png"
            self.ani_dictionary["died_frames"]=6
            self.ani_dictionary["idle_ani"]=r"Character image/Blueduck/Blueduck Idle Ani.png"
            self.ani_dictionary["idle_frames"]=3
            self.ani_dictionary["win_ani"]=r"Character image/Blueduck/Blueduck win.png"
            self.ani_dictionary["win_frames"]=9
            # self.atk_thing_ani=r"Character image/Blueduck/Blueduck atk thing.png" #frames=5
        self.basic_status_dictionary={}
        if True:
            self.basic_status_dictionary["atk_type"] ="shooting"
            self.basic_status_dictionary["speed"]=8
            self.basic_status_dictionary["health_point"]=1250
            self.basic_status_dictionary["low_power"]=250
            self.basic_status_dictionary["high_power"]=400
            self.basic_status_dictionary["reach"]=32
            self.basic_status_dictionary["cooldown"]=1
            self.basic_status_dictionary["square"]=(0,0,32,32)
            self.basic_status_dictionary["enlargement"]=1
            self.basic_status_dictionary["skill"] = "All_kill"
            self.basic_status_dictionary["skill_image"] = r"Character image/Blueduck/Blueduck skill.png"
            self.basic_status_dictionary["skill_cooldown"] = 10
            self.basic_status_dictionary["skill_sound"] = r"Music/Crash.wav"
            # self.basic_status_dictionary[]=
       
        super().__init__(pos,groups,obstacles_sprites,
                         self.basic_status_dictionary,
                         self.ani_dictionary)
        # self.idle_ani=Animation(r"Character image/Somebody/somebody_idle.png",(0,0,40,50),2,0.75,-1,True,10)
