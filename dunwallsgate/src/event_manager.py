#!/bin/python3

import itertools

import pygame.locals as pg


class EventManager():
    """
    Manage all the event of the game
    """

    def __init__(self):
        self.globalCallbacks = {"mouse": {}, "key": {}, "custom": {}}
        self.screenCallbacks = {"mouse": {}, "key": {}, "custom": {}}

    def on_key_down(self, callback, which=None, global_=False):
        """
        Register an event when a key is pressed
        callback - The function to call when the event occurs
        which - The key to watch, if no key is given, then the callback is
                call each time a key is pressed. which can be a single char
                string or a K_* from pygame.locals
        global_ - specify if the callbacks are automatically deactivate when
                  the screen change or not
        """
        if global_:
            callbacks = self.globalCallbacks
        else:
            callbacks = self.screenCallbacks
        try:
            callbacks["key"].append((which, callback))
        except:
            callbacks["key"] = [(which, callback)]

    def on_click_on(self, collidable, callback, button=1, global_=False):
        """
        Register a callback called when the collidable object is clicked.
        collidable - The object that might be clicked, must implement a
                     collidepoint method, a get_rect method or a rect property
        callback - the callback to be triggered when the collidable is clicked
        button - The mouse button to be clicked so as to trigger the event,
                 must be either a int or a tuple.
                 ex : 1 - left mouse button, (1, 2) - left and right mouse
                 buttons, 0 : all mouse buttons (including scroll up & down)
        """
        if global_:
            callbacks = self.globalCallbacks
        else:
            callbacks = self.screenCallbacks
        if not isinstance(button, tuple):
            button = (button,)
        try:
            callbacks["mouse"].append((button, collidable, callback))
        except:
            callbacks["mouse"] = [(button, collidable, callback)]

    def on_quit(self, callback, global_=False):
        if global_:
            callbacks = self.globalCallbacks
        else:
            callbacks = self.screenCallbacks
        try:
            callbacks["quit"].append(callback)
        except KeyError:
            callbacks["quit"] = [callback]
        return (callbacks["quit"], callback)

    def run(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                for callback in self.both_callbacks("key"):
                    if callback[0] is None or callback[0] == event.key or\
                            callback[0] == event.unicode:
                        callback[1](event.key, event.unicode)
            elif event.type == pg.QUIT:
                for callback in self.both_callbacks("quit"):
                    callback()
            elif event.type == pg.MOUSEBUTTONUP:
                for callback in self.both_callbacks("mouse"):
                    if event.button in callback[0]:
                        try:
                            if callback[1].collidepoint(event.pos):
                                callback[2]()
                        except AttributeError:
                            try:
                                if (callback[1].get_rect()
                                    .collidepoint(event.pos)):
                                    callback[2]()
                            except AttributeError:
                                if callback[1].rect.collidepoint(event.pos):
                                    callback[2]()

    def on_custom_event(self, event_name, data, callback, global_=False):
        if global_:
            callbacks = self.globalCallbacks
        else:
            callbacks = self.screenCallbacks
        try:
            callbacks["custom"][event_name].append(callback)
        except KeyError:
            callbacks["custom"][event_name] = [callback]
        return (callbacks["custom"][event_name], callback)  # ID used to remove
                                                            # event

    def both_callbacks(self, *keys):
        stop_gcall = False
        stop_scall = False
        gcall = self.globalCallbacks
        scall = self.screenCallbacks
        for key in keys:
            if not stop_gcall:
                try:
                    gcall = gcall[key]
                except KeyError:
                    stop_gcall = True
                    gcall = []
            if not stop_scall:
                try:
                    scall = scall[key]
                except KeyError:
                    stop_scall = True
                    scall = []
        return itertools.chain(gcall, scall)
