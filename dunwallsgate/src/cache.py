import pygame
from screens.text_render import TextRender

class CacheSystem():
	"""
	Define a character and its abilities
	"""
	def __init__(self, characters):
		self.portraits = {}
		self.characters = characters
		self.set_portraits()
		
	def set_portraits(self):
		print("ok")
		#Add image in "portraits" list to avoid useless LOADS
		for character in self.characters:
			for _type in ["transmitter", "receiver"]:
				id_portrait = (character.name, _type)
				self.portraits[id_portrait] = pygame.sprite.DirtySprite()
				self.portraits[id_portrait].image = pygame.image.load(character.front_image)
				self.portraits[id_portrait].image = self.portraits[id_portrait].image.convert_alpha()
				self.portraits[id_portrait].image = (pygame.transform.scale(self.portraits[id_portrait].image, (440, 221)))
				if _type == "transmitter":
					name = TextRender((300,100), "joystix", 35, (200,80,15), ">"+character.name)
				else:
					name = TextRender((300,100), "joystix", 30, (160,50,10), character.name)
					self.portraits[id_portrait].image.fill((255, 255, 255, 140), None, pygame.BLEND_RGBA_MULT)
				transparent = pygame.Surface((300,100), pygame.SRCALPHA)
				transparent.fill((0,0,0,200))
				self.portraits[id_portrait].image.blit(transparent, (20,185))
				self.portraits[id_portrait].image.blit(name.next(), (25,181))