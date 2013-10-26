#!/bin/python3

import pygame
from pygame.locals import *

class HomeScreen():
	"""
	The home screen of the game. It is displayed at start up
	"""
	background = pygame.image.load('../data/images/home/background.gif')

	def __init__(self):
		pass
	
	def set_window(self, window):
		self.window = window
	
	def draw(self):
		self.window.surface.blit(self.background, (0,0))