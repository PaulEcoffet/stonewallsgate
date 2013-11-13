#!/bin/python3


import pygame
import pygame.locals as pg
from screens.storyscreen import StoryScreen


class HomeScreen():
    """
    The home screen of the game. It is displayed at start up
    """

    background = None
    exit_btn = None
    load_btn = None
    start_btn = None

    def __init__(self):
        self.theme_playing = True
        self.first_draw = False

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.first_draw = True

        self.init_sprites()
        # Soundtrack management
        try:
            self.soundtrack = pygame.mixer.Sound(
                '../data/sound/dunwalls_theme.ogg')
        except pygame.error as e:
            print("Dismissed exception: ", e)
        else:
            self.eventmanager.on_key_down(self.toggle_theme, pg.K_s)
            self.toggle_theme(force=True)

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
			self.start_btn,
            lambda e: self.window.set_screen(StoryScreen()))

    def toggle_theme(self, *args, **kwargs):
        try:
            self.theme_playing = kwargs["force"]
        except KeyError:
            self.theme_playing = not self.theme_playing
        if self.theme_playing:
            self.soundtrack.play(-1)
        else:
            self.soundtrack.stop()

    def draw(self):
        if self.first_draw:
            self.surface.blit(self.background, (0, 0))
            self.first_draw = False
        self.buttons.clear(self.surface, self.background)
        self.buttons.draw(self.surface)

    def shutdown(self):
        self.surface.fill(0)

    def init_sprites(self):
        if not self.background:
            self.background = (pygame.image.load(
                '../data/images/home/background.gif').convert())
        if not self.exit_btn:
            self.exit_btn = pygame.sprite.DirtySprite()
            self.exit_btn.image = (pygame.image.load(
                '../data/images/home/exit_button.gif').convert())
        if not self.load_btn:
            self.load_btn = pygame.sprite.DirtySprite()
            self.load_btn.image = (pygame.image.load(
                '../data/images/home/load_button.gif').convert())
        if not self.start_btn:
            self.start_btn = pygame.sprite.DirtySprite()
            self.start_btn.image = (pygame.image.load(
                '../data/images/home/start_button.gif').convert())
