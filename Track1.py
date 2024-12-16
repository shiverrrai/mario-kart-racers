#Track1.py

import pygame, math, random
from pygame.locals import *
pygame.init()

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

#class for Player Car object 
class Car(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self) #call Sprite superclass
		#load image from same directory
		(self.image, self.rect)=getImage("car.png") 
		#scale image to appropriate size
		self.image=pygame.transform.scale(self.image, (125,125))
		self.width=width
		self.height=height
		self.offset=80 
		(self.rect.center)=(self.width/2-self.offset, self.height/2)
		self.original=self.image #creates copy of image
		self.carFacing=0 
		self.spinning=0

	#returns False if car is still spinning, True if done spinning
	def isSpinning(self):
		if(self.spinning):
			if(self.spin()):
				return True
			else:
				return False

	#resets to initial car position
	def restart(self):
		self.__init__(self.width, self.height)
	
	#takes in a direction
	#rotates car about center
	def move(self, direction):
		fullRotation=360.0
		self.carFacing+=direction
		center=self.rect.center
		#rotate copy of image to preserve image quality
		self.image=pygame.transform.rotate(self.original, self.carFacing)
		self.rect = self.image.get_rect(center=center)
		self.carFacing%=fullRotation #reset direction every complete rotation
		return self.carFacing

	#ADAPTED FROM:
	#pygame examples: chimp.py
	def spin(self):
		center = self.rect.center
		self.spinning=self.spinning+12
		if(self.spinning>=360):
			self.spinning=0
			self.image=pygame.transform.rotate(self.original, self.carFacing)
			self.rect=self.image.get_rect(center=center)
			return True #car has completed spinning
		else:
			self.image=pygame.transform.rotate(self.original, 
				self.carFacing+self.spinning)
			self.rect = self.image.get_rect(center=center)
			return False #car is still spinning

#represents racetrack object
#racetrack moves in opposing direction to create illusion of motion
class RaceTrack(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect)=getImage("mariokarttrack2.png")
		self.original=self.image
		self.width, self.height=width, height
		#magnifies racetrack to 5000x5000 pixels
		self.image=pygame.transform.scale(self.original, (5000,5000))
		startingLineLocation=(-3700,-2000)
		self.rect.center=startingLineLocation #aligns car at starting line
		self.carLocationX=width/2
		self.carLocationY=height/2
		self.motion=10 #starting speed
		self.terminalSpeed=75 #max speed
		#RGBA of racetrack
		self.courseRGBA1,self.courseRGBA2=(112, 112, 112, 255),(96, 96, 96, 255)
		self.laps=1 #current lap
		#create a Rect object to represent starting line
		self.startingLine=pygame.Rect((4300, 2700),(500, 100)) 
		self.moving=False
		#distance traveled and minimum distance to avoid double-counting laps
		self.distance, self.minDistance=0,100 
		self.gameOver=False 
		#player car's current location relative to track
		self.offset=50
		self.location=(self.carLocationX-self.rect.x-self.offset,
			self.carLocationY-self.rect.y)
		self.prevRect=self.rect
		
	#resets to initial map position
	def restart(self):
		self.__init__(self.width, self.height)

	#"erases" bananas that have been rolled over by drawing a new racetrack
	#and centering it at the car's previous location
	def clearBanana(self, location):
		(self.image, self.rect)=getImage("mariokarttrack2.png")
		self.original=self.image
		self.image=pygame.transform.scale(self.original, (5000,5000))
		self.rect=self.prevRect
	
	#returns player car's current location relative to track
	def getLocation(self):
		return self.location

	#scrolls background to represent motion
	def accelerate(self, carFacing):
		if(self.gameOver==False):
			#(x,y) is car's location relative to track
			(x,y)=(self.carLocationX-self.rect.x,self.carLocationY-self.rect.y)
			accelerationFactor=5
			#cannot move if off course
			if(not(0<x<self.image.get_width()) or 
				not(0<y<self.image.get_height())):
				return
			#keep accelerating while under max velocity
			if(self.motion<self.terminalSpeed):
				self.motion+=accelerationFactor
			else:
				self.motion=self.terminalSpeed
			carFacing=math.radians(carFacing)
			#calculates direction of motion based on where car is facing
			direction=(self.motion*math.cos(math.pi/2-carFacing), 
					self.motion*math.sin(math.pi/2-carFacing))
			self.prevRect=self.rect
			newPos=self.rect.move(direction) #moves image in specified direction
			self.rect=newPos
			self.distance+=1
			#return current car position relative to entire course
			self.location=(x-self.offset,y)
			return (x,y)
		else: return False

	#decreases car's speed when user releases gas or veers off race course
	def decelerate(self):
		self.motion=10

	#game over when car is off entire course
	def outOfBounds(self):
		#(x,y) is car's location relative to track
		(x,y)=(self.carLocationX-self.rect.x,self.carLocationY-self.rect.y)
		if(not(0<x<self.image.get_width()) or not(0<y<self.image.get_height())):
			self.gameOver=True
			return True
		else:
			return False

	#decreases car's speed when off racetrack
	def offCourse(self):
		#(x,y) is car's location relative to track
		(x,y)=(int(self.carLocationX-self.rect.x), int(self.carLocationY-self.rect.y))
		if(self.image.get_at((x,y))!=self.courseRGBA1 and 
			self.image.get_at((x,y))!=self.courseRGBA2):
			return True
		else:
			return False

	#returns True if car is in motion, False otherwise
	def inMotion(self, moving):
		if(moving==True):
			self.moving=True
		else:
			self.moving=False
		return self.moving

	#returns speed and location of player car
	def speedometer(self):
		self.location=(self.carLocationX-self.rect.x-self.offset,
			self.carLocationY-self.rect.y)
		return (self.motion, self.location)

	#keeps track of player car's lap count
	def countLaps(self):
		#car must pass starting line, be in motion, and travel a minimum 
		#distance to complete a lap
		if(self.startingLine.collidepoint(self.carLocationX-self.rect.x,
			self.carLocationY-self.rect.y)==True and self.moving==True and 
			self.distance>=self.minDistance):
			self.laps+=1
			self.distance=0 #reset distance traveled
		if(self.laps>=4): #complete 3 laps to win game
			self.gameOver=True
		return self.laps

