#!/bin/python3

import pygame

from window import Window
from homescreen import HomeScreen


def main():
    pygame.init()
    homeScreen = HomeScreen()
    window = Window(homeScreen)
    window.run()

if __name__ == "__main__":
    main()
