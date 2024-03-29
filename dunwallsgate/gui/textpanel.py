#!/usr/bin/python3
"""
Render a text in one or several panels.

Uses freetype to render text on any surface with word wraping in one or
several panels that can be switched easily

"""

import math
import pygame
import pygame.freetype
from data import get_fonts_path

INF = float("+inf")


def _wrap_word(line, font, box):
    if line == "":
        return []
    elif font.get_rect(line).width <= box[0]:
        return [line]
    else:
        cur_line = ""
        next_line = line
        while font.get_rect(cur_line).width <= box[0]:
            linesplit = next_line.split(" ", 1)
            cur_line += linesplit[0] + " "
            if len(linesplit) > 1:
                next_line = linesplit[1]
            else:
                next_line = ""
        cur_line = cur_line.strip()  # Remove the " " at the end
        linesplit = cur_line.rsplit(" ", 1)
        cur_line = linesplit[0].strip()
        if len(linesplit) > 1:  # If it's not the word that's too big
            next_line = linesplit[1] + " " + next_line
        next_line = next_line.strip()
        return [cur_line] + _wrap_word(next_line, font, box)


class TextPanel(pygame.sprite.DirtySprite):

    """
    It's a text manager which cut a string in multiple panel.

    font_size: dictionnary which stocks font_size for each
    type of message.

    """

    _font_cache = {}

    def __init__(self, text, **options):
        self.realtext = text
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.image = None
        self._cursor_char = 0
        self.cursor_line = 0
        self.panel_first_line_index = 0
        self.color = pygame.Color(*options.get("color", (0, 0, 0)))
        font_tuple = options.get("font", ("larabiefont", 15))
        self.font = TextPanel._font_cache.get(font_tuple,
                                              TextPanel._load_font(font_tuple))
        self.font.origin = True
        self.box = options.get("box", (options.get("width", INF),
                               options.get("height", INF)))
        self.lines = self._create_lines()
        self.line_interval = math.ceil(self.font.get_sized_height() + 2)
        self.lines_per_panel = self.box[1] / self.line_interval
        if self.lines_per_panel != INF:
            self.lines_per_panel = int(self.lines_per_panel)
        self._current_panel_index = 0
        self.cursor_char = 0
        self.update_image()

    def _create_lines(self):
        if not self.font:  # pragma: no coverage
            raise TypeError("Current font is not valid")
        final_lines = []
        for line in self.realtext.splitlines():
            final_lines.extend(_wrap_word(line, self.font, self.box))
        return final_lines

    @property
    def current_panel_index(self):
        return int(self.panel_first_line_index / self.lines_per_panel)

    @current_panel_index.setter
    def current_panel_index(self, value):
        if not isinstance(value, int):
            raise ValueError("Value for current_panel_index should be a int"
                             "not a {}".format(type(value)))
        if value >= math.ceil(len(self.lines) / self.lines_per_panel):
            raise ValueError("There is less than {} panels".format(value - 1))
        if value >= 0:
            self.panel_first_line_index = value * self.lines_per_panel
        else:
            self.panel_first_line_index = max(
                0, len(self.lines) - (abs(value) * self.lines_per_panel))
        self.cursor_line = self.panel_first_line_index
        self.cursor_char = 0

    def next(self, to_end=False):
        self.current_panel_index += 1
        if to_end:
            self.to_end()
        else:
            self.update_image()

    def prev(self, to_end=False):
        self.current_panel_index = max(0, self.current_panel_index - 1)
        if to_end:
            self.to_end()
        else:
            self.update_image()

    def to_end(self):
        self.cursor_line = self.panel_last_line_index
        self.cursor_char = len(self.lines[self.panel_last_line_index]) - 1
        self.update_image()

    def update(self, **options):
        to_end = options.get("to_end", False)
        if not to_end and not self.anim_has_ended:
            self.cursor_char += 1
            self.update_image()
        elif to_end:
            self.to_end()

    def update_image(self):
        if self.lines_per_panel == INF:
            lines_to_draw = self.lines[self.panel_first_line_index:]
        else:
            lines_to_draw = self.lines[self.panel_first_line_index:
                                       self.panel_last_line_index + 1]
        width = max([self.font.get_rect(text).width
                     for text in lines_to_draw])
        height = self.line_interval * len(lines_to_draw)
        bg = pygame.Surface((width, height)).convert_alpha()
        bg.fill((255, 255, 255, 0))
        for i, line in enumerate(lines_to_draw):
            pos = (0, i * self.line_interval + self.font.get_sized_ascender())
            if i + self.panel_first_line_index > self.cursor_line:
                break
            elif i + self.panel_first_line_index == self.cursor_line:
                stop = self.cursor_char + 1
            else:
                stop = len(line)
            self.font.render_to(bg, pos, line[:stop], self.color)
        self.image = bg
        self.rect.size = (width, height)

    @property
    def anim_has_ended(self):
        return self.cursor_line == self.panel_last_line_index and \
            self.cursor_char == \
            len(self.lines[self.panel_last_line_index]) - 1

    @property
    def panel_last_line_index(self):
        return min(self.panel_first_line_index + self.lines_per_panel - 1,
                   len(self.lines) - 1)

    @property
    def has_next(self):
        return self.panel_last_line_index < len(self.lines) - 1

    @property
    def cursor_char(self):
        return self._cursor_char

    @cursor_char.setter
    def cursor_char(self, value):
        self._cursor_char = value
        while self._cursor_char >= len(self.lines[self.cursor_line]):
                self.cursor_line += 1
                self._cursor_char = 0

    @classmethod
    def _load_font(cls, font_tuple):
        if font_tuple not in cls._font_cache:
            try:
                cls._font_cache[font_tuple] = pygame.freetype.Font(
                    get_fonts_path("{}.ttf".format(font_tuple[0])),
                    font_tuple[1])
            except OSError as e:
                print("fail while loading {} : {}".format(font_tuple, e))
                print("Loading larabiefont instead")
                cls._font_cache[font_tuple] = pygame.freetype.Font(
                    get_fonts_path("{}.ttf".format("larabiefont")),
                    font_tuple[1])
        return cls._font_cache[font_tuple]
