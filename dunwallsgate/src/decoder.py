import json
import os.path

import data
from structures import Event, Scene, Dialogues

_characters_list = None


def get_character_data(ref):
    global _characters_list
    if not _characters_list:
        with open(
                data.get_config_path("characters.json"), "r", encoding="utf8")\
                as f:
            _characters_list = json.load(f)
    for character in _characters_list:
        if character["ref"] == ref or character["name"] == ref :
            return character


def get_scene(scene_name):
    """
    Get and decode a scene directory and use it to fill the Scene object which
    is return.
    """

    current_folder = data.get_config_path(os.path.join("scenes/", scene_name))
    scene = Scene()
    scene.background = os.path.join(current_folder, "background.png")
    scene.events = get_events(scene_name)
    return scene


def get_events(scene_name):
    """
    Get all the events of a scene
    """
    current_folder = data.get_config_path(os.path.join("scenes/", scene_name))
    events = []
    with open(os.path.join(current_folder, "events.json"), "r",
              encoding="utf8") as events_file:
        json_events = json.load(events_file)
        for json_event in json_events:
            event = Event()
            event.conditions = json_event['conditions']
            event.dialogues = get_dialogues(current_folder,
                                          json_event['dialogs'])
            event.triggers = json_event['triggers']
            events.append(event)
    return events


def get_dialogues(current_folder, ref_dialogues):
    """
    Get and decode the right json dialog file to fill
    each parameters in a Dialogues object that is returned.
    """
    with open(
            os.path.join(current_folder, "dialogues", ref_dialogues + ".json"),
            "r", encoding="latin-1") as dialogues_file:
        json_dialogues = json.load(dialogues_file)
        dialogues = Dialogues()
        for json_dialogue in json_dialogues:
            transmitter = None
            receiver = None
            choices = None
            if "transmitter" in json_dialogue:
                transmitter = json_dialogue["transmitter"]
            if "receiver" in json_dialogue:
                receiver = json_dialogue["receiver"]
            if "choices" in json_dialogue:
                choices = json_dialogue["choices"]
            dialogues.messages.append({"talker" : transmitter,
                                       "hearer" : receiver,
                                       "choices" : choices,
                                       "msg" : json_dialogue["message"]})
    return dialogues
