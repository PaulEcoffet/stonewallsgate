#!/bin/python3


import pygame
import pygame.locals as pg
from decoders.json_structures import *


class StoryScreen():
    """
    The story screen of the game.
    """

    scene_background = None
    text_box = None
    zone_box = None
    charac = None

    def __init__(self, scene="", act="", round=""):
        self._scene = scene
        self._act = act
        self._round = round
        
        self.theme_playing = True
        self.first_draw = False

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.first_draw = True

        self.init_sprites()
        # Soundtrack management
        try:
            self.soundtrack = pygame.mixer.Sound(
                '../data/sound/dunwalls_theme.ogg')
        except pygame.error as e:
            print("Dismissed exception: ", e)
        else:
            self.eventmanager.on_key_down(self.toggle_theme, pg.K_s)
            self.toggle_theme(force=True)

        # Sprites placement
        self.text_box.rect = self.text_box.image.get_rect(
            bottomright=(self.surface.get_width(),
                         self.surface.get_height()))
        self.zone_box.rect = self.zone_box.image.get_rect(
            topleft=(0,0))
        self.charac.rect = self.charac.image.get_rect(midtop=(250,140))
        self.buttons = pygame.sprite.RenderPlain(self.text_box,
                                                 self.zone_box,self.charac)

        self.gameplay()
        
    def toggle_theme(self, *args, **kwargs):
        try:
            self.theme_playing = kwargs["force"]
        except KeyError:
            self.theme_playing = not self.theme_playing
        if self.theme_playing:
            self.soundtrack.play(-1)
        else:
            self.soundtrack.stop()

    def draw(self):
        if self.first_draw:
            self.surface.blit(self.scene_background, (0, 0))
            self.first_draw = False
        self.buttons.clear(self.surface, self.scene_background)
        self.buttons.draw(self.surface)
        
    def shutdown(self):
        """
        Shutdown screen playing (fill a black screen)
        Underconstruction : Remove all events and spirits from this screen.   
        """
        self.surface.fill(0)

    def init_sprites(self):
        if not self.scene_background:
            self.scene_background = pygame.image.load(
                '../data/images/storyscreen/background/demo.jpg').convert()
            self.scene_background = (pygame.transform.scale(self.scene_background,
                                                           (1024, 361)))
        if not self.text_box:
            self.text_box = pygame.sprite.DirtySprite()
            self.text_box.image = pygame.image.load(
                '../data/images/storyscreen/text_box.png').convert()
            self.text_box.image = (pygame.transform.scale(self.text_box.image,
                                                   (1024, 213)))
        if not self.zone_box:
            self.zone_box = pygame.sprite.DirtySprite()
            self.zone_box.image = pygame.image.load(
                '../data/images/storyscreen/zone_box.png').convert()
            self.zone_box.image = (pygame.transform.scale(self.zone_box.image,
                                                   (249, 36)))
        if not self.charac:
            self.charac = pygame.sprite.DirtySprite()
            self.charac.image = pygame.image.load(
                '../data/images/storyscreen/characters/unknown.png').convert_alpha()
            self.charac.image = (pygame.transform.scale(self.charac.image,
                                                   (273, 221)))

    def gameplay(self):
        entry = "scene1"
        self.current_scene = getScene(entry)
        self.scene_background = pygame.image.load('../data/images/storyscreen/background/%s.jpg'%self.current_scene.background).convert()
        self.scene_background = (pygame.transform.scale(self.scene_background,(1024, 361))) #screen backgorund
        for event in self.current_scene.events:
            if "test" in event.conditions: #event = dict
                if event["test"] == "debut_scene":
                    pass
                else:
                    pass
            if event.dialogs is not None:
                for dialog in event.dialogs:
                    myfont = pygame.font.SysFont("monospace", 25)
                    charac_label = myfont.render(dialog.character, 1, (255,255,0))
                    message_label = myfont.render(dialog.message, 1, (255,200,0))
                    self.text_box.image.blit(charac_label, (10, 20))
                    self.text_box.image.blit(message_label, (15, 60))
                    break
