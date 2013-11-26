#!/bin/python3


import pygame
import pygame.locals as pg

from screens.text_render import TextRender

class StoryScreen():
    """
    The story screen of the game.
    """

    scene_background = None
    dialogue_box = None
    suite_box = None
    exit_btn = None

    def __init__(self, game, event):
        self.start_scene = True
        self.game = game
        self.event = event

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.init_sprites()

        # Sprites placement
        self.dialogue_box.rect = self.dialogue_box.image.get_rect(x=50, y=380)
        self.suite_box.rect = self.suite_box.image.get_rect(x=897, y=543)
        self.exit_btn.rect = self.exit_btn.image.get_rect(x=897, y=20)
        self.graphic_elements = pygame.sprite.OrderedUpdates(self.dialogue_box, self.exit_btn)
        self.portraits_elements = pygame.sprite.RenderUpdates()
        self.eventmanager.on_click_on(self.exit_btn, lambda e: self.window.set_do_run(False))
        self.init_story()

    def draw(self):
        if self.start_scene:
            self.surface.blit(self.scene_background, (0, 0))
            transparent = pygame.Surface((265,30), pygame.SRCALPHA)
            transparent.fill((0,0,0,140))
            note = TextRender((320,50), "joystix", 20, (255,50,10), 
                                               "ALPHA version 2")
            transparent.blit(note.next(), (5,3))
            self.surface.blit(transparent, (10,10))
            self.start_scene = False
            
        self.graphic_elements.clear(self.surface, self.scene_background)
        if self.choices:
            self.graphic_elements = pygame.sprite.OrderedUpdates(
                self.dialogue_box, self.exit_btn, self.choices)
        else:
            self.graphic_elements = pygame.sprite.OrderedUpdates(
                self.dialogue_box, self.exit_btn, self.suite_box)         
        self.graphic_elements.draw(self.surface)
        if self.new_portraits is not None or self.start_scene:
            self.portraits_elements.clear(self.surface, self.scene_background)
            self.portraits_elements = pygame.sprite.RenderUpdates(self.new_portraits)
            self.portraits_elements.draw(self.surface)
            self.new_portraits = None

    def init_sprites(self):
        if not self.scene_background:
            self.scene_background = pygame.image.load(
                self.event.background).convert()
            self.scene_background = (pygame.transform.scale(
                self.scene_background, (1024, 574)))

        if not self.dialogue_box:
            self.dialogue_box = pygame.sprite.DirtySprite()
            self.dialogue_box.image = pygame.Surface((924,163), pygame.SRCALPHA)
            self.purge_textbox()
            
        if not self.suite_box:
            self.suite_box = pygame.sprite.DirtySprite()
            self.suite_box.image = pygame.Surface((77,20), pygame.SRCALPHA)
            self.suite_box.image.fill((0,0,0,120))
            text = TextRender((500,500), "joystix", 14, (255,158,0), "SUITE")
            self.suite_box.image.blit(text.next(), (6,1))
            
        if not self.exit_btn:
            self.exit_btn = pygame.sprite.DirtySprite()
            self.exit_btn.image = pygame.Surface((170, 20), pygame.SRCALPHA)
            self.exit_btn.image.fill((0,0,0,120))
            text = TextRender((500,500), "joystix", 14, (255,158,0), "EXIT")
            self.exit_btn.image.blit(text.next(), (6,1))
            
    def purge_textbox(self):
        self.dialogue_box.image.fill((0,0,0,140))

    def init_story(self):
        self.game.cache.clear_dialogues()
        self.game.cache.format_dialogues(self.event.dialogues)
        self.left_one = ""
        self.pass_dial_id = []
        self.choices = []
        self.new_portraits = []
        self.choices_actions = []
        self.show_dialogue()
        self.pass_dial_id.append(self.eventmanager.on_key_down(self.show_dialogue, pg.K_SPACE))
        self.pass_dial_id.append(self.eventmanager.on_click_on(self.suite_box, self.show_dialogue))
        
    def show_dialogue(self, *args):
        self.msg = self.game.cache.next_panel()
        if self.msg:
            self.choices = self.ask_choices()
            self.new_portraits = self.set_portraits()
            self.purge_textbox()
            self.dialogue_box.image.blit(self.msg["img_txt"], (10,10))
            self.msg = None
        else:
            self.event.done = True

    def set_portraits(self):
        """ Manage portraits (DirtySprite) to display, if there is. 
        First charac to speak is always display on the left side."""
        characs = []
        for _id in self.msg:
            if self.msg[_id] and _id in ["talker", "hearer"]:
                characs.append(self.game.cache.portraits[(self.msg[_id], _id)])
                if _id == "talker" and self.left_one != self.msg["hearer"]:
                    self.left_one = self.msg[_id]
                if self.msg[_id] == self.left_one:
                    characs[-1].rect = characs[-1].image.get_rect(midtop=(250, 160))
                else:
                    characs[-1].rect = characs[-1].image.get_rect(midtop=(800, 160))
        return characs
        
    def ask_choices(self):
        choices_sprite = []
        if self.msg["choices"]:
            for i, choice in enumerate(self.msg["choices"]):
                choices_sprite.append(pygame.sprite.DirtySprite())
                choices_sprite[-1].image = pygame.Surface((870,34), pygame.SRCALPHA)
                choices_sprite[-1].image.fill((180-i*30,255-i*30,0+i*15,50))
                choices_sprite[-1].rect = choices_sprite[i].image.get_rect(x=75, y=35*i+425)
                text = TextRender((870,130), "unispace_italic", 26, (255,158,0), choice["txt"])
                choices_sprite[-1].image.blit(text.next(), (0,0))
                self.choices_actions.append(self.eventmanager.on_click_on(choices_sprite[-1], (lambda trigger, params: lambda x: self.game.game_event.game_triggers[trigger](params))(choice["trigger_cat"], choice["txt"])))
                self.choices_actions.append(self.eventmanager.on_click_on(choices_sprite[-1], self.show_dialogue))
                self.eventmanager.remove_callback(*self.pass_dial_id)
                self.pass_dial_id = []
                self.choices_actions.append(self.eventmanager.on_click_on(choices_sprite[-1], lambda x: self.pass_dial_id.append(self.eventmanager.on_click_on(self.suite_box, self.show_dialogue))))
                self.choices_actions.append(self.eventmanager.on_click_on(choices_sprite[-1], lambda x: self.pass_dial_id.append(self.eventmanager.on_key_down(self.show_dialogue, pg.K_SPACE))))
                self.eventmanager.on_click_on(choices_sprite[-1], lambda x: self.eventmanager.remove_callback(*self.choices_actions))
                self.eventmanager.on_click_on(choices_sprite[-1], lambda x: self.clear_list(self.choices_actions))
        return choices_sprite
        
    def clear_list(self, _list):
        _list = []
        
