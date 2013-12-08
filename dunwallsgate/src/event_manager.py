#!/bin/python3

import pygame.locals as pg


class EventManager():
    """
    Manage all the event of the game
    """

    def __init__(self, *protected_categories):
        self.callbacks = CallbacksContainer()
        if protected_categories:
            self.protected_categories = list(protected_categories)
        else:
            self.protected_categories = []

    def purge_callbacks(self, category):
        self.callbacks.purge_category(category)

    def on_key_down(self, callback, cat, which=None):
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

    def on_click_on(self, collidable, callback, cat, buttons=1):
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
            "mousedown", cat,
            lambda e: self._watch_click(collidable, callback, buttons, cat),
            {"buttons": buttons, "collidable": collidable})

    def _watch_click(self, collidable, callback, buttons, cat):
        def on_release(e, id_):
            if self._collide_with(e.pos, collidable):
                callback(e)
            self.callbacks.remove_callback(id_)
        id_ = self.callbacks.add_callback(
            "mouseup", cat, None, {"buttons": buttons})
        call = self.callbacks.get_callback_object(id_)
        call.callback = lambda e: on_release(e, id_)

    def on_mouse_up(self, callback, cat, buttons=1, collidable=None):
        if not isinstance(buttons, tuple):
            buttons = (buttons,)
        return self.callbacks.add_callback(
            "mouseup", cat, callback,
            {"buttons": buttons, "collidable": collidable})

    def on_mouse_down(self, callback, cat, buttons=1, collidable=None):
        if not isinstance(buttons, tuple):
            buttons = (buttons,)
        return self.callbacks.add_callback(
            "mousedown", cat, callback,
            {"buttons": buttons, "collidable": collidable})

    def on_mouse_in(self, collidable, callback, cat):
        """
        Triggered when the mouse is in a collidable.
        """
        return self.callbacks.add_callback(
            "mousemotion", cat, callback,
            {"collidable": collidable})

    def on_mouse_out(self, collidable, callback, cat):
        return self.callbacks.add_callback(
            "mousemotion", cat,
            lambda e: self._watch_move_out(callback, cat, collidable),
            {"collidable": collidable})

    def _watch_move_out(self, callback, cat, collidable):
        def when_is_out(event, id_):
            if not self._collide_with(event.pos, collidable):
                callback(event)
                self.remove_callback(id_)
        id_ = self.on_mouse_move(None, cat)
        call = self.callbacks.get_callback_object(id_)
        call.callback = lambda e: when_is_out(e, id_)

    def on_mouse_move(self, callback, cat):
        return self.callbacks.add_callback(
            "mousemotion", cat, callback, None)

    def on_quit(self, callback, cat):
        self.callbacks.add_callback("quit", cat, callback, None)

    def run(self, events):
        callbacks_to_run = []
        for event in events:
            if event.type == pg.KEYDOWN:
                callbacks_to_run.extend(
                    self.manage_key_event(event, "keydown"))
            elif event.type == pg.QUIT:
                callbacks_to_run.extend((
                    (callback.callback, event) for callback
                    in self.callbacks.get_type("quit")))
            elif event.type == pg.MOUSEBUTTONUP:
                callbacks_to_run.extend(
                    self.manage_mouse_button_event(event, "mouseup"))
            elif event.type == pg.MOUSEBUTTONDOWN:
                callbacks_to_run.extend(
                    self.manage_mouse_button_event(event, "mousedown"))
            elif event.type == pg.MOUSEMOTION:
                callbacks_to_run.extend(
                    self.manage_mouse_motion_event(event))
        self._do_run(callbacks_to_run)

    def _do_run(self, callbacks_to_run):
        for callback in callbacks_to_run:
            callback[0](callback[1])

    def manage_key_event(self, event, type_):
        callbacks_to_run = []
        for callback in self.callbacks.get_type(type_):
            if callback.params["key"] is None or\
                    callback.params["key"] == event.key or\
                    callback.params["key"] == event.unicode:
                callbacks_to_run.append((callback.callback, event))
        return callbacks_to_run

    def manage_mouse_motion_event(self, event):
        callbacks_to_run = []
        for callback in self.callbacks.get_type("mousemotion"):
            try:
                if self._collide_with(event.pos,
                                      callback.params["collidable"]):
                    callbacks_to_run.append((callback.callback, event))
            except KeyError:
                callbacks_to_run.append((callback.callback, event))
        return callbacks_to_run

    def manage_mouse_button_event(self, event, type_):
        callbacks_to_run = []
        for callback in self.callbacks.get_type(type_):
            if event.button in callback.params["buttons"]:
                try:
                    collide = self._collide_with(
                        event.pos, callback.params["collidable"])
                except KeyError:
                    callbacks_to_run.append((callback.callback, event))
                else:
                    if collide:
                        callbacks_to_run.append((callback.callback, event))
        return callbacks_to_run

    def _collide_with(self, coord, collidable):
        if (hasattr(collidable, "collidepoint")
                and collidable.collidepoint(coord)):
            return True
        elif (hasattr(collidable, "get_rect")
                and collidable.get_rect().collidepoint(coord)):
            return True
        elif (hasattr(collidable, "rect")
                and collidable.rect.collidepoint(coord)):
            return True
        return False

    def remove_callback(self, *args):
        for id_call in args:
            self.callbacks.remove_callback(id_call)

    def lock_callback(self, *ids):
        for id_call in ids:
            self.callbacks.lock_callback(id_call)
        return ids

    def lock_categories(self, *categories):
        for category in categories:
            self.callbacks.lock_category(category)
        return categories

    def unlock_callback(self, *ids):
        for id_call in ids:
            self.callbacks.unlock_callback(id_call)

    def unlock_categories(self, *categories):
        for category in categories:
            self.callbacks.unlock_category(category)

    def lock_all_categories_but(self, *categories, **options):
        lock_protected = options.get("lock_protected", False)
        if not lock_protected:
            categories = list(categories) + self.protected_categories
        locked_categories = [category for category in
                             self.callbacks.categories
                             if category not in categories]
        return self.lock_categories(*locked_categories)


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
            for i, callback in enumerate(callbackslist):
                if callback.category == cat:
                    del callbackslist[i]

    def get_callback_object(self, id_):
        """
        Return the callback object depending of the id

        Even though the callback object is self contained in the id, this
        method is provided for abstraction. The way id are implemented may
        vary in the future.
        """
        return id_[1]

    def lock_callback(self, id_):
        self.get_callback_object(id_).lock()

    def unlock_callback(self, id_):
        self.get_callback_object(id_).unlock()

    def get_type(self, type_, with_locked=False):
        try:
            return [callback for callback in self._callbacks[type_]
                    if not callback.is_locked or with_locked]
        except KeyError:
            return []

    def get_category(self, category, with_locked=False):
        callbacks = []
        for callbackslist in self._callbacks.values():
            for callback in callbackslist:
                if callback.category is category:
                    callbacks.append(callback)
        return callbacks

    def lock_category(self, category):
        for callback in self.get_category(category, True):
            callback.lock()

    def unlock_category(self, category):
        for callback in self.get_category(category, True):
            callback.unlock()

    @property
    def categories(self):
        categories = []
        for callbackslist in self._callbacks.values():
            for callback in callbackslist:
                if callback.category not in categories:
                    categories.append(callback.category)
        return categories


