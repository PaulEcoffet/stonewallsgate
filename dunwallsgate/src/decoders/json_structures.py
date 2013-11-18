#!/bin/python3

import json
import os.path

from decoders.structures import *
from data import get_config_path


def get_scene(scene_name):
    """
    Get and decode a scene directory and use it to fill the Scene object which
    is return.
    """

    current_folder = get_config_path(os.path.join("scenes/", scene_name))
    scene = Scene()
    scene.background = os.path.join(current_folder, "background.png")
    scene.events = get_events(scene_name)
    return scene


def get_events(scene_name):
    """
    Get all the events of a scene
    """
    current_folder = get_config_path(os.path.join("scenes/", scene_name))
    events = []
    with open(os.path.join(current_folder, "events.json"), "r",
              encoding="utf8") as events_file:
        json_events = json.load(events_file)
        for json_event in json_events:
            event = Event()
            event.conditions = json_event['conditions']
            event.dialogs = get_dialog(current_folder, json_event['dialogs'])
            event.triggers = json_event['triggers']
    return events


def get_dialog(current_folder, ref_dialogs):
    """
    Get and decode the right json dialog file to fill
    each parameters in a Dialog object that is returned.
    """
    with open(
            os.path.join(current_folder, "dialogues", ref_dialogs + ".json"),
            "r", encoding="latin-1") as json_file:
        list_dct = json.load(json_file)
        dialogs = [Dialog() for dct in list_dct]
        for i, dct in enumerate(list_dct):
            dialogs[i].character = dct['character']
            dialogs[i].message = dct['message']
    return dialogs
