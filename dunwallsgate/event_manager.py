#!/bin/python3
__authors__ = "Paul ECOFFET, Elias RHOUZLANE"
"""
Ce module contient la class EventManager, qui s'occupe de gérer l'ensemble
des évènements envoyé par pygame tel que les évènements envoyés par la souris
ou bien par le clavier.

Elle contient aussi la classe CallbacksContainer, utilisé par l'EventManager
pour ajouter, supprimer ou verrouiller un ou plusieurs évènements.

Enfin, la classe Callback contient des informations sur les paramètres du
callback ainsi que des méthodes pour le verouiller ou déverouiller.
"""

import pygame.locals as pg


class EventManager():
    """
    Gère l'ensemble des évènements du jeu.
    """

    def __init__(self, *protected_categories):
        """
        Initialise l'EventManager
        *protected_catogories - Catégories qui ne seront pas verouillés par
        lock_all_but sauf si ce comportement est forcé.
        """
        self.callbacks = CallbacksContainer()
        if protected_categories:
            self.protected_categories = list(protected_categories)
        else:
            self.protected_categories = []

    def purge_callbacks(self, category):
        """
        Supprime tous les callbacks d'une category
        category - La catégorie de callback à supprimer. Elle peut être
                   un objet quelconque
        """
        self.callbacks.purge_category(category)

    def on_key_down(self, callback, cat, which=None):
        """
        Enregistre un callback déclenché quand une touche est pressé
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        which - La touche à observer, si aucune touche n'est donnée,
                alors le callback est appelé à chaque appuie de touche.
                `which` peut être une chaîne d'un caractère ou bien une
                constante `pygame.locals.K_*`
        """
        return self.callbacks.add_callback("keydown", cat, callback,
                                           {"key": which})

    def on_click_on(self, collidable, callback, cat, buttons=1):
        """
        Enregistre un `callback` déclenché quand un objet `collidable` est
        cliqué.
        Un `collidable` est considéré comme cliqué si le bouton de la souris
        est pressé ET relâché sur ce `collidable`.
        collidable - L'objet qui peut être cliqué, il doit posséder une
                     méthode `collidepoint`, une méthode `get_rect` ou une
                     propriété `rect`
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        buttons - Le bouton de la souris qui doit être utilisé pour le clic,
                  il doit être soit un `int` soit un `tuple`.
                  ex : 1 - bouton de souris gauche, (1, 2) - bouton gauche
                  ou droit
        """
        if not isinstance(buttons, tuple):
            buttons = (buttons,)
        return self.callbacks.add_callback(
            "mousedown", cat,
            lambda e: self._watch_click(collidable, callback, buttons, cat),
            {"buttons": buttons, "collidable": collidable})

    def _watch_click(self, collidable, callback, buttons, cat):
        """
        Surveille la présence d'un click complet sur un `collidable`.
        Ne doit pas être appelé en dehors de l'EventManager
        Voir on_click_on
        collidable - L'objet qui peut être cliqué
        callback - La fonction appelé quand l'évènement se produit
        buttons - Le bouton de la souris qui doit être utilisé pour le clic.
        cat - La catégorie du callback. C'est un objet quelconque.
        """
        def on_release(e, id_):
            """
            Callback déclenché au relâchement de la souris
            """
            if self._collide_with(e.pos, collidable):
                callback(e)
            self.callbacks.remove_callback(id_)
        id_ = self.callbacks.add_callback(
            "mouseup", cat, None, {"buttons": buttons})
        call = self.callbacks.get_callback_object(id_)
        call.callback = lambda e: on_release(e, id_)

    def on_mouse_up(self, callback, cat, buttons=1, collidable=None):
        """
        Enregistre un `callback` déclenché quand le ou les boutons `buttons`
        de la souris sont relâchés. un objet `collidable` peut être fourni,
        si c'est le cas, l'évènement n'est déclenché que si les boutons sont
        relâchés quand la souris est sur le `collidable`.
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        buttons - Le bouton de la souris qui doit être utilisé pour le clic.
        collidable - L'objet qui doit être en collision avec la souris.
        """
        if not isinstance(buttons, tuple):
            buttons = (buttons,)
        return self.callbacks.add_callback(
            "mouseup", cat, callback,
            {"buttons": buttons, "collidable": collidable})

    def on_mouse_down(self, callback, cat, buttons=1, collidable=None):
        """
        Enregistre un `callback` déclenché quand le ou les boutons `buttons`
        de la souris sont pressés. un objet `collidable` peut être fourni,
        si c'est le cas, l'évènement n'est déclenché que si les boutons sont
        pressés quand la souris est sur le `collidable`.
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        buttons - Le bouton de la souris qui doit être utilisé pour le clic.
        collidable - L'objet qui doit être en collision avec la souris.
        """
        if not isinstance(buttons, tuple):
            buttons = (buttons,)
        return self.callbacks.add_callback(
            "mousedown", cat, callback,
            {"buttons": buttons, "collidable": collidable})

    def on_mouse_in(self, collidable, callback, cat):
        """
        Enregistre un `callback` déclenché quand la souris entre dans un
        objet `collidable`.
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        collidable - L'objet qui doit être en collision avec la souris.
        """
        def unlock_remove(id1, id2):
            self.unlock_callback(id1)
            self.remove_callback(id2)

        def inside(event, id_):
            callback(event)
            self.lock_callback(id_)
            id2 = self.on_mouse_out(collidable, None, cat)
            call = self.callbacks.get_callback_object(id2)
            call.callback = lambda e: self._watch_move_out(
                lambda e: unlock_remove(id_, id2), cat, collidable)
        id_ = self.callbacks.add_callback(
            "mousemotion", cat, None,
            {"collidable": collidable})
        call = self.callbacks.get_callback_object(id_)
        call.callback = lambda e: inside(e, id_)
        return id_

    def on_mouse_out(self, collidable, callback, cat):
        """
        Enregistre un `callback` déclenché quand la souris sort d'un
        objet `collidable`.
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        collidable - L'objet qui doit être en collision avec la souris.
        """
        return self.callbacks.add_callback(
            "mousemotion", cat,
            lambda e: self._watch_move_out(callback, cat, collidable),
            {"collidable": collidable})

    def _watch_move_out(self, callback, cat, collidable):
        """
        Fonction interne qui surveille la sortie de la souris
        d'un collidable. Quand c'est le cas, `callback` est déclenché.
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        collidable - L'objet qui doit être en collision avec la souris.
        """
        def when_is_out(event, id_):
            if not self._collide_with(event.pos, collidable):
                callback(event)
                self.remove_callback(id_)
        id_ = self.on_mouse_move(None, cat)
        call = self.callbacks.get_callback_object(id_)
        call.callback = lambda e: when_is_out(e, id_)

    def on_mouse_move(self, callback, cat):
        """
        Enregistre un `callback` déclenché quand la souris se déplace
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        """
        return self.callbacks.add_callback(
            "mousemotion", cat, callback, None)

    def on_quit(self, callback, cat):
        """
        Enregistre un `callback` déclenché quand le jeu est quitté,
        c'est-à-dire quand l'utilisateur clique sur la "X" ou bien
        fait Alt+F4 par exemple.
        callback - La fonction appelé quand l'évènement se produit
        cat - La catégorie du callback. C'est un objet quelconque.
        """
        self.callbacks.add_callback("quit", cat, callback, None)

    def run(self, events):
        """
        Récolte et déclenche les callbacks qui correspondent aux
        `events` reçus. Cette fonction doit être déclenchée à chaque tour
        de boucle prinicipale.
        L'ordre d'éxecution des callbacks n'est pas garanti.
        events - Les events pygame qui se sont déroulés depuis le dernier
                 appel de `run`
        """
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
        """
        Appel réel des callbacks à déclencher
        """
        for callback in callbacks_to_run:
            callback[0](callback[1])

    def manage_key_event(self, event, type_):
        """
        Récupère tous les callbacks correspondant aux évènements
        qui se sont produit. Spécialisé pour le clavier
        event - L'event clavier à traiter
        type_ - le type d'event (KEY_DOWN ou KEY_UP)
        """
        callbacks_to_run = []
        for callback in self.callbacks.get_type(type_):
            if callback.params["key"] is None or\
                    callback.params["key"] == event.key or\
                    callback.params["key"] == event.unicode:
                callbacks_to_run.append((callback.callback, event))
        return callbacks_to_run

    def manage_mouse_motion_event(self, event):
        """
        Récupère tous les callbacks correspondant aux évènements
        qui se sont produit. Spécialisé pour les mouvements de la souris
        event - L'event mouse_motion à traiter
        """
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
        """
        Récupère tous les callbacks correspondant aux évènements
        qui se sont produit. Spécialisé pour les clics souris.
        event - L'event souris à traiter
        type_ - le type d'event ("mousedown" ou "mouseup")
        """
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
        """
        Test la collision entre une coordonée `coord` et
        un `collidable`.
        coord - les coordonnées (typiquement un tuple (x, y)
        collidable - L'objet auquel on test la collision
        """
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
        """
        Supprime les callbacks `*args`
        *args - l'id des callbacks à supprimer
        """
        for id_call in args:
            self.callbacks.remove_callback(id_call)

    def lock_callback(self, *ids):
        """
        Verrouille les callbacks `*ids`. Ils ne sont pas
        appelés s'ils sont verouillés, mais ne sont pas non plus
        supprimé.
        Les verrous s'ajoutent. Il faut donc déverrouiller autant de fois
        que le callback a été verouillé pour qu'il puisse de nouveau
        s'exécuter.
        *ids - Les ids des callbacks à verouiller
        """
        for id_call in ids:
            self.callbacks.lock_callback(id_call)
        return ids

    def lock_categories(self, *categories):
        """
        Verrouille les callbacks appartenant aux `*categories`.
        Ils ne sont pas appelés s'ils sont verouillés, mais ne sont
        pas non plus supprimés.
        Les verrous s'ajoutent. Il faut donc déverrouiller autant de fois
        que le callback a été verouillé pour qu'il puisse de nouveau
        s'exécuter.
        *ids - Les catégories des callbacks à verouiller
        """
        for category in categories:
            self.callbacks.lock_category(category)
        return categories

    def unlock_callback(self, *ids):
        """
        Déverrouille les callbacks `*ids`. Ils ne sont pas
        appelés s'ils sont verouillés, mais ne sont pas non plus
        supprimé.
        Les verrous s'ajoutent. Il faut donc déverrouiller autant de fois
        que le callback a été verouillé pour qu'il puisse de nouveau
        s'exécuter.
        *ids - Les ids des callbacks à déverouiller
        """
        for id_call in ids:
            self.callbacks.unlock_callback(id_call)

    def unlock_categories(self, *categories):
        """
        Déverrouille les callbacks appartenant aux `*categories`.
        Ils ne sont pas appelés s'ils sont verouillés, mais ne sont
        pas non plus supprimés.
        Les verrous s'ajoutent. Il faut donc déverrouiller autant de fois
        que le callback a été verouillé pour qu'il puisse de nouveau
        s'exécuter.
        *ids - Les catégories des callbacks à verouiller
        """
        for category in categories:
            self.callbacks.unlock_category(category)

    def lock_all_categories_but(self, *categories, **options):
        """
        Verouille toutes les catégories de callback sauf celles
        présentent dans `categories` ainsi que celle protégées
        (voir EventManager.__init__).
        Les catégories protégées peuvent être forcées à être verouillées avec
        `lock_all_categories_but(categorie1, lock_protected=True)`
        categories - Les catégories à *ne pas* verouiller
        options - si lock_protected=True, alors forcer le verouillage
                  des catégories protégées
        """
        lock_protected = options.get("lock_protected", False)
        if not lock_protected:
            categories = list(categories) + self.protected_categories
        locked_categories = [category for category in
                             self.callbacks.categories
                             if category not in categories]
        return self.lock_categories(*locked_categories)


