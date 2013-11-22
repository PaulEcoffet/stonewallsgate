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
	zone_box = None
	next_btn = None

	def __init__(self, hero, event):
		self.end_scene = True
		self.hero = hero
		self.event = event
		self.end = False

	def start(self, window, eventmanager):
		self.window = window
		self.surface = window.surface
		self.eventmanager = eventmanager
		self.end_scene = True
		self.portraits_cache = {}
		self.img_cache = {}

		self.init_sprites()

		# Sprites placement
		self.dialogue_box.rect = self.dialogue_box.image.get_rect(
			bottomright=(self.surface.get_width()-50,
						 self.surface.get_height()-30))
		self.graphic_elements = pygame.sprite.RenderPlain(self.dialogue_box)

		self.init_story()



	def draw(self):
		if self.end_scene:
			self.surface.blit(self.scene_background, (0, 0))
			transparent = pygame.Surface((230,30), pygame.SRCALPHA)
			transparent.fill((0,0,0,140))
			self.test = TextRender((300,50), "joystix", 20, (255,50,10), 
                                               "ALPHA version")
			transparent.blit(self.test.next(), (5,3))
			self.surface.blit(transparent, (10,10))
			self.end_scene = False
		self.graphic_elements.clear(self.surface, self.scene_background)
		self.graphic_elements.draw(self.surface)

	def init_sprites(self):
		if not self.scene_background:
			self.scene_background = pygame.image.load(self.event.background).convert()
			self.scene_background = (pygame.transform.scale(
				self.scene_background, (1024, 574)))

		if not self.dialogue_box:
			self.dialogue_box = pygame.sprite.DirtySprite()
			self.dialogue_box.image = pygame.image.load(
				data.get_image_path('storyscreen/text_box.png'))
			self.dialogue_box.image = self.dialogue_box.image.convert_alpha()
			self.dialogue_box.image = pygame.transform.scale(self.dialogue_box.image, (924, 163))
			self.dialogue_box.image.set_alpha(0)


	def update_textbox(self):
		self.dialogue_box.size = (924,163)
		self.dialogue_box.size_text = (904,163)
		self.dialogue_box.image = pygame.image.load(
			data.get_image_path('storyscreen/text_box.png'))
		self.dialogue_box.image = self.dialogue_box.image.convert_alpha()
		self.dialogue_box.image = pygame.transform.scale(self.dialogue_box.image, self.dialogue_box.size )
		self.dialogue_box.image.set_alpha(0)
		self.transparent = pygame.Surface(self.dialogue_box.size, pygame.SRCALPHA)
		self.transparent.fill((0,0,0,128))
		self.dialogue_box.image.blit(self.transparent, (0,0))

	def init_story(self):
		self.scene = get_scene("intro")
		self.update_textbox()
		self.dialogue_end = True
		self.dialogues = self.event.dialogues
		self.message = self.dialogues.next()
		self.old_message = None
		self.text_render = TextRender(self.dialogue_box.size_text, "unispace_italic", 20, (255,158,0) , self.message["message"])
		self.show_dialogue()

		# Events registration
		self.eventmanager.on_key_down(self.show_dialogue, pg.K_RIGHT)
		self.eventmanager.on_click_on(self.dialogue_box, self.show_dialogue)

	def portrait_creation(self, type, position):
		#Add image in "cache" list to avoid useless LOADS
		id_image = self.message[type]
		if not id_image in self.img_cache:
			self.img_cache[id_image] = data.get_image_path('characters/%s'%get_character_data(id_image)["front_image"])
		#Add full portrait (text + image + layouts) in "cache" list to avoid useless PROCESS 
		id_portrait = (self.message[type], position)
		if not id_portrait in self.portraits_cache:
			self.portraits_cache[id_portrait] = pygame.sprite.DirtySprite()
			self.portraits_cache[id_portrait].image = pygame.image.load(self.img_cache[id_image])
			self.portraits_cache[id_portrait].image = self.portraits_cache[id_portrait].image.convert_alpha()
			self.portraits_cache[id_portrait].image = (pygame.transform.scale(self.portraits_cache[id_portrait].image, (440, 221)))
			self.portraits_cache[id_portrait].rect = self.portraits_cache[id_portrait].image.get_rect(midtop=position)
			name = TextRender((300,100), "joystix", 35, (160,50,10), self.message["%s"%type])
			transparent = pygame.Surface((300,100), pygame.SRCALPHA)
			transparent.fill((0,0,0,200))
			if type == "receiver":
				self.portraits_cache[id_portrait].image.fill((255, 255, 255, 200), None, pygame.BLEND_RGBA_MULT)
			self.portraits_cache[id_portrait].image.blit(transparent, (20,185))
			self.portraits_cache[id_portrait].image.blit(name.next(), (25,181))
		return self.portraits_cache[id_portrait]
		
	def show_dialogue(self, *args):
		next_text = self.text_render.next()
		if next_text is None:
			self.message = self.dialogues.next()
			if self.message is None:
				self.event.done = True
				return None
			self.text_render = TextRender(self.dialogue_box.size_text, "larabiefont", 25, (255,158,0) , self.message["message"])
			next_text = self.text_render.next()
		self.update_textbox()
		self.dialogue_box.image.blit(next_text, (10,10))
		if self.message != self.old_message:
			self.old_message = self.message
			if self.message["receiver"]:
				charac1 = self.portrait_creation("transmitter", (250,160))
				charac2 = self.portrait_creation("receiver", (800, 160))
				self.graphic_elements = pygame.sprite.RenderPlain(
					self.dialogue_box, charac1, charac2)
			elif self.message["transmitter"]:
				charac1 = self.portrait_creation("transmitter", (250,160))
				self.graphic_elements = pygame.sprite.RenderPlain(
					self.dialogue_box, charac1)
