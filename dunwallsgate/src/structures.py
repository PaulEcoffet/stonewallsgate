#!/bin/python3

class Scene():
    def __init__(self):
        self.events = []  # dct
        self.background = ""

######

class Event():
    def __init__(self):
        self.conditions = {}
        self.dialogues = Dialogues()
        self.battle = None
        self.triggers = {}
        self.done = False

######

class Battle():
    def __init__(self):
        self.allies = []
        self.ennemies = []

######

class Dialogues():
    def __init__(self):
        self.messages = []
        self.begin = True

    def next(self):
        if len(self.messages) > 1 or self.begin:
            if not self.begin:
                del self.messages[0]
            else:
                self.cache = self.messages[:]
                self.begin = False
            return self.messages[0]
        elif len(self.messages) == 1:
            self.messages = []
         
            
    def restore_messages(self):
        try:
            self.messages = self.cache[:]
            self.begin = True
        except AttributeError:
            pass