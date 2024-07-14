#Welcome to Worldle! In this game, the user must guess the name of a country based on the silhouette they are shown on screen using pygame. If your guess is incorrect, the geodesic api will calculate how far away in kilometres your guess was from the correct country. If the user guesses the correct country in under 6 guesses, they will be given points relative to how many guesses it took. There are also two harder modes. In the "rotated countries" mode, the silhouette of the country is randomly rotated to make it less easy to recognize. In the "Quandale" mode, a picture of Mr. Quandale Dingle is shown instead of the country silhouette, making the game significantly harder. Additionally, there is also a hint system which will display either the continent of the capital of the country. Finally, once the user quits the game, their score will be added to a file which can be viewed through the menu's "Leaderboard" option. Enjoy!
#Importing the different modules into python
from PIL import Image
import pygame, sys
import time
from time import sleep
import random
import os
#Instructions function, displays the instructions of the game
def instructions():
	global text
	text = "Welcome to Worldle! In this game, you must guess the name of a country based on the silhouette you are shown on screen. If your guess is incorrect, you will be given the distance in kilometres that your guess was away from the correct country. There is also a hint system which will either display to you the capital or the continent of the country. Good Luck!"
#Typewriter function, allows the text to be displayed in a typewriter-like manner. Text is assigned to the 'text' variable and then the typewriter function is called.
def typeWriter():
	global text
	for letter in text:
		print(letter, end ="")
		sys.stdout.flush()
		sleep(0.03)
	print('')
os.system('clear')
#Importing the different text files so that they can be read as lists.
countries = open('countries.txt').read().splitlines()
latitudes = open('latitude.txt').read().splitlines()
longitudes = open('longitude.txt').read().splitlines()
computer = open('computer.txt').read().splitlines()
continents = open('continents.txt').read().splitlines()
capitals = open('capitals.txt').read().splitlines()
name = input("Please enter your name: ")
print('')
#prints out an ASCII art globe that looks pretty cool.
globe = open('earth.txt').read().splitlines()
loading = open('loading.txt').read().splitlines()
globeMulti = []
for num in range(28):
	globeMulti.insert(-1,globe[num])
for line in globeMulti:
	print(line)
	sys.stdout.flush()
	sleep(0.07)
print('')
sleep(3)
os.system('clear')
#importing geodesic, the api that calculates distances.
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
#The maingame function is aptly where all the main game code is located. It is summoned through the menu function and contains all the code for the hint system, the pygame display, and the main code for determining if the user's guess is correct.
def mainGame():
	global text
	global totalPoints
	global choice
	while True:
		#randomly chooses a country
		randomNum = random.randint(0,196)
		country = countries[randomNum]
		country = country.lower()
		#gets the png for the country
		if choice != "5":
			countryFile = "countries/" + country + ".png"
		else: 
			countryFile = "countries/quandale.png"
		pygame.init()
		X = 360
		Y = 360
		#uses pygame to display the image of the country
		white = (255, 255, 255)
		display_surface = pygame.display.set_mode((X, Y))
		pygame.display.set_caption('Worldle')
		image = pygame.image.load(countryFile)
		image = pygame.transform.smoothscale(image, (300,300))
		#rotates the image depending on if the user chose the rotated countries mode.
		if choice == "4":
			rotation = random.randint(0,360)
		else: rotation = 0
		#pygame related code such as making the canvas white and "blitting" the image onto the canvas.
		image = pygame.transform.rotate(image, rotation )
		country = countries[randomNum]
		display_surface.fill(white)
		display_surface.blit(image, (0, 0))
		for event in pygame.event.get():
			 if event.type == pygame.QUIT:
				 pygame.quit()
				 quit()
		pygame.display.update()
		#gets the latitudes and longitudes of the country
		countryLat = float(latitudes[randomNum])
		countryLon = float(longitudes[randomNum])
		countryCoords = (countryLat, countryLon)
		guesses = 0
		#the main loop of the user's guesses.
		while guesses < 6:
			#hint system
			while True:
				hintCheck = input("Would you like a hint? y/n: ")
				if hintCheck == "y":
					#chooses between capitals or continents for the hint
					hintGen = random.randint(0,1)
					if hintGen == 0:
						hint = continents[randomNum]
						text = "The country is located on the continent of " + hint
						typeWriter()
					elif hintGen == 1:
						hint = capitals[randomNum]
						text = "The country's capital city is " + hint
						typeWriter()
					break
				elif hintCheck == "n":
					break
				else: print("Please enter a valid option")
			#loop involving the actual country guessing
			while True:
				inList = "no"
				countryInput = input("Please enter a country: ")
				countryInput = countryInput.lower()
				#loop checking if the country the user guessed is actually a valid country.
				for num in range(len(countries)):
					if countryInput == countries[num]:
						inList = "yes"
						#gets the latitude and longitude of the guessed country
						inputLat = float(latitudes[num])
						inputLon = float(longitudes[num])
						inputCoords = (inputLat, inputLon)
				if inList == "yes":
					break
				else: print("Please enter a valid country")
			#geodesic calculates the distance between the input country and the correct country.
			distance = (geodesic(countryCoords, inputCoords).km)
			roundedDistance = round(distance)
			if roundedDistance == 0:
				percentageCloseRounded = 10
			#calculates how far in percentages the guess was from the correct answer.
			else:
				percentageClose = ((1-((roundedDistance)/20000))*10)
				percentageCloseRounded = round(percentageClose)
				if percentageCloseRounded == 10:
					percentageCloseRounded = 9
				if percentageCloseRounded == 0:
					percentageCloseRounded = 1
			#prints out a cool animated loading bar to show the percentage.
			for num in range(percentageCloseRounded):
				os.system('clear')
				print(loading[num])
				sleep(0.1)
			print("Your guess is", roundedDistance, "kilometres away")
			guesses += 1
			if countryInput == country:
				break
		if countryInput == country:
			#calculates how many points to give
			points = 7-guesses
			text = "You got " + str(points) + " points!"
			typeWriter()
			if guesses == 1:
				text = "Congratulations! You guessed the country in " + str(guesses) + " guess"
				typeWriter()
			else: 
				text = "Congratulations! You guessed the country in " + str(guesses) + " guesses"
				typeWriter()
		else: 
			points = 0
			text = ("You lose! The correct country was " + country)
			typeWriter()
		sleep(2)
		os.system('clear')
		return points
