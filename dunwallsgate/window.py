#!/bin/python3

import pygame
import pygame.locals as pg

from event_manager import EventManager
from screens.homescreen import HomeScreen

FPS = 30


class Window():
    def __init__(self,):
        """
        Définit une Window et un screen qui y est dessiné
        """
        self.surface = pygame.display.set_mode((1024, 574), pg.DOUBLEBUF)
        pygame.display.set_caption("Dunwall's Gate")
        self.eventmanager = EventManager(self)
        self._screen = None
        self.game = None
        self.set_screen(HomeScreen())
        self.fpsClock = pygame.time.Clock()
        self.do_run = True

    def set_screen(self, screen):
        """
        Définit l'écran affiché dans la Window
        """
        if self._screen is not None:
            self._screen.surface.fill(0)
            self._screen.shutdown()
            self.eventmanager.purge_callbacks(self._screen)
        self._screen = screen
        self._screen.start(self, self.eventmanager)

    def set_do_run(self, value=True):
        self.do_run = value

    def start_game(self, game):
        self.game = game
        game.start(self)

    def run(self):
        """
        Lance le jeu
        """
        self.eventmanager.on_quit(lambda x: self.set_do_run(False), "global")
        while self.do_run:
            self._screen.update()
            self._screen.draw()
            if self.game:
                self.game.game_event.update()
            self.eventmanager.run(pygame.event.get())
            pygame.display.flip()
            self.fpsClock.tick(FPS)
        pygame.quit()
