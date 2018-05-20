import random


class bcolors:
    HEADER = "\033[95M"
    OKBLUE = "\033[94m"
    OKGREEN = '\033[92m'
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = "\033[4m"


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atklow = atk - 10
        self.atkhigh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atklow, self.atkhigh)

    def heal(self, hp):
        self.hp += hp
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + "Actions")
        for item in self.actions:
            print(str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + "Magic")
        for spell in self.magic:
            print(str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_items(self):
        i = 1
        print(bcolors.OKGREEN + bcolors.BOLD + "Items:" + bcolors.ENDC)
        for item in self.items:
            print(str(i) + ".", item["item"].name, ":", item["item"].description, "(x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n " + bcolors.FAIL + bcolors.BOLD + "      Target:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1

        choice = int(input("    Choose Target:")) - 1
        return choice

    def get_stats(self):

        hp_bar = ""
        hp_bar_ticks = (self.hp / self.maxhp) * 100 / 4
        mp_bar = ""
        mp_bar_ticks = (self.mp / self.maxmp) * 100 / 10

        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        if len(str(self.hp)) == 3:
            hp_space = 20
        else:
            hp_space = 19

        if len(str(self.mp)) == 2:
            mp_space = 10
        else:
            mp_space = 9

        print("Name                  HP                                       MP")
        print(" " * (hp_space + mp_space) + "_________________________              __________")
        print(
            self.name + "               " + str(self.hp) + "/" + str(
                self.maxhp) + "|" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|       " + str(self.mp) + "/" + str(
                self.maxmp) + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1
        while len(hp_bar) < 50:
            hp_bar += " "

        hp_space = 26 + len(str(self.hp))

        print("Name                  HP                                       ")
        print(" " * hp_space + "__________________________________________________")
        print(
            self.name + "               " + str(self.hp) + "/" + str(
                self.maxhp) + "|" + bcolors.FAIL + hp_bar + bcolors.ENDC + "|       ")
        print("\n")

    def choose_enemy_spell(self):

        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_damage = spell.generate_damage()

        pct = self.hp / self.maxhp * 100

        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_damage
