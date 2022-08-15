# Legend of the Red Dragon
# Requires at least Python 3.6.1

# Importing Python functions for use later on
import sys

# Global variables stored inside a dictionary for easy access
player_char = { 
	'player_race' : ' ',
	'player_class' : ' ',
	'player_health' : 0,
	'player_defence' : 0,
	'player_attack' : 0,
	'player_name' : ' ',
	'player_armor' : ' ',
	'player_experience' : 0,
	'player_level' : 1,
	'player_gold' : 10
	# This is the default template for a new character
	# Defined each time the program is loaded
	# Loaded characters will load the stats they had when they saved
	# Can be accessed with player_char['stat' : str/integer]
}

# The below section is dedicated to defining functions, that act as 
# the game's modular structure. Because of this modularity, functions 
# are defined in reverse order so they can be accessed freely
# by the program.

# The start menu is found at the bottom of the program, which is where
# order the player will be assumed to go in, though it is mostly dependent
# on which areas are accessible by the player in each instance e.g. the
# player can't go straight to the shop from the inn, and vice versa

def InnLocation():
	while True:
		inn_input = input("""
The innkeeper looks at you as you enter.

"How might I help you?" he says.

"Heard any [R]umors lately? 
[S]ave Game - "I'd like to rest here." 
[H]eal - "I'm hurt."
[G]o Back - "Nothing, thanks. I'll take my leave."
""").lower()
		if inn_input == "r":
			print("Haven't heard anything yet, check by later.")
		elif inn_input == "s":
			player_char = open
		elif inn_input == "h":
			pass
		elif inn_input == "g":
			VillageHub()
			break
		else:
			print("Enter one of the letters inside the brackets")


def VillageHub():
	while True:
		village_location_input = input("""
You stand in the village square. Where do you want to go?

Visit the [I]nn
Visit the [S]hop
Visit the [T]rainer
Visit the [F]orest
[R]etire from your investigation into the 'Red Dragon'
""").lower()
		if village_location_input == "i":
			InnLocation()
			break
		elif village_location_input == "s":
			ShopLocation()
			break
		elif village_location_input == "t":
			TrainerLocation()
			break
		elif village_location_input == "f":
			ForestLocation()
			break
		elif village_location_input == "r"
			print("You retire. [placeholder message]")
			StartMenu()
			break
		else:
			print("Enter one of the letters inside the brackets")

def CharacterCreation():
	while True:
		player_race_input = input("""
The land of Caladaria is inhabited by three races -- humans, elves and dwarves.
You find yourself to be:
[H]uman
[E]lvish
[D]warven
""").lower() 
		if player_race_input == "h":
			player_char['player_race'] = 'Human'
			player_char['player_health'] = 10
			player_char['player_defence'] = 10
			player_char['player_attack'] = 10
			print("""
Humans, jack of all trades, master of none. Lacking the offensive capabilities
of the Dwarves and the natural protection of the Elves, Humans make up for it
in their tendency to exceed against ever-rising odds. Perhaps you may find the
answers you seek in the lush monster-infested land of Caladaria, where your 
parents went missing several years ago in search of the 'Red Dragon.'""")
			break
		elif player_race_input == "e":
			player_char['player_race'] = "Elf"
			player_char['player_health'] = 12
			player_char['player_defence'] = 8
			player_char['player_attack'] = 10
			print("""
Elves, the first recorded inhabitants of Caladaria. Your innate, mutual affinity
 towards the natural world lends you additional survivability against your 
enemies, but is offset by your inherent frailness. Perhaps you may find the
answers you seek in the lush monster-infested land of Caladaria, where your 
parents went missing several years ago in search of the 'Red Dragon.' """)
			break
		elif player_race_input == "d":
			player_race = "Dwarf"
			player_char['player_health'] = 8
			player_char['player_defence'] = 10
			player_char['player_attack'] = 12
			print("""
Dwarves, a proud short-statured race that is capable of more than meets the 
 eye. Against enemies, you are able to exploit weak spots and deal increased 
amounts of damage, though your studyness is slightly outclassed by other races.
 Perhaps you may find the answers you seek in the lush monster-infested land 
of Caladaria, where your parents went missing several years ago in search 
of the 'Red Dragon.' """)
			break
		else:
			print("Enter one of the letters inside the brackets")
	while True:
		player_class_input = input("""
You see a lit up village in the distance. Along with a inconsistent arrangement
 of houses up ahead, you see four distinct buildings in the distance, with one 
of them looking like an inn. You decide that would be a good place to settle in
 during your invesigation into the red dragon mystery.

When you are ready, you grab your:
[S]word (Warrior)
[D]agger (Rogue)
[St]aff (Mage) 
""").lower()
		if player_class_input == "s":
			player_char['player_class'] = 'Warrior'
			player_char['player_health'] += 5
			player_char['player_defence'] += 5
			player_char['player_attack'] += 5
		elif player_class_input == "d":
			player_char['player_class'] = 'Rogue'
			player_char['player_health'] += 4
			player_char['player_defence'] += 7
			player_char['player_attack'] += 6
		elif player_class_input == "st":
			player_char['player_class'] = 'Mage'
			player_char['player_health'] += 3
			player_char['player_defence'] += 3
			player_char['player_attack'] += 7
		else:
			print("Enter one of the letters inside the brackets")
		player_name_input = input("""
What is your name?
""")
		player_char['player_name'] = player_name_input
		break
	while True:
		player_confirmation_input = input("""
Before you venture on...

Is this your true self?

Name : {}
Race : {}
Class : {}
Health : {}
Defence : {}
Attack : {}
		
[Y]es
[N]o, I want to go back
""".format(player_char['player_name'], player_char['player_race'],
			 player_char['player_class'], player_char['player_health'], 
			 player_char['player_defence'], player_char['player_attack'])).lower()
		if player_confirmation_input == "y":
			VillageHub()
		elif player_confirmation_input == "n":
			CharacterCreation()
			break # stop the loop just in case it still runs later on
		else:
			print("Enter one of the letters inside the brackets")

def LoadGame():
	print("this works")

def StartMenu():
	repeat = True
	while repeat == True:
		main_menu_input = input("""
[N]ew Game
[L]oad Game
[E]xit Game
""").lower()
		if main_menu_input == "n":
			CharacterCreation()
		elif main_menu_input == "l":
			LoadGame()
		elif main_menu_input == "e":
			sys.exit() # this is assuming ‘sys’ has been imported prior to this code being executed
		else:
			print("Enter one of the letters inside the brackets.")

StartMenu()