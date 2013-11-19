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
    load_btn = None
    start_btn = None

    def __init__(self):
        self.first_draw = False

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.first_draw = True

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
            bottomright=(self.surface.get_width(),
                         self.surface.get_height() - 15))
        self.load_btn.rect = self.load_btn.image.get_rect(
            bottomright=self.exit_btn.rect.topright)
        self.start_btn.rect = self.start_btn.image.get_rect(
            bottomright=self.load_btn.rect.topright)
        self.buttons = pygame.sprite.RenderPlain(self.exit_btn, self.load_btn,
                                                 self.start_btn)
        # Events registration
        self.eventmanager.on_click_on(self.exit_btn,
                                      lambda e: self.window.set_do_run(False))
        self.eventmanager.on_click_on(
            self.start_btn, lambda e: self.window.start_game(Game()))

    def toggle_theme(self, event):
        soundmanager.toggle_music(500)

    def draw(self):
        if self.first_draw:
            self.surface.blit(self.background, (0, 0))
            self.first_draw = False
        self.buttons.clear(self.surface, self.background)
        self.buttons.draw(self.surface)

    def shutdown(self):
        self.surface.fill(0)
        soundmanager.stop_music(500)

    def init_sprites(self):
        if not self.background:
            self.background = (pygame.image.load(
                get_image_path("home/background.gif")).convert())
        if not self.exit_btn:
            self.exit_btn = pygame.sprite.DirtySprite()
            self.exit_btn.image = (pygame.image.load(
                get_image_path('home/exit_button.gif')).convert())
        if not self.load_btn:
            self.load_btn = pygame.sprite.DirtySprite()
            self.load_btn.image = (pygame.image.load(
                get_image_path('home/load_button.gif')).convert())
        if not self.start_btn:
            self.start_btn = pygame.sprite.DirtySprite()
            self.start_btn.image = (pygame.image.load(
                get_image_path('home/start_button.gif')).convert())
