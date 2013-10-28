#!/bin/python3


import pygame
import pygame.locals as pg


class HomeScreen():
    """
    The home screen of the game. It is displayed at start up
    """
    background = pygame.image.load('../data/images/home/background.gif')
    exit = pygame.image.load('../data/images/home/exit_button.gif')
    load = pygame.image.load('../data/images/home/load_button.gif')
    start = pygame.image.load('../data/images/home/start_button.gif')

    def __init__(self):
        self.theme_playing = True

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        try:
            self.soundtrack = pygame.mixer.Sound(
                '../data/sound/dunwalls_theme.ogg')
        except pygame.error as e:
            print("Dismissed exception: ", e)
        else:
            self.eventmanager.on_key_down(self.toggle_theme, pg.K_s)
            self.toggle_theme(force=True)
        self.eventmanager.on_click_on(self.exit, lambda: self.window.set_do_run(False))

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
        self.background.blit(self.exit, (
            self.surface.get_width() - self.exit.get_width(),
            self.surface.get_height() - self.exit.get_height()
            ))
        self.surface.blit(self.background, (0, 0))
