"""
"""

def get_conditions_dict(game):
    """
    Return a dict with all the conditions that can be called from a json object
    """
    return {"is_lock": lambda args: game.hero_state["is_lock"],
            "life_under_10%": lambda args: game.hero_state["life_under_10"],
            "is_key_item": lambda args: game.hero_state["is_key_item"],
            "has_fellow": lambda args: args[0] in game.hero_fellows,
            "is_food": lambda args: game.hero_state["is_food"],
            "is_water": lambda args: game.hero_state["is_water"],
            "is_energy": lambda args: game.hero_state["is_energy"],
			"water_under": lambda args: game.water < args[0]
            }
