"""
"heal_hero": game.heal_hero,
"heal_team": game.heal_team,
"give_item_to_hero": game.add_item_to_hero,
"give_item_to_base": game.add_item_to_base,
"add_food": game.add_food,
"add_water": game.add_water,
"add_energy": game.add_energy,
"activate_quest": game.activate_quest,
"lock": game.lock,
"unlock": game.unlock
"""

def get_triggers_dict(game):
	"""
	Return a dict with all the triggers that can be called from a json object
	"""
	return {
			"change_scene": lambda args: game.change_scene(args),
			"print" : lambda args: print(args)
			}