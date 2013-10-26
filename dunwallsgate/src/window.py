#!/bin/python3

import pygame, sys
from pygame.locals import *

FPS = 30

class Window():
	def __init__(self, screen):
		"""
		Define a new window with a given screen
		
		For now, only one Window object should exist
		"""
		self.surface = pygame.display.set_mode((1024, 574), DOUBLEBUF)
		pygame.display.set_caption("Dunwall's Gate")
		self._screen = None
		self.set_screen(screen)
		self.fpsClock = pygame.time.Clock()
	
	def set_screen(self, screen):
		"""
		Define the screen to be displayed in the window
		"""
		self._screen = screen
		self._screen.set_window(self)
	
	def run(self):
		"""
		Run the game
		"""
		run = True
		while run:
			self._screen.draw()
			for event in pygame.event.get():
				if event.type == QUIT:
					run = False
			pygame.display.flip()
			self.fpsClock.tick(FPS)
		pygame.quit()