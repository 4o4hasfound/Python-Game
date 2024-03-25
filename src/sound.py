import pygame

pygame.init()
pygame.mixer.init()

class sound:
    def __init__(self,track,volumn):
        self.s=pygame.mixer.Sound(track)
        self.s.set_volume(volumn)
    '''
    # def input(self):
    #     key=pygame.key.get_pressed()
        
    #     if key[pygame.K_1]:
    #         self.s.set_volume(0.1)
    #     if key[pygame.K_2]:
    #         self.s.set_volume(0.2)
    #     if key[pygame.K_3]:
    #         self.s.set_volume(0.3)
    #     if key[pygame.K_4]:
    #         self.s.set_volume(0.4)
    #     if key[pygame.K_5]:
    #         self.s.set_volume(0.5)
    #     if key[pygame.K_6]:
    #         self.s.set_volume(0.6)
    #     if key[pygame.K_7]:
    #         self.s.set_volume(0.7)
    #     if key[pygame.K_8]:
    #         self.s.set_volume(0.8)
    #     if key[pygame.K_9]:
    #         self.s.set_volume(0.9)

    # def update(self):
    #     self.input()
    '''
    
    def Go_off(self):
        self.s.play()

    def Ok_ler(self):
        self.s.stop()

