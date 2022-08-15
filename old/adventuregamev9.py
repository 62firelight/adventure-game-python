# Legend of the Red Dragon
# Requires at least Python 3.6.1

# Importing Python functions for use later on
import sys # so we can use sys.exit() to exit the game
import os  # so we can check if a savegame exists before loading it
import random # for forest encounters that generate a random enemy
			  # with different stats

# Global variables stored inside a dictionary for easy access
# (char = character)
player_char = { 
	'player_race' : ' ',
	'player_class' : ' ',
	'player_health' : 0,
	'player_defence' : 0,
	'player_attack' : 0,
	'player_name' : ' ',
	'player_shield' : 0, # Shields count as an armor piece
	'player_boots' : 0, # Armor pieces give a defence boost
	'player_gauntlets' : 0, # There is no inventory system so the names
	'player_helmet' : 0, 	# of the items don't need to shown after they
	'player_armor' : 0,		# have been bought
	'player_weapon' : 0, # Same with weapons, except they give more attack
	'player_experience' : 0,
	'player_level' : 1,
	'player_gold' : 100,
	'first_visit_i' : True, # Is automatically set to False when the player 
							# triggers first encounter dialogue in the inn
	'first_visit_s' : True, # Same as the inn variable, except it's for the inn
	'first_visit_t' : True # Same as the shop variable, except it's for the trainer

	# This is the default template for a new character
	# that is defined each time the program is loaded

	# Loaded characters will load the stats they had when they saved

	# Can be accessed with player_char['stat' : str/integer]
}

# Enemies not yet finalized
starter_forest_enemies = ['Abyssal Beast', 'Lesser Skeleton', 'Feral Wolf']
mid_forest_enemies = ['Hollow Knight', 'Abyss-corrupted Giant', 
					'Decrepit Monstrocity']
end_forest_enemies = ['Speaker of the Abyss', 'Primordial Snake', 
					'Elder Beast']
# These lists should be the same every time the game is run
# meaning that they don't need to be saved to savegame.txt

trainer_disposition = 0
# The above variable is used for dialogue purposes only

player_xp_gain = 50
# Variable for how much XP the player gains from winning fights

invalid_message = "\nEnter the number/letter(s) inside one of the brackets."
# String for when the program expects a number/letter input and the player 
# enters an invalid/unexpected input

# The below section is dedicated to defining functions, that act as 
# the game's modular structure. Because of this modularity, functions 
# are defined in reverse order so they can be accessed freely
# by the program.

# The start menu is found at the bottom of the program, which is the order in
# which the player will be assumed to go in, though it is mostly dependent
# on which areas are accessible by the player in each instance e.g. the
# player can't go straight to the shop from the inn, and vice versa

# Need to implement gold
# Need to implement player_experience and player_level

def debug():
	print("\nIf you are seeing this, it works")

