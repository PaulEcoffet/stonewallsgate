"""
Ce module comporte l'objet Battle, qui décrit un combat, et les
différentes exceptions qui peuvent se produire durant celui-ci.
"""
import random

import inventory


class Battle(object):
    """Represente un Battle"""

    def __init__(self, team1, team2):
        """
        Initialise un Battle avec `team1` et `team2` des list de Characters
        """
        self.team1 = team1
        self.team2 = team2
        self.run = [False, False]
        self.turn_list = sorted(team1 + team2,
                                key=lambda character: character.initiative,
                                reverse=True)
        self.cur_player_index = 0
        self.has_played = False
        self.last_action = ""

    @property
    def playing_char(self):
        """
        Le joueur qui a la main
        """
        return self.turn_list[self.cur_player_index]

    @property
    def cur_player_team(self):
        """
        L'indice de la team du joueur qui a la main
        """
        if self.playing_char in self.team1:
            return 1
        else:
            return 2

    @property
    def winner(self):
        """
        L'indice de la team qui a gagné le combat. Si personne n'a gagné, alors
        winner vaut None
        """
        if not [charact for charact in self.team1 if charact.is_alive] or self.run[0]:
            return 2
        elif not [charact for charact in self.team2 if charact.is_alive] or self.run[1]:
            return 1
        else:
            return None

    @property
    def all_characters(self):
        """
        La liste de l'ensemble des protagonistes du combat
        """
        return self.team1 + self.team2

    def do_attack(self, target):
        """
        Faire attaquer effectivement le joueur qui a la main sur `target`.
        Peut émettre une CantAttackException ou une AlreadyPlayedException.
        """
        if not self.has_played:
            if self.can_attack(target):
                try:
                    damage = max(0, round(
                        (self.playing_char.attack
                         + self.playing_char.weapon.use_weapon()
                         - target.defense) * random.gauss(1, 0.05)))
                    target.health -= damage
                except inventory.IncompatibleAmmoException:
                    raise CantAttackException("Le chargeur est vide. Rechargez ou changez d'arme")
                else:
                    self.has_played = True
                    if self.playing_char.weapon.ammo:
                        self.last_action = "{} a attaqué {} avec {} et {}."\
                            " Cela lui a infligé {} dégats.".format(
                                self.playing_char.name, target.name,
                                self.playing_char.weapon.caracts["name"],
                                self.playing_char.weapon.ammo.caracts["name"],
                                damage)
                    else:
                        self.last_action = "{} a attaqué {} avec {}."\
                            " Cela lui a infligé {} dégats.".format(
                                self.playing_char.name, target.name,
                                self.playing_char.weapon.caracts["name"],
                                damage)
            else:
                raise CantAttackException("Cible impossible")
        else:
            raise AlreadyPlayedException()

    def can_attack(self, target):
        """
        Renvoie True si le joueur qui a la main peut attaquer `target`, sinon
        retourne False
        """
        return ((target in self.team1 and self.playing_char in self.team2)
                or (target in self.team2 and self.playing_char in self.team1)
                and target.is_alive)

    def possible_targets_attack(self):
        """
        Renvoie la liste des cibles possibles en attaque pour le joueur qui a la main
        """
        if self.cur_player_team == 1:
            return [character for character in self.team2
                    if character.is_alive]
        else:
            return [character for character in self.team1
                    if character.is_alive]

    def change_weapon(self, weapon, ammo):
        """
        Change l'arme actuel du joueur qui a la main pour l'arme `weapon` avec
        les munitions `ammo`.
        Peut émettre une CantChangeWeaponException ou une
        AlreadyPlayedException.
        """
        if not self.has_played:
            if weapon in self.playing_char.inventory.weapons:
                if ammo in self.playing_char.inventory.items or not ammo:
                    try:
                        weapon.ammo = ammo
                        old_weapon = self.playing_char.weapon
                        self.playing_char.weapon = weapon
                    except inventory.IncompatibleAmmoException as e:
                        raise e
                    else:
                        self.has_played = True
                        if old_weapon.ammo:
                            self.last_action = "{} change son {} avec {} pour ".format(
                                self.playing_char.name,
                                old_weapon.caracts["name"],
                                old_weapon.ammo.caracts["name"])
                        else:
                            self.last_action = "{} change son {} pour ".format(
                                self.playing_char.name,
                                old_weapon.caracts["name"])
                        if weapon.ammo:
                            self.last_action += "{} avec {}".format(
                                weapon.caracts["name"], weapon.ammo.caracts["name"])
                        else:
                            self.last_action += "{}".format(
                                weapon.caracts["name"])
                else:
                    raise CantChangeWeaponException("Ces munitions ne sont pas dans votre sac")
            else:
                raise CantChangeWeaponException("Cette arme n'est pas dans votre sac")
        else:
            raise AlreadyPlayedException()

    def do_run(self):
        """
        Fait fuire l'équipe du joueur qui a la main
        """
        if self.playing_char in self.team1:
            self.run[0] = True
        else:
            self.run[1] = True

    def end_turn(self):
        """
        Termine le tour du joueur qui a la main et donne la main au joueur
        suivant.
        """
        self.has_played = False
        self.cur_player_index = ((self.cur_player_index + 1)
                                 % len(self.turn_list))
        while self.playing_char.is_dead:
            self.cur_player_index = ((self.cur_player_index + 1)
                                     % len(self.turn_list))
        return self.last_action


class CantAttackException(Exception):
    """Exception lancéé si le joueur ne peut pas attaquer"""
    pass


class CantChangeWeaponException(Exception):
    """Exception lancée si le joueur ne peut pas changer d'arme"""
    pass


class AlreadyPlayedException(Exception):
    """
    Exception lancée si le joueur a déjà joué et ne peut pas effectuer une
    deuxième action
    """
    pass


