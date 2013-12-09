from decoder import get_character_data
from inventory import Inventory
from random import gauss, randint
import inventory


LIST_CARAC = ["name", "maxhealth",
              "range_attack", "attack", "defense", "initiative",
              "abilities"]


class UnexistingCharacterException(Exception):
    pass


class Character(object):
    """
    Define a character and its abilities
    """

    def __init__(self, reference=None, **custom):
        if reference:
            try:
                data = get_character_data(reference)
            except ValueError:
                raise UnexistingCharacterException(
                    "The reference \"{}\" doesn't exist".format(reference))
            else:
                for key in LIST_CARAC:
                    if not key in data:
                        data[key] = get_character_data("unknown")[key]
        else:
            data = get_character_data("unknown")
        self._health = 0
        self._inventory = inventory.Inventory()
        self.name = self.operations(custom.get("name", data["name"]))
        self.maxhealth = self.operations(custom.get(
            "maxhealth", data["maxhealth"]))
        self.health = custom.get("health", self.maxhealth)
        self.range_attack = self.operations(custom.get(
            "range_attack", data["range_attack"]))
        self.attack = self.operations(custom.get(
            "attack", data["attack"]))
        self.defense = self.operations(custom.get(
            "defense", data["defense"]))
        self.initiative = self.operations(custom.get(
            "initiative", data["initiative"]))
        self.inventory = Inventory(custom.get("inventory", None))
        self.abilities = self.operations(custom.get(
            "abilities", data["abilities"]))
        self.ref = reference
        self.inventory.add(inventory.create_item("bare_hands"))
        self.weapon = self.inventory.weapons[0]  # Take the first
                                                 # weapon found

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._inventory = value
        if not self.inventory.ref_in(inventory.create_item("bare_hands")):
            self.inventory.add(inventory.create_item("bare_hands"))

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

    def operations(self, caract):
        if isinstance(caract, dict) and "_random_" in caract:
            if caract["_random_"] == "gauss":
                result = -1
                while not(caract.get("min", 0) <= result
                          and result <= caract.get("max", 10 ** 5)):
                    result = int(gauss(caract["mean"],
                                       caract["deviation"]) / 10) * 10
            elif caract["random"] == "choice":
                if caract["max_items"] < 1:
                    result = caract["items"][randint(0, len(caract["items"]))]
                else:
                    item = None
                    result = None
                    for i in caract["max_items"]:
                        while not item or item in result:
                            item = caract["items"][randint(
                                0, len(caract["items"]))]
                        result.append(item)
            elif caract["random"] == "equiproba":
                caract = int(randint(caract["min"], caract["max"]) / 10) * 10
            return result
        else:
            return caract

    def __str__(self):
        return str(self.__dict__)
