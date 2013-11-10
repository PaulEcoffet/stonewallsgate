#!/bin/python3
import json

class Scene():
    def __init__(self, name=""):
        self.name = name
        self.background = ""
        self.events = []
        self.getJson()
        
    def deserialiseur(self, dct):
        self.background = dct["background"]
        self.events = dct["events"]
                
    def getJson(self):
        with open("../config/%s.json"%self.name, "r", encoding="utf-8") as file:
            self = json.load(file, object_hook=self.deserialiseur)
            
    def __str__(self):
        return ("""
                name : %s
                background : %s
                events : %s
                """)%(self.name, self.background, " ".join(self.events))
    
print(Scene("scene_structure"))

class Dialog():
    def __init__(self, name=""):
        self.name = name
        self.dialogs = ()
        self.getJson()
                
    def getJson(self):
        with open("../config/%s.json"%self.name, "r", encoding="utf-8") as file:
            for dict in json.load(file):
                self.character = dict["character"]
                self.message = dict["message"]
                self.dialogs += (self.character, self.message)

    def __str__(self):
        return ("""
                name : %s
                dialogs : %s
                """)%(self.name, self.dialogs)
    
print(Dialog("dialog_structure"))

class Quest():
    def __init__(self, name=""):
        self.name = name
        self.quest_name = ""
        self.failure_conditions = []
        self.on_success = []
        self.on_failure = []
        self.getJson()
        
    def deserialiseur(self, dct):
        self.quest_name = dct["quest_name"]
        self.failure_conditions = dct["failure_conditions"]
        self.on_success = dct["on_success"]
        self.on_failure = dct["on_failure"]
        
    def getJson(self):
        with open("../config/%s.json"%self.name, "r", encoding="utf-8") as file:
            self = json.load(file, object_hook=self.deserialiseur)
            
    def __str__(self):
        return ("""
                name : %s
                quest_name : %s
                failure_conditions : %s
                on_success : %s
                on_failure : %s
                """)%(self.name, self.quest_name, " ".join(self.failure_conditions),
                      " ".join(self.on_success), " ".join(self.on_failure))
    
class Event():
    def __init__(self, name=""):
        self.name = name
        self.conditions = []
        self.dialogue = ""
        self.triggers = []
        self.getJson()
        
    def deserialiseur(self, dct):
        print(dct)
        self.conditions = dct["conditions"]
        self.dialogue = dct["dialogue"]
        self.triggers = dct["triggers"]
                
    def getJson(self):
        with open("../config/%s.json"%self.name, "r", encoding="utf-8") as file:
            self = json.load(file, object_hook=self.deserialiseur)
            
    def __str__(self):
        return ("""
                name : %s
                conditions : %s
                dialogue : %s
                triggers : %s
                """)%(self.name, " ".join(self.conditions), self.dialogue,
                                                    " ".join(self.triggers))

