#!/bin/python3

class Character():
    def __init__(self):
        self.nom = ""
        self.hp = 0
    
######

class Scene():
    def __init__(self):
        self.background = "" #txt (image?)
        self.events = {} #dct

######
        
class Event():
    def __init__(self):
        self.conditions = Conditions()
        self.dialogs = [] #list of Dialog()
        self.triggers = []

class Conditions():
    def __init__(self):
        self.test = ""
        self.params = []
        self.param = ""
        
class Triggers():
    def __init__(self):
        self.trigger = ""
        self.params = []
        
######
        
class Dialog():
    def __init__(self):
        self.character = ""
        self.message = ""
######
        
