from screens.storyscreen import StoryScreen
import quest, conditions, decoder
from inventory import Inventory
from character import Character


class GameEvent():
	"""Define what to do and when during the game"""

	def __init__(self, game, current_scene=decoder.get_scene("intro")):
		self.scene = current_scene
		self.game = game
		self.game_conditions = conditions.get_conditions_dict(game)
		self.first = True

		#For all events in the scene, check if one event checks all conditions
		self.update()

		#when all events are done, scene is over
		self.end_scene = True
		
	def search_event(self):
		self.event_found = False
		for event in self.scene.events:
			if self.is_valid(event) and not event.done:
				self.event = event
				self.event.background = self.scene.background
				self.event_found = True
				break

	def is_valid(self, event):
		"""Check if event valid all conditions (with game data)"""

		for condition in event.conditions:
			if not self.game_conditions[condition["test"]](condition["params"]):
				return False
		return True

	def update(self):
		"""Launch the screen which correspond with the current event"""
		if self.first or self.event.done:
			self.search_event()
			if self.event_found:
				if self.event.dialogues:
					self.game.screen = StoryScreen(self.game.hero, self.event)
				elif self.event.combat:
					self.game.screen = CombatScreen(self.game.hero, self.event)
				self.game.change_screen()
				self.first = False