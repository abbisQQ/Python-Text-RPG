from MiniGame.game import Person, bcolors
from MiniGame.magic import Spell
from MiniGame.inventory import Item
import random

# create magic
fire = Spell("Fire", 15, 150, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 6, 60, "black")
meteor = Spell("Meteor", 20, 200, "black")
cure = Spell("Cure", 10, 100, "white")
cura = Spell("Cura", 20, 200, "white")

# create items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Restore hp and mana of one party member to max values", 9999)
megaelixer = Item("MegaElixer", "elixer", "Restore hp and mana to max values to all the party members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, blizzard, thunder, meteor, cure, cura]

enemy_spells = [fire, meteor, blizzard]

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": megaelixer, "quantity": 5}, {"item": grenade, "quantity": 5}]

# create some people
player1 = Person("Valos: ", 660, 65, 60, 34, player_spells, player_items)
player2 = Person("Nick:  ", 460, 65, 60, 34, player_spells, player_items)
player3 = Person("Robot: ", 960, 65, 60, 34, player_spells, player_items)

players = [player2, player1, player3]

enemy2 = Person("Imp: ", 1200, 100, 45, 55, enemy_spells, [])
enemy1 = Person("Magus", 3000, 100, 45, 55, enemy_spells, [])
enemy3 = Person("Imp: ", 1200, 100, 45, 55, enemy_spells, [])

enemies = [enemy1, enemy2, enemy3]


running = True
i = 0


while running:
    print("================================ New Turn ======================================")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        print(player.get_stats())

    for player in players:

        player.choose_action()

        choice = input("Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(" You attacked " + enemies[enemy].name + " for ", dmg, "point of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has been defeted.")
                del enemies[enemy]

        elif index == 1:

            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_damage = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not enough mp \n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_damage)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_damage), " HP" + bcolors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_damage)

                print(bcolors.OKGREEN + "\n " + spell.name + " deals ", str(magic_damage), " points of damage. to "
                      + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has been defeted.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choise = int(input("Choose item ")) - 1
            if item_choise == -1:
                continue

            if player.items[item_choise]["quantity"] == 0:
                print(bcolors.FAIL + " Noone left...." + bcolors.ENDC)
                continue

            item = player.items[item_choise]["item"]
            player.items[item_choise]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + "deals", str(item.prop), " points of damage to "
                      + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has been defeted.")
                    del enemies[enemy]
    # check if the battle is over
    defeated_enemies = 0
    defeated_players = 0

    for player in players:
        if player.hp == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    # check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win " + bcolors.ENDC)
        running = False
    # check if enemy won
    elif defeated_players == 2:
        print(bcolors.OKGREEN + "You Loose " + bcolors.ENDC)
        running = False

    # enemy phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            print(bcolors.FAIL + bcolors.BOLD + " AN ENEMY ATTACKS!" + bcolors.ENDC)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + bcolors.BOLD +" Enemy " + enemy.name + " attacked " +
                  players[target].name.replace(" ", "") + " for ", enemy_dmg,
                  " point of damage." +bcolors.ENDC)

        elif enemy_choice == 1:

            spell, magic_damage = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                enemy.heal(magic_damage)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + " for ", str(magic_damage), " HP" + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)

                players[target].take_damage(magic_damage)
                print(bcolors.FAIL + bcolors.BOLD + " AN ENEMY ATTACKS!" + bcolors.ENDC)
                print(bcolors.FAIL + " " + enemy.name + ": cast " + spell.name + " deals ",
                      str(magic_damage), " points of damage. to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has been defeted.")
                    del players[target]