def TrainerLocation():
	if player_char['first_visit_t'] == True: # When the player first goes to
											 # the trainer
		while True: 
			trainer_input = input("""
Upon entering, you spot a man fully clad in black-iron armor striking against 
what appears to be a training dummy. You notice that the entire building takes 
the shape of a large. rectangular arena.

As you approach him, he stops and turns to face you.

"Ah, another who seeks the Red Dragon? Clearly, you must be of some worth, 
to be able to navigate through the abyssal fog in the outskirts of the city.
It's not a task that any odd traveler can accomplish, no.

Yes, I know of the Red Dragon, of where he resides. He is an extraordinarily 
powerful beast, more so than you realize. Many travellers like you have come
and gone, but none of them have survived the gauntlet that precedes him. 

So I must ask, what is your name, and what compels you to seek such a monster?"

[1] "I am %s, and I have come here in search of my parents."
[2] "I am %s, and I seek the glory and fame that comes with slaying the dragon."
[3] "I am %s, a humble explorer that seeks the dragon for my own purposes."
[4] "I am %s, and I'm just a mindless wanderer here for reasons of my own."
""" % (player_char['player_name'], player_char['player_name'], 
	player_char['player_name'], player_char['player_name']))
			if trainer_input == str(1):
				print("""
"You are not the first of your kind. I have seen many orphans travel here in 
search of answers, all of whom have failed in their journey. How far are you 
willing to go for answers? Only time will tell." """)
				trainer_disposition = 1
				confirm = input("\nPush any key to continue.\n")
			elif trainer_input == str(2):
				print("""
"Glory and fame, both very valid reasons for one to travel to this small town, 
but the question remains -- how far will you be willing to go in your quest? 
Only time will tell." """)
				trainer_disposition = 2
				confirm =  input("\nPush any key to continue.\n")
			elif trainer_input == str(3):
				print("""
"A 'humble explorer' you say? To be able to reach this little town through the
abyssal fog is a hefty task in itself, but so is the task of slaying the dragon.
I suppose only time will tell as to how dedicated you will be in your quest." """)
				trainer_disposition = 3
				confirm = input("\nPush any key to continue.\n")
			elif trainer_input == 4:
				print("""
"Navigating through the fog on this town's outskirts is not a task that many
simple 'wanderers' can manage. You have your own reasons for coming here, 
but I believe that only time will tell as to whether these reasons are 
compelling enough for you to accomplish this task." """)
				trainer_disposition = 4
				confirm = input("\nPush any key to continue.\n")
			else: 
				print(invalid_message)
			print("""
"Very well. If you wish to slay the Red Dragon, then hear me out.

Venture out into the forest. There you will find beasts corrupted by the fog, 
who you can challenge and slay. Your power shall elevate with each beast you 
slay, but know that if you fall, then your name will be added to an already
gargantuan list of those who have failed. 

Now go, begone. You will know when to return." """)
			confirm = input("\nPush any key to continue.\n")
			player_char['first_visit_t'] = False
			VillageHub()
			break
	# If the player has visited the trainer before
	print("\nYou enter the trainer's arena.")
	while True:
		trainer_input = input("""
"What is it that you want, {}?"

[T]rain - "I've come here to train with you."
[E]xit - "Nothing. I'll leave."
""".format(player_char['player_name'])).lower()
		if trainer_input == 't':
			if player_char['player_level'] < 5:
				print("\nYou are not yet worthy.")
			elif player_char['player_level'] == 5:
				fight('Trainer', 30, 5, False)
			elif player_char['player_level'] < 10:
				print("\nYou are not yet worthy.")
			elif player_char['player_level'] == 10:
				fight('Trainer', 42, 7, False)
			elif player_char['player_level'] < 15:
				print("\nYou are not yet worthy.")
			elif player_char['player_level'] == 15:
				fight('Trainer', 54, 9, False)
		elif trainer_input == 'e':
			VillageHub()
			break
		else:
			print(invalid_message)

def fight(enemy_name, enemy_health, enemy_attack, in_forest):
	fight_rounds = 0 # Assignment for a variable that will be used later on
#	if in_forest == True:
#		can_flee = True # So the player can attempt to flee at least once in
#						# forest encounters, this variable is initialized
#	else: 
#		can_flee == False # The only place where the fight() function is called
						  # is at the trainer's arena, where the player can't flee\
	fled_once = False
	print("\nYou encounter the {}!".format(enemy_name))
	while True:
		fight_input = input("""
Your hitpoints: {}
Enemy hitpoints: {} 

[F]ight for 1 round
[Fi]ght for 5 rounds
[Fig]ht for 10 rounds
[A]ttempt to flee
""".format(player_char['player_health'], 
				enemy_health)).lower()
		# This block of code handles inputs
		if fight_input == 'f': # Fight for one round
			fight_rounds = 1 # Set fight_rounds to this value so the fight can happen
		elif fight_input == 'fi': # Fight for five rounds
			fight_rounds = 5
		elif fight_input == 'fig': # Fight for ten rounds
			fight_rounds = 10
		elif fight_input == 'a' and in_forest == True: # Attempt to flee (1st time)
			can_flee = random.choice([True, False])
			if can_flee == True and fled_once == False:
				print("\nYou manage to escape the {}.".format(enemy_name))
				ForestLocation(False)
				break
			elif can_flee == False and fled_once == False:
				print("\nYou attempt to flee, but the {} stops you from doing so!"
					.format(enemy_name))
				fled_once = True
			else: # Attempt to flee (not 1st time)
				print("\nThe {} stops you in your tracks!".format(enemy_name))