class CallbacksContainer():
    """
    Contient les callbacks et les manipulent
    """

    def __init__(self):
        """
        Initialise le conteneur
        """
        self._callbacks = {}

    def add_callback(self, type_, category, callback, params=None):
        """
        Ajoute un callback et retourne l'id du callback pour
        pouvoir le supprimer ensuite.
        """
        callbackObj = Callback(callback, params, category)
        try:
            self._callbacks[type_].append(callbackObj)
        except KeyError:
            self._callbacks[type_] = [callbackObj]
        return (type_, callbackObj)

    def remove_callback(self, id_):
        """
        Supprime un callback grâce à son id
        id_ - L'id du callback
        """
        try:
            self._callbacks[id_[0]] = [x for x in self._callbacks[id_[0]]
                                       if x != id_[1]]
        except KeyError:
            pass
        except ValueError:
            pass

    def purge_category(self, cat):
        """
        Supprime tous les callbacks d'une categorie
        cat - La catégorie, qui peut être n'importe quel objet
        """
        for callbackslist in self._callbacks.values():
            for i, callback in enumerate(callbackslist):
                if callback.category == cat:
                    del callbackslist[i]

    def get_callback_object(self, id_):
        """
        Retourne l'objet Callback correspondant à son id.

        Bien que le callback soit contenu dans son id, cette méthode
        doit être utilisée pour éviter des erreurs dûes à des changements
        dans l'implémentation des id.
        """
        return id_[1]

    def lock_callback(self, id_):
        """
        Verouille le callback qui a l'id `id_`.
        """
        self.get_callback_object(id_).lock()

    def unlock_callback(self, id_):
        """
        Déverouille le callback qui a l'id `id_`.
        """
        self.get_callback_object(id_).unlock()

    def get_type(self, type_, with_locked=False):
        """
        Retourne tous les callbacks correspondant au type `type_`.
        Si `with_locked` est à `True`, alors même les callbacks
        verrouillés sont retournés.
        """
        try:
            return [callback for callback in self._callbacks[type_]
                    if not callback.is_locked or with_locked]
        except KeyError:
            return []

    def get_category(self, category, with_locked=False):
        """
        Retourne tous les callbacks correspondant à la catégorie `category`.
        Si `with_locked` est à `True`, alors même les callbacks
        verrouillés sont retournés.
        """
        callbacks = []
        for callbackslist in self._callbacks.values():
            for callback in callbackslist:
                if callback.category is category:
                    callbacks.append(callback)
        return callbacks

    def lock_category(self, category):
        """
        Verrouille les callbacks contenus dans la catégorie `category`.
        """
        for callback in self.get_category(category, True):
            callback.lock()

    def unlock_category(self, category):
        """
        Déverrouille les callbacks contenus dans la catégorie `category`.
        """
        for callback in self.get_category(category, True):
            callback.unlock()

    @property
    def categories(self):
        """
        Propriétés qui contient la liste de toutes les catégories présentes
        dans le conteneur.
        """
        categories = []
        for callbackslist in self._callbacks.values():
            for callback in callbackslist:
                if callback.category not in categories:
                    categories.append(callback.category)
        return categories


class Callback():
    """Objet Callback"""

    def __init__(self, callback, params, category):
        """
        Initialise le Callback
        callback - La fonction à exécuter
        params - Les paramètres du callback
        category - La catégorie du callback
        """
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
        """
        Nombre de fois que le callback a été verouillé
        """
        return max(0, self._num_locked)

    @num_locked.setter
    def num_locked(self, value):
        """
        Setter pour le nombre de fois que le callback a été verrouillé
        """
        self._num_locked = max(0, value)

    @property
    def is_locked(self):
        """
        Propriété qui retourne True si le callback est verrouillé
        """
        return self.num_locked > 0

    def lock(self):
        """Verrouille le callback"""
        self.num_locked += 1

    def unlock(self):
        """
        Deverrouille le callback.

        Le callback est effectivement déverrouiller si num_locked == 0,
        sinon, sont nombre de verrou ne fait que descendre de 1.
        """
        self.num_locked -= 1

    def __repr__(self):
        """
        Représentation d'un callback pour débuggage
        """
        return ("callback: " + repr(self.callback) + " ; params: "
                + repr(self.params)
                + " ; category: " + repr(self.category)
                + " ; num_locked: {}".format(self.num_locked))


def test():
    """
    Tests variés pour tester le système de callback
    """
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
