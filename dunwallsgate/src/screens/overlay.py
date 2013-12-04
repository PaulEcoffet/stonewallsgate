#!/bin/python3

import pygame
import pygame.locals as pg

from screens.text_render import TextRender
from character import Character
from customsprites import Button
from battle import Battle
        
class Overlay():
    """
    The story screen of the game.
    """

    def __init__(self, window, eventmanager, option_btn):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.e_registrations = []
        self.options = False
        self.option_btn = option_btn
        
    def desactive(self):
        self.options = False
        self.clear_options = True
        self.eventmanager.remove_callback(*self.e_registrations)
        self.e_registrations.append(self.eventmanager.on_click_on(self.option_btn,
                                      lambda e:  self.active()))
            
    def active(self):
        self.options = True
        self.eventmanager.remove_callback(*self.e_registrations)
        
        self.transparent = pygame.sprite.DirtySprite()
        self.transparent.image = pygame.Surface((self.surface.get_width(),self.surface.get_height()), pygame.SRCALPHA)
        self.transparent.image.fill((0,0,0,200))
        self.transparent.rect = self.transparent.image.get_rect(x=0, y=0)
        
        self.load_block = pygame.sprite.DirtySprite()
        self.load_block.image = pygame.Surface((265,self.surface.get_height()), pygame.SRCALPHA)
        self.load_block.image.fill((0,0,0,200))
        self.load_block.rect = self.load_block.image.get_rect(x=400, y=0)      
        
        transparent = pygame.Surface((700,200), pygame.SRCALPHA)
        transparent.fill((0,0,0,140))
        self.load_block.image.blit(transparent, (300,70))
        note = TextRender((320,50), "joystix", 16, (255,50,10), 
                                           "<OPTIONS>")
        self.load_block.image.blit(note.next(), (78,160))
        self.exit_btn = Button("EXIT")
        self.save_btn = Button("SAVE")
        self.exit_btn.rect = self.exit_btn.image.get_rect(x=410, y=280)
        self.save_btn.rect = self.save_btn.image.get_rect(x=410, y=200)
        self.loads_elements = pygame.sprite.OrderedUpdates(self.transparent, self.load_block, self.exit_btn, self.save_btn)
        
        self.e_registrations.append(self.eventmanager.on_click_on(
            self.surface, lambda e: self.desactive()))
        self.e_registrations.append(self.eventmanager.on_click_on(
            self.exit_btn, lambda e: self.window.set_do_run(False)))

        
