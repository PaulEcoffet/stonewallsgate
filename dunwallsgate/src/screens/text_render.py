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
        nb_line = 1
        self.nb_panel = 0
        self.box_size = box_size
        self._font = {"type" : _font, "color" : color, "size" : font_size}
        try:
            font_file = get_fonts_path("%s.ttf"%self._font["type"])
            self.pg_font = pygame.font.Font(font_file, self._font["size"])
        except:
            self.pg_font = pygame.font.SysFont("monospace", self._font["size"])
        self.letter_size = {"width" : self.pg_font.size(" ")[0], "height": self.pg_font.size(" ")[1]}
        max_carac = round(box_size[0]/(self.letter_size["width"]), 0)
        max_lines = round(box_size[1]/(self.letter_size["height"]), 0)
        line, panel, self.panels = [], [], []
        if len(string) <= max_carac:
            self.width = len(string)*self.letter_size["width"]
            self.height = self.letter_size["height"]
            panel.append(string)
            self.panels.append(panel)
        else:
            for i, mot in enumerate(string.split(" ")+[""]):
                if len(" ".join(line)) >= max_carac: #Dépassement du seuil de caractère par ligne
                    panel.append(" ".join(line[:-1])) #Ajout de la ligne sans le dernier mot dans le panneau
                    line = line[-1:] #Une nouvelle ligne est créée avec pour élement le mot de trop de l'autre ligne
                    nb_line += 1
                if i == len(string.split(" ")+[""])-1: #On se retrouve au dernier mot du texte (avant le marqueur [""])
                    if len(panel) >= max_lines - 1:
                        self.panels.append(panel) #On ajoute le panneau dans la liste de panneaux            
                        self.panels.append([" ".join(line)]) #On ajoute la ligne dans le panneau
                    else:
                        panel.append(" ".join(line)) #On ajoute la ligne dans le panneau
                        self.panels.append(panel) #On ajoute le panneau dans la liste de panneaux
                    break
                if len(panel) >= max_lines - 1: #Il y a trop de ligne dans le panneau
                    line = line[-1:] 
                    if len(panel) > 0:
                        panel[-1] += ' ...' #on affiche ... si il y a d'autres panels à afficher
                    self.panels.append(panel)
                    panel = []
                line.append(mot)
            self.width = max_carac*self.letter_size["width"]
            self.height = nb_line*self.letter_size["height"]*1.15
            

    def next(self):
        if self.nb_panel < len(self.panels):
            try:
                self.transparent = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            except:
                self.transparent = pygame.Surface(self.box_size, pygame.SRCALPHA)
            self.transparent.fill((0,0,0,0))
            for i, line in enumerate(self.panels[self.nb_panel]):
                render_line = self.pg_font.render(line, 1, self._font["color"])
                if i > 0:
                    self.transparent.blit(render_line, (0,i*self.letter_size["height"]*1.15))
                else:
                    self.transparent.blit(render_line, (0,i*self.letter_size["height"]))
            self.nb_panel += 1
            return self.transparent
        else:
            return None
