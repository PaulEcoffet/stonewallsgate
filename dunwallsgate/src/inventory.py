#!/usr/bin/python3

import os.path
import random
import copy
import json

import data


class Inventory(object):

    def __init__(self, inventory=None):
        if isinstance(inventory, Inventory):
            self.inventory = inventory
        elif isinstance(inventory, list):
            self.load_inventory_from_list(inventory)
        elif isinstance(inventory, str):
            self.load_inventory_from_ref(inventory)
        else:
            self._items = []

    def load_inventory_from_list(self, items):
        for item in items:
            item_object = create_item(item, self)
            self._items.append(item_object)

    def load_inventory_from_ref(self, ref):
        with open(data.get_config_path(os.path.join(
                "inventories", ref + ".json"))) as f:
            items_list = json.load(f)
        self.load_inventory_from_list(items_list)

    def is_inside(self, other_item):
        for item in self._items:
            if item == other_item:
                return True
        return False


def create_item(item, inventory):
    return None


class Item(object):

    """Represent an item."""

    _items_dict = None

    def __init__(self, ref=None, inventory=None):
        self.caracts = {}
        if not Item._items_dict:
            Item._load_items_dict()
        if isinstance(ref, str):
            self.ref = ref
            self._compute_caracts(Item._items_dict[ref])
        self.inventory = inventory

    def _compute_caracts(self, base_item):
        item_caracts = copy.copy(base_item)
        for caract in item_caracts.keys():
            if isinstance(caract, dict) and "_random_" in caract:
                if caract["random"] == "gauss":
                    item_caracts[caract] = random.gauss(
                        caract["mean"], caract["deviation"])
                else:
                    item_caracts[caract] = random.randint(
                        caract["min"], caract["max"])
        self.caracts = item_caracts

    @classmethod
    def _load_items_dict(cls):
        pass


class ItemDecorator(Item):

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.caracts = item.caracts


class Consumable(ItemDecorator):

    def __init__(self, item, amount=1):
        super().__init__(item)
        self._amount = 0
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = max(0, value)
        if self._amount == 0 and self.inventory:
            self.inventory.remove(self)

    @amount.deleter
    def amount(self):
        del self._amount


class Ammo(Consumable):

    def __init__(self, item, weapon_compatibility=None, amount=1):
        super().__init__(item, amount)
        if weapon_compatibility:
            self.caracts["weapon_compatibility"] = weapon_compatibility


class Usable(ItemDecorator):

    def __init__(self, item, action, consumable=None, infight=True,
                 outoffight=False):
        super().__init__(item)
        self.can_be_used_in_fight = infight
        self.can_be_used_out_of_fight = outoffight
        self._use = action
        self.consumable = consumable

    def is_usable(self, infight):
        if self.consumable and self.consumable.amount <= 0:
            return False
        if infight and self.can_be_used_in_fight:
            return True
        elif not infight and self.can_be_used_out_of_fight:
            return False

    def use(self, *args, **kwargs):
        if self.consumable and self.consumable.amount <= 0:
            raise CantBeUsedException("There is no consumable")
        else:
            self.consumable.amount -= 1
            self._use(*args, **kwargs)


class CantBeUsedException(Exception):
    pass


class Weapon(Usable):

    def __init__(self, item, type_, consumable=None):
        super().__init__(item, self.attack, None, True, False)
        self.consumable = consumable

    def attack(self, other):
        print("using weapon on {}".format(other))


def test():
    inventory = Inventory()
    ammo = Ammo(Item(), None, 30)
    print(ammo.amount)
    ammo.amount -= 1
    print(ammo.amount)
    print("isinstance(ammo, Ammo): {}".format(
        isinstance(ammo, Ammo)))
    print("isinstance(ammo, Consumable): {}".format(
        isinstance(ammo, Consumable)))
    print("isinstance(item, Item): {}".format(
        isinstance(ammo, Item)))

    potion = Usable(Consumable(Item(), 3), lambda e: print("using potion"))
    print("isinstance(potion.item, Consumable): {}".format(
        isinstance(potion.item, Consumable)))
    potion.consumable = potion.item
    for dummy in range(4):
        try:
            potion.use(True)
        except CantBeUsedException as e:
            print("Expected exception: {}".format(e))

    gun = Weapon(Item(), "all", ammo)
    for dummy in range(31):
        try:
            gun.use("bad guy")
        except CantBeUsedException as e:
            print("Expected exception: {}".format(e))

if __name__ == "__main__":
    test()