class Callback():
    """Callback object"""

    def __init__(self, callback, params, category):
        self.callback = callback
        if params:
            self.params = params
        else:
            self.params = {}
        self.category = category
        self._num_locked = 0
        self.num_locked = 0

    @property
    def num_locked(self):
        return max(0, self._num_locked)

    @num_locked.setter
    def num_locked(self, value):
        self._num_locked = max(0, value)

    @property
    def is_locked(self):
        return self.num_locked > 0

    def lock(self):
        self.num_locked += 1

    def unlock(self):
        self.num_locked -= 1

    def __repr__(self):
        return ("callback: " + repr(self.callback) + " ; params: "
                + repr(self.params)
                + " ; category: " + repr(self.category)
                + " ; num_locked: {}".format(self.num_locked))


def test():
    em = EventManager()
    cat = object()
    cat2 = object()
    id1 = em.on_key_down(lambda: None, cat)
    id2 = em.on_key_down(lambda: None, cat)
    id3 = em.on_key_down(lambda: None, cat2)
    id4 = em.on_key_down(lambda: None, cat2)
    locked_cat = em.lock_all_categories_but(cat2)
    print("id1.is_locked: {}, id3.is_locked: {}".format(id1[1].is_locked,
                                                        id3[1].is_locked))
    em.unlock_categories(*locked_cat)
    print("id1.is_locked: {}, id3.is_locked: {}".format(id1[1].is_locked,
                                                        id3[1].is_locked))
    em.lock_callback(id1)
    print("id1.is_locked: {}, id3.is_locked: {}".format(id1[1].is_locked,
                                                        id3[1].is_locked))
    em.unlock_callback(id1)
    print("id1.is_locked: {}, id3.is_locked: {}".format(id1[1].is_locked,
                                                        id3[1].is_locked))
    print(id1, id2, id3, id4)


if __name__ == "__main__":
    test()
