#!/bin/python3


import pygame
import pygame.locals as pg

from game import Game
from data import get_image_path

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
        """Démarre l'écran
        window - La fenêtre du jeu
        eventmanager - Le gestionnaire d'évènement
        """
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
            self.eventmanager.on_key_down(self.toggle_theme, pg.K_s,
                                          self.window)

        # Sprites placement
        self.exit_btn.rect = self.exit_btn.image.get_rect(
            bottomleft=(30,
                        self.surface.get_height() - 83))
        self.new_btn.rect = self.new_btn.image.get_rect(
            bottomleft=(30,
                        self.surface.get_height() - 125))
        self.buttons = pygame.sprite.RenderPlain(self.exit_btn,
                                                 self.new_btn)
        # Events registration
        self.eventmanager.on_click_on(self.exit_btn,
                                      lambda e: self.window.set_do_run(False),
                                      self)
        self.eventmanager.on_click_on(self.continue_btn,
                                      lambda e: self.game_load(), self)
        self.eventmanager.on_click_on(
            self.new_btn, lambda e: self.window.start_game(Game()), self)

    def toggle_theme(self, event):
        """
        Démarre ou eteint la musique avec 500ms de fondu
        """
        soundmanager.toggle_music(500)

    def update(self):
        pass

    def draw(self):
        """
        Efface puis (re)déssine les elements graphiques
        """
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
        self.eventmanager.purge_callbacks(self)

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