#keeps track of user's current lap
class Score(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.displayScore(1)

	#resets lap count
	def restart(self):
		self.__init__()

	#displays lap number on window
	#adapted from pygame tutorials 
	#http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
	def displayScore(self, laps):
		font = pygame.font.Font(None, 36) #creates font object
		text = font.render("Current Lap: %s"%laps, 1, (10, 10, 10)) 
		#creates image and rect attributes for drawing
		self.image=text 
		self.rect=self.image.get_rect() 

#keeps track of time
class Timer(object):
	def __init__(self, startTime):
		self.elapsedTime=0
		self.startTime=startTime

	#updates timer with time since game started
	def updateTimer(self):
		time=self.getElapsedTime()
		return self.displayTime(time)

	#restarts timer
	def restartTimer(self, startTime):
		self.__init__(startTime)

	#displays time elapsed on window
	#adapted from pygame tutorials 
	#http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
	def displayTime(self, time):
		font=pygame.font.Font(None, 36)
		text=font.render("Time Elapsed: %s" % time, 1, (10, 10, 10))
		return text

	#calculates time elapsed since user starts game 
	def getElapsedTime(self):
		self.elapsedTime=pygame.time.get_ticks()-self.startTime 
		#format into minutes and seconds
		seconds=str(round((self.elapsedTime/1000.0)%60, 1))
		minutes=str((self.elapsedTime/60000)%60)
		t=minutes+"."+seconds
		return t

#creates a map of car's location on track
class Map(pygame.sprite.Sprite):
	def __init__(self, winWidth, winHeight):
		pygame.sprite.Sprite.__init__(self)
		self.winWidth,self.winHeight=winWidth,winHeight
		(self.image, self.rect)=getImage("mariokarttrack2.png")
		self.original=self.image
		self.width, self.height=150,150
		#scale image to 150x150 pixels
		self.image=pygame.transform.scale(self.original, 
			(self.width,self.height))
		#move image to bottom right corner of window
		self.rect=self.image.get_rect().move(0,winHeight-self.height)
		#calculated by dividing length of map by length of course (150/5000)
		self.scalingFactor=0.03 

	#resets map
	def restart(self):
		self.__init__(self.winWidth,self.winHeight)

	#returns (x,y) location of car relative to track
	def getLoc(self, carLocation):
		#calculate car location
		if(carLocation!=None):
			(x,y)=(int(carLocation[0]*self.scalingFactor), 
				int(carLocation[1]*self.scalingFactor))
			return (x,y)
		else:
			return None

#displays player car's location on map
class CarLocation(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect)=getImage("playerDot.gif")
		self.width, self.height=10,10 
		#scale image to 10x10 pixels
		self.image=pygame.transform.scale(self.image, (self.width,self.height))
		startingLineLocation=(136,635)
		#move to starting line
		self.rect=self.image.get_rect(center=startingLineLocation) 
		winHeight, mapHeight = 700, 150 
		self.offset=winHeight-mapHeight

	#resets car position on map
	def restart(self):
		self.__init__()

	#displays car's location on map
	def displayCar(self,carLocation):
		#move car to corresponding location in map
		(x,y)=(carLocation[0],self.offset+carLocation[1]) 
		self.rect=self.image.get_rect(center=(x,y))

#displays AI car's location on map
class AI_CarLocation(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect)=getImage("dot2.gif")
		self.width, self.height=10,10 
		#scale image to 10x10 pixels
		self.image=pygame.transform.scale(self.image, (self.width,self.height))
		startingLineLocation=(136,635)
		#move to starting line
		self.rect=self.image.get_rect(center=startingLineLocation) 
		winHeight, mapHeight = 700, 150 
		self.offset=winHeight-mapHeight

	#reset car's position on map
	def restart(self):
		self.__init__()

	#updates AI car's location on map
	def update(self, location):
		self.displayCar(location)

	#displays car's location on map
	def displayCar(self, location):
		if(location!=None):
			#move car to corresponding location in map
			(x,y)=(location[0],self.offset+location[1]) 
			self.rect=self.image.get_rect(center=(x,y))

#creates a computer-driven car
class AI_Car(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect)=getImage("car2.png")
		self.original=self.image
		self.width=width
		self.height=height
		self.offset=80 
		self.rect.center=(self.width/2+self.offset, self.height/2)
		self.carFacing=math.pi/2 
		self.screenLocation=self.rect.center
		self.prevTrackLocation=(4562,2862) #starting track location
		self.step=300 #distance ahead car "sees"
		self.speed=self.step/5 #speed at which car travels
		self.carLocation=(4730,2850) 
		self.prevCarLocation=self.carLocation #stores previous location of car
		self.laps=1
		self.distance, self.minDistance=0,100
		self.startingLine=pygame.Rect((4300, 2700),(500, 100)) 
		self.spinning=0

	#returns False if car is still spinning, True if done spinning
	def isSpinning(self):
		if(self.spinning):
			if(self.spin()):
				return True
			else:
				return False

	#returns car's location
	def getLocation(self):
		return self.carLocation

	#ADAPTED FROM:
	#pygame examples: chimp.py
	def spin(self):
		center = self.rect.center
		self.spinning=self.spinning+12
		if(self.spinning>=360):
			self.spinning=0
			self.image=pygame.transform.rotate(self.original, 
				math.degrees(self.carFacing)-90)
			self.rect = self.image.get_rect(center=center)
			return True #car has completed spinning
		else:
			self.image=pygame.transform.rotate(self.original, 
				math.degrees(self.carFacing)+self.spinning-90)
			self.rect = self.image.get_rect(center=center)
			return False #car is still spinning

	def restart(self):
		self.__init__(self.width, self.height)

	#updates car's position every frame
	#receives speed and track location from player's car
	def update(self, speed, location): 
		trackLocation=self.move(speed, location)
		laps=self.getLaps(trackLocation)
		self.distance+=1
		return trackLocation,laps

	#returns current lap of AI car
	def getLaps(self, trackLocation):
		if(trackLocation!=None):
			if(self.startingLine.collidepoint(trackLocation[0],trackLocation[1])
				and self.distance>self.minDistance):
				self.laps+=1
				self.distance=0
		return self.laps

	#controls AI car's movement relative to the screen and racetrack
	def move(self, speed, location):
		changeInTrackLocation=[abs(location[0]-self.prevTrackLocation[0]),
			abs(location[1]-self.prevTrackLocation[1])] 
		#reverse sign if moving right or up
		if(location[0]-self.prevTrackLocation[0]>0):
			changeInTrackLocation[0]*=-1
		if(location[1]-self.prevTrackLocation[1]>0):
			changeInTrackLocation[1]*=-1
		self.prevTrackLocation=location
		trackLocation=self.controlCar() #stores track location of car
		if(trackLocation!=None):
			changeInCarLocation=(trackLocation[0]-self.prevCarLocation[0],
				trackLocation[1]-self.prevCarLocation[1])
			#moves car on screen relative to player's location
			self.screenLocation=(changeInTrackLocation[0]+
				self.screenLocation[0]+changeInCarLocation[0],
				changeInTrackLocation[1]+self.screenLocation[1]
				+changeInCarLocation[1])
		self.prevCarLocation=trackLocation
		self.rect.center=self.screenLocation
		return trackLocation
	
	#moves forward or turns left/right based on whether a position is valid
	def controlCar(self):
		#test if direction in front of car is valid
		testDir=(int(self.carLocation[0]+self.step*math.cos(self.carFacing)),
			int(self.carLocation[1]-self.step*math.sin(self.carFacing)))
		valid=isValid(testDir)
		if(valid==True):
			#if valid, move car to tested location 
			self.carLocation=(int(self.carLocation[0]+
				self.speed*math.cos(self.carFacing)),
				int(self.carLocation[1]-self.speed*math.sin(self.carFacing)))
			return self.carLocation
		else:
			#try turning left
			testDir=self.turnLeft()
			if(testDir!=None):
				self.carLocation=testDir
				return self.carLocation
			else:
				#try turning right
				testDir=self.turnRight()
				if(testDir!=None):
					self.carLocation=testDir
					return self.carLocation

	#turns car left by 30 degrees
	def turnLeft(self):
		angle=self.carFacing+math.pi/6
		#test direction
		testDir=(self.carLocation[0]+int(self.step*math.cos(angle)), 
					self.carLocation[1]-int(self.step*math.sin(angle))) 
		valid=isValid(testDir)
		if(valid==True):
			self.carFacing=angle%(2*math.pi)
			#rotate image
			self.image=pygame.transform.rotate(self.original, 
				math.degrees(self.carFacing)-90)
			#reset car location
			self.carLocation=(self.carLocation[0]+
				int(self.speed*math.cos(angle)), 
				self.carLocation[1]-int(self.speed*math.sin(angle)))
			return self.carLocation
		else: 
			return None

	#turns car right by 30 degrees
	def turnRight(self):
		angle=self.carFacing-math.pi/6
		testDir=(self.carLocation[0]+int(self.step*math.cos(angle)), 
					self.carLocation[1]-int(self.step*math.sin(angle))) 
		valid=isValid(testDir)
		if(valid==True):
			self.carFacing=angle%(2*math.pi)
			self.image=pygame.transform.rotate(self.original,
				math.degrees(self.carFacing)-90)
			self.carLocation=(self.carLocation[0]+
				int(self.speed*math.cos(angle)), 
				self.carLocation[1]-int(self.speed*math.sin(angle)))
			return self.carLocation
		else: 
			return None

#determines whether a given location is valid (in bounds and on track)
def isValid(location):
	racetrack=RaceTrack(700,700)
	courseRGBA1=(112,112,112,255)
	courseRGBA2=(96,96,96,255)
	startingLineRGBA1=(0,0,0,255)
	startingLineRGBA2=(248,248,248,255)
	inBounds=(0<location[0]<racetrack.image.get_width() and 
		0<location[1]<racetrack.image.get_height())
	onTrack=(racetrack.image.get_at(location)==courseRGBA1 or 
		racetrack.image.get_at(location)==courseRGBA2 or 
		racetrack.image.get_at(location)==startingLineRGBA1 or 
		racetrack.image.get_at(location)==startingLineRGBA2)
	if(inBounds and onTrack):
		return True
	return False

#represents banana object
class Banana(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect)=getImage("mkBanana.png")
		racetrack=RaceTrack(700,700)
		(self.racetrackImage,self.racetrackRect)=(racetrack.image,
			racetrack.image.get_rect())
		self.courseRGBA1=(112, 112, 112, 255) #RGBA of racetrack
		self.courseRGBA2=(96, 96, 96, 255) #RGBA of racetrack
		start=(4562,2862)
		self.trackPixels=set()
		#retrieve potential locations to place bananas
		self.floodTrack(start[0],start[1]) 
		self.chooseBananaLocation() #pick locations to place bananas

	#create a set of all pixels on track
	#MODIFIED FROM floodFill-pixel-based.py from course notes
	def floodTrack(self, x, y):
		seen=(x,y) in self.trackPixels
		sameColor=(self.racetrackImage.get_at((x,y))==self.courseRGBA1 or 
		    self.racetrackImage.get_at((x,y))==self.courseRGBA2)
		if(seen==True or sameColor==False or len(self.trackPixels)>1000):
		    return self.trackPixels
		else:
		    self.trackPixels.add((x,y))
		    self.floodTrack(x-50,y) #left
		    self.floodTrack(x,y-50) #up
		    self.floodTrack(x+50,y) #right
		    self.floodTrack(x,y+50) #down

    #choose a random location on racetrack and place banana there
	def chooseBananaLocation(self):
		loc=random.sample(self.trackPixels, 1)
		newPos=self.rect.move(loc[0][0], loc[0][1])
		self.rect=newPos