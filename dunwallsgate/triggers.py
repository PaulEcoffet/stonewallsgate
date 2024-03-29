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

import screens
import inventory

INACTIVE = 0
ACTIVE = 1
VALIDATED = 2


def get_triggers_dict(game):
    """
    Return a dict with all the triggers that can be called from a json object
    """
    return {
        "active_quest": lambda quest: active_quest(game, quest),
        "valid_quest": lambda quest: valid_quest(game, quest),
        "add_item": lambda item: add_item(game, item),
        "add_fellow": lambda ref: game.hero_companions.append(game.get_character(ref)),
        "inactive_quest": lambda quest: inactive_quest(game, quest),
        "switch_scene": lambda name: switch_scene(game, name),
        "modif_health": lambda args: add_health(game.get_character(args[0]), args[1]),
        "def_next_scene": lambda name: def_next_scene(game, name),
        "restart_event": lambda args: restart_event(game),
        "force_stop_event": lambda args: force_stop_event(game),
    }

def add_health(charac, hp):
    charac.health += hp

def add_item(game, item):
    if isinstance(item, list):
        args = item[1:]
        item = item[0]
    else:
        args = []
    try:
        game.hero.inventory.add(inventory.create_item(item, *args))
    except inventory.InventoryFullException:
        print("Fail: {}".format(e))


def def_next_scene(game, name):
    """ Utilisé via un choix notamment ou à la fin d'un combat (perdu/gagné) - On force le changement de scène """
    game.next_scene = name


def switch_scene(game, name):
    """ Si on forçage de changement de scène est en cours, sinon on met la scène par défaut """
    if game.next_scene:
         game.change_scene(game.next_scene)
    else:
         assert isinstance(name, str), "Aucune scène n'a été mise en paramètre ni dans events.json ni dans les dialogues, ni dans les combats (pourtant un switch_scene a été demandé => vérifiez vos JSON)"
         game.change_scene(name)


def active_quest(game, quest):
    game.hero_state["quests"][quest] = ACTIVE


def valid_quest(game, quest):
    game.hero_state["quests"][quest] = VALIDATED


def inactive_quest(game, quest):
    game.hero_state["quests"][quest] = INACTIVE


def restart_event(game):
    game.screen.restart_event= True


def force_stop_event(game):
    game.game_event.event_done = True
