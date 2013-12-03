#!/bin/python3


import pygame
import pygame.locals as pg

from game import Game
from data import get_image_path
from screens.text_render import TextRender

import soundmanager


class HomeScreen():
    """
    The home screen of the game. It is displayed at start up
    """

    background = None
    exit_btn = None
    continue_btn = None
    new_btn = None

    def __init__(self):
        self.first_draw = False

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.first_draw = True
        self.load_active = False
        self.e_registrations = []

        self.init_sprites()
        # Soundtrack management
        try:
            soundmanager.play_music("dunwalls_theme", -1)
        except pygame.error as e:
            print("Dismissed exception: ", e)
        else:
            self.eventmanager.on_key_down(self.toggle_theme, pg.K_s)

        # Sprites placement
        self.exit_btn.rect = self.exit_btn.image.get_rect(
            bottomleft=(30,
                         self.surface.get_height() - 83))
        self.continue_btn.rect = self.continue_btn.image.get_rect(
            bottomleft=(30,
                         self.surface.get_height() - 170))
        self.new_btn.rect = self.new_btn.image.get_rect(
            bottomleft=(30,
                         self.surface.get_height() - 125))
        self.buttons = pygame.sprite.RenderPlain(self.exit_btn, self.continue_btn,
                                                 self.new_btn)
        # Events registration
        self.e_registrations.append(self.eventmanager.on_click_on(self.exit_btn,
                                      lambda e: self.window.set_do_run(False)))
        self.e_registrations.append(self.eventmanager.on_click_on(self.continue_btn,
                                      lambda e: self.game_load()))
        self.e_registrations.append(self.eventmanager.on_click_on(
            self.new_btn, lambda e: self.window.start_game(Game())))

    def toggle_theme(self, event):
        soundmanager.toggle_music(500)

    def draw(self):
        if self.first_draw:
            self.surface.blit(self.background, (0, 0))
            self.first_draw = False

        self.buttons.clear(self.surface, self.background)
        if self.load_active:
            self.loads_elements.clear(self.surface, self.background)
        self.buttons.draw(self.surface)
        if self.load_active:
            self.loads_elements.draw(self.surface)

    def shutdown(self):
        self.surface.fill(0)
        soundmanager.stop_music(500)
    
    def game_load(self):
        self.load_active = True
        self.eventmanager.remove_callback(*self.e_registrations)
        
        self.transparent = pygame.sprite.DirtySprite()
        self.transparent.image = pygame.Surface((self.surface.get_width(),self.surface.get_height()), pygame.SRCALPHA)
        self.transparent.image.fill((0,0,0,200))
        self.transparent.rect = self.transparent.image.get_rect(
            bottomright=(self.surface.get_width(),
                         self.surface.get_height()))
                         
        self.load_block = pygame.sprite.DirtySprite()
        self.load_block.image = pygame.Surface((self.surface.get_width(),self.surface.get_height()/2), pygame.SRCALPHA)
        self.load_block.image.fill((0,0,0,200))
        self.load_block.rect = self.load_block.image.get_rect(
            topleft=(0,
                         self.surface.get_height()/4))
                         
        transparent = pygame.Surface((700,200), pygame.SRCALPHA)
        transparent.fill((0,0,0,140))
        note = TextRender((700,700), "joystix", 16, (255,255,255), 
                                           "Aucune sauvegarde n'a été trouvé")
        note2 = TextRender((700,700), "joystix", 27, (255,255,255), 
                                           "Désolé !")
        transparent.blit(note.next(), (0,0))
        transparent.blit(note2.next(), (125,50))
        self.load_block.image.blit(transparent, (300,70))
                         
        self.loads_elements = pygame.sprite.OrderedUpdates(self.transparent, self.load_block)
        
        self.e_registrations.append(self.eventmanager.on_click_on(
            self.surface, lambda e: self.desactiv_game_load()))
        
    def desactiv_game_load(self):
        self.load_active = False
        self.loads_elements.clear(self.surface, self.background)
        self.buttons.draw(self.surface)
        self.eventmanager.remove_callback(*self.e_registrations)
        self.e_registrations.append(self.eventmanager.on_click_on(self.exit_btn,
                                      lambda e: self.window.set_do_run(False)))
        self.e_registrations.append(self.eventmanager.on_click_on(self.continue_btn,
                                      lambda e: self.game_load()))
        self.e_registrations.append(self.eventmanager.on_click_on(
            self.new_btn, lambda e: self.window.start_game(Game())))
            
        
    def init_sprites(self):
        if not self.background:
            self.background = (pygame.image.load(
                get_image_path("home/background.gif")).convert_alpha())
        if not self.exit_btn:
            self.exit_btn = pygame.sprite.DirtySprite()
            self.exit_btn.image = (pygame.image.load(
                get_image_path('home/exit_btn.png')).convert_alpha())
        if not self.continue_btn:
            self.continue_btn = pygame.sprite.DirtySprite()
            self.continue_btn.image = (pygame.image.load(
                get_image_path('home/continue_btn.png')).convert_alpha())
        if not self.new_btn:
            self.new_btn = pygame.sprite.DirtySprite()
            self.new_btn.image = (pygame.image.load(
                get_image_path('home/new_btn.png')).convert_alpha())
