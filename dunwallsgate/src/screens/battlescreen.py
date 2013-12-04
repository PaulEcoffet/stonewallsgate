#!/bin/python3

import pygame
import pygame.locals as pg

from screens.text_render import TextRender
from character import Character
from customsprites import Button
from battle import Battle
from screens.overlay import Overlay

class BattleScreen(Overlay):
    """
    The story screen of the game.
    """

    battle_background = None
    combat_box = None
    info_box = None
    attack_btn = None
    switchwep_btn = None
    run_btn = None
    bag_btn = None
    buttons = pygame.sprite.RenderUpdates()

    def __init__(self, game, event):
        self.start_battle = True
        self.game = game
        self.event = event
        self.end = False
    
    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.options_active = False
        self.init_sprites()

        # Sprites placement
        self.info_box.rect = self.info_box.image.get_rect(x=330, y=385)
        self.combat_box.rect = self.combat_box.image.get_rect(x=50, y=380)
        self.attack_btn.rect = self.attack_btn.image.get_rect(x=60, y=385)
        self.switchwep_btn.rect = self.switchwep_btn.image.get_rect(x=60, y=470)
        self.run_btn.rect=self.switchwep_btn.image.get_rect(x=700, y=470)
        self.bag_btn.rect=self.bag_btn.image.get_rect(x=700, y=385)
        
        self.graphic_elements = pygame.sprite.OrderedUpdates(self.combat_box, self.info_box)
        self.lifebars_elements = pygame.sprite.OrderedUpdates()
        self.portraits_elements = pygame.sprite.RenderUpdates()
        super().__init__(self.window, self.eventmanager, self.run_btn)
        self.init_battle()
        self.e_registrations.append(self.eventmanager.on_click_on(self.run_btn,
                                      lambda e:  self.active()))

    def draw(self):
        if self.start_battle:
            self.surface.blit(self.battle_background, (0, 0))
            self.start_battle = False
            self.clear_options = False
        if self.options:
            self.loads_elements.clear(self.surface, self.battle_background)
            self.loads_elements.draw(self.surface)
        else:
            if self.clear_options:
                self.loads_elements.clear(self.surface, self.battle_background)
                self.clear_options = False
            self.lifebars_elements.update()
            self.portraits_elements.clear(self.surface, self.battle_background)
            self.portraits_elements = pygame.sprite.RenderUpdates(self.new_portraits)
            self.lifebars_elements.clear(self.surface, self.battle_background)
            self.lifebars_elements = pygame.sprite.OrderedUpdates(self.new_lifebars)
            self.lifebars_elements.draw(self.surface)
            self.portraits_elements.draw(self.surface)

            self.graphic_elements.clear(self.surface, self.battle_background)
            self.graphic_elements = pygame.sprite.OrderedUpdates(
                    self.combat_box, self.info_box)         
            self.graphic_elements.draw(self.surface)
            self.buttons.clear(self.surface, self.battle_background)
            self.buttons.draw(self.surface)
            if self.game.hero.health == 0:
                self.game.combat_state = "loose"
                self.end = True
            for charac in self.ennemies:
                if charac.health != 0:
                    break
                else:
                    self.game.combat_state = "win"     
                    self.end = True
    def init_sprites(self):
            
        if not self.battle_background:
            self.battle_background = pygame.image.load(
                self.event.background).convert()
            self.battle_background = (pygame.transform.scale(
                self.battle_background, (1024, 574)))

        if not self.combat_box:
            self.combat_box = pygame.sprite.DirtySprite()
            self.combat_box.image = pygame.Surface((924,163), pygame.SRCALPHA)
            self.purge_box(self.combat_box)
            
        if not self.info_box:
            self.info_box = pygame.sprite.DirtySprite()
            self.info_box.image = pygame.Surface((350,163), pygame.SRCALPHA)
            self.purge_box(self.info_box, 195)
        
        if not self.attack_btn:
            self.attack_btn = Button("ATTACK", buttons=self.buttons)
            
        if not self.switchwep_btn:
            self.switchwep_btn = Button("WEAPONS", buttons=self.buttons)
            
        if not self.run_btn:
            self.run_btn = Button("RUN", buttons=self.buttons, color=(255,69,0)) 
            
        if not self.bag_btn:
            self.bag_btn = Button("MY BAG", buttons=self.buttons, color=(255,69,0))    
            
    def purge_box(self, sprite, alphakey=140):
        sprite.image.fill((0,0,0,alphakey))
    
    def init_battle(self):
        self.characs = []
        self.lifebars = []
        self.set_elements(self.game.hero_companions+[self.game.hero], "allies")
        self.ennemies = [self.game.cache.get_charac(charac) for charac in self.event.battle.ennemies]
        self.set_elements(self.ennemies, "ennemies")
        self.new_portraits = self.characs
        self.new_lifebars = self.lifebars
                
            
        
    def set_elements(self, characters, type):
        if type == "allies":
            position_portraits = lambda i: (190*(i*1.2+1), 217)
            position_bars = lambda i: (160*(i*1.4+1), 365)
        else:
            position_portraits = lambda i: (100*(i*1.2+1)+775, 10)
            position_bars = lambda i: (100*(i*1.4+1)+740, 160)
            
        for i, companion in enumerate(characters):
            portrait = self.game.cache.get_charac(companion.name).front_portrait["Highlighted"]
            portrait.resize(300,150)
            portrait.move(*position_portraits(i))
            self.characs.append(portrait)
            lifebar = companion.lifebar
            lifebar.move(*position_bars(i))
            self.lifebars.append(lifebar)
        

        
