#!/bin/python3


import pygame
import pygame.locals as pg


class HomeScreen():
    """
    The home screen of the game. It is displayed at start up
    """
    background = pygame.image.load('../data/images/home/background.gif')

    def __init__(self):
        self.theme_playing = True

    def start(self, surface, eventmanager):
        self.surface = surface
        self.eventmanager = eventmanager
        try:
            self.soundtrack = pygame.mixer.Sound(
                '../data/sound/dunwalls_theme.ogg')
        except pygame.error as e:
            print("Dismissed exception: ", e)
        else:
            self.eventmanager.on_key_down(self.toggle_theme, pg.K_s)
            self.toggle_theme(force=True)

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
        self.surface.blit(self.background, (0, 0))
