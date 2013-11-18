#!/bin/python3


import pygame
from decoder import *

from screens.text_render import TextRender
import data 

class StoryScreen():
    """
    The story screen of the game.
    """

    scene_background = None
    dialog_box = None
    zone_box = None
    charac1 = None
    charac2 = None

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
        self.dialog_box.rect = self.dialog_box.image.get_rect(
            bottomright=(self.surface.get_width()-50,
                         self.surface.get_height()-30))
        
        self.zone_box.rect = self.zone_box.image.get_rect(
            topleft=(0, 0))
        self.charac1.rect = self.charac1.image.get_rect(midtop=(250, 160))
        self.charac2.rect = self.charac2.image.get_rect(midtop=(750, 160))
        self.graphic_elements = pygame.sprite.RenderPlain(self.dialog_box)

        self.init_story()

        

    def draw(self):
        if self.end_scene:
            self.surface.blit(self.scene_background, (0, 0))
            self.test = TextRender((500,100), "joystix", 9, (200,100,10), "Scene de demonstration (Dunwall's Gate)")
            self.surface.blit(self.test.next(), (20,0))
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
                data.get_image_path('storyscreen/background/demo.jpg')).convert()
            self.scene_background = (pygame.transform.scale(
                self.scene_background, (1024, 574)))
            
        if not self.dialog_box:
            self.dialog_box = pygame.sprite.DirtySprite()
            self.dialog_box.image = pygame.image.load(
                data.get_image_path('storyscreen/text_box.png'))
            self.dialog_box.image = self.dialog_box.image.convert_alpha()
            self.dialog_box.image = pygame.transform.scale(self.dialog_box.image, (924, 163))
            self.dialog_box.image.set_alpha(0)
            
        if not self.zone_box:
            self.zone_box = pygame.sprite.DirtySprite()
            self.zone_box.image = pygame.image.load(
                data.get_image_path('storyscreen/zone_box.png')).convert()
            self.zone_box.image = (pygame.transform.scale(self.zone_box.image,
                                                          (249, 36)))
        if not self.charac1:
            self.charac1 = pygame.sprite.DirtySprite()
            self.charac1.image = pygame.image.load(
                data.get_image_path('storyscreen/characters/unknown.png'))
            self.charac1.image = self.charac1.image.convert_alpha()
            self.charac1.image = (pygame.transform.scale(self.charac1.image,
                                                        (440, 221)))
        if not self.charac2:
            self.charac2 = pygame.sprite.DirtySprite()
            self.charac2.image = pygame.image.load(
                data.get_image_path('storyscreen/characters/charac1.png'))
            self.charac2.image = self.charac2.image.convert_alpha()
            self.charac2.image = (pygame.transform.scale(self.charac2.image,
                                                        (440, 221)))

    def update_textbox(self):
        self.dialog_box.size = (924,163)
        self.dialog_box.size_text = (904,163)
        self.dialog_box.image = pygame.image.load(
            data.get_image_path('storyscreen/text_box.png'))
        self.dialog_box.image = self.dialog_box.image.convert_alpha()
        self.dialog_box.image = pygame.transform.scale(self.dialog_box.image, self.dialog_box.size )
        self.dialog_box.image.set_alpha(0) 
        self.transparent = pygame.Surface(self.dialog_box.size , pygame.SRCALPHA)   
        self.transparent.fill((0,0,0,128))                         
        self.dialog_box.image.blit(self.transparent, (0,0))
        
    def init_story(self):
        self.scene = get_scene("scene1")
        self.update_textbox()
        self.event = self.scene.events[0]
        self.dialog_end = True
        self.dialogs = self.event.dialogs
        self.new_message = self.dialogs.next()
        self.text_render = TextRender(self.dialog_box.size_text, "DroidSansMono", 20, (255,158,0) , self.new_message[2])
        self.show_dialog()
        self.eventmanager.on_key_down(self.show_dialog)

    def show_dialog(self, *args):
        next_text = self.text_render.next()
        if next_text is None:
            self.new_message = self.dialogs.next()
            if self.new_message is None:
                return None
            self.text_render = TextRender(self.dialog_box.size_text, "larabiefont", 25, (255,158,0) , self.new_message[2])
            next_text = self.text_render.next()
        self.update_textbox()
        self.dialog_box.image.blit(next_text, (20,0))
        if self.new_message[1]:
            self.graphic_elements = pygame.sprite.RenderPlain(self.dialog_box, self.charac1, self.charac2)
        elif self.new_message[0]:
            self.graphic_elements = pygame.sprite.RenderPlain(self.dialog_box, self.charac1)
            


