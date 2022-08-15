# Legend of the Red Dragon
# Requires at least Python 3.6.1

# Importing other Python modules for use later on
import sys # so we can use sys.exit() to exit the game
import os  # so we can check if a savegame exists before loading it
import random # for forest encounters that generate a random enemy
			  # with different stats, also for fights

# Global variables for player stats is located at the bottom of the program
# for bug-fix purposes

# Global Variables - Game Settings

player_xp_gain = 50
# Variable for how much XP the player gains from winning fights

player_xp_required = 250
# Variable for how much XP the player requires to level up

player_heal_amount = 10
# Variable for how much HP the player heals from drinking potions

milestones = [5, 10, 15]
# List for the player's level milestones. Once they reach this level, they
# have to fight the trainer to level up into the next set of levels
# e.g. beat the trainer at level 5 to unlock levels 6 - 10
# As of now:
# Levels 1 - 5 = Starter Tier
# Levels 6 - 10 = Mid Tier
# Levels 11 - 15 = End Tier

inn_heal_required = 5
# How much gold the player needs to heal at the end

inn_refill_required = 30
# How much gold the player needs to refill potions

# Enemies not yet finalized
starter_forest_enemies = ['Abyssal Beast', 'Lesser Skeleton', 'Feral Wolf']
mid_forest_enemies = ['Hollow Knight', 'Abyss-corrupted Giant', 
					'Decrepit Monstrocity']
end_forest_enemies = ['Speaker of the Abyss', 'Primordial Snake', 
					'Elder Beast']
# These lists should be the same every time the game is run
# meaning that they don't need to be saved to savegame.txt

forest_win_gold = 5
# How much gold the player gets when they win a fight in the forest

trainer_disposition = 0
# The above variable is used for trainer dialogue only

trainer_required_xp = 100
trainer_required_gold = 75
# Variables dictating how much xp and gold the player will need to face the 
# trainer. The player's xp and gold they have at that moment when they face the 
# trainer is not deducted, and it only requires them to have at least that
# certain amount to fight the trainer.

invalid_message = "\nEnter the number/letter(s) inside one of the brackets."
# String used for when the program expects a number/letter input and the player
# enters an invalid/unexpected input

confirm_prompt = "\nPush any key to continue.\n"
# String used for a confirm prompt.

# The below section is dedicated to defining functions, that act as 
# the game's modular structure. Because of this modularity, functions 
# are defined in reverse order so they can be accessed freely
# by the program.

# The start menu is found at the bottom of the program, which is the order in
# which the player will be assumed to go in, though it is mostly dependent
# on which areas are accessible by the player in each instance e.g. the
# player can't go straight to the shop from the inn, and vice versa

def debug():
	print("\nIf you are seeing this, it works")

