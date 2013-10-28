#!/bin/python3


import pygame
import pygame.locals as pg


class HomeScreen():
    """
    The home screen of the game. It is displayed at start up
    """

    # TODO UGLY
    background = None
    exit = None
    load = None
    start = None

    def __init__(self):
        self.theme_playing = True
        self.first_draw = False

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.first_draw = True

        if not self.background:
            self.background = (pygame.image.load(
                '../data/images/home/background.gif').convert())
            self.exit = pygame.sprite.DirtySprite()
            self.exit.image = (pygame.image.load(
                '../data/images/home/exit_button.gif').convert())
            self.load = pygame.sprite.DirtySprite()
            self.load.image = (pygame.image.load(
                '../data/images/home/load_button.gif').convert())
            self.start = pygame.sprite.DirtySprite()
            self.start.image = (pygame.image.load(
                '../data/images/home/start_button.gif').convert())

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
        self.exit.rect = self.exit.image.get_rect(
            bottomright=(self.surface.get_width(),
                         self.surface.get_height() - 15))
        self.load.rect = self.load.image.get_rect(
            bottomright=self.exit.rect.topright)
        self.start.rect = self.start.image.get_rect(
            bottomright=self.load.rect.topright)

        self.buttons = pygame.sprite.RenderPlain(self.exit, self.load,
                                                 self.start)

        # Events registration
        self.eventmanager.on_click_on(self.exit,
                                      lambda: self.window.set_do_run(False))

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
