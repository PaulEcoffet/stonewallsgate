#!/bin/python3

import pygame
import pygame.locals as pg

pygame.font.init()
FPS = 30

class TextRender():
    """
    It's a text manager which cut a string in multiple panel
    font_size : dictionnary which stocks font_size for each
    type of message.
    """
    
    def __init__(self, box_size, _font, font_size, color, string, custom=None):
        #assert isinstance(font, dict)
        #assert isinstance(box_size, tuple), type(box_size)
        
        self._font = {"type" : _font, "color" : color, "size" : font_size} 
        self.pg_font = pygame.font.SysFont(self._font["type"], self._font["size"])
        letter_size = {"width" : self.pg_font.size(" ")[0], "height": self.pg_font.size(" ")[1]}
        text_size = {"width" : self.pg_font.size(string)[0], "height": letter_size["height"]}

        max_carac = int(box_size[0]/letter_size["width"]) 
        max_lines = int(box_size[1]/letter_size["height"]) 
        line, panel, self.panels = [], [], [""]
        for i, mot in enumerate(string.split(" ")+[""]):
            if len("".join(line)) >= max_carac:
                #if line is full, line is add to panel
                panel.append(" ".join(line))
                line = []
            if i == len(string.split(" ")+[""])-1:
                #check if text is empty
                panel.append(" ".join(line))
                self.panels.append(panel)
            line.append(mot)
            if len(panel) >= max_lines:
                #check if panel is full
                panel.append(" ".join(line))
                self.panels.append(panel)
                panel = []
                line = []
                
    def next(self):
        try:
            del self.panels[0]
            result = []
            for line in self.panels[0]:
                result += [self.pg_font.render(line, 1, self._font["color"])]
            return result
        except IndexError:
            return None
