from screens.storyscreen import StoryScreen
import quest, conditions, decoder, triggers
from inventory import Inventory
from character import Character


class GameEvent():
    """Define what to do and when during the game"""

    def __init__(self, game, current_scene=decoder.get_scene("intro")):
        self.scene = current_scene
        self.game = game
        self.game_conditions = conditions.get_conditions_dict(game)
        self.game_triggers = triggers.get_triggers_dict(game)
        self.start = True
        self.event_done = False

    def search_event(self):
        if self.game.restart_event:
            self.event_done = False
            self.game.restart_event = False
            if self.event.dialogues:
                self.event.dialogues.restore_messages()
            return True
        for event in self.scene.events:
            #Look if event have been done and if it is valid (PS: event.done is set True in the end of StoryScreen)
            if self.is_valid(event):
                self.event = event
                self.event.background = self.scene.background
                self.event_done = False
                return True
        return False

    def is_valid(self, event):
        """Check if event valid all conditions (with game data)"""
        for condition in event.conditions:
            if not self.game_conditions[condition["test"]](condition["params"]):
                return False
        return True

    def execute_triggers(self, event):
        for trigger in event.triggers:
            self.game_triggers[trigger["trigger"]](trigger.get("params", None))

    def update(self):
        """Update every 30sec the screen to be sure that it correspond with the current event (check window.py)"""
        if self.game.screen and self.game.screen.end:
            self.event_done = True
            self.execute_triggers(self.event) #on execute les triggers à la fin d'un evenement après le combat ou les cinématiques
        #If it's the first update or if previous event are done, search new event and execute it (with triggers)
        if (self.start or self.event_done) and self.search_event():
            if self.event.dialogues and self.event.dialogues.messages:
                self.game.screen = StoryScreen(self.game, self.event)
                self.game.change_screen()
            elif False and self.event.combat:
                self.game.screen = CombatScreen(self.game, self.event)
                self.game.change_screen()
            elif self.event.triggers:
                self.execute_triggers(self.event) #si l'evenement contient uniquement des triggers
                self.event_done = True
            if self.start:
                self.start = False