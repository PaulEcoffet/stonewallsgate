#!/bin/python3

import pygame.locals as pg


class EventManager():
    """
    Manage all the event of the game
    """

    def __init__(self):
        self.callbacks = CallbacksContainer()

    def purge_callbacks(self, category):
        self.callbacks.purge_category(category)

    def on_key_down(self, callback, which=None, cat="screen"):
        """
        Register an event when a key is pressed
        callback - The function to call when the event occurs
        which - The key to watch, if no key is given, then the callback is
                call each time a key is pressed. which can be a single char
                string or a K_* from pygame.locals
        global_ - specify if the callbacks are automatically deactivate when
                  the screen change or not
        """
        return self.callbacks.add_callback("keydown", cat, callback,
                                           {"key": which})

    def on_click_on(self, collidable, callback, buttons=1, cat="screen"):
        """
        Register a callback called when the collidable object is clicked.
        This means that the mouse click is down on the collidable, and it is
        released while it is on the collidable.
        collidable - The object that might be clicked, must implement a
                     collidepoint method, a get_rect method or a rect property
        callback - the callback to be triggered when the collidable is clicked
        button - The mouse button to be clicked so as to trigger the event,
                 must be either a int or a tuple.
                 ex : 1 - left mouse button, (1, 2) - left and right mouse
                 buttons, 0 : all mouse buttons (including scroll up & down)
        """
        if not isinstance(buttons, tuple):
            buttons = (buttons,)
        return self.callbacks.add_callback(
            "mouseup", cat,
            callback,
            {"buttons": buttons, "collidable": collidable})

    def on_quit(self, callback, cat="screen"):
        self.callbacks.add_callback("quit", cat, callback, None)

    def run(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                self.manage_key_event(event, "keydown")
            elif event.type == pg.QUIT:
                for callback in self.callbacks.get_type("quit"):
                    callback()
            elif event.type == pg.MOUSEBUTTONUP:
                self.manage_mouse_button_event(event, "mouseup")

    def manage_key_event(self, event, type_):
        for callback in self.callbacks.get_type(type_):
            if callback.params["key"] is None or\
                    callback.params["key"] == event.key or\
                    callback.params["key"] == event.unicode:
                callback.callback(event.key, event.unicode)

    def manage_mouse_button_event(self, event, type_):
        for callback in self.callbacks.get_type(type_):
            if event.button in callback.params["buttons"]:
                try:
                    if (callback.params["collidable"]
                            .collidepoint(event.pos)):
                        callback.callback()
                except AttributeError:
                    try:
                        if (callback.params["collidable"].get_rect()
                                .collidepoint(event.pos)):
                            callback.callback()
                    except AttributeError:
                        try:
                            if (callback.params["collidable"].rect
                                    .collidepoint(event.pos)):
                                callback.callback()
                        except AttributeError:
                            callback.callback()

    def on_custom_event(self, event_name, callback, cat="screen"):
        return self.callbacks.add_callback(event_name, cat, callback)


class CallbacksContainer():
    """Contain the callbacks and can operate on them"""

    def __init__(self):
        self._callbacks = {}

    def add_callback(self, type_, category, callback, params=None):
        """
            add a callback, return an id to remove this callback.
        """
        callbackObj = Callback(callback, params, category)
        try:
            self._callbacks[type_].append(callbackObj)
        except KeyError:
            self._callbacks[type_] = [callbackObj]
        return (type_, callbackObj)

    def remove_callback(self, id_):
        try:
            self._callbacks[id_[0]] = [x for x in self._callbacks[id_[0]]
                                       if x != id_[1]]
        except KeyError:
            pass
        except ValueError:
            pass

    def purge_category(self, cat):
        for callbackslist in self._callbacks.values():
            for i in range(len(callbackslist)):
                if callbackslist[i].category == cat:
                    del callbackslist[i]

    def get_type(self, type_):
        try:
            return self._callbacks[type_]
        except KeyError:
            return []


class Callback():
    """Callback object"""

    def __init__(self, callback, params, category):
        self.callback = callback
        self.params = params
        self.category = category

    def __repr__(self):
        return ("callback: " + repr(self.callback) + " ; params: "
                + repr(self.params)
                + " ; category: " + repr(self.category))