def TrainerLocation():
	# Derived values for trainer encounters for each tier
	starter_trainer_health = 60
	starter_trainer_attack = 11
	mid_trainer_health = 84
	mid_trainer_attack = 18
	final_boss_hp = 96
	final_boss_attack = 22
	# When the player first goes to the trainer
	if player_char['first_visit_t'] == True:
		# Print amazingly written, totally not pretentious dialogue
		# It's just meant to be serviceable (at best), so, yeah, it's pretty bad 
		print("""
Upon entering, you spot a man fully clad in black-iron armor. You notice that the 
entire building takes the shape of a large. rectangular arena, surrounded by 
rusting stone.

As you approach him, he stops and turns to face you.

"Ah, another who seeks the Red Dragon? Clearly, you must be of some worth, 
to be able to navigate through the abyssal fog in the outskirts of the city.
It's not a task that any odd traveler can accomplish, no.

Yes, I know of the Red Dragon, of where he resides. He is an extraordinarily 
powerful beast, more so than you realize. Many travellers like you have come
and gone, but none of them have survived the gauntlet that precedes him. 

So I must ask, what is your name, and what compels you to seek such a monster?\"""")
		while True: 
			trainer_input = input("""
[1] "I am %s, and I have come here in search of my parents."
[2] "I am %s, and I seek the glory and fame that comes with slaying the dragon."
[3] "I am %s, a humble explorer that seeks the dragon for my own purposes."
[4] "I am %s, and I'm just a mindless wanderer here for reasons of my own."
""" % (player_char['player_name'], player_char['player_name'], 
	player_char['player_name'], player_char['player_name'])) 
	# % is equivalent of .format()
			global trainer_disposition # Declaring global variable
			if trainer_input == str(1):
				print("""
"You are not the first of your kind. I have seen many orphans travel here in 
search of answers, all of whom have failed in their journey. How far are you 
willing to go for answers? Only time will tell." """)
				trainer_disposition = 1 
				# Inconsequential variable used for experimental dialogue purposes
				confirm = input(confirm_prompt)
				# Confirm message that just paces the dialogue
				# Not used for anything else in particular other than that
				break
			elif trainer_input == str(2):
				print("""
"Glory and fame, both very valid reasons for one to travel to this small town, 
but the question remains -- how far will you be willing to go in your quest? 
Only time will tell." """)
				trainer_disposition = 2
				confirm =  input(confirm_prompt)
				break
			elif trainer_input == str(3):
				print("""
"A 'humble explorer' you say? To be able to reach this little town through the
abyssal fog is a hefty task in itself, but so is the task of slaying the dragon.
I suppose only time will tell as to how dedicated you will be in your quest." """)
				trainer_disposition = 3
				confirm = input(confirm_prompt)
				break
			elif trainer_input == str(4):
				print("""
"Navigating through the fog on this town's outskirts is not a task that many
simple 'wanderers' can manage. You have your own reasons for coming here, 
but I believe that only time will tell as to whether these reasons are 
compelling enough for you to accomplish this task." """)
				trainer_disposition = 4
				confirm = input(confirm_prompt)
				break
			else: 
				print(invalid_message)
		print("""
"Very well, I am Turgon. If you wish to slay the Red Dragon, then hear me out.

Venture out into the forest. There you will find beasts corrupted by the fog, 
who you can challenge and slay. Your power shall elevate with each beast you 
slay, but know that if you fall, then your name will be added to an already
gargantuan list of warriors who have failed on their journey.

Now go, begone. You will know when to return." """)
		confirm = input(confirm_prompt)
		player_char['first_visit_t'] = False
		VillageHub()
	# If the player has visited the trainer before
	print("\nYou enter the trainer's arena.")
	while True:
		trainer_input = input("""
"What is it that you want, {}?"

[T]rain - "I've come here to train with you." ({} XP and {} Gold required)
[E]xit - "Nothing. I'll leave."
""".format(player_char['player_name'], trainer_required_xp,
	trainer_required_gold)).lower()
		if trainer_input == 't':
			# In order of evaluation
			if (player_char['player_level'] < milestones[0]):
			# This is automatically false if the player is a higher level
				print("\nYou are not yet worthy.")
			# Trainer fight at Level 5
			elif player_char['player_level'] == milestones[0] and (
			player_char['player_gold'] >= trainer_required_gold
			and player_char['player_experience'] >= trainer_required_xp):
				if trainer_disposition == 1:
					dialogue_lvl5 = 'answers'
				elif trainer_disposition == 2:
					dialogue_lvl5 = 'glory and fame'
				elif trainer_disposition == 3:
					dialogue_lvl5 = 'secrets'
				elif trainer_disposition == 4:
					dialogue_lvl5 = 'whatever it is you desire'
				else:
					dialogue_lvl5 = 'answers'
				print("""
"I see that your dedication towards seeking {} has not yet wavered."

Turgon approaches you, his greatsword sheath quivering with each step.

"I know not the challenges that led you here, nor where you are from, but if it
is answers you seek, then look no further." """.format(dialogue_lvl5))
				confirm = input(confirm_prompt)
				print("""
"For many years, I have sought to find and train a warrior that, one day, will
be able to face the Red Dragon and live to tell the tale. I believe you may be
that warrior."

Turgon reaches out for his sheathe, and pulls out his greatsword.

"Defeat me now, and you will become stronger than you ever will be."

"But should you fail, {}, then another warrior will take your place..." """
				.format(player_char['player_name']))
				confirm = input(confirm_prompt)
				fight('Trainer', starter_trainer_health, starter_trainer_attack, False)
			elif player_char['player_level'] < milestones[1]:
				print("\nYou are not yet worthy.")
			# Trainer fight at level 10
			elif player_char['player_level'] == milestones[1] and (
			player_char['player_gold'] >= trainer_required_gold
			and player_char['player_experience'] >= trainer_required_xp):
				print("""
"Ah, {}. You return, as powerful as ever. 

Let us see if you are worthy of upholding the title of Dragonslayer..."""
				.format(player_char['player_name']))
				confirm = input(confirm_prompt)
				fight('Trainer', mid_trainer_health, mid_trainer_attack, False)
			elif player_char['player_level'] < milestones[2]:
				print("\nYou are not yet worthy.")
			# Final trainer fight at level 15
			elif player_char['player_level'] == milestones[2] and (
			player_char['player_gold'] >= trainer_required_gold
			and player_char['player_experience'] >= trainer_required_xp):
				print(""" 
"Again, the well of monsters renews with new-found essence. I wonder if the 
awakening of monsters within the fog is due in part to your strength..."

Turgon pauses, seemingly for a moment of recollection.
				""")
				confirm = input(confirm_prompt)
				if trainer_disposition == 1:
					print("""
"If it brings you any closure, then you must know that your parents are dead, 
victims of the Red Dragon's attacks on this village, but you didn't come this
far just for answers..." """)
					confirm = input(confirm_prompt)
				print("""
His black-iron hands unclench, revealing a brown pouch in his possession.

In one swift motion, he unwraps the brown pouch. A thin yellow thread of 
energy hovers between his hands.""")
				confirm = input(confirm_prompt)
				print("""
"The Red Dragon is dead. Its corporeal form was slain long ago, but its spirit,
its essence -- its power, remains here in this soul."

Slowly, the soul follows as he rolls his right hand over. """)
				confirm = input(confirm_prompt)
				print("""
With the soul sitting ever so softly on his palm, he holds out his hand.

"Look upon the remains of the Red Dragon, for this is all you will ever see of 
it... but I cannot say the same for its strength." """)
				confirm = input(confirm_prompt)
				print(""" 
"Best me now, {}, and you will have won against the toughest foe that has ever
lived in this land of Caladaria."

"Fall, and you will suffer a thousand years in the afterlife with full 
knowledge of the fact that you let the Red Dragon continue its tyrannous
reign over this village, and Caladaria itself."

"Now... see to it that you do succeed, so that you may be the one to put the 
legend of the Red Dragon to rest."

Turgon's grip suddenly tightens, and crushes the Red Dragon's soul in one 
quick burst.

A red aura begins to envelop Turgon. His hands gravitate towards
the greatsword on his back, as he slowly walks towards you."""
				.format(player_char['player_name']))
				confirm = input(confirm_prompt)
				while True:
					final_boss_phase1_input = input("""
What do you do?
[A]ttack him
[B]ack away
""")
					if final_boss_phase1_input == 'a':
						print("""
You charge towards Turgon, and manage to get a few slashes in before he repels
you with a shockwave, inflicting minor damage. """)
						final_boss_hp -= int(round(player_char['player_attack'] / 2, 0) * 3)
						player_char['player_health'] -= 4
						break
					elif final_boss_phase1_input == 'b':
						print("""
You slowly back away from Turgon. """)
						break
					else: 
						print(invalid_message)
				fight('Red Dragon', final_boss_hp, final_boss_attack, False)
				break
			if player_char['player_experience'] < trainer_required_xp:
				print("\nYou do not have enough XP to face the trainer.")
			if player_char['player_gold'] < trainer_required_gold:
				print("\nYou do not have enough gold to face the trainer.")
		elif trainer_input == 'e':
			VillageHub()
			break
		else:
			print(invalid_message)

