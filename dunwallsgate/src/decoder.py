import json
import data
from structures import *

_characters_list = None


def get_character_data(ref):
    global _characters_list
    if not _characters_list:
        with open(
                data.get_config_path("characters.json"), "r", encoding="utf8")\
                as f:
            _characters_list = json.load(f)
    for character in _characters_list:
        if character["ref"] == ref:
            return character
			
def get_scene(file):
    """
    Get and decode the right json scene file to fill it
    in a Scene object that is return.
    """

    current_folder = data.get_config_path("scenes/{}".format(file))
    scene = Scene()

    with open("%s/%s.json"%(current_folder,file), "r", \
                encoding="latin-1") as file:
        scene = Scene()
        dct = json.load(file)
        scene.background = dct[0]["background"]
        scene.events = get_events(current_folder, dct[0]["events"])
    return scene

def get_events(current_folder, ref_events):
    """
    Get and decode the right json event file to fill
    each parameters of each events in multiple Events
    object that are return in one single list.
    """

    events = [Event() for ref_event in ref_events]
    for i, ref_event in enumerate(ref_events):
        with open("%s/events/%s.json"%(current_folder, ref_event), "r", \
                  encoding="latin-1") as file:
            dct = json.load(file)
            events[i].conditions = dct['conditions']
            events[i].dialogs = get_dialogs(current_folder, dct['dialogs'])
            events[i].triggers = dct['triggers']
    return events

def get_dialogs(current_folder, ref_dialogs):
    """
    Get and decode the right json dialog file to fill
    each parameters in a Dialog object that is return.
    """
    with open("%s/events/dialogs/%s.json"%(current_folder, ref_dialogs), \
              "r", encoding="latin-1") as file:
        list_dct = json.load(file)
        dialogs = Dialogs()
        listener = None
        main_character = None
        for dct in list_dct:
            if 'listener' in dct:
                listener = dct['listener']
            if 'main_character' in dct:
                main_character = dct['main_character']
            dialogs.messages.append((main_character, listener, dct['message']))
    return dialogs
