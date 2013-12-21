import unittest
from collections import Counter

import battle
import inventory
from character import Character


class TestBattle(unittest.TestCase):

    def test_init_battle(self):
        char1 = Character(None, maxhealth=100, initiative=1000)
        char2 = Character(None, maxhealth=100, initiative=1)
        battle1 = battle.Battle([char1], [char2])
        self.assertListEqual(battle1.team1, [char1])
        self.assertListEqual(battle1.team2, [char2])
        self.assertIs(battle1.playing_char, char1)

    def test_possible_target(self):
        char1 = Character(None, maxhealth=100, initiative=1000)
        char2 = Character(None, maxhealth=100, initiative=10)
        char3 = Character(None, maxhealth=100, initiative=1)
        battle1 = battle.Battle([char1], [char2, char3])
        self.assertEqual(Counter(battle1.possible_targets_attack()),
                         Counter([char2, char3]))
        battle1.end_turn()
        self.assertEqual(Counter(battle1.possible_targets_attack()),
                         Counter([char1]))

    def test_do_attack(self):
        char1 = Character(None, maxhealth=100, initiative=1000, attack=2)
        char2 = Character(None, maxhealth=100, initiative=1, defense=0)
        battle1 = battle.Battle([char1], [char2])
        battle1.do_attack(char2)
        self.assertLessEqual(char2.health, char2.maxhealth)
        battle1.end_turn()
        self.assertRaises(battle.CantAttackException, battle1.do_attack,
                          char2)

    def test_end_turn(self):
        char1 = Character(None, maxhealth=100, initiative=1000, attack=2)
        char2 = Character(None, maxhealth=100, initiative=1, defense=0)
        battle1 = battle.Battle([char1], [char2])
        battle1.end_turn()
        self.assertIs(battle1.playing_char, char2)

    def test_get_all_character(self):
        char1 = Character(None, maxhealth=100, initiative=1000, attack=2)
        char2 = Character(None, maxhealth=100, initiative=1, defense=0)
        battle1 = battle.Battle([char1], [char2])
        self.assertEqual(Counter((char1, char2)),
                         Counter(battle1.all_characters))

    def test_get_current_playe_team(self):
        char1 = Character(None, maxhealth=100, initiative=1000, attack=2)
        char2 = Character(None, maxhealth=100, initiative=1, defense=0)
        battle1 = battle.Battle([char1], [char2])
        self.assertEqual(battle1.cur_player_team, 1)
        battle1.end_turn()
        self.assertEqual(battle1.cur_player_team, 2)

    def test_win(self):
        char1 = Character(None, maxhealth=10, initiative=1000)
        char2 = Character(None, maxhealth=10, initiative=10)
        char3 = Character(None, maxhealth=10, initiative=1)
        battle1 = battle.Battle([char1], [char2, char3])
        self.assertIsNone(battle1.winner)
        battle1.do_run()
        self.assertEqual(battle1.winner, 2)
        battle2 = battle.Battle([char1], [char2, char3])
        while char1.is_alive:
            if battle2.cur_player_team == 2:
                battle2.do_attack(char1)
            battle2.end_turn()
        self.assertEqual(battle2.winner, 2)

        char1 = Character(None, maxhealth=10, initiative=1)
        char2 = Character(None, maxhealth=10, initiative=1000)
        char3 = Character(None, maxhealth=10, initiative=10)
        battle3 = battle.Battle([char1], [char2, char3])
        battle3.do_run()
        self.assertEqual(battle3.winner, 1)
        battle4 = battle.Battle([char1], [char2, char3])
        while char2.is_alive or char3.is_alive:
            if battle4.cur_player_team == 1:
                battle4.do_attack(battle4.possible_targets_attack()[0])
            battle4.end_turn()
        self.assertEqual(battle4.winner, 1)

    def test_can_attack(self):
        char1 = Character(None, maxhealth=100, initiative=1000, attack=2)
        char2 = Character(None, maxhealth=0, initiative=1, defense=0)
        char3 = Character(None, maxhealth=10, initiative=1, defense=0)
        battle1 = battle.Battle([char1], [char2, char3])
        self.assertFalse(battle1.can_attack(char1))
        self.assertFalse(battle1.can_attack(char2))
        self.assertTrue(battle1.can_attack(char3))

    def test_already_played(self):
        char1 = Character(None, maxhealth=100, initiative=1000)
        char2 = Character(None, maxhealth=100, initiative=1)
        gun = inventory.create_item("gun")
        ammo = inventory.create_item("gun_ammo", 20)
        char1.inventory.add(gun)
        char1.inventory.add(ammo)
        battle1 = battle.Battle([char1], [char2])
        battle1.do_attack(battle1.possible_targets_attack()[0])
        self.assertRaises(battle.AlreadyPlayedException,
                          battle1.change_weapon, gun, ammo)
        self.assertRaises(battle.AlreadyPlayedException,
                          battle1.do_attack,
                          battle1.possible_targets_attack()[0])

    def test_change_weapon(self):
        char1 = Character(None, maxhealth=100, initiative=1000)
        gun = inventory.create_item("gun")
        ammo = inventory.create_item("gun_ammo", 20)
        char1.inventory.add(gun)
        char1.inventory.add(ammo)
        battle1 = battle.Battle([char1], [])
        battle1.change_weapon(gun, ammo)
        battle1.end_turn()
        self.assertRaises(battle.CantChangeWeaponException,
                          battle1.change_weapon,
                          inventory.create_item("gun"), ammo)
        self.assertRaises(battle.CantChangeWeaponException,
                          battle1.change_weapon,
                          gun, inventory.create_item("gun_ammo"))
        self.assertRaises(inventory.IncompatibleAmmoException,
                          battle1.change_weapon,
                          gun, None)
        battle1.change_weapon(char1.inventory.get_first("bare_hands"), None)
