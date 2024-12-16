#Shiv Wadwani
#15112 TERM PROJECT
#December 4, 2014
#Section B

import math, random, Buttons, Track1, Track2
import pygame
from pygame.locals import * #imports pygame local constants

#ADAPTED FROM:
#http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
#returns image and its area rectangle with given filename
def getImage(fileName):
	image=pygame.image.load(fileName) #loads image
	image=image.convert() #converts image to same format as Surface
	#set colorkey to color at top left corner of image
	colorkey=image.get_at((0,0))
	image.set_colorkey(colorkey)
	return image, image.get_rect()


#determines if player car collides with AI car
def isCarCollision(player, ai, racetrack):
	#decelerate if forward-crash
	if(ai.rect.collidepoint(player.rect.topleft) or 
		ai.rect.collidepoint(player.rect.topright)):
		racetrack.decelerate()
	#accelerate if rear-ended
	if(ai.rect.collidepoint(player.rect.bottomleft) or 
		ai.rect.collidepoint(player.rect.bottomright)):
		accelerationFactor=5
		racetrack.motion+=accelerationFactor

#player car spins if it collides with a banana
#MODIFIED FROM:
#PYGAME IMPLEMENTATION OF pygame.sprite.spritecollide()
def carBananaCollision(playerLoc, bananas, player):
	collisionList = []
	for s in bananas.sprites():
		if s.rect.collidepoint(playerLoc):
			collisionList.append(s)
	if(len(collisionList)!=0):
		player.spin()
		return collisionList[0]
	else:
		return None

#AI car spins if it collides with a banana
#MODIFIED FROM:
#PYGAME IMPLEMENTATION OF pygame.sprite.spritecollide()
def aiBananaCollision(aiCarLoc, bananas, aiCar):
	collisionList = []
	for s in bananas.sprites():
		if s.rect.collidepoint(aiCarLoc):
			collisionList.append(s)
	if(len(collisionList)!=0):
		aiCar.spin()
		return collisionList[0]
	else:
		return None

#creates and renders text
def getText(text):
	font=pygame.font.Font(None, 72) #creates font object
	title=text
	textImage=font.render(title, 1, (10, 10, 10))
	textPos=textImage.get_rect()
	return textImage, textPos

#sets background window
def getBackground(screen):
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((255,255,255)) #white background
	return background

#start screen
def getHomeScreen(background):
	#load image from same directory
	(screenImage, screenRect)=getImage("mariokarthomepage.jpg")
	original=screenImage
	backgroundDimensions=background.get_size()
	#scale image down to appropriate size
	screenImage=pygame.transform.scale(original, backgroundDimensions)
	background.blit(screenImage, screenRect)
	(titleImage, titleRect)=getImage("mariokarttext.png")
	original=titleImage
	titleImage=pygame.transform.scale(original, (backgroundDimensions[0],
		backgroundDimensions[1]/4))
	background.blit(titleImage,titleRect)
	(raceImage, raceRect)=getImage("racersImg.png")
	original=raceImage
	raceImage=pygame.transform.scale(original, (backgroundDimensions[0]/2,
		backgroundDimensions[1]/6))
	raceRect=(200, 150)
	background.blit(raceImage, raceRect)
	instruction, instructionPos=getText("SPACEBAR TO CONTINUE")
	instructionPos.midbottom=background.get_rect().midbottom
	background.blit(instruction,instructionPos)
	return background

#creates instruction screen
def getInstructionScreen(background):
	background.fill((100,175,100)) #light green
	#create text
	instruction1, instructionPos1=getText("Use arrow keys to maneuver")
	#position text
	instructionPos1.center=(350, 50)
	instruction2, instructionPos2=getText("Avoid bananas")
	instructionPos2.center=(350, 150)
	instruction3, instructionPos3=getText("Finish 3 Laps")
	instructionPos3.center=(350,250)
	instruction4, instructionPos4=getText("Press spacebar to continue")
	instructionPos4.center=(350, 350)
	instruction5, instructionPos5=getText("h for help, r for restart")
	instructionPos5.midbottom=background.get_rect().midbottom
	#paste text onto background surface
	background.blit(instruction1, instructionPos1)
	background.blit(instruction2, instructionPos2)
	background.blit(instruction3, instructionPos3)
	background.blit(instruction4, instructionPos4)
	background.blit(instruction5, instructionPos5)
	return background

#creates screen for selecting track
def getSelectionScreen(background):
	button1=Buttons.Button()
	button2=Buttons.Button()
	button1.create_button(background, (24,189,214), 50, 150, 150, 75, 0, "Track 1", (0,0,0))
	button2.create_button(background, (24,189,214), 400, 150, 150, 75, 0, "Track 2", (0,0,0))
	(img1,imgRect1)=getImage("mariokarttrack2.png")
	img1=pygame.transform.scale(img1, (250,250))
	imgRect1.topleft=(50, 250)
	(img2,imgRect2)=getImage("mariokarttrack3.png")
	img2=pygame.transform.scale(img2, (250,250))
	imgRect2.topleft=(400, 250)
	background.blit(img1, imgRect1)
	background.blit(img2, imgRect2)
	return background, button1, button2