# Parameters for the fight function, which are defined when it is called
# These arguments are used as variables
def fight(enemy_name, enemy_health, enemy_attack, in_forest):
	fight_rounds = 0 # Assignment for a variable that will be used later on
	fled_once = False
	enemy_min_attack = 0 # Minimum attack enemies can have during encounters
						 # Makes it so they can attack the player once and
						 # miss only if the player has a superior defence value
	# Making enemies tougher
	if player_char['player_level'] >= milestones[0]:
		enemy_min_attack += 1
	elif player_char['player_level'] >= milestones[1]:
		enemy_min_attack += 2
	if in_forest == False:
		print("\nThe {} challenges you to a duel!".format(enemy_name))
	else:
		print("\nYou encounter the {}!".format(enemy_name))
	while True:
		fight_input = input("""
Your hitpoints: {}
Enemy hitpoints: {} 

[F]ight for 1 round
[Fi]ght for 5 rounds
[Fig]ht for 10 rounds
[H]eal ({} healing potion(s) left)
[A]ttempt to flee
""".format(player_char['player_health'], 
				enemy_health, player_char['current_healing_potions'])).lower()
		# This block of code handles inputs
		# Fight for one round
		if fight_input == 'f': 
			fight_rounds = 1 # Set fight_rounds to this value so the fight can happen
		# Fight for five rounds
		elif fight_input == 'fi':
			fight_rounds = 5
		# Fight for ten rounds
		elif fight_input == 'fig':
			fight_rounds = 10
		# Attempt to flee (1st time)
		elif fight_input == 'a' and in_forest == True: # Fleeing (in forest)
			can_flee = random.choice([True, False]) # Randomly true or false
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
		elif fight_input == 'a' and in_forest == False: # Fleeing (out of forest)
			print("\nYou can't run from a fight with the trainer!")
		# Player uses a healing potion
		elif fight_input == 'h': 
			if player_char['current_healing_potions'] > 0: # If the player has a potion
				player_heal_combat = (player_char['player_max_hp']
					- player_char['player_health']) # Calculate amount to be healed
				if player_heal_combat > player_heal_amount: # Make sure it doesn't heal up to max HP
					player_heal_combat = player_heal_amount
				player_char['player_health'] += player_heal_combat # Heal player
				print("\nYou heal {} hp.".format(player_heal_combat)) # Feedback to player
				player_char['current_healing_potions'] -= 1 # Take away a healing potion
			# Otherwise print a message and don't do anything else
			else:
				print("\nYou don't have any healing potions left!")
		else:
			print(invalid_message)
		# If fight_rounds has been set previously
		if fight_rounds >= 0: 
			for i in range(fight_rounds): # Depending on fight_rounds, it will perform
										  # the steps below X amount of times where X is fight_rounds
										  # i is used solely to iterate through fight_rounds
				# Calculating player damage
				fight_damage_p = random.randint(0, 
				player_char['player_attack']) # Calculate a random integer for player
											  # damage up to their attack
				if fight_damage_p == 0:
					print("\nYou whiff your attack and miss!")
				else:
					print("""
You hit the {} for {} damage.""".format(enemy_name, fight_damage_p))
				enemy_health -= fight_damage_p # Take away enemy hitpoints
				# Player wins
				# This is after the player deals damage, so the player doesn't kill the 
				# enemy and then die because the enemy was able to attack again
				if enemy_health <= 0: 
					print("""
The {} falls by your hand!

You gain {} experience points.

You survive the fight with {} hitpoints remaining.""".format(enemy_name, player_xp_gain,
					player_char['player_health']))
					 # If player isn't at level 5, 10 or 15
					 # In order of evaluation:
					if (player_char['player_level'] < milestones[0]):
						player_char['player_experience'] += player_xp_gain
					elif (player_char['player_level'] < milestones[1]):
						player_char['player_experience'] += player_xp_gain
					elif (player_char['player_level'] < milestones[2]): 
						player_char['player_experience'] += player_xp_gain
					# If the player has sufficient XP to level up 
					if (player_char['player_experience'] == player_xp_required
					and player_char['player_level'] < milestones[0]) or (
					player_char['player_experience'] == player_xp_required
					and player_char['player_level'] < milestones[1]) or (
					player_char['player_experience'] == player_xp_required
					and player_char['player_level'] < milestones[2]):
						player_char['player_level'] += 1 # Add a level
						player_char['player_max_hp'] += 1 # Add more health
						print("\nYou levelled up from {} to {}!".format(
							player_char['player_level'] - 1, 
							player_char['player_level']))
						player_char['player_experience'] = 0 # Reset XP
					# If the player is already at a milestone 
					# and has to go to the trainer to level up
					elif (player_char['player_level'] == milestones[0] 
					or player_char['player_level'] == milestones[1] 
					or player_char['player_level'] == milestones[2]) and (
					in_forest == True):
						print("""
You feel as if you are sufficiently powerful enough to challenge 
the trainer.""")
#						player_char['player_experience'] += player_xp_gain
						player_char['player_experience'] = trainer_required_xp
					# Done regardless of the player's level
					player_char['player_gold'] += forest_win_gold 
					print("\nYou gain {} gold.".format(forest_win_gold))
					if in_forest == True:
						ForestLocation(False)
					else: # If the player wins a fight with what is assumed to be the trainer
						if player_char['player_level'] < milestones[2]:
							confirm = input(confirm_prompt)
							print("""
"Very good.. very good, indeed... 
							
You have grown stronger, but you must keep growing if you have 
any desire to survive an encounter with the Red Dragon." """)
							player_char['player_level'] += 1
							player_char['player_max_hp'] += 1
							player_char['bought_weapon'] = False
							player_char['bought_shield'] = False
							player_char['bought_boots'] = False
							player_char['bought_gauntlets'] = False
							player_char['bought_helmet'] = False
							player_char['bought_armor'] = False
							print("\nYou levelled up from {} to {}!".format(
								player_char['player_level'] - 1,
								player_char['player_level']))
							print("\nNew gear is available at the shop.")
						elif player_char['player_level'] == milestones[2]:
							confirm = input(confirm_prompt)
							print("""
The Red Dragon dissolves in a blinding white light as you strike the final 
blow. Turgon, and the Red Dragon are no more. 

You go outside into the village square to see that the abyssal fog that
once haunted the village outskirts has cleared. The bright light of the sun
shines once again into the town.

The legend of the Red Dragon is no more. """)
							print("\nCongratulations. You completed the game.")
							confirm = input(confirm_prompt)
							StartMenu()
						confirm = input(confirm_prompt)
						TrainerLocation()
					break
				# Calculating enemy damage
				fight_damage_e = (random.randint(enemy_min_attack, int(enemy_attack)) # Same as before, 
					) - int(round(player_char['player_defence'] / 3, 0)) # but for enemy damage
				if fight_damage_e < 0:	# If the enemy's damage is negative, then make it
					fight_damage_e = 0  # zero so the player doesn't heal from being attacked
				if fight_damage_e == 0:
					print("\nThe {} whiffs and misses you!".format(enemy_name))
				else:
					print("""
The {} hits you for {} damage.""".format(enemy_name, fight_damage_e))
				player_char['player_health'] -= fight_damage_e # Take away player hitpoints
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
			fight_rounds = 0 # Reset fight rounds so it doesn't repeat the fight

