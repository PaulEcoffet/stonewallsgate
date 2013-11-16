from screens.storyscreen import StoryScreen
import quest
from inventory import Inventory


class Game():
    """Contains the current state of the game"""

    def __init__(self):
        self.window = None
        self.quests = quest.get_quests_dict()
        self.base = Base()
        self.hero = {"current_scene": "scene1"}
        self.screen = StoryScreen(self.hero)

    def start(self, window):
        self.window = window
        self.window.set_screen(self.screen)


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
