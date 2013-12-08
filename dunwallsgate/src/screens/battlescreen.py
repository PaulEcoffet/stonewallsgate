#!/bin/python3

import pygame

from customsprites import Portrait, LifeBar
from button import Button

class BattleScreen():
    """
    The story screen of the game.
    """

    background = None
    combat_box = None
    info_box = None
    attack_btn = None
    switchwep_btn = None
    run_btn = None
    bag_btn = None

    def __init__(self, battle, event, game):
        self.start_battle = True
        self.battle = battle
        self.event = event
        self.end = False
        self.window = None
        self.eventmanager = None
        self.game = game
        self.portraits = []
        self.buttons = None

    def start(self, window, eventmanager):
        self.window = window
        self.surface = window.surface
        self.eventmanager = eventmanager
        self.init_sprites()

        # Sprites placement
        self.info_box.rect = self.info_box.image.get_rect(x=330, y=385)
        self.combat_box.rect = self.combat_box.image.get_rect(x=50, y=380)
        self.attack_btn.rect = self.attack_btn.image.get_rect(x=60, y=385)
        self.switchwep_btn.rect = self.switchwep_btn.image.get_rect(x=60,
                                                                    y=470)
        self.run_btn.rect = self.switchwep_btn.image.get_rect(x=700, y=470)
        self.bag_btn.rect = self.bag_btn.image.get_rect(x=700, y=385)

        self.graphic_elements = pygame.sprite.OrderedUpdates(self.combat_box,
                                                             self.info_box)
        self.lifebars_elements = pygame.sprite.OrderedUpdates()
        self.portraits_elements = pygame.sprite.RenderUpdates()

    def update(self):
            self.lifebars_elements.update()
            self.buttons.update()

    def draw(self):
        if self.start_battle:
            self.surface.blit(self.background, (0, 0))
            self.start_battle = False
        else:
            self.portraits_elements.clear(self.surface, self.background)
            self.portraits_elements = pygame.sprite.RenderUpdates(
                self.new_portraits)
            self.lifebars_elements.clear(self.surface, self.background)
            self.lifebars_elements = pygame.sprite.OrderedUpdates(
                [lifebar for lifebar in self.lifebars.values()])
            self.lifebars_elements.draw(self.surface)
            self.portraits_elements.draw(self.surface)

            self.graphic_elements.clear(self.surface, self.background)
            self.graphic_elements = pygame.sprite.OrderedUpdates(
                self.combat_box, self.info_box)
            self.graphic_elements.draw(self.surface)
            self.buttons.clear(self.surface, self.background)
            self.buttons.draw(self.surface)

    def init_sprites(self):
        if not self.background:
            self.bg_ref = self.event.background
            try:
                self.background = self.game.cache.image_backgrounds[self.bg_ref]
            except KeyError:
                self.background = self.game.cache.image_backgrounds["default"]
                print("Warning: images/scenes/%s.png does not exist ! Default BG has been set"%self.bg_ref)

        if not self.combat_box:
            self.combat_box = pygame.sprite.DirtySprite()
            self.combat_box.image = pygame.Surface((924, 163), pygame.SRCALPHA)
            self.purge_box(self.combat_box)
        if not self.info_box:
            self.info_box = pygame.sprite.DirtySprite()
            self.info_box.image = pygame.Surface((350, 163), pygame.SRCALPHA)
            self.purge_box(self.info_box, 195)
        if not self.attack_btn:
            self.attack_btn = Button(self.eventmanager, self, "ATTACK")
        if not self.switchwep_btn:
            self.switchwep_btn = Button(self.eventmanager, self, "WEAPONS")
        if not self.run_btn:
            self.run_btn = Button(self.eventmanager, self, "RUN")
        if not self.bag_btn:
            self.bag_btn = Button(self.eventmanager, self, "MY BAG")
        self.buttons = pygame.sprite.RenderUpdates(self.attack_btn, self.switchwep_btn,
                                                   self.run_btn, self.bag_btn)

    def purge_box(self, sprite, alphakey=140):
        sprite.image.fill((0, 0, 0, alphakey))

    def init_battle(self):
        self.characs = []
        self.lifebars = {character: LifeBar(character) for character
                         in self.battle.all_characters}
        self.set_elements(self.battle.team1, "allies")
        self.set_elements(self.battle.team2, "ennemies")
        self.new_portraits = self.characs

    def set_elements(self, characters, type_):
        if type_ == "allies":
            position_portraits = lambda i: (190 * (i * 1.2 + 1), 217)
            position_bars = lambda i: (160 * (i * 1.4 + 1), 365)
        else:
            position_portraits = lambda i: (100 * (i * 1.2 + 1) + 775, 10)
            position_bars = lambda i: (100 * (i * 1.4 + 1) + 740, 160)
        for i, companion in enumerate(characters):
            print(companion)
            portrait = self.get_character_portrait(companion, "front")
            portrait.resize(300, 150)
            portrait.move(*position_portraits(i))
            self.characs.append(portrait)
            self.lifebars[companion].move(*position_bars(i))
            
    def get_character_portrait(self, charac, cat):
        for portrait in self.portraits:
            if (charac, cat) == portrait.id:
                return portrait
        self.portraits.append(
            Portrait(self.game.cache, charac, cat))
        return self.portraits[-1]