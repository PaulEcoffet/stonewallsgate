#!/bin/python3

import pygame

from customsprites import Portrait, LifeBar
from button import Button
from screens.text_render import TextRender
import battle

ALLIES = 1
ENNEMIES = 2

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

    def __init__(self, battle, event, game):
        self.start_battle = True
        self.battle = battle
        self.event = event
        self.end = False
        self.window = None
        self.eventmanager = None
        self.game = game
        self.portraits = []
        self.highlighted = []
        self.main_buttons = None
        self.portraits_elements = None
        self.atk_cat = object()
        self.info_box_cat = object()
        self._action_mode = None

    def start(self, window, eventmanager):
        """Démarre l'écran
        window - La fenêtre du jeu
        eventmanager - Le gestionnaire d'évènement
        """
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

        self.graphic_elements = pygame.sprite.OrderedUpdates(self.combat_box,
                                                             self.info_box)
        self.lifebars_elements = pygame.sprite.OrderedUpdates(
            [lifebar for lifebar in self.lifebars.values()])
        self.portraits_elements = pygame.sprite.RenderUpdates([portrait for portrait in self.portraits.values()])

    def update(self):
        if self.battle.winner:
            self.end = True
        self.lifebars_elements.update()
        self.main_buttons.update()
        self.info_box_buttons.update()
        self.portraits_elements.update(self.highlighted)

    def draw(self):
        if self.start_battle:
            self.surface.blit(self.background, (0, 0))
            self.start_battle = False
        else:
            self.lifebars_elements.clear(self.surface, self.background)
            self.lifebars_elements.draw(self.surface)
            self.portraits_elements.clear(self.surface, self.background)
            self.portraits_elements.draw(self.surface)
            self.graphic_elements.clear(self.surface, self.background)
            self.graphic_elements.draw(self.surface)
            self.main_buttons.clear(self.surface, self.background)
            self.main_buttons.draw(self.surface)
            self.info_box_buttons.clear(self.surface, self.info_box.image)
            self.info_box_buttons.draw(self.surface)

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
            self.attack_btn.on_click(lambda e: self.set_action_mode("attack"))
        if not self.switchwep_btn:
            self.switchwep_btn = Button(self.eventmanager, self, "WEAPONS")
            self.switchwep_btn.on_click(lambda e: self.set_action_mode("change_weapon"))
        if not self.run_btn:
            self.run_btn = Button(self.eventmanager, self, "RUN")
            self.run_btn.on_click(lambda e: self.set_action_mode("run"))
        self.main_buttons = pygame.sprite.RenderUpdates(self.attack_btn, self.switchwep_btn,
                                                   self.run_btn)
        self.info_box_buttons = pygame.sprite.RenderPlain()

    def set_action_mode(self, mode):
        if self._action_mode == mode:
            return
        else:
            self._action_mode = mode
            self.purge_info_box()
            self.info_box_buttons.empty()
            self.highlighted = [self.portraits[self.battle.playing_char]]
        if mode == "attack":
            self.show_attack_action()
        elif mode == "change_weapon":
            self.show_ch_weapon_action()
        elif mode == "run":
            self.show_run_action()

    def show_attack_action(self):
        self.set_info_box_text("Choisissez votre cible")
        portrait_targets = [(char, self.portraits[char])
                            for char in
                            self.battle.possible_targets_attack()]
        for char, portrait in portrait_targets:
            self.eventmanager.on_click_on(portrait, (lambda chara :lambda e: self.do_attack(chara))(char), self.atk_cat)
        self.highlighted = [portrait for char, portrait in portrait_targets]

    def do_attack(self, char):
        self.eventmanager.purge_callbacks(self.atk_cat)
        if self._action_mode == "attack":
            try:
                self.battle.do_attack(char)
            except battle.CantAttackException as e:
                self.set_action_mode(None)
                self.set_info_box_text(str(e))
            else:
                self.end_turn()

    def show_ch_weapon_action(self):
        for i, weapon in enumerate(self.battle.playing_char.inventory.weapons):
            button =  Button(self.eventmanager, self.info_box_cat, weapon.caracts["name"][:20], (320, 30), "dialogue_choices")
            button.on_click((lambda weapon_ :lambda e: self.show_ch_ammo_action(weapon_))(weapon))
            button.rect.move_ip(self.info_box.rect.x + 10, self.info_box.rect.y + i * 40 + 10)
            self.info_box_buttons.add(button)

    def show_ch_ammo_action(self, weapon):
        self.purge_info_box()
        for i, ammo in enumerate(self.battle.playing_char.inventory.get_compatible_ammo(weapon)):
            if ammo is None:
                button =  Button(self.eventmanager, self.info_box_cat, "Pas de munition", (320, 30), "dialogue_choices")
            else:
                button =  Button(self.eventmanager, self.info_box_cat, "{} x {}".format(ammo.caracts["name"][:15], ammo.amount), (320, 30), "dialogue_choices")
            button.on_click((lambda weapon_, ammo_ :lambda e: self.do_change_weapon(weapon_, ammo_))(weapon, ammo))
            button.rect.move_ip(self.info_box.rect.x + 10, self.info_box.rect.y + i * 40 + 10)
            self.info_box_buttons.add(button)

    def do_change_weapon(self, weapon, ammo):
        try:
            self.battle.change_weapon(weapon, ammo)
        except battle.CantChangeWeaponException as e:
            self.set_action_mode(None)
            self.set_info_box_text(str(e))
        else:
            self.end_turn()

    def show_run_action(self):
        button = Button(self.eventmanager, self.info_box_cat, "Fuir comme un couard", (320, 30), "dialogue_choices")
        button.rect.move_ip(self.info_box.rect.x + 10, self.info_box.rect.y + 10)
        button.on_click(lambda e: self.battle.do_run())
        self.info_box_buttons.add(button)

    def set_info_box_text(self, text):
        panel = TextRender((self.info_box.image.get_width() - 20,
                           self.info_box.image.get_height() - 20),
                          "larabiefont", 25, (255, 158, 0), text)
        self.purge_info_box()
        self.info_box.image.blit(panel.next(), (10, 10))

    def end_turn(self):
        self.battle.end_turn()
        self.set_action_mode(None)

    def purge_info_box(self):
        self.purge_box(self.info_box)
        self.eventmanager.purge_callbacks(self.info_box_cat)
        self.info_box_buttons.empty()

    def purge_box(self, sprite, alphakey=140):
        sprite.image.fill((0, 0, 0, alphakey))

    def init_battle(self):
        self.lifebars = {character: LifeBar(character) for character
                         in self.battle.all_characters}
        self.portraits = {character: Portrait(self.game.cache, character) for character
                          in self.battle.all_characters}
        self.place_elements()
        self.highlighted = [self.portraits[self.battle.playing_char]]

    def place_elements(self):
        i_team1 = -1  # Correct padding
        i_team2 = -1  # Correct padding
        i = -1
        for character, portrait in self.portraits.items():
            if character in self.battle.team1:
                position_portraits = lambda i: (190 * (i * 1.2 + 1), 217)
                position_bars = lambda i: (160 * (i * 1.4 + 1), 365)
                i_team1 += 1
                i = i_team1
            else:
                position_portraits = lambda i: (100 * (i * 1.2 + 1) + 775, 10)
                position_bars = lambda i: (100 * (i * 1.4 + 1) + 740, 160)
                i_team2 += 1
                i = i_team2
            portrait.resize(300, 150)
            portrait.move(*position_portraits(i))
            self.lifebars[character].move(*position_bars(i))
