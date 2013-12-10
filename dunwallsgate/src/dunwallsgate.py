# ==============================================================================
"""DUNWALL'S GATE : an interactive fiction game"""
# ==============================================================================
__author__  = "Ecoffet Paul and Rhouzlane Elias"
__version__ = "1.0"
__date__    = "2013-12-11"
# ==============================================================================
#!/bin/python3

import pygame

from window import Window



def main():
    pygame.init()
    window = Window()
    window.run()

if __name__ == "__main__":
    main()
