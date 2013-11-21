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
	charac1 = None
	charac2 = None
	next_btn = None

	def __init__(self, hero, event):
		self.end_scene = True
		self.hero = hero
		self.event = event

	def start(self, window, eventmanager):
		self.window = window
		self.surface = window.surface
		self.eventmanager = eventmanager
		self.end_scene = True

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
			self.test = TextRender((300,100), "joystix", 11, (200,100,10),
								   "Scene de demonstration (Dunwall's Gate)")
			self.surface.blit(self.test.next(), (10,10))
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
			self.dialogue_box.image = pygame.transform.scale(self.dialogue_box.image,
														   (924, 163))
			self.dialogue_box.image.set_alpha(0)
		
		if not self.charac1:
			self.charac1 = pygame.sprite.DirtySprite()
			
		if not self.charac2:
			self.charac2 = pygame.sprite.DirtySprite()


	def update_textbox(self):
		self.dialogue_box.size = (924,163)
		self.dialogue_box.size_text = (904,163)
		self.dialogue_box.image = pygame.image.load(
			data.get_image_path('storyscreen/text_box.png'))
		self.dialogue_box.image = self.dialogue_box.image.convert_alpha()
		self.dialogue_box.image = pygame.transform.scale(self.dialogue_box.image,
													   self.dialogue_box.size )
		self.dialogue_box.image.set_alpha(0)
		self.transparent = pygame.Surface(self.dialogue_box.size,
										  pygame.SRCALPHA)
		self.transparent.fill((0,0,0,128))
		self.dialogue_box.image.blit(self.transparent, (0,0))

	def init_story(self):
		self.scene = get_scene("intro")
		self.update_textbox()
		self.event = self.scene.events[0]
		self.dialogue_end = True
		self.dialogues = self.event.dialogues
		self.message = self.dialogues.next()
		self.old_message = None
		self.text_render = TextRender(self.dialogue_box.size_text, "unispace_italic",
									  20, (255,158,0) , self.message["message"])
		self.show_dialogue()

		# Events registration
		self.eventmanager.on_key_down(self.show_dialogue, pg.K_RIGHT)
		self.eventmanager.on_click_on(self.dialogue_box,
									  self.show_dialogue)

	def show_dialogue(self, *args):
		next_text = self.text_render.next()
		if next_text is None:
			self.message = self.dialogues.next()
			if self.message is None:
				return None
			self.text_render = TextRender(self.dialogue_box.size_text, "larabiefont",
										  25, (255,158,0) , self.message["message"])
			next_text = self.text_render.next()
		self.update_textbox()
		self.dialogue_box.image.blit(next_text, (10,10))
		if self.message != self.old_message:
			self.old_message = self.message
			if self.message["receiver"]:
				img = data.get_image_path('characters/%s'%get_character_data(self.message["transmitter"])["front_image"])
				self.charac1.image = pygame.image.load(img)
				self.charac1.image = self.charac1.image.convert_alpha()
				self.charac1.image = (pygame.transform.scale(self.charac1.image,
															(440, 221)))
				self.charac1.rect = self.charac1.image.get_rect(midtop=(250, 160))
				img = data.get_image_path('characters/%s'%get_character_data(self.message["receiver"])["front_image"])
				self.charac2.image = pygame.image.load(img)
				self.charac2.image = self.charac2.image.convert_alpha()
				self.charac2.image = (pygame.transform.scale(self.charac2.image,
															(440, 221)))
				self.charac2.rect = self.charac2.image.get_rect(midtop=(750, 160))
				self.graphic_elements = pygame.sprite.RenderPlain(
					self.dialogue_box, self.charac1, self.charac2)
			elif self.message["transmitter"]:
				img = data.get_image_path('characters/%s'%get_character_data(self.message["transmitter"])["front_image"])
				self.charac1.image = pygame.image.load(img)
				self.charac1.image = self.charac1.image.convert_alpha()
				self.charac1.image = (pygame.transform.scale(self.charac1.image,
															(440, 221)))
				self.charac1.rect = self.charac1.image.get_rect(midtop=(250, 160))
				self.graphic_elements = pygame.sprite.RenderPlain(
					self.dialogue_box, self.charac1)



