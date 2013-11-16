from decoders import character_decoder
from inventory import Inventory


class Character():
    """
    Define a character and its abilities
    """

    def __init__(self, reference=None, **custom):
        if reference:
            data = character_decoder(reference)
        else:
            data = {}
        self.name = custom.get("name", data["name"])
        self.front_image = custom.get("front_image", data["front_image"])
        self.back_image = custom.get("back_image", data["back_image"])
        self.health = custom.get("health", data["health"])
        self.range_attack = custom.get("range_attack", data["range_attack"])
        self.attack = custom.get("attack", data["attack"])
        self.defense = custom.get("defense", data["defense"])
        self.initiative = custom.get("initiative", data["initiative"])
        self.inventory = custom.get("inventory", Inventory(data["inventory"]))
        self.abilities = ["attack", "range_attack"]

    def attack(self, opponent):
        pass

    def range_attack(self, opponent):
        pass
