import pygame
from pygame.locals import *
from screens.text_render import TextRender
import random

GREEN_RGB = (0,255,0)
YELLOW_RGB = (255,215,0)
RED_RGB = (255,0,0)
BLACK_RGB = (0,0,0)
ORANGE_RGB = (255,69,0)

class Button(pygame.sprite.DirtySprite):
    """generic button which can be improved"""
    
    def __init__(self, text, buttons=None, size=(250,70), color=ORANGE_RGB):
        self.text = text
        if not buttons is None:
            pygame.sprite.DirtySprite.__init__(self, buttons)
        else:
            pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.surface.Surface(size)
        pygame.draw.rect(self.image, color, (0,0,250,70), 3)
        self.rect = self.image.get_rect()
        attack = TextRender((500,500), "joystix", 40, (255,158,0), self.text)
        self.image.blit(attack.next(), (5,6))
            
class LifeBar(pygame.sprite.Sprite):
    """shows a bar with the health of a charac"""
    
    def __init__(self, charac):
        self.charac = charac
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((200,15))
        pygame.draw.rect(self.image, BLACK_RGB, (0,0,200,15), 1)
        self.rect = self.image.get_rect()
        
        self.percent = 0
        self.oldpercent = 0
        self.smooth_revision = 0
        self.health = self.charac.health
        self.i = 0
        self.maxhealth = self.charac.maxhealth
        self.block = False
        
    def resize(self, width=0, height=0):
        self.image = pygame.transform.scale(self.image, (width, height))
        
    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))
        
    def draw_greenbar(self, health, color):
        pygame.draw.rect(self.image, color, (0,0,
            int(200 * health/self.maxhealth),15),0) # fill green
        self.pg_font = pygame.font.SysFont("joystix", 26)
        if health != 0:
            a = self.pg_font.render("%d/%d"%(health,self.maxhealth), 1, (200,80,15))
            self.image.blit(a, (147,1))
        else:
            a = self.pg_font.render("DEAD", 1, RED_RGB)    
            self.image.blit(a, (75,1))
        
    def get_color(self, health):
        if health == 0:
            color = (0,0,0)
        elif health < 20:
            self.i = self.i + 1
            if self.i % 10 == 0:
                color = ORANGE_RGB
            else:
                color = RED_RGB
            self.i = 0
        elif health < 50:
            color = YELLOW_RGB
        else:
            color = GREEN_RGB
        return color
        
    def update(self):
        if self.smooth_revision == self.health:
            self.charac.health = self.health
            if self.health != 0:
                self.health = random.choice([x for x in range(0,self.maxhealth,10)])
            
        if self.smooth_revision != self.health:
            health_left = self.smooth_revision - self.health
            self.smooth_revision -= abs(health_left)/health_left
            #self.percent = self.charac.health / self.maxhealth
            self.percent = self.smooth_revision / self.maxhealth
            color = self.get_color(self.smooth_revision)
            if self.percent != self.oldpercent or color != self.old_color:
                pygame.draw.rect(self.image, BLACK_RGB, (0,0,200-2,15)) # fill black
                self.draw_greenbar(self.smooth_revision, color)
                self.oldpercent = self.percent
                self.old_color = color

        if self.percent == 0:
            pygame.draw.rect(self.image, BLACK_RGB, (0,0,200-2,15)) # fill black
            self.draw_greenbar(self.health, self.get_color(self.health))

class Portrait(pygame.sprite.Sprite):
        
    def __init__(self, name, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (440, 221))
        self.transparent = pygame.Surface((300,100), pygame.SRCALPHA)
        self.transparent.fill((0,0,0,200))
        
    def resize(self, width=440, height=221):
        self.image = pygame.transform.scale(self.image, (width, height))
        
    def move(self, x=0, y=0):
        self.rect = self.image.get_rect(midtop=(x, y))
        
class HighlightedPortrait(Portrait):

    def __init__(self, name, image):
        super().__init__(name, image)
        label = TextRender((300,100), "joystix", 35, (200,80,15), ">"+name)
        self.image.blit(self.transparent, (20,185))
        self.image.blit(label.next(), (25,181))
        
class AttenuatedPortrait(Portrait):

    def __init__(self, name, image):
        super().__init__(name, image)
        label = TextRender((300,100), "joystix", 35, (200,80,15), ">"+name)
        self.image.fill((255, 255, 255, 140), None, pygame.BLEND_RGBA_MULT)
        self.image.blit(self.transparent, (20,185))
        self.image.blit(label.next(), (25,181))
        

            