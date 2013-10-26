#!/bin/python3


import pygame


class HomeScreen():
    """
    The home screen of the game. It is displayed at start up
    """
    background = pygame.image.load('../data/images/home/background.gif')

    def __init__(self):
        pass

    def start(self, window):
        self.window = window
        try:
            soundtrack = pygame.mixer.Sound('../data/sound/dunwalls_theme.ogg')
        except pygame.error as e:
            print("Dismissed exception: ", e)
        else:
            soundtrack.play(-1)

    def draw(self):
        self.window.surface.blit(self.background, (0, 0))
