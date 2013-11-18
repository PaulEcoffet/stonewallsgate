#!/bin/python3


import pygame

from decoders.json_structures import *
from screens.text_render import TextRender
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
            bottomright=(self.surface.get_width()-50,
                         self.surface.get_height()-30))

        self.zone_box.rect = self.zone_box.image.get_rect(
            topleft=(0, 0))
        self.charac.rect = self.charac.image.get_rect(midtop=(250, 140))
        self.graphic_elements = pygame.sprite.RenderPlain(self.text_box)

        self.init_story()



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
                self.scene_background, (1024, 574)))

        if not self.text_box:
            self.text_box = pygame.sprite.DirtySprite()
            self.text_box.image = pygame.image.load(
                get_image_path('storyscreen/text_box.png'))
            self.text_box.image = self.text_box.image.convert_alpha()
            self.text_box.image = pygame.transform.scale(self.text_box.image, (924, 163))
            self.text_box.image.set_alpha(0)

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

    def update_textbox(self):
        self.text_box.image = pygame.image.load(
            get_image_path('storyscreen/text_box.png'))
        self.text_box.image = self.text_box.image.convert_alpha()
        self.text_box.image = pygame.transform.scale(self.text_box.image, (924, 163))
        self.text_box.image.set_alpha(0)
        self.transparent = pygame.Surface((1000,750), pygame.SRCALPHA)
        self.transparent.fill((0,0,0,128))
        self.text_box.image.blit(self.transparent, (0,0))

    def init_story(self):
        self.scene = get_scene("intro")
        self.update_textbox()
        self.event = self.scene.events[0]
        self.dialog_end = True
        self.dialogs = self.event.next_dialog()
        self.full_dialog = TextRender((680,70), "lucidaconsole", 20, (255,158,0) , self.dialogs.message)
        self.show_dialog()
        self.eventmanager.on_key_down(self.show_dialog)

    def show_dialog(self, *args):
        if self.dialogs:
            next_dialog = self.full_dialog.next()
            if not next_dialog:
                self.dialogs = self.event.next_dialog()
                if self.dialogs:
                    self.full_dialog = TextRender((680,70), "lucidaconsole", 20, (255,158,0) , self.dialogs.message)
                    self.dialog_end = True
                    next_dialog = self.full_dialog.next()
                else:
                    return None
            self.update_textbox()
            for i, line in enumerate(next_dialog):
                self.text_box.image.blit(line, (20,20+i*35))

