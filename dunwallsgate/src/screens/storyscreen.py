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
        self.graphic_elements = pygame.sprite.OrderedUpdates(self.dialogue_box)
        self.portraits_elements = pygame.sprite.RenderUpdates()
        self.init_story()

    def draw(self):
        if self.start_scene:
            self.surface.blit(self.scene_background, (0, 0))
            transparent = pygame.Surface((230,30), pygame.SRCALPHA)
            transparent.fill((0,0,0,140))
            note = TextRender((300,50), "joystix", 20, (255,50,10), 
                                               "ALPHA version")
            transparent.blit(note.next(), (5,3))
            self.surface.blit(transparent, (10,10))
            self.start_scene = False
            self.old_portraits = None
        if self.message is not None:
            self.graphic_elements.clear(self.surface, self.scene_background)
            self.graphic_elements = pygame.sprite.OrderedUpdates(
                self.dialogue_box, self.choices)
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

    def purge_textbox(self):
        self.dialogue_box.image.fill((0,0,0,140))

    def init_story(self):
        self.dialogues = self.event.dialogues
        self.message = self.dialogues.next()
        self.text_render = TextRender((904,163), "unispace_italic", 
            20, (255,158,0) , self.message["message"])
        self.left_charac = None
        self.new_portraits = self.set_portraits()
        self.choices = self.ask_choices()
        self.show_dialogue()

        # Events registration
        self.eventmanager.on_key_down(self.show_dialogue, pg.K_RIGHT)
        #self.eventmanager.on_click_on(self.dialogue_box, self.show_dialogue)
        
        
    def show_dialogue(self, *args):
        next_text = self.text_render.next()
        if next_text is None:
            #End of ONE conversation
            self.message = self.dialogues.next()
            if self.message is None:
                #End of Storyscreen (the event is done)
                self.event.done = True
                return None
            self.text_render = TextRender((904,163), "larabiefont", 25, 
                (255,158,0), self.message["message"])
            next_text = self.text_render.next()
            self.new_portraits = self.set_portraits()
            self.choices = self.ask_choices()
        self.purge_textbox()
        self.dialogue_box.image.blit(next_text, (10,10))
        
    def set_portraits(self):
        """ Manage portraits (DirtySprite) to display, if there is. 
        First charac to speak is always display on the left side."""
        characs = []
        for type in self.message:
            if self.message[type] and type in ["transmitter", "receiver"]:
                characs.append(self.game.cache.portraits[(self.message[type], type)])
                if type == "transmitter" and (self.left_charac != self.message["receiver"] or not self.message["receiver"]):
                    self.left_charac = self.message[type]
                if self.message[type] == self.left_charac:
                    characs[-1].rect = characs[-1].image.get_rect(midtop=(250, 160))
                else:
                    characs[-1].rect = characs[-1].image.get_rect(midtop=(800, 160))
        return characs
        
    def ask_choices(self):
        choices_spirit = []
        if self.message["choices"]:
            for i, choice in enumerate(self.message["choices"]):
                choices_spirit.append(pygame.sprite.DirtySprite())
                choices_spirit[-1].image = pygame.Surface((870,34), pygame.SRCALPHA)
                choices_spirit[-1].image.fill((180-i*30,255-i*30,0+i*15,50))
                choices_spirit[-1].rect = choices_spirit[i].image.get_rect(x=75, y=35*i+425)
                text = TextRender((870,130), "unispace_italic", 26, (255,158,0), choice["text"])
                choices_spirit[-1].image.blit(text.next(), (0,0))
                self.eventmanager.on_click_on(choices_spirit[-1], lambda args: print(i)) #self.game.game_event.game_triggers[choice["trigger"]](choice["params"])
        return choices_spirit
