from decoder import get_character_data
from inventory import Inventory
from data import get_image_path


class Character():
    """
    Define a character and its abilities
    """

    def __init__(self, reference=None, **custom):
        if reference:
            data = get_character_data(reference)
        else:
            data = get_character_data("unknown")
        self.name = custom.get("name", data["name"])
        self.front_image = get_image_path("characters\%s"%custom.get("front_image", data["front_image"]))
        self.back_image = get_image_path("characters\%s"%custom.get("back_image", data["back_image"]))
        self.maxhealth = custom.get("maxhealth", data["maxhealth"])
        self.health = custom.get("health", self.maxhealth)
        self.range_attack = custom.get("range_attack", data["range_attack"])
        self.attack = custom.get("attack", data["attack"])
        self.defense = custom.get("defense", data["defense"])
        self.initiative = custom.get("initiative", data["initiative"])
        self.inventory = custom.get("inventory", Inventory())
        self.abilities = custom.get("abilities", data["abilities"])

    def attack(self, opponent):
        pass

    def range_attack(self, opponent):
        pass

    def __str__(self):
        return str(self.__dict__)