def ForestLocation(from_village):
	# The from_village parameter is used to check if the player is either going
	# to the forest from the village (True) or coming back from a forest encounter
	# (False). It is called with ForestLocation(True) or ForestLocation(False)

	# This is mostly done to acknowledge the player's theoretical location within 
	# the game

	# Derived values for random forest encounters at each tier
	starter_enemy_health = int(10 + random.randrange(0, 6))
	starter_enemy_attack = str(5 + random.randrange(0, 3))
	mid_enemy_health = int(15 + random.randrange(0, 6))
	mid_enemy_attack = str(12 + random.randrange(0, 3))
	end_enemy_health = int(20 + random.randrange(0, 6))
	end_enemy_attack = str(24 + random.randrange(0, 3))
	# Values could use a bit more balancing since the player gets stupidly OP
	# at the end of the game if they buy items
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
			if player_char['player_level'] <= milestones[0]: # Less than level 5
				fight(random.choice(starter_forest_enemies), starter_enemy_health, 
				starter_enemy_attack, True) 
				break
			elif (player_char['player_level'] > milestones[0] 
			and player_char['player_level'] <= milestones[1]): # Between 6 and 10
				fight(random.choice(mid_forest_enemies), mid_enemy_health,
				mid_enemy_attack, True)
				break
			elif (player_char['player_level'] > milestones[1]
			and player_char['player_level'] <= milestones[2]): # Between 11 and 15
				fight(random.choice(end_forest_enemies), mid_enemy_health,
				mid_enemy_attack, True)
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

