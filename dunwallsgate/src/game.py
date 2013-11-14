from screens.storyscreen import StoryScreen

class Game():
    """Contains the current state of the game"""
    
    def __init__(self):
        self.window = None
        self.quests = []
        self.hero = {}
        self.screen = StoryScreen()
    
    def start(self, window):
        self.window = window
        self.window.set_screen(self.screen)
