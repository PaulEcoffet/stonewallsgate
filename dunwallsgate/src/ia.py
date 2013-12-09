import random


class IA(object):

    def __init__(self, battle):
        self.battle = battle

    def play(self):
        playing_char = self.battle.playing_char
        best = self.get_best_weapon()
        if (best[0] is not playing_char.weapon
                or best[1] is not playing_char.weapon.ammo):
            self.battle.change_weapon(*best)
        else:
            self.battle.do_attack(
                random.choice(self.battle.possible_targets_attack()))

    def get_best_weapon(self):
        playing_char = self.battle.playing_char
        best = (playing_char.inventory.get_first("bare_hands"), None)
        for weapon in playing_char.inventory.weapons:
            for ammo in (playing_char.inventory
                         .get_compatible_ammo(weapon)):
                if (weapon.weapon_power_with(ammo)
                        > best[0].weapon_power_with(best[1])):
                    if not ammo or ammo.amount > 0:
                        best = (weapon, ammo)
        return best
