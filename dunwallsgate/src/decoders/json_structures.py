#!/bin/python3
import json
from decoders.structures import *

class getScene():
    def __init__(self, file):
        self.current_folder = "./config/scenes/%s"%file
        self.scene = Scene()

        with open("%s/%s.json"%(self.current_folder,file), "r", encoding="latin-1") as file:
            self.scene = Scene()
            self.scene = json.load(file, object_hook=self.deserialiseur)
            
    def deserialiseur(self, dct):
        self.background = dct["background"]
        self.events = getEvent(self.current_folder, dct["events"])

    def __str__(self):
        return ("""
                name : %s
                background : %s
                events : %s
                """)%(self.name, self.background, " ".join(self.events))
    
     
def getEvent(current_folder, ref_events):
        events = [Event() for ref_event in ref_events]
        for i, ref_event in enumerate(ref_events):
            with open("%s/events/%s.json"%(current_folder, ref_event), "r", encoding="latin-1") as file:
                dct = json.load(file)
                events[i].conditions = dct['conditions']
                events[i].dialogs = getDialog(current_folder, dct['dialogs'])
                events[i].triggers = dct['triggers']
        return events

def getDialog(current_folder, ref_dialogs):
        with open("%s/events/dialogs/%s.json"%(current_folder, ref_dialogs), "r", encoding="latin-1") as file:
            list_dct = json.load(file)
            dialogs = [Dialog() for dct in list_dct]
            for i, dct in enumerate(list_dct):
                dialogs[i].character = dct['character']
                dialogs[i].message = dct['message']
        return dialogs