# A gap between the two blocks of code here to separate the if statements
		if fight_rounds >= 0: # If fight_rounds has been set previously
			for i in range(fight_rounds): # Depending on fight_rounds, it will perform
			 							  # the steps below X amount of times where X is fight_rounds
				fight_damage_p = random.randint(0, 
				player_char['player_attack'])
				print("""
You hit the {} for {} damage!""".format(enemy_name, fight_damage_p))
				enemy_health -= fight_damage_p
				fight_damage_e = (random.randint(0, int(enemy_attack))
					) - player_char['player_defence']
				if fight_damage_e < 0:	# If the enemy's damage is negative, then make it
					fight_damage_e = 0  # zero so the player doesn't heal from being attacked
				print("""
The {} hits you for {} damage!""".format(enemy_name, fight_damage_e))
				player_char['player_health'] -= fight_damage_e
				if player_char['player_health'] <= 0: # Death
					while True: # The player's death could be handled by a function that
								# starts at this while loop, but for now it stays here as this is the
								# only time where the player can die
						death_input = input("""
You died.

[L]oad a previously saved game
[E]xit to Main Menu
""").lower() # Ask the player what they want to do
						if death_input == "l":
							print("\nLoading saved game...")
							LoadGame()
							break
						elif death_input == "e":
							print("\nExiting to main menu...")
							StartMenu()
							break
						else:
							print(invalid_message)
				elif enemy_health <= 0: # Player wins
					print("""
The {} falls by your hand!

You gain 50 experience points.

Your hitpoints: {}""".format(enemy_name, 
					player_char['player_health']))
					player_char['player_experience'] += 50
					ForestLocation(False)
		else:
			print(invalid_message)

def ForestLocation(from_village):
	# The from_village parameter is used to check if the player is either going
	# to the forest from the village (True) or coming back from a forest encounter
	# (False). It is called with ForestLocation(True) or ForestLocation(False)

	# This is mostly done to acknowledge the player's theoretical location within 
	# the game
	if from_village == True: 
		print("""
As you walk along the path leading up to the forest, you notice that the 
green foliage present in the forest has begun to wither as the path leads on to 
the gloomy abyssal fog ahead.""") # Print statement for consistency with the
								  # player's theoretical location within the game
	while True:
		forest_input = input(""" 
What do you decide to do?

[H]unt - Proceed into the darkness and hunt for monsters.
[E]xit - Retrace your steps back to the village.
""").lower()
		if forest_input == 'h':
			# Calling the fight function with arguments that scale off the 
			# player's level

			# The str() function is used to convert integers to strings
			# Built-in random functions are used to randomize the choice of enemy
			# and their stats. This is where enemy stats can be configured
			if player_char['player_level'] <= 5:
				fight(random.choice(starter_forest_enemies), int(10 + 
					random.randrange(0, 6)), str(4 + random.randrange(0, 3)), True) 
				break
			elif player_char['player_level'] > 5 and player_char['player_level'] <= 10:
				fight(random.choice(mid_forest_enemies), int(15 + random.randint(0, 6)),
					str(6 + random.randint(0, 3)), True)
				break
			elif player_char['player_level'] > 10:
				fight(random.choice(end_forest_enemies), int(20 + random.randint(0, 6)),
					str(8 + random_randint(0, 3)), True)
				break
			else:
				print("\nERROR: Could not generate encounter") # Else statement here
															 # just in case the player
															 # is an unknown level
			break
		elif forest_input == "e":
			VillageHub()
			break
		else:
			print(invalid_message)