def ShopLocation():
	# Gear names, which are purely cosmetic and can only be seen in the shop
	starter_tier_name = "Steel"
	mid_tier_name = "Knight"
	end_tier_name = "Elite Knight"
	# Ordered by [Sword, Shield, Boots, Gauntlets, Helmet, Armor]
	starter_tier_stats = [2, 2, 1, 2, 2, 3]
	mid_tier_stats = [3, 3, 3, 3, 3, 4]
	end_tier_stats = [4, 4, 4, 4, 4, 5]
	# Weapons will always be the first item in the list
	# Now check what items the shopkeeper will sell
	# (depending on the player's level)
	if player_char['player_level'] <= milestones[0]:
		gear_name = starter_tier_name
		shop_selling = starter_tier_stats
	elif (player_char['player_level'] > milestones[0]
		 and player_char['player_level'] <= milestones[1]):
		gear_name = mid_tier_name
		shop_selling = mid_tier_stats
	elif (player_char['player_level'] > milestones[1]
		and player_char['player_level'] <= milestones[2]):
		gear_name = end_tier_name
		shop_selling = end_tier_stats
	# These variables are used so three different code instances of the player
	# buying different tiers of gear wouldn't have to be created
	prices = [shop_selling[0] * 10 + 10, 
			  shop_selling[1] * 10 + 10,
			  shop_selling[2] * 10 + 10,
			  shop_selling[3] * 10 + 10,
			  shop_selling[4] * 10 + 10,
			  shop_selling[5] * 10 + 10] 
	# Calculating list of prices
	print("""
The shopkeeper welcomes you to his shop. You see a tidy arrangement of weapons
and armor pieces sitting along the bench behind him.

"What can I do you for?" he asks.""")
	# Store the shop menu's string inside a variable so the whole menu
	# doesn't have to be reprinted again when it is refreshed
	shop_menu = """
[Weapons]
[{}] {} Sword - Attack + {} ({} Gold)

[Armor]
[{}] {} Shield - Defence + {} ({} Gold)
[{}] {} Boots - Defence + {} ({} Gold)
[{}] {} Gauntlets - Defence + {} ({} Gold)
[{}] {} Helmet - Defence + {} ({} Gold)
[{}] {} Armor - Defence + {} ({} Gold)

[R]efresh List
[E]xit - "Nothing right now." """.format(
1, gear_name, shop_selling[0], prices[0],
2, gear_name, shop_selling[1], prices[1],
3, gear_name, shop_selling[2], prices[2],
4, gear_name, shop_selling[3], prices[3],
5, gear_name, shop_selling[4], prices[4],
6, gear_name, shop_selling[5], prices[5])
	# Should have suffixed each item with Bought if the player had bought the 
	# item already
	# Could've involved the use of seven other variables and 
	# if statements to go along with each variable
	print(shop_menu)
	while True:
		# This is a template for the weapons/armor in the game

		shop_input = input("""
You currently have {} gold.

What do you decide to do?
""".format(player_char['player_gold'])).lower()
		try: # Try/except structure used here, so if an IndexError occurs,
			 # then the game prints a message and keeps going, instead of just
			 # crashing on a numeric input
			# If the player has already bought this item
			if (shop_input == str(1) and player_char['bought_weapon'] == True) or (
			shop_input == str(2) and player_char['bought_shield'] == True) or (
			shop_input == str(3) and player_char['bought_boots'] == True) or (
			shop_input == str(4) and player_char['bought_gauntlets'] == True) or (
			shop_input == str(5) and player_char['bought_helmet'] == True) or (
			shop_input == str(6) and player_char['bought_armor'] == True):
				print("\nYou have already bought this item!")
			# If the player doesn't have enough gold and hasn't bought the item before
			# Also check if the number of the input is in the list
			elif str(shop_input) <= str(len(prices)) and ( 
			player_char['player_gold'] < prices[int(shop_input) - 1])  and (
			((shop_input == str(1) and player_char['bought_weapon'] == False) or (
			shop_input == str(2) and player_char['bought_shield'] == False) or (
			shop_input == str(3) and player_char['bought_boots'] == False) or (
			shop_input == str(4) and player_char['bought_gauntlets'] == False) or (
			shop_input == str(5) and player_char['bought_helmet'] == False) or (
			shop_input == str(6) and player_char['bought_armor'] == False))):
				print("\nYou don't have enough gold to buy this item!")
			# Buying items from the shop
			# All of these conditions follow the same format:
			# If shop_input is equal to a valid input, player hasn't bought that weapon
			# before and the player has enough gold
			elif (shop_input == str(1) and player_char['bought_weapon'] == False and 
			player_char['player_gold'] >= prices[0]): 
				player_char['player_attack'] -= player_char['player_weapon']
				player_char['player_weapon'] = shop_selling[0]
				player_char['bought_weapon'] = True
				print("\n{} Sword bought for {} gold.".format(gear_name, prices[0]))
				player_char['player_gold'] -= prices[0]
			elif (shop_input == str(2) and player_char['bought_shield'] == False and
			player_char['player_gold'] >= prices[1]):
				player_char['player_defence'] -= player_char['player_shield']
				player_char['player_shield'] = shop_selling[1]
				player_char['bought_shield'] = True
				print("\n{} Shield bought for {} gold.".format(gear_name, prices[1]))
				player_char['player_gold'] -= prices[1]
			elif (shop_input == str(3) and player_char['bought_boots'] == False and
			player_char['player_gold'] >= prices[2]):  
				player_char['player_defence'] -= player_char['player_boots']
				player_char['player_boots'] = shop_selling[2]
				player_char['bought_boots'] = True
				print("\n{} Boots bought for {} gold.".format(gear_name, prices[2]))
				player_char['player_gold'] -= prices[2]
			elif (shop_input == str(4) and player_char['bought_gauntlets'] == False and
			player_char['player_gold'] >= prices[3]):
				player_char['player_defence'] -= player_char['player_gauntlets']
				player_char['player_gauntlets'] = shop_selling[3]
				player_char['bought_gauntlets'] = True
				print("\n{} Gauntlets bought for {} gold.".format(gear_name, prices[3]))
				player_char['player_gold'] -= prices[3]
			elif (shop_input == str(5) and player_char['bought_helmet'] == False and
			player_char['player_gold'] >= prices[4]):
				player_char['player_defence'] -= player_char['player_helmet']
				player_char['player_helmet'] = shop_selling[4]
				player_char['bought_helmet'] = True
				print("\n{} Helmet bought for {} gold.".format(gear_name, prices[4]))
				player_char['player_gold'] -= prices[4]
			elif (shop_input == str(6) and player_char['bought_armor'] == False and
			player_char['player_gold'] >= prices[5]):
				player_char['player_defence'] -= player_char['player_armor']
				player_char['player_armor'] = shop_selling[5]
				player_char['bought_armor'] = True
				print("\n{} Armor bought for {} gold.".format(gear_name, prices[5]))
				player_char['player_gold'] -= prices[5]
			# If the player chooses to refresh the list
			elif shop_input == 'r':
				print(shop_menu)
			# Whenever they exit the shop,
			# Add attack/defence values onto the player's stats
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
		# If an error occurs (since this is prone to list errors)
		except IndexError: # Specific error used so the program can exit properly
			print(invalid_message) 

