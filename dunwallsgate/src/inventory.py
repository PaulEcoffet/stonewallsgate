#!/usr/bin/python3

import os.path
import random
import copy
import json

import data


def use_potion(self, target):
    print("using potion on {}, recovering {}hp".format(
        target, self.caracts["heal"]))


action_dict = {"use_potion": use_potion}


class Inventory(object):

    def __init__(self, inventory=None, maxsize=None):
        if maxsize:
            self.maxsize = maxsize
        else:
            self.maxsize = float("+inf")
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
            item_object = Item(item)
            self._items.append(item_object)

    def load_inventory_from_ref(self, ref):
        with open(data.get_config_path(os.path.join(
                "inventories", ref + ".json"))) as f:
            items_list = json.load(f)
        self.load_inventory_from_list(items_list)

    def __contains__(self, other_item):
        for item in self._items:
            if item == other_item:
                return True
        return False

    def add(self, item):
        if self.size + item.weight > self.maxsize:
            raise InventoryFullException()
        self._items.append(item)
        item.inventory = self

    def remove(self, item):
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError("inventory.remove(item): item not in inventory")

    @property
    def items(self):
        return self._items

    @property
    def size(self):
        if self._items:
            return sum((item.weight for item in self._items))
        else:
            return 0


class Item(object):

    """Represent an item."""

    _items_dict = None

    def __init__(self, ref=None, inventory=None):
        self.inventory = inventory
        self.caracts = {}
        if not Item._items_dict:
            Item._load_items_dict()
        if isinstance(ref, str):
            self.ref = ref
            self._compute_caracts(Item._items_dict[ref])

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

    @property
    def weight(self):
        return self.caracts["weight"]

    @classmethod
    def _load_items_dict(cls):
        with open(data.get_config_path("items.json")) as f:
            cls._items_dict = json.load(f)


class Weapon(Item):
    """Represents a weapon"""

    def __init__(self, ref):
        super().__init__(ref)
        self._ammo = None
        self.compatible_ammo = self.caracts["compatible_ammo"]

    @property
    def ammo(self):
        return self._ammo

    @ammo.setter
    def ammo(self, ammo):
        if ammo.ref in self.compatible_ammo:
            self._ammo = ammo
        else:
            raise IncompatibleAmmoException()

    def use_weapon(self):
        if self.can_use_weapon():
            if self.ammo:
                self.ammo.amount -= 1
            return self.weapon_power
        else:
            raise IncompatibleAmmoException()

    def can_use_weapon(self):
        if self.ammo.ref in self.compatible_ammo:
            if self.ammo:
                return self.ammo.amount > 0
            else:
                return True
        else:
            return False

    @property
    def weapon_power(self):
        if self.ammo:
            return self.caracts["power"] * self.ammo.caracts["coef"]
        else:
            return self.caracts["power"]


class Stackable(Item):
    """Represents Stackable item"""
    def __init__(self, ref=None, amount=1, inventory=None):
        super().__init__(ref)
        self._amount = 0
        self.unit_weight = self.caracts["weight"]
        self.amount = amount

    @property
    def amount(self):
        return max(0, self._amount)

    @amount.setter
    def amount(self, value):
        if value < 0:
            raise BelowZeroAmountException()
        if (self.inventory and self.inventory.size +
                (value - self.amount) * self.unit_weight
                > self.inventory.maxsize):
            raise InventoryFullException()
        self._amount = value
        if self.amount == 0 and self.inventory:
            self.inventory.remove(self)

    @property
    def weight(self):
        return self.unit_weight * self.amount


class BelowZeroAmountException(Exception):
    pass


class InventoryFullException(Exception):
    pass


class IncompatibleAmmoException(Exception):
    pass


def test():
    inventory = Inventory(50)
    gun = Weapon("gun")
    inventory.add(gun)
    print("inventory.size = {}".format(inventory.size))
    gun_ammo = Stackable("gun_ammo", 30)
    inventory.add(gun_ammo)
    print("inventory.size = {}".format(inventory.size))
    print(inventory.items)
    gun.ammo = gun_ammo
    for i in range(32):
        try:
            print(gun.use_weapon())
        except IncompatibleAmmoException as e:
            print(repr(e))
    print(inventory.items)

if __name__ == "__main__":
    test()
