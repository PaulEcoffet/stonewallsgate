#!/bin/python3

import pygame
import pygame.locals as pg

from customsprites import Portrait
from button import Button


class StoryScreen():
    """
    The story screen of the game.
    """

    background = None
    dialogue_box = None
    suite_box = None
    gameversion = None

    def __init__(self, game, event):
        self.start_scene = True
        self.game = game
        self.game_event = game.game_event
        self.event = event
        self.end = False
        self.portrait_update = False
        self.portraits = []
        self.highlighted_pending = []
        self.old_portraits_element = None
        self.restart_event = False
        self.choice_actions_cat = object()  # Event manager category
        self.next_dialogue_cat = object()  # Event manager category

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
        self.dialogue_box.rect = self.dialogue_box.image.get_rect(x=50, y=380)
        self.suite_box.rect = self.suite_box.image.get_rect(x=897, y=543)
        self.graphic_elements = pygame.sprite.OrderedUpdates(self.dialogue_box)
        self.portraits_elements = pygame.sprite.RenderUpdates()
        self.eventmanager.on_key_down(self.show_dialogue,
                                      self.next_dialogue_cat, pg.K_SPACE)
        self.eventmanager.on_click_on(self.suite_box, self.show_dialogue,
                                      self.next_dialogue_cat)
        self.init_story()

    def smooth_update(self, event):
        """
        Récupère un nouvel evenement 
        Actualise l'écran avec ses nouveautés
        (nouveau fond ou nouveaux dialogues)
        """
        self.event = event
        self.end = False
        if self.bg_ref != self.event.background:
            self.set_background(self.event.background)
            self.new_background = True
        self.init_story()

    def update(self):
        """
        Met à jour des elements graphiques de l'écran 
        (Bouttons, Portraits) si besoin est
        """
        if self.choices:
            self.suite_box.click_time = 0
        self.graphic_elements.update()
        if self.portrait_update or self.start_scene:
            self.old_portraits_element = self.portraits_elements
            self.portraits_elements = pygame.sprite.RenderUpdates(
                self.new_portraits)
            self.portraits_elements.update(self.highlighted_pending)
            self.highlighted_pending = []

    def draw(self):
        """
        Efface puis (re)déssine les elements graphiques
        """
        if self.start_scene or self.new_background:
            self.surface.blit(self.background, (0, 0))
            self.start_scene = False
            self.new_background = False
        self.graphic_elements.clear(self.surface, self.background)
        if self.choices:
            self.graphic_elements = pygame.sprite.OrderedUpdates(
                self.dialogue_box, self.choices)
        else:
            self.graphic_elements = pygame.sprite.OrderedUpdates(
                self.dialogue_box, self.suite_box)
        self.graphic_elements.draw(self.surface)
        if self.portrait_update or self.start_scene:
            self.old_portraits_element.clear(self.surface,
                                             self.background)
            self.portraits_elements.draw(self.surface)
            self.portrait_update = False

    def init_sprites(self):
        """
        Initialise les elements graphiques de base
        (Fond, boite de dialogue et boutton 'suite')
        """
        if not self.background:
            self.set_background(self.event.background)

        if not self.dialogue_box:
            self.dialogue_box = pygame.sprite.DirtySprite()
            self.dialogue_box.image = pygame.Surface((924, 163),
                                                     pygame.SRCALPHA)
            self.purge_textbox()

        if not self.suite_box:
            self.suite_box = Button(self.eventmanager,
                                    self, "SUITE", (77, 20), "box_options")

    def purge_textbox(self):
        """
            Vidage du contenu de la boite de dialogue via
            Application d'un film noir transparent
        """
        self.dialogue_box.image.fill((0, 0, 0, 140))

    def set_background(self, background):
        """
            Récupère le fond depuis le cache
        """
        self.bg_ref = background
        try:
            self.background = self.game.cache.image_backgrounds[self.bg_ref]
        except KeyError:
            self.background = self.game.cache.image_backgrounds["default"]
            print(("Warning: images/scenes/%s.png does not exist !"
                  "Default BG has been set") % self.bg_ref)

    def init_story(self):
        """
            Démarre la cinématique
            Formatte depuis le cache les dialogues 
            (Le cache contiendra les panneaux)
        """
        self.game.cache.clear_dialogues()
        self.game.cache.format_dialogues(self.event.dialogues)
        self.left_one = ""
        self.choices = []
        self.new_portraits = []
        self.show_dialogue()

    def show_dialogue(self, *args):
        """
            Enclanche l'apparition des dialogues sur l'ecran
            Si un redémarrage de l'evenement est demandé:
                on reformatte les dialogues via les messages 
                stockés dans l'evenement
            Si aucun panneau de message trouvé:
                Déclaration de l'écran comme terminé
                Effacement des dialogues du cache
        """
        self.msg = self.game.cache.next_panel()
        if self.msg and isinstance(self.msg, dict):
            self.choices = self.ask_choices()
            self.new_portraits = self.set_portraits()
            self.portrait_update = True
            self.purge_textbox()
            self.dialogue_box.image.blit(self.msg["img_txt"], (10, 10))
            self.msg = None
        elif self.restart_event:
            self.end = False
            self.game.cache.clear_dialogues()
            self.game.cache.format_dialogues(self.event.dialogues)
            self.restart_event = False
        else:
            self.end = True
            self.game.cache.clear_dialogues()

    def set_portraits(self):
        """ 
        Place les portraits aux bons emplacement.
        Le premier personnage qui parle se situra toujours 
        à gauche tant qu'il est présent.
        """
        portraits = []
        for _id in self.msg:
            if self.msg[_id] and _id in ["talker", "hearer"]:
                charac = self.game.get_character(self.msg[_id])
                portrait = self.get_character_portrait(charac, "front")
                if _id == "talker":
                    self.highlighted_pending.append(portrait)
                    if self.left_one != self.msg["hearer"]:
                        self.left_one = self.msg[_id]
                if self.msg[_id] == self.left_one:
                    portrait.rect = (portrait.image
                                     .get_rect(midtop=(250, 160)))
                else:
                    portrait.rect = (portrait.image
                                     .get_rect(midtop=(800, 160)))
                portrait.resize()
                portraits.append(portrait)
        return portraits

    def get_character_portrait(self, charac, cat):
        """Récupère le portait du personnage 
        depuis le cache, sinon création d'un portrait
        """
        for portrait in self.portraits:
            if (charac, cat) == portrait.id:
                return portrait
        self.portraits.append(
            Portrait(self.game.cache, charac, cat))
        return self.portraits[-1]

    def ask_choices(self):
        """
        Placement des bouttons de choix si choix dans le dialogue
        Prépare au déclanchement des triggers à l'appui du boutton
        """
        choices_sprite = []
        if self.msg["choices"]:
            self.eventmanager.lock_categories(self.next_dialogue_cat)
            for i, choice in enumerate(self.msg["choices"]):
                if len(self.msg["choices"]) > 3:
                    choices_sprite.append(
                        Button(self.eventmanager, self,  choice["txt"],
                               (435, 27), "dialogue_choices"))
                    if len(choices_sprite) > 3:
                        choices_sprite[-1].rect = \
                            (choices_sprite[i].image.get_rect(x=530,
                                                              y=35 * i + 305))
                    else:
                        choices_sprite[-1].rect = \
                            (choices_sprite[i].image.get_rect(x=75,
                                                              y=35 * i + 425))
                else:
                    choices_sprite.append(
                        Button(self.eventmanager, self,  choice["txt"],
                               (870, 27), "dialogue_choices"))
                    choices_sprite[-1].rect = (choices_sprite[i].image
                                               .get_rect(x=75,
                                                         y=35 * i + 425))
                if "triggers" in choice:
                    for trigger in choice["triggers"]:
                        self.eventmanager.on_click_on(
                            choices_sprite[-1], (lambda trigger_cat, params:
                                lambda e: self.exec_trigger(trigger_cat, params))
                                    (trigger.get("trigger_cat", None),
                                     trigger.get("params", None)),
                                     self.choice_actions_cat)
                elif "trigger_cat" in choice:
                    self.eventmanager.on_click_on(choices_sprite[-1],
                            (lambda trigger_cat, params: \
                                lambda e: self.exec_trigger(trigger_cat, params)) \
                                    (choice.get("trigger_cat", None),
                                     choice.get("params", None)),
                                     self.choice_actions_cat)
                self.eventmanager.on_click_on(choices_sprite[-1],
                    lambda e: self.activate_dialogue_events(),
                        self.choice_actions_cat)
                self.eventmanager.on_click_on(choices_sprite[-1],
                    lambda e: self.purge_choice_actions(),
                        self.choice_actions_cat)
                self.eventmanager.on_click_on(choices_sprite[-1],
                    self.show_dialogue, self.choice_actions_cat)
        return choices_sprite

    def exec_trigger(self, trigger_cat, params=None):
        """
        Déclanchement du trigger
        trigger_cat - trigger à enclencher
        params - paramètres du trigger
        """
        if trigger_cat:
            self.game.game_event.game_triggers[trigger_cat](params)

    def activate_dialogue_events(self):
        """
            Déblocage des evenements enregistrées
        """
        self.eventmanager.unlock_categories(self.next_dialogue_cat)

    def purge_choice_actions(self):
        """
            Supression des evenements enregistrées
        """
        self.eventmanager.purge_callbacks(self.choice_actions_cat)

    def shutdown(self):
        """
            Supression complète des evenements enregistrées
        """
        self.eventmanager.purge_callbacks(self.choice_actions_cat)
        self.eventmanager.purge_callbacks(self.next_dialogue_cat)
