#!/usr/bin/python3

import os.path
import random
import copy
import json

import data


class Inventory(object):

    def __init__(self, inventory=None, maxsize=None):
        self._items = []
        if maxsize:
            self.maxsize = maxsize
        else:
            self.maxsize = float("+inf")
        if isinstance(inventory, Inventory):
            self = inventory
        elif isinstance(inventory, list):
            self.load_inventory_from_list(inventory)
        elif isinstance(inventory, str):
            self.load_inventory_from_ref(inventory)

    def load_inventory_from_list(self, items):
        """
        Charge un inventaire à partir d'une liste de ref et leurs arguments
        items - La liste de references et paramètres.
                ex : [["crossbow"], ["bolt", 30]]
        """
        for item in items:
            if isinstance(item, list):
                args = item[1:]
                item = item[0]
            else:
                args = []
            item_object = create_item(item, *args)
            self._items.append(item_object)

    def load_inventory_from_ref(self, ref):
        """
        Charge un inventaire depuis une référence d'inventaire situé dans
        data/config/inventories/
        """
        with open(data.get_config_path(os.path.join(
                "inventories", ref + ".json"))) as f:
            items_list = json.load(f)
        self.load_inventory_from_list(items_list)

        return False

    def ref_in(self, ref):
        """
        Détermine si un objet ayant la même référence se situe dans
        l'inventaire
        """
        for item in self.items:
            if item.ref == ref.ref:
                return True
        return False

    def add(self, item):
        """
        Ajoute un item dans l'inventaire
        """
        found = False
        if self.size + item.weight > self.maxsize:
            raise InventoryFullException()
        if isinstance(item, Stackable):
            for current in self.items:
                if item.ref == current.ref:
                    current.amount += item.amount
                    item = current
                    found = True
                    break
            if not found:
                self._items.append(item)
        else:
            self._items.append(item)
        item.inventory = self
        return item

    def remove(self, item):
        """
        Supprime l'item `item` de l'inventaire
        """
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError("inventory.remove(item): item not in inventory")

    @property
    def items(self):
        """
        Retourne la liste de tous les items de l'inventory
        """
        return self._items

    @property
    def weapons(self):
        """
        Retourne la liste de toutes les armes de l'inventory
        """
        return [weapon for weapon in self.items if isinstance(weapon, Weapon)]

    @property
    def size(self):
        """
        Retourne la taille actuelle de l'inventaire
        """
        if self._items:
            return sum((item.weight for item in self._items))
        else:
            return 0

    def get_first(self, ref):
        """Retourne la première occurence de l'item ayant pour ref `ref`"""
        for item in self.items:
            if item.ref == ref:
                return item
        raise ValueError("There is no item with the ref " + ref + " in this "
                         "inventory")

    def get_compatible_ammo(self, weapon):
        """
        Retourne la liste de munitions compatible avec `weapon` présentes
        dans l'inventaire
        """
        ammo_list = []
        for item in self.items:
            if isinstance(item, Ammo) and item.ref in weapon.compatible_ammo:
                ammo_list.append(item)
        if None in weapon.compatible_ammo:
            ammo_list.append(None)
        return ammo_list


def create_item(ref, *args):
    """
    Crée un item avec la sous-class adapté en fonction de sa référence
    et des paramètres donnés
    """
    a = Item.get_item_base(ref)
    if a["type"] == "weapon":
        return Weapon(ref)
    elif a["type"] == "stackable":
        return Stackable(ref, *args)
    elif a["type"] == "ammo":
        return Ammo(ref, *args)
    else:
        return Item(ref)


class Item(object):

    """Represente un item."""

    _items_dict = None

    def __init__(self, ref=None, inventory=None):
        self.inventory = inventory
        self.caracts = {}
        if isinstance(ref, str):
            self.ref = ref
            self._compute_caracts(Item.get_item_base(ref))
        else:
            self.ref = None

    def _compute_caracts(self, base_item):
        """
        Calcule les caractéristique variable d'un item, notamment
        ceux aléatoire
        """
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
        """
        Retourne le poids de l'item
        """
        return self.caracts["weight"]

    @classmethod
    def _load_items_dict(cls):
        """
        Charge l'ensemble des caractéristiques générales des items, avant
        quelles ne soient "calculées"
        """
        with open(data.get_config_path("items.json")) as f:
            cls._items_dict = json.load(f)

    @classmethod
    def get_item_base(cls, ref):
        """
        Retourne l'item général correspondant à la référence `ref`
        """
        if not Item._items_dict:
            Item._load_items_dict()
        return Item._items_dict[ref]


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
        """
        Défini les munitions à utiliser
        """
        if not ammo and None in self.compatible_ammo:
            self._ammo = ammo
        elif ammo.ref in self.compatible_ammo:
            self._ammo = ammo
        else:
            raise IncompatibleAmmoException()

    def use_weapon(self):
        """
        Utilise l'arme et consomme une munition
        """
        if self.can_use_weapon():
            if self.ammo:
                self.ammo.amount -= 1
            return self.weapon_power
        else:
            raise IncompatibleAmmoException()

    def can_use_weapon(self):
        """
        Permet de savoir si l'arme peut être utilisé
        """
        if not self.ammo:
        # No ammo needed
            return self.ammo in self.compatible_ammo
        elif self.ammo.ref in self.compatible_ammo:
            if self.ammo:
                return self.ammo.amount > 0
            else:
                return True
        else:
            return False

    @property
    def weapon_power(self):
        return self.weapon_power_with(self.ammo)

    def weapon_power_with(self, ammo=None):
        """
        Retourne la force de l'arme en fonction des munitions utilisées
        """
        if ammo:
            coef = ammo.caracts["coef"]
        else:
            coef = 1
        return self.caracts["power"] * coef


class Stackable(Item):
    """Represents Stackable item"""
    def __init__(self, ref=None, amount=1, inventory=None):
        super().__init__(ref)
        self._amount = 0
        self.unit_weight = self.caracts["weight"]
        self.amount = amount

    @property
    def amount(self):
        """Retourne la quantité d'items stackables dans l'objet"""
        return max(0, self._amount)

    @amount.setter
    def amount(self, value):
        """Défini la quantité d'items stackables dans l'objet"""
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


class Ammo(Stackable):
    """Classe de munition, équivalente à Stackable"""
    pass


class BelowZeroAmountException(Exception):
    pass


class InventoryFullException(Exception):
    pass


class IncompatibleAmmoException(Exception):
    pass


def test():
    inventory = Inventory("begining_inventory", 50)
    inventory.add(create_item("gun_ammo", 2))
    print("inventory.size = {}".format(inventory.size))
    print(inventory.items)
    for item in inventory.items:
        if isinstance(item, Weapon):
            gun = item
        if isinstance(item, Ammo):
            print(item.caracts["name"])
            gun_ammo = item
    gun.ammo = gun_ammo
    for i in range(32):
        try:
            print(gun.use_weapon())
        except IncompatibleAmmoException as e:
            print(repr(e))
    print(inventory.items)

if __name__ == "__main__":
    test()
