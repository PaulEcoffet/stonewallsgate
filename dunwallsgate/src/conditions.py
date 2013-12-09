"""
"""

import inventory

INACTIVE = 0
ACTIVE = 1
VALIDATED = 2

def get_conditions_dict(game):
    """
    Return a dict with all the conditions that can be called from a json object
    """
    return {
        "hero_name": lambda args: game.hero_state["hero_name"],
        "is_item": lambda item: game.hero.inventory.ref_in(inventory.create_item(item)),
        "is_quest_valid": lambda quest: game.hero_state["quests"][quest] == VALIDATED,
        "is_quest_active": lambda quest: game.hero_state["quests"][quest] == ACTIVE,
        "is_quest_inactive": lambda quest: game.hero_state["quests"][quest] == INACTIVE,
        "combat_state": lambda state: game.combat_state == state,
        "is_fellow": lambda ref: game.get_character(ref) in game.hero_companions,
        "max_fellow_not_reached": lambda args: len(game.hero_companions) < 4,
        "is_food": lambda args: game.hero_state["is_food"],
        "is_water": lambda args: game.hero_state["is_water"],
        "is_energy": lambda args: game.hero_state["is_energy"],
        "water_under": lambda args: game.water < args[0]
    }