def main():
	pygame.init() #initialize pygame modules
	width=700
	height=700
	screen = pygame.display.set_mode((width, height)) #create window
	#create start window as background
	background=getBackground(screen)
	background=getHomeScreen(background)
	#display background
	screen.blit(background, (0, 0))
	pygame.display.flip()
	pygame.mouse.set_visible(True)
	runGame(width, height, background, screen)
	pygame.quit()

#runs main loop of program
def runGame(width, height, background, screen):
	#prepare game objects
	car=Track1.Car(width, height)
	racetrack1=Track1.RaceTrack(width, height)
	score=Track1.Score()
	courseMap1=Track1.Map(width,height)
	mapCar1=Track1.CarLocation()
	ai_car1=Track1.AI_Car(width, height)
	aiMapCar1=Track1.AI_CarLocation()

	racetrack2=Track2.RaceTrack(width,height)
	courseMap2=Track2.Map(width,height)
	mapCar2=Track2.CarLocation()
	ai_car2=Track2.AI_Car(width, height)
	aiMapCar2=Track2.AI_CarLocation()

	track1_GameObjects=[racetrack1, car, score, courseMap1, mapCar1, ai_car1, aiMapCar1]
	track2_GameObjects=[racetrack2, car, score, courseMap2, mapCar2, ai_car2, aiMapCar2]

	gameObjects=[]
	displayStartWindow(background, screen)
	displayInstructions(background,screen)
	track=displaySelectionScreen(background, screen, gameObjects)

	if(track==1):
		gameObjects=track1_GameObjects
		bananaList=[]
		for i in range(15): #place 15 bananas on track
			b=Track1.Banana()
			bananaList.append(b)
	elif(track==2):
		gameObjects=track2_GameObjects
		bananaList=[]
		for i in range(15):
			b=Track2.Banana()
			bananaList.append(b)
	bananas=pygame.sprite.Group((bananaList))

	#Sprite OrderedUpdates Group- accesses sprites in order they are added
	allsprites = pygame.sprite.OrderedUpdates(gameObjects)
	background.fill((255,255,255))
	allsprites.draw(screen)
	countDown(background, screen) #count down until race begins
	pygame.time.delay(3000) #countdown for 3 seconds (3000 milliseconds)
	pygame.display.flip()
	#only initialize time when game is about to start
	time=Track1.Timer(pygame.time.get_ticks()) 
	gameObjects.append(time)
	background.fill((255,255,255))
	runMainLoop(background, screen, gameObjects, allsprites, bananas)

#count down to race
def countDown(background,screen):
	countdown, countdownRect=getText("3...2...1...GO!")
	countdownRect.center=background.get_rect().center
	background.blit(countdown, countdownRect)
	screen.blit(background, (0,0))
	pygame.display.flip()

#displays starting window
def displayStartWindow(background, screen):
	while True:
		event=pygame.event.poll() 
		#wait until user presses spacebar to proceed to next slide
		if(event.type==KEYDOWN and event.key==K_SPACE):
			return

#displays instructions for user reference
def displayInstructions(background, screen):
	background.fill((255,255,255))
	background=getInstructionScreen(background)
	screen.blit(background, (0, 0))
	pygame.display.flip()
	while True:
		event=pygame.event.poll()
		#wait until user presses spacebar to proceed to next slide
		if(event.type==KEYDOWN and event.key==K_SPACE):
			return

#displays game selection screen
def displaySelectionScreen(background, screen, gameObjects):
	background.fill((255,255,255))
	background,button1, button2=getSelectionScreen(background)
	screen.blit(background, (0, 0))
	pygame.display.flip()
	while True:
		event=pygame.event.poll()
		if(event.type==MOUSEBUTTONDOWN):
			if(button1.pressed(pygame.mouse.get_pos())):
				return 1
			elif(button2.pressed(pygame.mouse.get_pos())):
				return 2

#displays game over message, time, and result when game is over
def displayGameOver(background, screen, finalTime, result):
	background.fill((255,255,255))
	gameOverText, textPos=getText("Game Over!")
	timeText, timePos= getText("Time: %s" % finalTime)
	resultText, resultPos=getText(result)
	textPos.center=(350,350)
	timePos.center=(350, 150)
	resultPos.center=(350, 550)
	background.blit(gameOverText, textPos)
	background.blit(timeText, timePos)
	background.blit(resultText, resultPos)
	return background

