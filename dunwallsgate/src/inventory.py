import data

class Inventory():

    def __init__(self, inventory=None):
        if isinstance(inventory, Inventory):
            self = inventory
        elif isinstance(inventory, list):
            self.load_inventory_from_list(inventory)
        elif isinstance(inventory, str):
            self.load_inventory_from_ref(inventory)
        else:
            self._items = []

    def load_inventory_from_list(self, items):
        for item in item:
            self._items.append(create_item(item))

    def load_inventory_from_ref(self, ref):
        with open(get_config_path(os.path.join("inventories", ref+".json"))) \
                as f:
            items_list = json.load(f)
        self.load_inventory_from_list(self, items_list)


# Will be changed to follow a decorator pattern

class Item():
    pass

class QuestItem(Item):
    pass

class Weapon(Item):
    pass

class Consumable(Item):
    pass
