#!/bin/python3

import json

from decoders.structures import *

def get_scene(file):
    """
    Get and decode the right json scene file to fill it
    in a Scene object that is return.
    """
    
    current_folder = "./config/scenes/%s"%file
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
            events[i].dialogs = getDialog(current_folder, dct['dialogs'])
            events[i].triggers = dct['triggers']
    return events

def get_dialog(current_folder, ref_dialogs):
    """
    Get and decode the right json dialog file to fill
    each parameters in a Dialog object that is return.
    """
    
        with open("%s/events/dialogs/%s.json"%(current_folder, ref_dialogs), \
                  "r", encoding="latin-1") as file:
            list_dct = json.load(file)
            dialogs = [Dialog() for dct in list_dct]
            for i, dct in enumerate(list_dct):
                dialogs[i].character = dct['character']
                dialogs[i].message = dct['message']
        return dialogs
