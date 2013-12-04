import os.path

from decoder import get_character_data
from inventory import Inventory
from data import get_image_path
import inventory


class Character():
    """
    Define a character and its abilities
    """

    def __init__(self, reference=None, **custom):
        if reference:
            data = get_character_data(reference)
        else:
            data = get_character_data("unknown")
        self._health = 0
        self.name = custom.get("name", data["name"])
        self.front_image = get_image_path(os.path.join(
            "characters", custom.get("front_image", data["front_image"])))
        self.back_image = get_image_path(os.path.join(
            "characters", custom.get("back_image", data["back_image"])))
        self.maxhealth = custom.get("maxhealth", data["maxhealth"])
        self.health = custom.get("health", self.maxhealth)
        self.range_attack = custom.get("range_attack", data["range_attack"])
        self.attack = custom.get("attack", data["attack"])
        self.defense = custom.get("defense", data["defense"])
        self.initiative = custom.get("initiative", data["initiative"])
        self.inventory = Inventory(custom.get("inventory", None))
        self.abilities = custom.get("abilities", data["abilities"])
        try:
            self.weapon = self.inventory.weapons[0]  # Take the first
                                                     # weapon found
        except IndexError:
            self.weapon = inventory.create_item("bare_hands")

    @property
    def is_alive(self):
        return self.health > 0

    @property
    def is_dead(self):
        return not self.is_alive

    @property
    def health(self):
        return max(0, min(self._health, self.maxhealth))

    @health.setter
    def health(self, value):
        self._health = max(0, min(value, self.maxhealth))

    def __str__(self):
        return str(self.__dict__)
