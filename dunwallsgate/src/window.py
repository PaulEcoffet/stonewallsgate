#!/bin/python3

import pygame
import pygame.locals as pg

from event_manager import EventManager
from screens.homescreen import HomeScreen

FPS = 30


class Window():
    def __init__(self,):
        """
        Define a new window with a given screen

        For now, only one Window object should exist
        """
        self.surface = pygame.display.set_mode((1024, 574), pg.DOUBLEBUF)
        pygame.display.set_caption("Dunwall's Gate")
        self.eventmanager = EventManager()
        self._screen = None
        self.set_screen(HomeScreen())
        self.fpsClock = pygame.time.Clock()
        self.do_run = True

    def set_screen(self, screen):
        """
        Define the screen to be displayed in the window
        """
        if self._screen is not None:
            self._screen.shutdown()
        self._screen = screen
        self._screen.start(self, self.eventmanager)

    def set_do_run(self, value=True):
        self.do_run = value

    def run(self):
        """
        Run the game
        """
        self.eventmanager.on_quit(lambda x: self.set_do_run(False), "global")
        while self.do_run:
            self._screen.draw()
            self.eventmanager.run(pygame.event.get())
            pygame.display.flip()
            self.fpsClock.tick(FPS)
        pygame.quit()