def ShopLocation(): # gold hasn't been implemented
	# Check whether or not this is the player's first visit to the shop
	# If it is, reset all boughtX variables while also defining them in the
	# process and then set the first_visit variable to False so it doesn't
	# do this everytime the player visits the shop.
	if player_char['first_visit_s'] == True:
		boughtWeapon = False
		boughtShield = False
		boughtBoots = False
		boughtGauntlets = False
		boughtHelmet = False
		boughtArmor = False
		player_char['first_visit_s'] = False
	# Gear names, which are purely cosmetic and can only be seen in the shop
	starter_tier_name = "Steel"
	mid_tier_name = "Knight"
	end_tier_name = "Elite Knight"
	# Ordered by [Sword, Shield, Boots, Gauntlets, Helmet, Armor]
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
	elif player_char['player_level'] > 10:
		gear_name = end_tier_name
		shop_selling = end_tier_stats
	# These variables are used so three different code instances of the player
	# buying different tiers of gear wouldn't have to be created
	print("""
The shopkeeper welcomes you to his shop. You see a tidy arrangement of weapons
and armor pieces sitting along the bench behind him.

"What can I do you for?" he asks.""")
	while True:
		# This is a template for the weapons/armor in the game

		shop_input = input("""
[Weapons]
[{}] {} Sword - Attack + {} ({} Gold)

[Armor]
[{}] {} Shield - Defence + {} ({} Gold)
[{}] {} Boots - Defence + {} ({} Gold)
[{}] {} Gauntlets - Defence + {} ({} Gold)
[{}] {} Helmet - Defence + {} ({} Gold)
[{}] {} Armor - Defence + {} ({} Gold)

[E]xit - "Nothing right now."
""".format(
1, gear_name, shop_selling[0], shop_selling[0] * 10 + 10,
2, gear_name, shop_selling[1], shop_selling[1] * 10 + 10,
3, gear_name, shop_selling[2], shop_selling[2] * 10 + 10,
4, gear_name, shop_selling[3], shop_selling[3] * 10 + 10,
5, gear_name, shop_selling[4], shop_selling[4] * 10 + 10,
6, gear_name, shop_selling[5], shop_selling[5] * 10 + 10)).lower()
		if shop_input == '1' and boughtWeapon == False: # this will always be a weapon
			player_char['player_weapon'] = shop_selling[0]
			boughtWeapon = True
			print("{} Sword bought.".format(gear_name))
		elif shop_input == '2' and boughtShield == False:
			player_char['player_shield'] = shop_selling[1]
			boughtShield = True
			print("{} Shield bought.".format(gear_name))
		elif shop_input == '3' and boughtBoots == False: 
			player_char['player_boots'] = shop_selling[2]
			boughtBoots = True
			print("{} Boots bought.".format(gear_name))
		elif shop_input == '4' and boughtGauntlets == False:
			player_char['player_gauntlets'] = shop_selling[3]
			boughtGauntlets = True
			print("{} Gauntlets bought.".format(gear_name))
		elif shop_input == '5' and boughtHelmet == False:
			player_char['player_helmet'] = shop_selling[4]
			boughtHelmet = True
			print("{} Helmet bought.".format(gear_name))
		elif shop_input == '6' and boughtArmor == False:
			player_char['player_armor'] = shop_selling[5]
			boughtArmor = True
			print("{} Armor bought.".format(gear_name))
		elif (shop_input >= str(1) and shop_input <= str(6) 
			and boughtWeapon == True) or (shop_input >= str(1) and shop_input <= str(6)
			and boughtBoots == True) or (shop_input >= str(1) and shop_input <= str(6)
			and boughtShield == True) or (shop_input >= str(1) and shop_input <= str(6)
			and boughtGauntlets == True) or (shop_input >= str(1) 
			and shop_input <= str(6) and boughtHelmet == True) or (shop_input >= str(1) 
			and shop_input <= str(6) and boughtArmor == True):
			print("\nYou have already bought this item!")
		elif shop_input == "e":
			player_char['player_attack'] += player_char['player_weapon']
			player_char['player_defence'] += player_char['player_shield']
			player_char['player_defence'] += player_char['player_boots']
			player_char['player_defence'] += player_char['player_gauntlets']
			player_char['player_defence'] += player_char['player_helmet']
			player_char['player_defence'] += player_char['player_armor']
			VillageHub()
			break
		else:
			print(invalid_message)

def InnLocation():
	print("\nThe innkeeper looks at you as you enter.")
	while True:
		inn_input = input("""
"Welcome, traveler, to the Paledrake Inn. How might I help you?"

[A]sk - "What do you know about the Red Dragon?" 
[S]ave Game - "I'd like to rest here." 
[H]eal - "I'm hurt."
[E]xit - "Nothing, thanks. I'll take my leave."
""").lower()
		if inn_input == "a":
			if player_char['first_visit_i'] == True:
				print("""
"Another traveller seeking the Red Dragon I see? Well, I'll tell you what 
everyone in this town knows.""")
				player_char['first_visit_i'] = False
			else:
				print("""
"I'll tell you what I said before: """)
			print("""
The Red Dragon is said to be a powerful beast, perhaps the most powerful of all
in Caladaria. It is because of him that this town is surrounded by the abyssal 
fog, and it is only that when he is vanquished, that the fog will clear.

If you're looking to slay him, then I suggest that you go see the trainer. On 
your way to him, you should also pick up something at the local shop
nearby, maybe something better to use to defend yourself against the monsters 
in the forest, seeing as you look well-equipped already.

Don't forget that I house a boatload of healing potions here, so whenever 
you're hurt and out of potions, come by and I can heal you, for a small price, 
of course." """)
			confirm = input("\nPush any key to continue.\n") # This should be 
															 # self-explanatory, and this variable won't be used at all in 
															 # the same way other input variables are used
		elif inn_input == "s":
			while True:
				save_input = input("""
Saving the game will overwrite the currently saved character's data with this 
one. You should check for the presence of savegame.txt in the local directory
 for past characters. Are you sure you want to save your data?

[Y]es
[N]o
""").lower()
				if save_input == "y":
					f = open('savegame.txt',"w") # Create savegame.txt in write mode
					f.write (str(player_char)) # Write the player's stats to the file
					f.close() # Close the file
					print("\nSuccessfully saved to savegame.txt in local directory")
					break # Go back to the innkeeper
				elif save_input == "n":
					break 
		elif inn_input == "h":
			pass
		elif inn_input == "e":
			VillageHub()
			break
		else:
			print(invalid_message)


