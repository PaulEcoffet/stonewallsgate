import random

import inventory
from character import Character


class Battle(object):
    """Represent a Battle"""

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.run = [False, False]
        self.turn_list = sorted(team1 + team2,
                                key=lambda character: character.initiative)
        self.cur_player_index = 0
        self.has_played = False

    @property
    def playing_char(self):
        return self.turn_list[self.cur_player_index]

    @property
    def cur_player_team(self):
        if self.playing_char in self.team1:
            return 1
        else:
            return 2

    @property
    def winner(self):
        if not [charact for charact in self.team1 if charact.is_alive] or self.run[0]:
            return 2
        elif not [charact for charact in self.team2 if charact.is_alive] or self.run[1]:
            return 1
        else:
            return None

    @property
    def all_characters(self):
        return self.team1 + self.team2

    def do_attack(self, target):
        if not self.has_played:
            if self.can_attack(target):
                try:
                    target.health -= round(
                        (self.playing_char.attack
                         + self.playing_char.weapon.use_weapon()
                         - target.defense) * random.gauss(1, 0.05))
                except inventory.IncompatibleAmmoException:
                    raise CantAttackException("Plus de munitions")
                else:
                    self.has_played = True
            else:
                raise CantAttackException("Cible impossible")
        else:
            raise AlreadyPlayedException()

    def can_attack(self, target):
        return ((target in self.team1 and self.playing_char in self.team2)
                or (target in self.team2 and self.playing_char in self.team1)
                and target.is_alive)

    def possible_targets_attack(self):
        if self.cur_player_team == 1:
            return [character for character in self.team2
                    if character.is_alive]
        else:
            return [character for character in self.team1
                    if character.is_alive]

    def change_weapon(self, weapon, ammo):
        if not self.has_played:
            if weapon in self.playing_char.inventory.items:
                if ammo in self.playing_char.inventory.items or not ammo:
                    try:
                        weapon.ammo = ammo
                        self.playing_char.weapon = weapon
                    except inventory.IncompatibleAmmoException as e:
                        raise e
                    else:
                        self.has_played = True
                else:
                    raise CantChangeWeaponException("Ces munitions ne sont pas dans votre sac")
            else:
                raise CantChangeWeaponException("Cette arme n'est pas dans votre sac")
        else:
            raise AlreadyPlayedException()

    def end_turn(self):
        self.has_played = False
        self.cur_player_index = ((self.cur_player_index + 1)
                                 % len(self.turn_list))
        while self.playing_char.is_dead:
            self.cur_player_index = ((self.cur_player_index + 1)
                                     % len(self.turn_list))
        return self.winner


class CantAttackException(Exception):
    pass


class CantChangeWeaponException(Exception):
    pass


class AlreadyPlayedException(Exception):
    pass


def test():
    gordon = Character("hero")
    gordon.inventory = inventory.Inventory("begining_inventory")
    gordon.weapon = gordon.inventory.get_first("gun")
    gordon.weapon.ammo = gordon.inventory.get_compatible_ammo(
        gordon.weapon)[0]
    klim = Character("klim")
    battle = Battle([gordon], [klim])
    while not battle.winner:
        battle.do_attack(battle.possible_targets_attack()[0])
        print("klim health: {}".format(klim.health))
        print("gordon health: {}".format(gordon.health))
        battle.end_turn()
    print("The team {} has won".format(battle.winner))


if __name__ == "__main__":
    test()
