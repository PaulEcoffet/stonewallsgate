from screens.storyscreen import StoryScreen
import quest
from inventory import Inventory
from character import Character
from game_event import GameEvent
from cache import CacheSystem
import decoder


class Game():
    """Contient l'état actuel du jeu"""

    def __init__(self):
        self.window = None
        self.screen = None
        self.game_event = None
        self.quests = quest.get_quests_dict()
        self.base = Base()
        self.hero = Character("hero")
        self.hero_state = {"quests": self.quests, "hero_name": "Gordon"}
        self.hero_location = "intro"
        self.characters = [self.hero]
        self.hero_companions = []
        self.combat_state = ""
        self.cache = CacheSystem()
        self.next_scene = "intro"

    def get_character(self, ref):
        """
        Retourne le character demandé s'il existe, sinon, il le crée
        et le retourne
        """
        for charac in self.characters:
            if ref == charac.ref:
                return charac
        self.characters.append(Character(ref))
        return self.characters[-1]

    def start(self, window):
        """
        Démarre le jeu
        """
        self.window = window
        self.game_event = GameEvent(self)

    def change_screen(self):
        """Change l'écran de jeu"""
        self.window.set_screen(self.screen)

    def change_scene(self, scene_name=None):
        """Change la scene en cours"""
        if not scene_name:
            scene_name = self.next_scene
        self.game_event.scene = decoder.get_scene(scene_name)
        self.next_scene = None

class Base():
    """
    Contient l'état de la base du hero
    Cet élément du jeu n'a pas encore été développé
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