def VillageHub(): # Generic function that the player gets called to 
				  # whenever they start the game/back out of a menu
	print("""
You stand in the village square.""")
	while True:
		village_location_input = input("""
Where do you want to go?

Visit the [I]nn
Visit the [S]hop
Visit the [T]rainer
Visit the [F]orest
View [Stats]
[E]xit to Main Menu
""").lower() # The last option is mainly used to exit the game for debug purposes
			 # For each expected input, call the function corresponding to the player's
			 # decision and break just in case this loop is still active later on.
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
			ForestLocation(True)
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
#		elif village_location_input == "r": (Replaced with [E]xit to Main Menu)
#			print("[placeholder message]")  
#			StartMenu()
#			break 							This used to be the retirement option
		elif village_location_input == "e":
			print("\nExiting game...")
			StartMenu()
			break
		else:
			print(invalid_message)

def CharacterCreation():
	while True: # Multiple while loops are used here as sequential steps
				# For example, everytime the player enters an unexpected input in the 
				# race selection menu, then the player goes back to selecting race, 
				# instead of having to go back to the start of the character creation 
				# process
		player_race_input = input("""
The land of Caladaria is inhabited by three races -- humans, elves and dwarves.

You find yourself to be:
[H]uman
[E]lvish
[D]warven
""").lower() 
		if player_race_input == "h":
			player_char['player_race'] = 'Human' # Set the player's race and their 
			player_char['player_health'] = 10	 # stats
			player_char['player_defence'] = 2	 # This acts as a preset for further stat
			player_char['player_attack'] = 2 	 # modifications
			print("""
Humans, jack of all trades, master of none. Lacking the offensive capabilities
of the Dwarves and the natural protection of the Elves, Humans make up for it
in their tendency to exceed against ever-rising odds. Perhaps you may find the
answers you seek in the lush monster-infested parts of Caladaria, where your 
parents went missing several years ago in search of the 'Red Dragon.'""")
			break
		elif player_race_input == "e":
			player_char['player_race'] = "Elf"  # The race name is mostly for display
			player_char['player_health'] = 12
			player_char['player_defence'] = 1
			player_char['player_attack'] = 2
			print("""
Elves, the first recorded inhabitants of Caladaria. Your innate, mutual affinity
towards the natural world lends you additional survivability against your 
enemies, but is offset by your inherent frailness. Perhaps you may find the
answers you seek in the lush monster-infested parts of Caladaria, where your 
parents went missing several years ago in search of the 'Red Dragon.' """)
			break
		elif player_race_input == "d":
			player_char['player_race'] = "Dwarf"
			player_char['player_health'] = 8
			player_char['player_defence'] = 2
			player_char['player_attack'] = 3
			print("""
Dwarves, a proud short-statured race that is capable of more than meets the 
eye. Against enemies, you are able to exploit weak spots and deal increased 
amounts of damage, though your studyness is slightly outclassed by other races.
Perhaps you may find the answers you seek in the lush monster-infested parts  
of Caladaria, where your parents went missing several years ago in search 
of the 'Red Dragon.' """)
			break
		else:
			print(invalid_message)
	while True:
		player_class_input = input("""
You see a lit up village in the distance. Along with a inconsistent arrangement
of houses up ahead, you see four distinct buildings in the distance, with one 
of them looking like an inn. You decide that would be a good place to settle in
during your invesigation into the Red Dragon.

When you are ready, you grab your:
[S]word (Warrior)
[D]agger (Rogue)
[St]aff (Mage) 
""").lower()
		if player_class_input == "s":
			player_char['player_class'] = 'Warrior'
			player_char['player_health'] += 5  # Adding onto the preset stats instead 
			player_char['player_defence'] += 1 # of making them equal to a value
			player_char['player_attack'] += 2
			break
		elif player_class_input == "d":
			player_char['player_class'] = 'Rogue'
			player_char['player_health'] += 4
			player_char['player_defence'] += 1
			player_char['player_attack'] += 3
			break
		elif player_class_input == "st":
			player_char['player_class'] = 'Mage'
			player_char['player_health'] += 3
			player_char['player_defence'] += 1
			player_char['player_attack'] += 4
			break
		else:
			print(invalid_message)
	# Asking for the player's name can be outside of a while loop because
	# there shouldn't be any unexpected inputs to account for
	player_name_input = input("""
What is your name?
""")
	player_char['player_name'] = player_name_input # Player's name is a string
	 										   	   # so it should be able to accept most names
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
			print(invalid_message)

