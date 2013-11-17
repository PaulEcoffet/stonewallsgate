#!/bin/python3

class Scene():
    def __init__(self):
        self.background = ""  # txt (image?)
        self.events = {}  # dct

######
        
class Event():
    def __init__(self):
        self.conditions = Conditions()
        self.dialogs = Dialogs()
        self.triggers = []
        self.begin = True
        

        
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

class Dialogs():
    def __init__(self):
        self.characters = []
        self.messages = []
        self.old_messages = []
        self.begin = True
        
    def next(self):
        if len(self.messages) != 1:
            if not self.begin:
                self.messages_done = []
                self.messages_done.append(self.messages[0])
                del self.messages[0]
            else:
                self.begin = False
            return self.messages[0]