def InnLocation():
	print("\nThe innkeeper looks at you as you enter.")
	while True:
		inn_input = input("""
"Welcome, traveler, to the Paledrake Inn. How might I help you?"

[A]sk - "What do you know about the Red Dragon?" 
[S]ave Game - "I'd like to rest here." 
[H]eal - "I'm hurt. Can you heal me?" ({} Gold)
[R]efill - "Can you refill my healing potions?" ({} Gold)
[E]xit - "Nothing, thanks. I'll take my leave."

You currently have {} gold.
""".format(inn_heal_required, inn_refill_required, 
	player_char['player_gold'])).lower()
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
fog, and it is said that only when he is vanquished, that the fog will clear.

If you're looking to slay him, then I suggest that you go see the trainer. On 
your way to him, you should also pick up something at the local shop
nearby, maybe something better to use to defend yourself against the monsters 
in the forest, seeing as you look well-equipped already.

Don't forget that I house a whole stockpile of healing potions here, so 
whenever you're hurt and out of potions, come by and I can heal you, for a 
small price. I can also refill your own healing potions, but at a higher 
price than if you were to simply heal yourself." """)
			confirm = input(confirm_prompt)	 # This should be 
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
			# If the player has enough gold and can be healed
			if (player_char['player_gold'] >= inn_heal_required and 
			player_char['player_health'] < player_char['player_max_hp']):
				player_char['player_health'] = player_char['player_max_hp']
				print("\nHealed back up to {} hitpoints!"
					.format(player_char['player_max_hp']))
				player_char['player_gold'] -= inn_heal_required
			# If the player has enough gold but can't be healed
			elif (player_char['player_gold'] >= inn_heal_required and
			player_char['player_health'] == player_char['player_max_hp']):
				print("\n\"You don't look hurt at all.\" the innkeeper says.")
			# If the player doesn't have enough gold and is above the critical health value
			elif (player_char['player_gold'] < inn_heal_required and player_char['player_health'] >= 6):
				print("\n\"It doesn't look like you've got enough gold.\"")
			# If the player doesn't have enough gold and is below the critical health value
			elif (player_char['player_gold'] < inn_heal_required and player_char['player_health'] < 6):
				print("""
"Huh, well I'm not about to let you go die out there, so here's a freebie, 
on me." """)
				player_char['player_health'] = player_char['player_max_hp']
		elif inn_input == "r":
			# If player has enough gold and can refill potions
			if (player_char['player_gold'] >= inn_refill_required and
			player_char['current_healing_potions'] < 
			player_char['max_healing_potions']): 
				print("\nThe innkeeper refills your potions.")
				player_char['current_healing_potions'] = player_char['max_healing_potions']
				player_char['player_gold'] -= inn_refill_required
			# If player has the max amount of potions
			elif (player_char['current_healing_potions'] == 
			player_char['max_healing_potions']): 
				print("\n\"You can't carry any more potions.\"")
			# If player doesn't have enough gold
			elif (player_char['player_gold'] < inn_refill_required): 
				print("\n\"You don't have enough gold.\" ")
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