def LoadGame():
	print("\nLooking for savegame.txt in local directory...")
	# Give the player feedback as to what the program is doing
	if os.path.isfile('./savegame.txt') == True:
	# ^ checking for the existence of savegame.txt in the local directory
		global player_char # Declaring the global variable before using it
						   # Otherwise it would function as a local variable
						   # and not have the proper stats
		player_char = eval(open("savegame.txt").read())
	# Defining the player's stats as whatever is in the contents of the file
	# which should only consist of player_char
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
[E]xit to Main Menu
""".format(player_char['player_name'], player_char['player_race'],
			 player_char['player_class'], player_char['player_health'], 
			 player_char['player_defence'], player_char['player_attack'])).lower()
			# Display the stats of the savegame using {} and .format
			# Tell the player the stats of the character inside the savegame and
			# ask the player if they want to load the character or exit out to the
			# main menu
			if load_input == "l":
				InnLocation()
				# Go to the inn because it is the only place where the player can save
				break # Break the loop just in case it is still active later on
			elif load_input == "e":
				StartMenu()
				# Go back to the start menu
				break # Break the loop just in case it is still active later on
			else:
				print(invalid_message)
	else: # If savegame.txt doesn't exist in the local directory
		print("\nsavegame.txt was not found in local directory.") 
		# Print a message saying that it was not found
		StartMenu() # Go back to the Start Menu
		# No break because this isn't inside a loop

def StartMenu(): # A lot of the conventions throughout the game are used here:
	
	# This string is outside of the while loop and so it won't ever print again
	# whenever the user enters an invalid input
	# Was using ANSI escape codes to change the output's text color, but this also
	# had the side effect of changing the color of Powershell text
	# so it probably won't be used - \033[1;31;40m
	print("\nLegend of the Red Dragon") # Statements like this are formatted 
										# in this way (\n) so there is an empty line after the player's input
	# Using an infinite while loop so the player can enter all kinds of inputs
	# and not break the program. This will mean 'break' will have to be used so 
	# doesn't loop infinitely. These infinite while loops will be used repeatedly
	# throughout the program when player input is needed.
	while True:
		# True will always be true, and false will always be false
		# Store the player's input inside a localized variable (only appears inside
		# the function). The program stops for the player's input
		main_menu_input = input("""
--------------
[N]ew Game
[L]oad Game
[E]xit Game
--------------
""").lower() # Make the player's input lowercase so it can accept more inputs
		# The player is expected to enter one of the letters inside the brackets
		# It shouldn't matter if their input is capitalized or not, as the program
		# will make their input lowercase and so will only accept lowercase values.
		if main_menu_input == "n": # If the player enters this value,
			CharacterCreation()	   # then call the character creation function
			break # Break the loop in case it doesn't stop later on
		elif main_menu_input == "l":
			LoadGame()
			break
		elif main_menu_input == "e":
			sys.exit() # This is assuming ‘sys’ has been imported prior to this code being executed
					   # sys.exit() will stop the program when called
		else: # This else statement is used throughout the program to account for
			  # unexpected inputs, allowing for it to keep going regardless of what the
			  # player types, as it will go back to the beginning of the infinite loop
			print(invalid_message)
			# The loop doesn't get broken here, so it just goes back to the start of the while loop

StartMenu() # Initiate the game, other functions don't need to be called
			# because they will be called inside of each other