#!/bin/python3

import pygame
import pygame.locals as pg
from data import get_fonts_path

pygame.font.init()

class TextRender():
    """
    It's a text manager which cut a string in multiple panel
    font_size : dictionnary which stocks font_size for each
    type of message.
    """
    
    def __init__(self, box_size, _font, font_size, color, string, custom=None):
        #assert isinstance(font, dict)
        #assert isinstance(box_size, tuple), type(box_size)
        self.box_size = box_size
        self._font = {"type" : _font, "color" : color, "size" : font_size}
        try:
            font_file = get_fonts_path("%s.ttf"%self._font["type"])
            self.pg_font = pygame.font.Font(font_file, self._font["size"])
        except:
            self.pg_font = pygame.font.SysFont("monospace", self._font["size"])
        self.letter_size = {"width" : self.pg_font.size(" ")[0], "height": self.pg_font.size(" ")[1]}
        max_carac = int(box_size[0]/(self.letter_size["width"]))
        max_lines = int(box_size[1]/(self.letter_size["height"]))
        line, panel, self.panels = [], [], []
        for i, mot in enumerate(string.split(" ")+[""]):
            if len(" ".join(line)) >= max_carac:
                panel.append(" ".join(line[:-1]))
                line = line[-1:]
            if i == len(string.split(" ")+[""])-1:
                panel.append(" ".join(line))
                self.panels.append(panel)
                break
            if len(panel) >= max_lines - 1:
                line = line[-1:]
                panel[-1] += ' ...' #on affiche ... si il y a d'autres panels à afficher
                self.panels.append(panel)
                panel = []
            line.append(mot)
        self.nb_panel = 0
                
    def next(self):
        if self.nb_panel < len(self.panels):
            self.transparent = pygame.Surface(self.box_size, pygame.SRCALPHA)   
            self.transparent.fill((0,0,0,0))
            for i, line in enumerate(self.panels[self.nb_panel]):
                render_line = self.pg_font.render(line, 1, self._font["color"])
                self.transparent.blit(render_line, (0,i*self.letter_size["height"]*1.15))
            self.nb_panel += 1
            return self.transparent