#The menu function calls all the other functions and also displays the leaderboard and allows the user to select their gamemode.
def menu():
	#making variables global so they're easier to work with.
	global text
	global totalPoints
	global choice
	global computer
	totalPoints = 0
	instructions()
	typeWriter()
	#main menu loop
	while True:
		while True:
			#displays the user's choices.
			text = "1. Countries\n2. Quit\n3. Leaderboard\n4. Rotated Countries\n5. Quandale Mode (Hides Image)"
			typeWriter()
			choice = input("Choice: ")
			#summons the main game
			if choice == "1":
				os.system('clear')
				totalPoints += mainGame()
				break
			#quit option. Displays the users overall score and saves it to a file along with the user's name.
			elif choice == "2":
				print("Thank you for playing! You accrued", totalPoints, "total points!")
				file_scores = open(r"scores.txt", "a")
				file_scores.write("\n")
				file_scores.write(str(totalPoints))
				file_scores.close()
				file_names = open(r"names.txt", "a")
				file_names.write("\n")
				file_names.write(name)
				file_names.close()
				break
			#leaderboard option. Displays the highest score from the saved file. Also prints a cool computer ASCII art.
			elif choice == "3":
				os.system('clear')
				pointsListString = open('scores.txt').read().split()
				highPoints = 0
				#turns the scores file into a readable integer list
				pointsList = [int(s.split()[0])for s in pointsListString]
				#finds the highest score.
				if len(pointsList) > 0:
					highPoints = max(pointsList)
					pos = 0
					while True:
						if pointsList[pos] == highPoints:
							break
						pos += 1
				#finds the name associated with the highest score
				namesList = open('names.txt').read().splitlines()
				if len(namesList) > 0:
					highNames = namesList[pos]
				else: highNames = 'invalid'
				print("High score made by", highNames + ":", highPoints)
				computerMulti = []
				#previously mentioned cool computer ASCII art
				for num in range(14):
					computerMulti.insert(-1,computer[num])
				for num in range(len(computerMulti)):
					if num == 4:
						print("   || ",highNames + ":", highPoints)
					else:
						print(computerMulti[num])
					sys.stdout.flush()
					sleep(0.07)
				sleep(6)
				os.system('clear')
			#rotated countries mode.
			elif choice == "4":
				os.system('clear')
				totalPoints += mainGame()
				break
			#quandale mode
			elif choice == "5":
				os.system('clear')
				totalPoints += mainGame()
				break
			else: print("Please enter a valid option")
		#play again option. Only shown after the user finishes a game.
		if choice != "2":
			while True:
				playAgain = input("Would you like to play again? y/n: ")
				if playAgain == "y" or playAgain == "n":
					break
				else: print("Please enter a valid option")
			#like the quit option except after a user finishes a game. In a separate loop to prevent repeatition.
			if playAgain == "n":
				print("Thank you for playing! You accrued", totalPoints, "total points!")
				file_scores = open(r"scores.txt", "a")
				file_scores.write("\n")
				file_scores.write(str(totalPoints))
				file_scores.close()
				file_names = open(r"names.txt", "a")
				file_names.write("\n")
				file_names.write(name)
				file_names.close()
				break
			elif playAgain == "y": 
				os.system('clear')
		else: break
menu()