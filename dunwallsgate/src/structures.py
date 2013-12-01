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
        self.triggers = {}
        self.done = False

######

class Dialogues():
    def __init__(self):
        self.messages = []
        self.begin = True

    def next(self):
        if len(self.messages) != 1:
            if not self.begin:
                del self.messages[0]
            else:
                self.cache = self.messages[:]
                self.begin = False
            return self.messages[0]
            
    def restore_messages(self):
        try:
            self.messages =  [""] + self.cache[:]
        except AttributeError:
            pass