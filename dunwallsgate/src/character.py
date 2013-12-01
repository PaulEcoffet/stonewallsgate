import os.path

from decoder import get_character_data
from inventory import Inventory
from data import get_image_path
from random import gauss, randint
import os.path

class Character():
    """
    Define a character and its abilities
    """

    def __init__(self, reference=None, **custom):
        if reference:
            data = get_character_data(reference)
            for key in ["name", "front_image", "back_image", "maxhealth", "range_attack", "attack", "defense", "initiative", "abilities"]:
                if not key in data:
                    data[key] = get_character_data("unknown")[key]
        else:
            data = get_character_data("unknown")
        self.name = self.operations(custom.get("name", data["name"]))
        self.front_image = get_image_path(os.path.join("characters", self.operations(custom.get("front_image", data["front_image"]))))
        self.back_image = get_image_path(os.path.join("characters", self.operations(custom.get("back_image", data["back_image"]))))
        self.maxhealth = self.operations(custom.get("maxhealth", data["maxhealth"]))
        self.health = custom.get("health", self.maxhealth)
        self.range_attack = self.operations(custom.get("range_attack", data["range_attack"]))
        self.attack = self.operations(custom.get("attack", data["attack"]))
        self.defense = self.operations(custom.get("defense", data["defense"]))
        self.initiative = self.operations(custom.get("initiative", data["initiative"]))
        self.inventory = custom.get("inventory", Inventory())
        self.abilities = self.operations(custom.get("abilities", data["abilities"]))

    def attack(self, opponent):
        pass

    def range_attack(self, opponent):
        pass
        
    def operations(self, caract):
        if isinstance(caract, dict) and "_random_" in caract:
            if caract["_random_"] == "gauss":
                result = -1
                while not caract.get("min", 0) <= result <= caract.get("max", 10**5):
                    result = int(gauss(caract["mean"], caract["deviation"])/10)*10
            elif caract["random"] == "choice":
                if caract["max_items"] < 1:
                    result = caract["items"][randint(0, len(carac["items"]))]
                else:
                    item = None
                    result = None
                    for i in caract["max_items"]:
                        while not item or item in result:
                            item = caract["items"][randint(0, len(carac["items"]))]
                        result.append(item)
            elif caract["random"] == "equiproba": 
                caract = int(randint(caract["min"], caract["max"])/10)*10
            return result
        else:
            return caract
        
    
    def __str__(self):
        return str(self.__dict__)

