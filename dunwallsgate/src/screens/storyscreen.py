#!/bin/python3


import pygame
import pygame.locals as pg
import data

from decoder import *
from screens.text_render import TextRender


class StoryScreen():
	"""
	The story screen of the game.
	"""

	scene_background = None
	dialogue_box = None

	def __init__(self, game, event):
		self.start_scene = True
		self.game = game
		self.event = event

	def start(self, window, eventmanager):
		self.window = window
		self.surface = window.surface
		self.eventmanager = eventmanager
		self.cache = {}
		self.init_sprites()
		# Sprites placement
		self.dialogue_box.rect = self.dialogue_box.image.get_rect(x=50, y=380)
		self.graphic_elements = pygame.sprite.RenderPlain(self.dialogue_box)
		self.init_story()

	def draw(self):
		if self.start_scene:
			self.surface.blit(self.scene_background, (0, 0))
			transparent = pygame.Surface((230,30), pygame.SRCALPHA)
			transparent.fill((0,0,0,140))
			note = TextRender((300,50), "joystix", 20, (255,50,10), 
                                               "ALPHA version")
			transparent.blit(note.next(), (5,3))
			self.surface.blit(transparent, (10,10))
			self.start_scene = False
		self.graphic_elements.clear(self.surface, self.scene_background)
		self.graphic_elements.draw(self.surface)

	def init_sprites(self):
		if not self.scene_background:
			self.scene_background = pygame.image.load(
				self.event.background).convert()
			self.scene_background = (pygame.transform.scale(
				self.scene_background, (1024, 574)))

		if not self.dialogue_box:
			self.dialogue_box = pygame.sprite.DirtySprite()
			self.dialogue_box.image = pygame.Surface((924,163), pygame.SRCALPHA)
			self.purge_textbox()

	def purge_textbox(self):
		self.dialogue_box.image.fill((0,0,0,140))

	def init_story(self):
		self.dialogues = self.event.dialogues
		self.message = self.dialogues.next()
		self.text_render = TextRender((904,163), "unispace_italic", 
			20, (255,158,0) , self.message["message"])
		self.left_charac = None
		self.show_dialogue()

		# Events registration
		self.eventmanager.on_key_down(self.show_dialogue, pg.K_RIGHT)
		self.eventmanager.on_click_on(self.dialogue_box, self.show_dialogue)
		
	def show_dialogue(self, *args):
		next_text = self.text_render.next()
		if next_text is None:
			#End of ONE conversation
			self.message = self.dialogues.next()
			if self.message is None:
				#End of Storyscreen (the event is done)
				self.event.done = True
				return None
			self.graphic_elements.clear(self.surface, self.scene_background)
			self.graphic_elements = pygame.sprite.RenderPlain(
				self.dialogue_box, *self.get_portraits())
			self.text_render = TextRender((904,163), "larabiefont", 25, (255,158,0) , self.message["message"])
			next_text = self.text_render.next()
			if False and self.choices:
				for choice in self.choices:
					choice = pygame.sprite.DirtySprite()
					text_choice = TextRender((904,163), "larabiefont", 25, (255,158,0) , self.message["message"])
					choice.image = text_choice.next()
			self.purge_textbox()
		self.purge_textbox()
		self.dialogue_box.image.blit(next_text, (10,10))
		
	def get_portraits(self):
		""" Manage portraits (DirtySprite) to display, if there is. 
		First charac to speak is always display on the left side."""
		
		characs = []
		if self.message["transmitter"]:
			if self.message["transmitter"] == self.left_charac:
				characs.append(self.search_portrait("transmitter", (250,160)))
				if self.message["receiver"]:
					characs.append(self.search_portrait("receiver", (800,160)))
			elif self.message["receiver"] and self.message["receiver"] == self.left_charac: 
				characs.append(self.search_portrait("transmitter", (800,160)))
				characs.append(self.search_portrait("receiver", (250,160)))
			elif self.message["receiver"]:
				self.left_charac = self.message["transmitter"]
				characs.append(self.search_portrait("receiver", (800, 160)))
				characs.append(self.search_portrait("transmitter", (250, 160)))
			else:
				self.left_charac = self.message["transmitter"]
				characs.append(self.search_portrait("transmitter", (250, 160)))
		return characs
		
	def search_portrait(self, type, position):
		""" Get portrait from cache and set it at a position. """
		
		id_portrait = (self.message[type], type)
		self.game.cache.portraits[id_portrait].rect = self.game.cache.portraits[id_portrait].image.get_rect(midtop=position)
		return self.game.cache.portraits[id_portrait]