#runs main loop of program
def runMainLoop(background, screen, gameObjects, allsprites,bananas):
	clock=pygame.time.Clock()
	time=gameObjects[7]
	finalTime=0
	#mainloop
	going, gameOver=True, False
	while going:
		clock.tick(100) #run game at 100 frames per second
		#Handles user entrance/exit from game
		going=doEventQueue(going, allsprites, bananas, gameObjects, 
			background, screen)
		if(gameOver!=True):
			gameOver, result = handleGameEvents(gameObjects, bananas, allsprites)
		#delete everything
		screen.fill((0,0,0))
		screen.blit(background, (0,0))
		#Draw everything
		if(not gameOver):
			finalTime=time.getElapsedTime()
			allsprites.draw(screen)
			bananas.draw(gameObjects[0].image) #draw bananas on racetrack
			screen.blit(time.updateTimer(), (350,0))
			pygame.display.flip()
		else:
			gameOver=True
			background=displayGameOver(background, screen, finalTime, result)
			screen.blit(background, (0,0)) 
			pygame.display.flip()

#handles user entrance/exit from game
def doEventQueue(going, allsprites, bananas, gameObjects, background, screen):
	time=gameObjects[7]
	for event in pygame.event.get():
		if event.type == QUIT:
			going = False
			return going
		elif event.type == KEYDOWN and event.key==K_ESCAPE:
			going=False	
			return going
		#restart
		elif event.type==KEYDOWN and event.key==K_r:
			for sprite in allsprites.sprites():
				sprite.restart()
			time.restartTimer(pygame.time.get_ticks())
			return True
		#help window
		elif event.type==KEYDOWN and event.key==K_h:
			displayInstructions(background, screen)
			return True
	return True

#handles car maneuvering events of game
#takes in gameObjects, a list of the objects of game
def handleGameEvents(gameObjects, bananas, allsprites):
	#assigns elements to more appropriate names
	(racetrack,car,score,ai_car)=(gameObjects[0],gameObjects[1],
		gameObjects[2],gameObjects[5])
	laps=racetrack.countLaps() #transfer laps to Score class for display
	score.displayScore(laps)
	#check if player car collides with banana
	location=racetrack.getLocation()
	banana=carBananaCollision(location, bananas, car)
	if(banana!=None):
		if(not car.isSpinning()):
			return False, None
		else:
			banana.kill() #remove banana after car stops spinning
			racetrack.clearBanana(location)
	#check if AI car collides with banana
	location=ai_car.getLocation()
	banana=aiBananaCollision(location,bananas,ai_car)
	if(banana!=None):
		if(not ai_car.isSpinning()):
			return False, None
		else:
			banana.kill() #remove banana after car stops spinning
			racetrack.clearBanana(location)
	#check if player car and AI car collide with each other
	isCarCollision(car,ai_car,racetrack)
	keys=pygame.key.get_pressed()
	gameOver,result = onKeyPressed(keys, gameObjects, bananas)
	if(gameOver==True): return True, result
	return False, None #default

#handles key presses for car maneuverability
def onKeyPressed(keys, gameObjects, bananas):
	#assigns elements to more appropriate names
	(racetrack,car,score,courseMap,mapCar,ai_car,aiMapCar)=(gameObjects[0],
		gameObjects[1],gameObjects[2],gameObjects[3],gameObjects[4],
		gameObjects[5],gameObjects[6])
	(speed,location,turnFactor)=(None,None,11.25)
	#return that game is over 
	if(racetrack.outOfBounds()==True): return True, "OUT OF BOUNDS!" 
	#slow down speed if off track
	if(racetrack.offCourse()==True): racetrack.decelerate() 
	if keys[K_UP]:
		carPosition=car.move(0) #move car without changing direction
		location=racetrack.accelerate(carPosition) 
		if(location!=False): #game is still running
			#feed location into courseMap object for display
			(x,y)=courseMap.getLoc(location) 
			mapCar.displayCar((x,y))
			racetrack.inMotion(True) #the car is in motion
		else: return True, "YOU WIN!" #return that game is over
	if keys[K_RIGHT]: carPosition=car.move(-turnFactor) 
	if keys[K_LEFT]: carPosition=car.move(turnFactor)
	if (not (keys[K_UP])):
		racetrack.decelerate() #slow down speed if forward key released
		racetrack.inMotion(False) #car is no longer in motion
	(speed,location)=racetrack.speedometer() 
	#pass speed and location of car to ai_car
	aiCarLoc, AIlaps=ai_car.update(speed, location) 
	#get scaled down location of AI car for display on Map
	scaledAICarLoc=courseMap.getLoc(aiCarLoc) 
	#pass scaled location of AI Car to update position on Map
	aiMapCar.update(scaledAICarLoc) 
	if(AIlaps>=4): return True, "YOU LOSE!" #return that game is over
	return None,None #default

main()
