#!/bin/python3

class Scene():
    def __init__(self):
        self.background = ""  # txt (image?)
        self.events = {}  # dct

######
        
class Event():
    def __init__(self):
        self.conditions = Conditions()
        self.dialogs = [] #list of Dialog()
        self.triggers = []
        self.begin = True
        
    def next_dialog(self):
        if not self.begin:
            print(self.dialogs[0])
            self.dialog_done = []
            self.dialog_done.append(self.dialogs[0])
            del self.dialogs[0]
        else:
            self.begin = False
        if len(self.dialogs) != 0:
            return self.dialogs[0]
        
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

        self.message = []
        self.old_messages = []
        self.begin = True

