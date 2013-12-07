#!/bin/python3

import pygame
import pygame.locals as pg

from screens.text_render import TextRender
from customsprites import Portrait, Button
from screens.overlay import Overlay

class StoryScreen(Overlay):
    """
    The story screen of the game.
    """

    scene_background = None
    dialogue_box = None
    suite_box = None
    options_btn = None
    gameversion = None

    def __init__(self, game, event):
        self.start_scene = True
        self.game = game
        self.event = event
        self.end = False
        self.choice_actions_cat = object()  # Event manager category
        self.next_dialogue_cat = object()  # Event manager category

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.init_sprites()

        # Sprites placement
        self.dialogue_box.rect = self.dialogue_box.image.get_rect(x=50, y=380)
        self.suite_box.rect = self.suite_box.image.get_rect(x=897, y=543)
        self.options_btn.rect = self.options_btn.image.get_rect(x=897, y=20)
        self.graphic_elements = pygame.sprite.OrderedUpdates(self.dialogue_box, self.options_btn)
        self.portraits_elements = pygame.sprite.RenderUpdates()
        super().__init__(self.window, self.eventmanager, self.options_btn)
        self.e_registrations.append(self.eventmanager.on_click_on(self.options_btn,
                                      lambda e:  self.active(), self))
        self.eventmanager.on_key_down(self.show_dialogue, self.next_dialogue_cat, pg.K_SPACE)
        self.eventmanager.on_click_on(self.suite_box, self.show_dialogue, self.next_dialogue_cat)
        self.init_story()

    def draw(self):
        if self.start_scene:
            self.surface.blit(self.scene_background, (0, 0))
            transparent = pygame.Surface((205,25), pygame.SRCALPHA)
            transparent.fill((0,0,0,140))
            note = TextRender((320,50), "joystix", 16, (255,50,10),
                                               "ALPHA version 2")
            transparent.blit(note.next(), (5,3))
            self.surface.blit(transparent, (10,10))
            self.start_scene = False
            self.clear_options = False
        if self.options:
            self.loads_elements.clear(self.surface, self.scene_background)
            self.loads_elements.draw(self.surface)
        else:
            if self.clear_options:
                self.loads_elements.clear(self.surface, self.scene_background)
            self.graphic_elements.clear(self.surface, self.scene_background)
            if self.choices:
                self.graphic_elements = pygame.sprite.OrderedUpdates(
                    self.dialogue_box, self.options_btn, self.choices)
            else:
                self.graphic_elements = pygame.sprite.OrderedUpdates(
                    self.dialogue_box, self.options_btn, self.suite_box)
            self.graphic_elements.draw(self.surface)
            if self.portrait_update or self.start_scene or self.clear_options:
                self.portraits_elements.clear(self.surface, self.scene_background)
                self.portraits_elements = pygame.sprite.RenderUpdates(self.new_portraits)
                self.portraits_elements.draw(self.surface)
                self.portrait_update = False
            if self.clear_options:
                self.clear_options = False

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

        if not self.options_btn:
            self.options_btn = pygame.sprite.DirtySprite()
            self.options_btn.image = pygame.Surface((170, 20), pygame.SRCALPHA)
            self.options_btn.image.fill((0,0,0,120))
            text = TextRender((500,500), "joystix", 14, (255,158,0), "OPTIONS")
            self.options_btn.image.blit(text.next(), (6,1))

    def purge_textbox(self):
        self.dialogue_box.image.fill((0,0,0,140))

    def init_story(self):
        self.game.cache.clear_dialogues()
        self.game.cache.format_dialogues(self.event.dialogues)
        self.left_one = ""
        self.choices = []
        self.new_portraits = []
        self.show_dialogue()

    def show_dialogue(self, *args):
        self.msg = self.game.cache.next_panel()
        if self.msg and isinstance(self.msg, dict):
            self.choices = self.ask_choices()
            self.new_portraits = self.set_portraits()
            self.portrait_update = True
            self.purge_textbox()
            self.dialogue_box.image.blit(self.msg["img_txt"], (10,10))
            self.msg = None
        else:
            self.end = True
            self.game.cache.clear_dialogues()

    def set_portraits(self):
        """ Manage portraits (DirtySprite) to display, if there is.
        First charac to speak is always display on the left side."""
        characs = []
        for _id in self.msg:
            if self.msg[_id] and _id in ["talker", "hearer"]:
                if _id == "talker":
                    characs.append(self.game.cache.get_charac(self.msg[_id]).front_portrait["Highlighted"])
                    if self.left_one != self.msg["hearer"]:
                        self.left_one = self.msg[_id]
                else:
                    characs.append(self.game.cache.get_charac(self.msg[_id]).front_portrait["Attenuated"])
                if self.msg[_id] == self.left_one:
                    characs[-1].rect = characs[-1].image.get_rect(midtop=(250, 160))
                else:
                    characs[-1].rect = characs[-1].image.get_rect(midtop=(800, 160))
                characs[-1].resize()
        return characs

    def ask_choices(self):
        choices_sprite = []
        if self.msg["choices"]:
            self.eventmanager.lock_categories(self.next_dialogue_cat)
            self.pass_dial_id = []
            for i, choice in enumerate(self.msg["choices"]):
                choices_sprite.append(pygame.sprite.DirtySprite())
                choices_sprite[-1].image = pygame.Surface((870,34), pygame.SRCALPHA)
                choices_sprite[-1].image.fill((180-i*30,255-i*30,0+i*15,50))
                choices_sprite[-1].rect = choices_sprite[i].image.get_rect(x=75, y=35*i+425)
                text = TextRender((870,130), "unispace_italic", 26, (255,158,0), choice["txt"])
                choices_sprite[-1].image.blit(text.next(), (0,0))
                if "triggers" in choice:
                    for trigger in choice["triggers"]:
                        self.eventmanager.on_click_on(choices_sprite[-1], (lambda trigger_cat, params: lambda x: self.game.game_event.game_triggers[trigger_cat](params))(trigger.get("trigger_cat", "None"), trigger.get("params", None)), self.choice_actions_cat)
                elif "trigger_cat" in choice:
                        self.eventmanager.on_click_on(choices_sprite[-1], (lambda trigger_cat, params: lambda x: self.game.game_event.game_triggers[trigger_cat](params))(choice.get("trigger_cat", "None"), choice.get("params", None)), self.choice_actions_cat)
                self.eventmanager.on_click_on(choices_sprite[-1], lambda e: self.activate_dialogue_events(), self.choice_actions_cat)
                self.eventmanager.on_click_on(choices_sprite[-1], lambda e: self.purge_choice_actions(), self.choice_actions_cat)
                self.eventmanager.on_click_on(choices_sprite[-1], self.show_dialogue, self.choice_actions_cat)
        return choices_sprite

    def activate_dialogue_events(self):
        self.eventmanager.unlock_categories(self.next_dialogue_cat)

    def purge_choice_actions(self):
        self.eventmanager.purge_callbacks(self.choice_actions_cat)

    def shutdown(self):
        self.eventmanager.purge_callbacks(self.choice_actions_cat)
        self.eventmanager.purge_callbacks(self.next_dialogue_cat)
