from screens.storyscreen import StoryScreen
import quest
from inventory import Inventory
from character import Character


class GameEvent():
    """Define what to do and when during the game"""

    def __init__(self, current_event=get_events("intro"), game):
        self.event = current_event
        self.game = game
        self.game_conditions = conditions.get_conditions_dict(game)
        
    def is_valid(self):
        for condition in self.event.conditions:
            if not self.game_conditions[condition["name"]](condition["params"]):
                return False
        return True

    def start(self):
        if self.event.dialogues:
            for dialogue in self.event.dialogues:
            
        
