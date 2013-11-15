from screens.storyscreen import StoryScreen

class Game():
    """Contains the current state of the game"""
    
    def __init__(self):
        self.window = None
        self.quests = []
        self.hero = {"current_scene" : "scene1"}
        self.screen = StoryScreen(self.hero)
    
    def start(self, window):
        self.window = window
        self.window.set_screen(self.screen)
