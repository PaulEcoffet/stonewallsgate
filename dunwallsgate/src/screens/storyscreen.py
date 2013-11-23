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

	def __init__(self, characters, event):
		self.start_scene = True
		self.characters = characters
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
			self.purge_textbox()

	def purge_textbox(self):
		self.dialogue_box.image = pygame.Surface((924,163), pygame.SRCALPHA)
		self.dialogue_box.image.fill((0,0,0,140))

	def init_story(self):
		self.dialogues = self.event.dialogues
		self.message = self.dialogues.next()
		self.text_render = TextRender((904,163), "unispace_italic", 
			20, (255,158,0) , self.message["message"])
		self.master = None
		self.show_dialogue()

		# Events registration
		self.eventmanager.on_key_down(self.show_dialogue, pg.K_RIGHT)
		self.eventmanager.on_click_on(self.dialogue_box, self.show_dialogue)

	def portrait_creation(self, type, position):
		#Add image in "cache" list to avoid useless LOADS
		id_img = self.message[type]
		if not id_img in self.cache:
			for character in self.characters:
				if character.name == self.message[type]:
					self.cache[id_img] = data.get_image_path("characters\%s"%character.front_image)
		#Add full portrait (text + image + layouts) in "cache" list to avoid useless PROCESS 
		id_portrait = (id_img, type, position)
		if not id_portrait in self.cache:
			self.cache[id_portrait] = pygame.sprite.DirtySprite()
			self.cache[id_portrait].image = pygame.image.load(self.cache[id_img])
			self.cache[id_portrait].image = self.cache[id_portrait].image.convert_alpha()
			self.cache[id_portrait].image = (pygame.transform.scale(self.cache[id_portrait].image, (440, 221)))
			self.cache[id_portrait].rect = self.cache[id_portrait].image.get_rect(midtop=position)
			if type == "transmitter":
				name = TextRender((300,100), "joystix", 35, (200,80,15), ">"+id_img)
				transparent = pygame.Surface((300,100), pygame.SRCALPHA)
				transparent.fill((0,0,0,200))
			else:
				name = TextRender((300,100), "joystix", 30, (160,50,10), id_img)
				transparent = pygame.Surface((300,100), pygame.SRCALPHA)
				transparent.fill((0,0,0,200))
				self.cache[id_portrait].image.fill((255, 255, 255, 140), None, pygame.BLEND_RGBA_MULT)
			self.cache[id_portrait].image.blit(transparent, (20,185))
			self.cache[id_portrait].image.blit(name.next(), (25,181))
		return self.cache[id_portrait]
		
	def show_dialogue(self, *args):
		next_text = self.text_render.next()
		if next_text is None:
			#End of ONE conversation
			self.message = self.dialogues.next()
			if self.message is None:
				#End of Storyscreen (the event is done)
				self.event.done = True
				return None
			characs = []
			if self.message["transmitter"]:
				if self.message["transmitter"] == self.master:
					characs.append(self.portrait_creation("transmitter", (250,160)))
					if self.message["receiver"]:
						characs.append(self.portrait_creation("receiver", (800,160)))
				elif self.message["receiver"] and self.message["receiver"] == self.master: 
					characs.append(self.portrait_creation("transmitter", (800,160)))
					characs.append(self.portrait_creation("receiver", (250,160)))
				elif self.message["receiver"]:
					self.master = self.message["transmitter"]
					characs.append(self.portrait_creation("receiver", (800, 160)))
					characs.append(self.portrait_creation("transmitter", (250, 160)))
				else:
					self.master = self.message["transmitter"]
					characs.append(self.portrait_creation("transmitter", (250, 160)))
				
			self.graphic_elements.clear(self.surface, self.scene_background)
			self.graphic_elements = pygame.sprite.RenderPlain(
				self.dialogue_box, *characs)
			self.text_render = TextRender((904,163), "larabiefont", 25, (255,158,0) , self.message["message"])
			next_text = self.text_render.next()
		self.purge_textbox()
		self.dialogue_box.image.blit(next_text, (10,10))