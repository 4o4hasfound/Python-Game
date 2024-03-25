import pygame
import sys

class words:
    def __init__(self,word,size,color,pos):
        self.words=str(word)
        self.size=size
        self.color=color
        self.pos=pos
        self.font = pygame.font.SysFont(None, size)
        self.dis = self.font.render(self.words, True,  self.color )
   
    # def display(self,pos):

    def word_update(self,words):
        self.words=str(words)
        self.dis = self.font.render(self.words, True,  self.color )

    def pos_update(self,pos):
        self.pos = pos
        self.dis = self.font.render(self.words, True,  self.color )

    def color_update(self,color):
        self.color = color
        self.dis = self.font.render(self.words, True, self.color)