[I]nn - Visit the inn
[S]hop - Browse for weapons and armor
[T]rainer - Enter the trainer's arena
[F]orest - Venture out into the forest 
[Stats] - View character stats
[E]xit to Main Menu (Any unsaved progress will be lost)
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
Level : {}
XP : {} / {}
Race : {}
Class : {}
Health : {} / {}
Defence : {}
Attack : {} """.format(player_char['player_name'], player_char['player_level'], 
			 player_char['player_experience'], player_xp_required, 
			 player_char['player_race'], player_char['player_class'],
			 player_char['player_health'], player_char['player_max_hp'],
			 player_char['player_defence'], player_char['player_attack']))
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
[S]word - Knight
[Sh]ortsword - Thief
[Sp]ellsword - Mystical Warrior
""").lower()
		if player_class_input == "s":
			player_char['player_class'] = 'Knight'
			player_char['player_health'] += 5  # Adding onto the preset stats instead 
			player_char['player_defence'] += 1 # of making them equal to a value
			player_char['player_attack'] += 2
			break
		elif player_class_input == "sh":
			player_char['player_class'] = 'Thief'
			player_char['player_health'] += 4
			player_char['player_defence'] += 1
			player_char['player_attack'] += 3
			break
		elif player_class_input == "sp":
			player_char['player_class'] = 'Mystical Warrior'
			player_char['player_health'] += 3
			player_char['player_defence'] += 1
			player_char['player_attack'] += 4
			break
		else:
			print(invalid_message)
	# Asking for the player's name can be outside of a while loop because
	# there shouldn't be any unexpected inputs to account for
	player_name_input = input("""
Before you take your first steps towards the village, you recall your name.

Your name is: """)
	player_char['player_name'] = player_name_input # Player's name is a string
												   # so it should be able to accept most names
	while True:
		player_char['player_max_hp'] = player_char['player_health']
		player_confirmation_input = input("""
Before you venture on...

Is this your true self?

Name : {}
Race : {}
Class : {}
Max Health : {}
Defence : {}
Attack : {}
		
[Y]es, this is my character
[N]o, I want to go back and change my character
""".format(player_char['player_name'], player_char['player_race'],
		 player_char['player_class'], player_char['player_max_hp'],
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
		global player_char # Declaring a global variable so it isn't treated 
						   # like a local variable
		player_char = eval(open("savegame.txt").read())
	# Defining the player's stats as whatever is in the contents of the file
	# which should only consist of player_char
		while True:
			load_input = input("""
Character data:

Name : {}
Level : {}
XP : {} / {}
Race : {}
Class : {}
Health : {} / {}
Defence : {}
Attack : {}

[L]oad
[E]xit to Main Menu
""".format(player_char['player_name'], player_char['player_level'], 
			 player_char['player_experience'], player_xp_required, 
			 player_char['player_race'], player_char['player_class'],
			 player_char['player_health'], player_char['player_max_hp'], 
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
	# Global variables - Player Settings

	# Originally, this was at the top of the program for easier access, but
	# these variables would only be defined when the program is run again, 
	# and so starting consecutive new games with the program still running
	# caused first encounter dialogue for the NPCs to bug out and think that the
	# player had already visited them when they had not.

	# Putting these variables here was the only way to prevent 
	# that bug from occurring.

	# (char = character)
	global player_char 	  		# Declaring the global variable before using it
	global player_template_char	# Otherwise it would function as a local variable
								# and not have the proper stats 

	# Player stats are stored inside a dictionary for easy access
						   
	player_template_char = {  # All of these keys/variables are saved
		'player_race' : ' ',
		'player_class' : ' ',
		'player_health' : 0, 
		'player_max_hp' : 0, # Max HP points the player can have at any time
		'player_defence' : 0,
		'player_attack' : 0,
		'player_name' : ' ',
		'player_shield' : 0, # Shields count as an armor piece
		'player_boots' : 0, # Armor pieces give a defence boost
		'player_gauntlets' : 0, # There is no inventory system so the names
		'player_helmet' : 0, 	# of the items don't need to shown after they
		'player_armor' : 0,		# have been bought
		'player_weapon' : 0, # Same with weapons, except they give more attack
		'player_experience' : 0, # experience = Experience Points (XP)
		'player_level' : 1,
		'player_gold' : 100,
		'first_visit_i' : True, # Is automatically set to False when the player 
								# triggers first encounter dialogue in the inn
	#	'first_visit_s' : True, # Same as the inn variable, except it's for the inn [scrapped]
		'first_visit_t' : True, # Same as the shop variable, except it's for the trainer
		'bought_weapon' : False,
		'bought_shield' : False,
		'bought_boots' : False,
		'bought_gauntlets' : False,
		'bought_helmet' : False,
		'bought_armor' : False,
		'max_healing_potions' : 3, # Max amount of potions the player can have
		'current_healing_potions' : 3 # How many potions the player has currently

		# This is the default template for a new character
		# that is defined each time the program is loaded

		# Loaded characters will load the stats they had when they saved

		# Can be accessed with player_char['key']
		# A new character will have to be created if a new key is added here

		# In hindsight, I probably should've removed the 'player_' portion of the 
		# keys so referencing them later on would take less characters, but I
		# realized this too late after I had already put in too many references to
		# them in the code.
	}

	player_char = player_template_char

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
			sys.exit()  # sys.exit() will stop the program when called
		else: # This else statement is used throughout the program to account for
			  # unexpected inputs, allowing for it to keep going regardless of what the
			  # player types, as it will go back to the beginning of the infinite loop
			print(invalid_message)
			# The loop doesn't get broken here, so it just goes back to the start of the while loop

StartMenu() # Initiate the game, other functions don't need to be called
			# because they will be called inside each other