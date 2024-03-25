from random import randint
import pygame
import sys
import math
import pytmx
from pytmx.util_pygame import load_pygame
from pytmx.util_pyglet import load_pyglet
from src.Tile import *
from src.Map import *
from src.Enemy import *
from src.Player import *
from src.Potion import *
from src.words import *
from src.sound import *
from src.settings import *
from src.Animation import *

from typing import List, Dict

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.inRoom = False
        self.inPath = False
        self.potion_flag = False
        self.screen = pygame.display.get_surface()
        self.visible_sprites = ScrollGroup()
        self.obstacles_sprites = ScrollGroup()
        self.enemy = EnemyManager()  # self.enemy = Enemy((0, 0), self.visible_sprites, self.obstacles_sprites)
        self.potions = PotionManager()

        self.unmuted_icon = Animation(r"Other Image/sound_icon.png",(0,0,32,32),3,2,-1,True,20)
        self.muted_icon = Animation(r"Other Image/muted_icon.png",(0,0,32,32),3,2,-1,True,20)
        self.music_icon = self.unmuted_icon.next(0)
        self.mute_change = 0
        self.music_paused = False
        self.roomleft_display = words(-1, 45, WHITE, (0,540))

        self.maps: Dict[str, Map] = {}
        self.loadMap("Level")

        # This is FIRST Y THEN X !!!!!!!!!!!! VERY IPMORTANT
        self.visited: List[List[bool]] = [
            [
                False for x in range(len(self.maps["Level"].chunks[0]))
            ] for y in range(len(self.maps["Level"].chunks))
        ]
        self.roomsLeft: int = 0
        self.temp_inRoom_for_roomsleft: bool= False
        for y in range(len(self.maps["Level"].chunks)):
            for x in range(len(self.maps["Level"].chunks[0])):
                if isinstance(self.maps["Level"].chunkTypes[y][x], RoomInf):
                    self.roomsLeft += 1
        self.wall_build_delay=60
        self.now_wall_build = 0


        self.background_music = sound(r"Music/Zutomayo.wav", 0.1)
        self.starting_song = sound(r"Music/MILABO 8bit.wav", 0.1)
        self.winning_song = sound(r"Music/Winning song.wav",0.5)
        self.losing_song = sound(r"Music/Losing song.wav",0.5)
        self.icon = pygame.image.load(r"Not very important/player.png")
        # self.test=0

        # print(self.roomsLeft)

    def run(self):
        self.starting()

        while True:
            self.window.fill(WHITE)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.player.hp <= 0:
                self.ending()

            elif self.roomsLeft == 0:
                self.winning()

            else:
                self.update()
                
            
            pygame.display.update()
            self.clock.tick(FPS)
            # self.test+=1
            # if self.test>300:
            #     self.background_music.ok_ler()

    def starting(self):
        self.starting_song.Go_off()
        pygame.display.set_caption("Starting and testing")
        
        if True: #welcome
            self.window.fill(BLACK)
            self.starting_word = words("Welcome!!", 60, WHITE,
                                    (330, 270))
            self.window.blit(self.starting_word.dis, self.starting_word.pos)
            pygame.display.update()

            self.start_counter = 1
            while self.start_counter < 120:
                self.clock.tick(FPS)
                self.start_counter += 1
                self.key = pygame.key.get_pressed()
                if self.key[pygame.K_p]:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        if True: #RPG Game
            self.window.fill(BLACK)
            self.starting_word = words("This game is a kind of RPG game", 60,
                                    WHITE, (100, 270))
            self.window.blit(self.starting_word.dis, self.starting_word.pos)
            pygame.display.update()

            self.start_counter = 1
            while self.start_counter < 240:
                self.clock.tick(FPS)
                self.start_counter += 1
                self.key = pygame.key.get_pressed()
                if self.key[pygame.K_p]:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        if True: #Goal
            self.window.fill(BLACK)
            self.starting_word = words("Your goal is to fight enemies", 60, WHITE,
                                    (100, 270))
            self.window.blit(self.starting_word.dis, self.starting_word.pos)
            pygame.display.update()

            self.start_counter = 1
            while self.start_counter < 120:
                self.clock.tick(FPS)
                self.start_counter += 1
                self.key = pygame.key.get_pressed()
                if self.key[pygame.K_p]:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        if True: #Music
            self.window.fill(BLACK)
            self.starting_word = words("If you don't want the music", 60,
                                    WHITE, (100, 270))
            self.starting_word2 = words("in game, press M", 60,
                                    WHITE, (100, 370))
            self.window.blit(self.starting_word.dis, self.starting_word.pos)
            self.window.blit(self.starting_word2.dis, self.starting_word2.pos)
            pygame.display.update()

            self.start_counter = 1
            while self.start_counter < 120:
                self.clock.tick(FPS)
                self.start_counter += 1
                self.key = pygame.key.get_pressed()
                if self.key[pygame.K_p]:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        
        if True: #Choosing
            self.window.fill(BLACK)
            self.starting_word = words("You can move by pressing WASD", 60,
                                    WHITE, (70, 150))
            self.starting_word2 = words("You can attack by pressing space", 60,
                                        WHITE, (70, 250))
            self.starting_word3 = words("You can use your skill by F", 60,
                                        WHITE, (70, 350))
            self.starting_word4 = words("Press K to choose cat, L to choose duck", 40,
                                        WHITE, (230, 500))

            self.start_counter = 1
            while True:
                self.key = pygame.key.get_pressed()
                self.clock.tick(FPS)
                self.start_counter += 1
                if self.start_counter % 30 == 0:
                    self.window.fill((0, 0, 0))
                    self.window.blit(self.starting_word.dis,
                                    self.starting_word.pos)
                    self.window.blit(self.starting_word2.dis,
                                    self.starting_word2.pos)
                    self.window.blit(self.starting_word3.dis,
                                    self.starting_word3.pos)
                    if (self.start_counter / 30) % 2 == 0:
                        self.window.blit(self.starting_word4.dis,
                                        self.starting_word4.pos)
                    pygame.display.update()

                if self.key[pygame.K_k]:
                    self.player = Cat((100, 100), self.visible_sprites,
                                    self.obstacles_sprites)
                    break
                elif self.key[pygame.K_l]:
                    self.player = Duck((100, 100), self.visible_sprites,
                                    self.obstacles_sprites)
                    break

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        
        if True: #GOGO
            self.start_counter = 1
            self.starting_pos_y = 600
            while self.start_counter <= 100:
                self.window.fill(BLACK)
                self.starting_word = words("GOGO~~", 60, WHITE,
                                        (330, self.starting_pos_y))
                self.window.blit(self.starting_word.dis, self.starting_word.pos)
                pygame.display.update()
                self.starting_pos_y -= 6
                self.clock.tick(FPS)
                self.start_counter += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
       
        self.starting_song.Ok_ler()
        self.background_music.Go_off()
        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(self.icon)

    def ending(self):
        self.background_music.Ok_ler()
        self.losing_song.Go_off()
        offset = pygame.math.Vector2(self.player.rect.centerx - SCREEN_WIDTH / 2,
                                     self.player.rect.centery - SCREEN_HEIGHT / 2)
        while self.player.died_ani.now_picture_index != self.player.died_ani.count:
            self.clock.tick(FPS)
            self.window.fill(BLACK)
            self.window.blit(
                self.player.died_ani.next(self.player.where_to_face),
                (self.player.died_pos[0] - offset.x,
                 self.player.died_pos[1] - offset.y))
            pygame.display.update()

        self.window.fill(BLACK)
        self.ending_word = words("GGs ,Have A Nice day!!", 60, WHITE,
                                 (180, 270))
        self.window.blit(self.ending_word.dis, self.ending_word.pos)
        pygame.display.update()

        self.end_counter = 1
        while self.end_counter < 360:
            self.clock.tick(FPS)
            self.end_counter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.quit()
        sys.exit()

    def winning(self):
        self.background_music.Ok_ler()
        self.winning_song.Go_off()
        offset = pygame.math.Vector2(self.player.rect.centerx - SCREEN_WIDTH / 2,
                                     self.player.rect.centery - SCREEN_HEIGHT / 2)
        # print(self.player.win_ani.count)
        
        self.player.win_pos = self.player.rect.topleft
        while self.player.win_ani.now_picture_index != self.player.win_ani.count:
            self.clock.tick(FPS)
            self.window.fill(WHITE)
            self.window.blit(
                self.player.win_ani.next(self.player.where_to_face),
                (self.player.win_pos[0] - offset.x,
                 self.player.win_pos[1] - offset.y))
            pygame.display.update()

        self.window.fill(BLACK)
        self.ending_word = words("Congrats!! You've won!!", 60, WHITE,
                                 (150, 270))
        self.window.blit(self.ending_word.dis, self.ending_word.pos)
        pygame.display.update()

        self.end_counter = 1
        while self.end_counter < 240:
            self.clock.tick(FPS)
            self.end_counter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.quit()
        sys.exit()

    def update(self):
        obstacles = []
        xChunk = math.ceil(self.player.rect.topleft[0] / CHUNK_WIDTH) - 1
        yChunk = math.ceil(self.player.rect.topleft[1] / CHUNK_HEIGHT) - 1

        if len(self.enemy.enemies):
            self.now_wall_build += 1
            if (self.now_wall_build >= self.wall_build_delay):
                walls = self.maps["Level"].closed_chunk[xChunk][yChunk]
                for wall in walls:
                    obstacles += wall.obstacles
        objects = self.maps["Level"].chunks[xChunk][yChunk]
        if objects:
            obstacles += objects.obstacles
        self.player.update(obstacles, self.enemy)

        xChunk = math.ceil(self.player.rect.topleft[0] / CHUNK_WIDTH) - 1
        yChunk = math.ceil(self.player.rect.topleft[1] / CHUNK_HEIGHT) - 1

        if isinstance(self.maps["Level"].chunkTypes[xChunk][yChunk], RoomInf) and not self.inRoom and not self.visited[yChunk][xChunk]:
            self.inRoom = True
            self.temp_inRoom_for_roomsleft = True
            self.now_wall_build = 0
            self.enemy.generateEnemy(
                3,  # count
                self.maps["Level"].chunks[xChunk][yChunk],  # map
                CHUNK_WIDTH, CHUNK_HEIGHT,
                [xChunk * CHUNK_WIDTH, yChunk * CHUNK_HEIGHT],
                self.player)

        if not isinstance(self.maps["Level"].chunkTypes[xChunk][yChunk], RoomInf):
            self.inRoom = False
            self.enemy.appearing_ani.times = 0
            self.enemy.appearing_ani.iter()
            self.enemy.enemies.clear()

        self.enemy.update(
            self.player, self.maps["Level"].chunks[xChunk][yChunk].objectLayer.copy()
        )

        self.potions.update(
            self.player, self.maps["Level"].chunks[xChunk][yChunk].objectLayer.copy()
        )

        if isinstance(self.maps["Level"].chunkTypes[xChunk][yChunk], PathInf) and not self.inPath and self.potion_flag:
            self.inPath = True
            self.potion_flag = False
            self.visited[yChunk][xChunk] = True
            self.potions.generate_potion(
                3,  # count
                self.maps["Level"].chunks[xChunk][yChunk],  # map
                CHUNK_WIDTH, CHUNK_HEIGHT,
                [xChunk * CHUNK_WIDTH, yChunk * CHUNK_HEIGHT],
                self.player,
                self.maps["Level"].chunkTypes[xChunk][yChunk].dir)

        if not isinstance(self.maps["Level"].chunkTypes[xChunk][yChunk], PathInf):
            self.inPath = False

        self.blit_all_tiles("Level")
        self.check_for_music_mute()
        self.blit_other_things()
        
        # self.player.atk_cooldown_display.word_update("atk_CD:" + str(self.player.atk_cooldown))
        # self.window.blit(self.player.atk_cooldown_display.dis, self.player.atk_cooldown_display.pos)
    
    def check_for_music_mute(self):
        self.mute_change+=1
        self.key = pygame.key.get_pressed()
        if self.key[pygame.K_m] and self.mute_change > 60:
            self.mute_change = 0
            if not self.music_paused:
                self.background_music.Ok_ler()
                self.music_paused = True
            else:
                self.background_music.Go_off()
                self.music_paused= False

    def blit_other_things(self):
        if self.player.using_skill:
            self.window.blit(self.player.skill_effect.next(0),(0,0))

        self.window.blit(self.player.atk_cooldown_display.dis, (600,20))
        self.window.blit(self.player.skill_cooldown_display.dis, (600,60))

        #music icon
        self.music_icon = self.unmuted_icon.next(1) if (not self.music_paused) else  self.muted_icon.next(1)
        self.window.blit(self.music_icon,(0,0))

        #roomleft reminder
        self.roomleft_display.word_update("Rooms Left:" + str(self.roomsLeft))
        self.roomleft_display.pos_update((3,573))
        self.roomleft_display.color_update(BLACK)
        self.window.blit(self.roomleft_display.dis,self.roomleft_display.pos)
        self.roomleft_display.pos_update((0,570))
        self.roomleft_display.color_update(WHITE)
        self.window.blit(self.roomleft_display.dis,self.roomleft_display.pos)

    def loadMap(self, tilename):
        tiled_map = Map(self.obstacles_sprites, MAP_SIZE, MAP_SIZE)
        self.maps[tilename] = tiled_map

    def blit_all_tiles(self, tilename):
        offset = pygame.math.Vector2(self.player.rect.centerx - SCREEN_WIDTH / 2,
                                     self.player.rect.centery - SCREEN_HEIGHT / 2)
        tile_map = self.maps[tilename]
        obstacles = tile_map.blit(self.window, self.player)

        '''
        # if self.player.is_attacking:
        #     obstacles[self.player.atk_thing.rect.topleft] = self.player.atk_thing.atk_thing_ani.next(self.player.atk_thing.direction.x)
            # obstacles[self.player.atk_thing.atk_thing_pos.topleft] = self.player.atk_thing.atk_thing_ani.next(self.player.direction)

        # obstacles[self.player.rect.topleft] = self.player.image
        if self.player.atk_ani.i < self.player.atk_ani.count:
            self.player.image=self.player.atk_ani.next(self.player.direction)
            # player_atk = self.player.atk_ani.next(self.player.direction)
            things = self.player.atk_thing.atk_thing_ani.next(self.player.direction)
            # obstacles[self.player.atk_thing.atk_thing_pos.topleft] = player_atk
            obstacles[self.player.atk_thing.atk_thing_pos.topleft] = things
            obstacles[self.player.atk_num.pos] = self.player.atk_num.dis

        '''


        for potion in self.potions.potions:
            obstacles[potion.rect.topleft] = potion.image

        for thing in self.player.atk_things.things:
            obstacles[thing.rect.topleft] = thing.image
        
        obstacles[self.player.rect.topleft] = self.player.image
        obstacles[self.player.hp_display.pos] = self.player.hp_display.dis
        # obstacles[self.player.atk_cooldown_display.pos] = self.player.atk_cooldown_display.dis
        # obstacles[self.player.skill_cooldown_display.pos] = self.player.skill_cooldown_display.dis

        if self.enemy.appearing_ani.times < 3:
            for enemy in self.enemy.enemies:
                obstacles[enemy.rect.topleft] = self.enemy.appearing_ani.next(0)

        else:
            for enemy in self.enemy.enemies:
                if enemy.die == 1:
                    if enemy.died_ani.now_picture_index == 5:
                        self.enemy.enemies.remove(enemy)
                    else:
                        enemy_died_image = enemy.died_ani.next(enemy.where_to_face)
                        obstacles[enemy.died_pos] = enemy_died_image
                        # obstacles[enemy.health_display.
                        #           pos] = enemy.health_display.dis

                else:
                    obstacles[enemy.rect.topleft] = enemy.image

                obstacles[enemy.health_display.pos] = enemy.health_display.dis

        xChunk = math.ceil(
            self.player.rect.topleft[0] / CHUNK_WIDTH) - 1
        yChunk = math.ceil(
            self.player.rect.topleft[1] / CHUNK_HEIGHT) - 1
        if len(self.enemy.enemies):
            if (self.now_wall_build > self.wall_build_delay):
                walls = self.maps[tilename].closed_chunk[xChunk][yChunk]
                for wall in walls:
                    for obj in wall.obstacles:
                        obstacles[obj.rect.topleft] = obj.image
        else:
            if (not self.visited[yChunk][xChunk]) and self.temp_inRoom_for_roomsleft :
                self.roomsLeft -= 1
                self.temp_inRoom_for_roomsleft = False
                if self.inRoom:
                    self.potion_flag = True
            self.visited[yChunk][xChunk] = True
            
        for obj in sorted(obstacles.keys(), key=lambda pos: pos[1]):
            self.window.blit(obstacles[obj],
                             (obj[0] - offset.x, obj[1] - offset.y))


class ScrollGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)
        self.surface = pygame.display.get_surface()
        self.halfWidth = self.surface.get_size()[0] // 2
        self.halfHeight = self.surface.get_size()[1] // 2

        self.offset = pygame.math.Vector2(0, 0)

    def Draw(self, player):
        self.offset.x = player.rect.centerx - self.halfWidth

        self.offset.y = player.rect.centery - self.halfHeight

        for sprite in self.sprites():
            offsetRect = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offsetRect)