#!/bin/python3

class Event():
    pass

class Scene():
    def __init__(self):
        self.background = ""  # txt (image?)
        self.events = {}  # dct

<<<<<<< HEAD
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
=======
>>>>>>> 78c7f4051a12a33dee70e3112714b5bcdaacfb65

class Dialog():
    def __init__(self):
        self.character = ""
<<<<<<< HEAD
        self.message = []
        self.old_messages = []
        self.begin = True
        
    """def next(self):
        if self.begin:
            self.begin = False
        else:
            self.old_messages.append(self.messages[0])
            print(self.messages[0])
            del self.messages[0]

        return self.messages[0]
    
    def previous(self):
        if len(self.old_messages) > 0:
            self.messages.append(self.old_messages[len(self.old_messages)-1])
            del self.old_messages[len(self.old_messages)-1]
            return self.next()"""

######
=======
        self.message = ""
>>>>>>> 78c7f4051a12a33dee70e3112714b5bcdaacfb65
