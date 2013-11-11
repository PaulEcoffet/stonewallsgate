#!/bin/python3

import pygame

from window import Window
from screens.homescreen import HomeScreen
from screens.storyscreen import StoryScreen


def main():
    pygame.init()
#   homeScreen = HomeScreen()
#   window = Window(homeScreen)
    storyScreen = StoryScreen()
    window = Window(storyScreen)
    window.run()

if __name__ == "__main__":
    main()
