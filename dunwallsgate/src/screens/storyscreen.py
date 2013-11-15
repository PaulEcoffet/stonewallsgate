#!/bin/python3


import pygame

from decoders.json_structures import *
from data import get_image_path


class StoryScreen():
    """
    The story screen of the game.
    """

    scene_background = None
    text_box = None
    zone_box = None
    charac = None

    def __init__(self, hero):
        self.end_scene = True
        self.hero = hero

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.end_scene = True

        self.init_sprites()

        # Sprites placement
        self.text_box.rect = self.text_box.image.get_rect(
            bottomright=(self.surface.get_width(),
                         self.surface.get_height()))
        self.zone_box.rect = self.zone_box.image.get_rect(
            topleft=(0, 0))
        self.charac.rect = self.charac.image.get_rect(midtop=(250, 140))
        self.graphic_elements = pygame.sprite.RenderPlain(self.text_box,
                                                 self.zone_box, self.charac)
        self.set_scene(self.hero["current_scene"])

    def draw(self):
        if self.end_scene:
            self.surface.blit(self.scene_background, (0, 0))
            self.end_scene = False
        self.graphic_elements.clear(self.surface, self.scene_background)
        self.graphic_elements.draw(self.surface)

    def shutdown(self):
        """
        Shutdown screen playing (fill a black screen)
        Underconstruction : Remove all events and spirits from this screen.
        """
        self.surface.fill(0)

    def init_sprites(self):
        if not self.scene_background:
            self.scene_background = pygame.image.load(
                get_image_path('storyscreen/background/demo.jpg')).convert()
            self.scene_background = (pygame.transform.scale(
                self.scene_background, (1024, 361)))
        if not self.text_box:
            self.text_box = pygame.sprite.DirtySprite()
            self.text_box.image = pygame.image.load(
                get_image_path('storyscreen/text_box.png')).convert()
            self.text_box.image = (pygame.transform.scale(self.text_box.image,
                                                          (1024, 213)))
        if not self.zone_box:
            self.zone_box = pygame.sprite.DirtySprite()
            self.zone_box.image = pygame.image.load(
                get_image_path('storyscreen/zone_box.png')).convert()
            self.zone_box.image = (pygame.transform.scale(self.zone_box.image,
                                                          (249, 36)))
        if not self.charac:
            self.charac = pygame.sprite.DirtySprite()
            self.charac.image = pygame.image.load(
                get_image_path('storyscreen/characters/unknown.png'))
            self.charac.image = self.charac.image.convert_alpha()
            self.charac.image = (pygame.transform.scale(self.charac.image,
                                                        (273, 221)))

    def set_scene(self, entry):
        self.current_scene = get_scene(entry)
        self.scene_background = pygame.image.load(
            get_image_path('storyscreen/background/%s.jpg' %
                           self.current_scene.background)
        ).convert()
        self.scene_background = (pygame.transform.scale(
            self.scene_background, (1024, 361)))

        self.event = self.findProperEvent(self.current_scene.events)
        self.showDialog()
        self.eventmanager.on_key_down(self.showDialog)

    def showDialog(self, *args):
        try:
            self.dialog = self.event.dialogs[0]
            self.text_box.image = pygame.image.load(
                '../data/images/storyscreen/text_box.png').convert()
            self.text_box.image = (pygame.transform.scale(self.text_box.image,
                                                          (1024, 213)))
            self.render_text(self.dialog.character,
                             pygame.font.SysFont("monospace", 30),
                             (255, 255, 0), (20, 0))
            self.render_text(self.dialog.message,
                             pygame.font.SysFont("monospace", 25),
                             (255, 200, 10), (20, 38))
            del self.event.dialogs[0]
        except:
            self.end_scene = True
            self.set_scene("scene2")

    def render_text(self, string, font, color, placement):
        requested_lines = string.splitlines()
        for requested_line in requested_lines:
            if requested_line != "":
                tempsurface = font.render(requested_line, 1, color)
                placement = list(placement)
                placement[1] = placement[1] + 30
                self.text_box.image.blit(tempsurface, tuple(placement))

    def findProperEvent(self, events):
        return self.current_scene.events[0]
        all_conditions_valid = True
        for event in events:
            for condition in event.conditions:
                if condition != condition:
                    all_conditions_valid = False
                    break
            if all_conditions_valid:
                return event
