# Legend of the Red Dragon
# Requires at least Python 3.6.1

# Importing Python functions for use later on
import sys # so we can use sys.exit() to exit the game
import os  # so we can check if a savegame exists before loading it

# Global variables stored inside a dictionary for easy access
player_char = { 
	'player_race' : ' ',
	'player_class' : ' ',
	'player_health' : 0,
	'player_defence' : 0,
	'player_attack' : 0,
	'player_name' : ' ',
	'player_armor' : ' ',
	'player_weapon' : ' ',
	'player_experience' : 0,
	'player_level' : 1,
	'player_gold' : 100
	# This is the default template for a new character
	# Defined each time the program is loaded
	# Loaded characters will load the stats they had when they saved
	# Can be accessed with player_char['stat' : str/integer]
}

# The below section is dedicated to defining functions, that act as 
# the game's modular structure. Because of this modularity, functions 
# are defined in reverse order so they can be accessed freely
# by the program.

# The start menu is found at the bottom of the program, which is the order in
# which the player will be assumed to go in, though it is mostly dependent
# on which areas are accessible by the player in each instance e.g. the
# player can't go straight to the shop from the inn, and vice versa

def Debug():
	print("If you are seeing this, it works")

def ShopLocation():
	starter_tier_name = "Steel"
	mid_tier_name = "Knight"
	end_tier_name = "Elite Knight"
	# In the order of [Sword, Shield, Boots, Gauntlets, Helmet, Armor]
	starter_tier_stats = [6, 6, 1, 2, 3, 4]
	mid_tier_stats = [8, 8, 3, 4, 5, 6]
	end_tier_stats = [12, 10, 6, 8, 10, 12]
	# Weapons will always be the first item in the list
	# Now check what items the shopkeeper will sell
	# (depending on the player's level)
	if player_char['player_level'] <= 5:
		gear_name = starter_tier_name
		shop_selling = starter_tier_stats
	elif player_char['player_level'] >= 5 and player_char['player_level'] <= 10:
		gear_name = mid_tier_name
		shop_selling = mid_tier_stats
	elif player_char['player_level'] >= 10:
		gear_name = end_tier_name
		shop_selling = end_tier_stats
	# These variables are used so three different code instances of the player
	# buying different tiers of gear wouldn't have to be created
	while True:
		print("""
The shopkeeper welcomes you to his shop. You see a tidy arrangement of weapons
and armor pieces sitting along the bench behind him.

"What can I do you for?" he asks.""")
		shop_input = input("""
[Weapons]
[{}] {} Sword - Attack + {} ({} Gold)

[Armor]
[{}] {} Shield - Defence + {} ({} Gold)
[{}] {} Boots - Defence + {} ({} Gold)
[{}] {} Gauntlets - Defence + {} ({} Gold)
[{}] {} Helmet - Defence + {} ({} Gold)
[{}] {} Armor - Defence + {} ({} Gold)
""".format(
1, gear_name, shop_selling[0], shop_selling[0] * 10 + 10,
2, gear_name, shop_selling[1], shop_selling[1] * 10 + 10,
3, gear_name, shop_selling[2], shop_selling[2] * 10 + 10,
4, gear_name, shop_selling[3], shop_selling[3] * 10 + 10,
5, gear_name, shop_selling[4], shop_selling[4] * 10 + 10,
6, gear_name, shop_selling[5], shop_selling[5] * 10 + 10))
		if shop_input == 1: # this will always be a weapon
			player_char['player']


def InnLocation():
	print("The innkeeper looks at you as you enter.")
	while True:
		inn_input = input("""
"Welcome to the Paledrake Inn. How might I help you?"

"Heard any [R]umors lately? 
[S]ave Game - "I'd like to rest here." 
[H]eal - "I'm hurt."
[E]xit - "Nothing, thanks. I'll take my leave."
""").lower()
		if inn_input == "r":
			print("Haven't heard anything yet, check by later.")
		elif inn_input == "s":
			while True:
				save_input = input("""
Saving the game will overwrite the currently saved character's data with this 
one. Check for the presence of savegame.txt in the local directory for past 
characters. Are you sure you want to save your data?

[Y]es
[N]o
""").lower()
				if save_input == "y":
					f = open('savegame.txt',"w") # Create savegame.txt in write mode
					f.write (str(player_char)) # Write the player's stats to the file
					f.close() # Close the file
					print("Successfully saved to savegame.txt in local directory")
					break # Go back to the innkeeper
				elif save_input == "n":
					break 
		elif inn_input == "h":
			pass
		elif inn_input == "e":
			VillageHub()
			break
		else:
			print("Enter one of the letters inside the brackets")


def VillageHub():
	while True:
		village_location_input = input("""
You stand in the village square. 

Where do you want to go?

Visit the [I]nn
Visit the [S]hop
Visit the [T]rainer
Visit the [F]orest
View [Stats]
[R]etire from your investigation into the 'Red Dragon'
[E]xit to Main Menu
""").lower() # The last option is mainly used to exit the game for debug purposes
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
		elif village_location_input == "stats":
			print("""
Character data:

Name : {}
Race : {}
Class : {}
Health : {}
Defence : {}
Attack : {} """.format(player_char['player_name'], player_char['player_race'],
			 player_char['player_class'], player_char['player_health'], 
			 player_char['player_defence'], player_char['player_attack']))
		elif village_location_input == "r":
			print("[placeholder message]")
			StartMenu()
			break
		elif village_location_input == "e":
			print("Exiting game...")
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
	print("Looking for savegame.txt in local directory...")
	if os.path.isfile('./savegame.txt') == True:
	# checking for the existence of savegame.txt in the local directory
		player_char = eval(open("savegame.txt").read())
	# defining the player's stats as whatever is in the contents of the file
		while True:
			load_input = input("""
Character data:

Name : {}
Race : {}
Class : {}
Health : {}
Defence : {}
Attack : {}

[L]oad
[B]ack to Start Menu

""".format(player_char['player_name'], player_char['player_race'],
			 player_char['player_class'], player_char['player_health'], 
			 player_char['player_defence'], player_char['player_attack'])).lower()
			# tell the player the stats of the character inside the savegame
			if load_input == "l":
				InnLocation()
				# go to the inn because it is the only place where the player can save
				break # break the loop just in case it is still active later on
			elif load_input == "e":
				StartMenu()
				# go back to the start menu
				break # break the loop just in case it is still active later on
	else:
		print("savegame.txt was not found in local directory.")
		StartMenu()


def StartMenu():
	while True:
		main_menu_input = input("""
[N]ew Game
[L]oad Game
[E]xit Game
""").lower() # make the user's input lowercase for it to accept more inputs
		if main_menu_input == "n":
			CharacterCreation()
			break # break the loop in case it doesn't stop later on
		elif main_menu_input == "l":
			LoadGame()
			break
		elif main_menu_input == "e":
			sys.exit() # this is assuming ‘sys’ has been imported prior to this code being executed
		else:
			print("Enter one of the letters inside the brackets.")
			# the loop doesn't get broken here, so it just goes back to asking for input

StartMenu() # Initiate the game, other functions don't need to be called
			# because they will be called inside the functions