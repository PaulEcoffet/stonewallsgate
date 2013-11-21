from screens.storyscreen import StoryScreen
import quest, conditions, decoder, triggers
from inventory import Inventory
from character import Character


class GameEvent():
	"""Define what to do and when during the game"""

	def __init__(self, game, current_scene=decoder.get_scene("intro")):
		self.scene = current_scene
		self.game = game
		self.game_conditions = conditions.get_conditions_dict(game)
		self.game_triggers = triggers.get_triggers_dict(game)
		self.start = True
		
	def search_event(self):
		self.event_found = False
		for event in self.scene.events:
			#Look if event have been done and if it is valid (PS: event.done is set True in the end of StoryScreen)
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
		
	def execute_triggers(self, event):
		for trigger in event.triggers:
			self.game_triggers[trigger["trigger"]](trigger["params"])

	def update(self):
		"""Update every 30sec the screen to be sure that it correspond with the current event (check window.py)"""
		#If it's the first update or if previous event are done, search new event and execute it (with triggers)
		if self.start or self.event.done:
			self.search_event()
			if self.event_found:
				if self.event.dialogues:
					self.game.screen = StoryScreen(self.game.hero, self.event)
				elif self.event.combat:
					self.game.screen = CombatScreen(self.game.hero, self.event)
				self.game.change_screen()
				self.execute_triggers(self.event) #may change the screen (Check game.change_scene function)
				self.start = False