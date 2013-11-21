from screens.storyscreen import StoryScreen
import quest
from inventory import Inventory
from character import Character
from game_event import GameEvent
import decoder


class Game():
	"""Contains the current state of the game"""

	def __init__(self):
		self.window = None
		self.screen = None
		self.game_event = None
		self.quests = quest.get_quests_dict()
		self.base = Base()
		self.hero = Character("hero")
		self.hero_state = {"is_true" : "true", "hero_name" : "Gordon"}
		self.hero_location = "intro"
		self.hero_companions = []

	def start(self, window):
		self.window = window
		self.game_event = GameEvent(self)
		
	def change_screen(self):
		self.window.set_screen(self.screen)
	
	def change_scene(self, scene):
		self.game_event.scene = decoder.get_scene(scene)

class Base():
	"""
	Contains the state of the base of the hero.
	"""

	def __init__(self, food=0, water=0, energy=0, inventory=None):
		self._food = food
		self._water = water
		self._energy = energy
		if inventory:
			self.inventory = inventory
		else:
			self.inventory = Inventory()
		self.characters = []
