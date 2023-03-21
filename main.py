#########################################
# Name: David and Alia
# Date: 5/05/2022
# File Name: main.py
# Description: This program recreates the TRON Game.
#########################################

import pygame
pygame.init()

from random import randint, randrange

#Initialize global variables
HEIGHT = 600
WIDTH  = 800
font = pygame.font.SysFont("Ariel Black",30)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
outline=10

screen=pygame.display.set_mode((WIDTH,HEIGHT))

#Load sound
pygame.mixer.music.load("TronMusic.ogg")
pygame.mixer.music.set_volume(0.8)
chargeSound=pygame.mixer.Sound("chargeSound.ogg")

#Load and transform all of the images
car1 = pygame.image.load("blueLeftTop.png").convert_alpha()
car2 = pygame.image.load("yellowLeft.png").convert_alpha()
car2 = pygame.transform.scale(car2, (20,20))
car1 = pygame.transform.scale (car1, (20,20))
car1Right=pygame.transform.rotate(car1, 0)
car1Left=pygame.transform.rotate(car1, 180)
car1Up=pygame.transform.rotate(car1, 90)
car1Down=pygame.transform.rotate(car1, 270)
car2Right=pygame.transform.rotate(car2, 0)
car2Left=pygame.transform.rotate(car2, 180)
car2Up=pygame.transform.rotate(car2, 90)
car2Down=pygame.transform.rotate(car2, 270)
background = pygame.image.load("background.jpg").convert_alpha()
background = pygame.transform.scale(background, (WIDTH,HEIGHT))
introBackground = pygame.image.load("introBackground.jpg").convert_alpha()
introBackground=pygame.transform.scale(introBackground,(WIDTH,HEIGHT))
tronLogo = pygame.image.load("tronLogo.jpg")
tronLogo = pygame.transform.scale(tronLogo,(250,100))
charge = pygame.image.load("charge.png").convert_alpha()
obstacle = pygame.image.load("obstacle.png").convert_alpha()
obstacle = pygame.transform.scale(obstacle, (30,30))
star = pygame.image.load("star.png").convert_alpha()
star = pygame.transform.scale(star,(30,30))
temp1 = car1
temp2 = car2


#---------------------------------------#
# player's properties                   # 
#---------------------------------------#
class Player():
  def __init__(self,CLR=BLUE,startPosition=7,direction=-1):
    self.BODYSIZE = 3
    self.HSPEED = 3
    self.VSPEED = 3
    self.direction=direction
    self.speedX = self.HSPEED*direction
    self.speedY = 0
    self.segx = [(400-self.speedX*100), (400-self.speedX*100)-self.speedX, (400-self.speedX*100)-2*self.speedX]
    self.segy = [HEIGHT//2]*3
    self.CLR = CLR
    self.permCLR = CLR
    self.lives = 7
    self.invincible=False
    self.timeStart = 0

  def drawPlayer(self, image):
    #Draws the entire trail of the player along with the image. Dynamic with speed changes (increasing the body size with speed boosts)
    for i in range(len(self.segx)):
      pygame.draw.rect(screen, self.CLR, (self.segx[i], self.segy[i], self.BODYSIZE+round(abs(self.speedY+self.speedX)//1.4),self.BODYSIZE+round(abs(self.speedX+self.speedY)//1.4)), outline) 
      screen.blit(image,(self.segx[0]-10,self.segy[0]-10))
  
  def moveLeft(self):
    self.speedX = -self.HSPEED
    self.speedY = 0
    
  def moveRight(self):
    self.speedX = self.HSPEED
    self.speedY = 0
    
  def moveUp(self):
    self.speedX = 0
    self.speedY = -self.VSPEED
    
  def moveDown(self):
    self.speedX = 0
    self.speedY = self.VSPEED
    
  def extend(self):
    self.segx.append(self.segx[-1])           # assign the same x and y coordinates
    self.segy.append(self.segy[-1]) 

  def collisionCharge(self,chargeList):
    #Checks if the Tron collides with the charge
    for i in chargeList:
          if self.segy[0]-i.y<i.size and self.segy[0]-i.y>0 and self.segx[0]-i.x<i.size and self.segx[0]-i.x>0 and i.visible:
            
            chargeSound.play(loops=0) #Plays charge sound
            #Update speed depending on the size of the charge
            self.HSPEED=i.size//6
            self.VSPEED=i.size//6
            i.visible=False #Charge disappears
            #Updates speeds
            if self.speedX==0:
              if self.speedY>0:
                self.speedY=self.HSPEED
              if self.speedY<0:
                self.speedY=-self.HSPEED
            if self.speedY==0:
              if self.speedX>0:
                self.speedX=self.VSPEED
              if self.speedX<0:
                self.speedX=-self.VSPEED

  def collisionStar(self,starList):
    #Checks to see if the Tron collides with the Star, and the Tron becomes invincible
    for i in starList:
      if self.segy[0]-i.y<i.size and self.segy[0]-i.y>0 and self.segx[0]-i.x<i.size and self.segx[0]-i.x>0 and i.visible:
        self.timeStart= time #Finds what time the Tron collided with the Star
        self.invincible=True
        i.visible = False #Star disappears
    if self.invincible:
      self.CLR = (randint(0,255),randint(0,255),randint(0,255)) #Generates random colour every instance (like a rainbow)
      if time-self.timeStart>10: #If the Tron has been invincible for more than 10 seconds
        self.CLR = self.permCLR
        self.invincible=False

  def collisionWall(self,opponent,obstacleList,chargeList,starList):
    #If the tron goes out of the frame, reset all of the objects to default settings
    if self.segx[0] < 0 or self.segx[0]>WIDTH:
      self.reset()
      opponent.reset()
      for i in obstacleList:
          i.reset()
      for i in chargeList:
        i.reset()
      for i in starList:
        i.reset()
      return True
    if self.segy[0] < 0 or self.segy[0]>HEIGHT:
      self.reset()
      opponent.reset()
      for i in obstacleList:
        i.reset()
      for i in chargeList:
        i.reset()
      for i in starList:
        i.reset()
      return True

  def collisionObstacle(self,opponent,obstacleList,chargeList,starList):
    #If the Tron collides with the obstacle, reset all of the objects
    for j in obstacleList:
        if self.segy[0]-j.y<j.size and self.segy[0]-j.y>0 and self.segx[0]-j.x<j.size and self.segx[0]-j.x>0:
          self.reset()
          opponent.reset()
          for i in obstacleList:
              i.reset()
          for i in chargeList:
            i.reset()
          for i in starList:
              i.reset()
          return True   

  def collisions(self,opponent,obstacleList,chargeList,starList):
    #Checks to see if the Tron collides with itself
    for j in range(1,len(self.segx)):
      #Checks the range between the front of the Tron trail and the previous rectangle to prevent Trons from going in between rectangles 
        for l in range(-self.BODYSIZE+1,self.BODYSIZE):
          for k in range(-self.BODYSIZE+1,self.BODYSIZE):
            
            if self.segy[0]+l==self.segy[j] and self.segx[0]+k == self.segx[j]:
              #Reset everything to default values
              self.reset()
              opponent.reset()
              for i in obstacleList:
                i.reset()
              for i in chargeList:
                i.reset()
              for i in starList:
                i.reset()
              return True
          #Checks to see if the Tron collides with the opponent, using the same logic as above
          for k in range(-opponent.BODYSIZE+1,opponent.BODYSIZE):
            if self.segy[0]+l==opponent.segy[j] and self.segx[0]+k == opponent.segx[j]: #Resets everything to default values
              self.reset()
              opponent.reset()
              for i in obstacleList:
                i.reset()
              for i in chargeList:
                i.reset()
              for i in starList:
                i.reset()
              return True
    
  def move(self,opponent,obstacleList,chargeList,starList):
    
    #Checks for collisions with a Star or a Charge
    self.collisionStar(starList)
    self.collisionCharge(chargeList)

    #Decreases speeds if they are above 3
    if self.HSPEED>3:
      self.HSPEED-=0.01
      self.VSPEED-=0.01

    if self.speedX<0:
      if self.speedX>=-3:
        self.speedX= -3
      else:
        self.speedX+=0.01
    if self.speedX>0:
      if self.speedX<=3: 
        self.speedX=3
      else:
        self.speedX-=0.01
   
    if self.speedY<0:
      if self.speedY>=-3:
        self.speedY= -3
      else:
        self.speedY+=0.01
    if self.speedY>0:
      if self.speedY<=3: 
        self.speedY=3
      else:
        self.speedY-=0.01

    #Shifts all of the coordinates backwards by 1 and updates the current position of the Tron.
    for i in range(len(self.segx)-1,0,-1):
        self.segx[i]=self.segx[i-1]       
        self.segy[i]=self.segy[i-1] 
    self.segx[0] += self.speedX
    self.segy[0] += self.speedY
    self.segx[0] = round(self.segx[0])
    self.segy[0] = round(self.segy[0])

    #Checks if Tron collids with the walls
    if self.collisionWall(opponent,obstacleList,chargeList,starList):
      return -1

    #Checks if the Tron collided with an obstacle, the opponent, or itself (as long as there is no star ability active - invincible = False
    if not self.invincible:  
      if self.collisionObstacle(opponent,obstacleList,chargeList,starList):
        return -1
      if self.collisions(opponent,obstacleList,chargeList,starList):
        return -1      
    return 0

  def reset(self):
    #Resets the Tron to its default settings
    self.BODYSIZE = 3
    self.HSPEED = 3
    self.VSPEED = 3
    self.speedX = self.HSPEED*self.direction
    self.speedY = 0
    self.segx = [(400-self.speedX*100), (400-self.speedX*100)-self.speedX, (400-self.speedX*100)-2*self.speedX]
    self.segy = [HEIGHT//2]*3
    self.invincible=False
    if self.speedX<0:  
      self.CLR = BLUE
    else:
      self.CLR = YELLOW

#---------------------------------------#
# function that redraws all objects     
#---------------------------------------#
      

#---------------------------------------#
# Obstacle, Charge, and Star properties #                    
#---------------------------------------#

class Obstacle():
  def __init__(self):
    self.x = randint(0,WIDTH)
    self.y=HEIGHT//2
    while HEIGHT//2-self.y<30 and HEIGHT//2-self.y>=0:   
      self.y = randint(0,HEIGHT)
    self.size = 30
  def drawObstacle(self):
    screen.blit(obstacle,(self.x,self.y))
  def reset(self):
    self.x = randint(0,WIDTH)
    while HEIGHT//2-self.y<30 and HEIGHT//2-self.y>=0:   
      self.y = randint(0,HEIGHT)
    self.size = 30    
class Charge():
  def __init__(self):
    self.x = randrange(20,WIDTH-20)
    self.y = randrange(20,HEIGHT-20)
    self.size = randint(25,35)
    self.image = pygame.transform.scale(charge, (self.size,self.size))
    self.visible = True
  def drawCharge(self):
    screen.blit(self.image,(self.x,self.y))
  def reset(self):
    self.x = randint(0,WIDTH)
    self.y = randint(0,HEIGHT)
    self.size=randint(25,40)
    self.image = pygame.transform.scale(charge, (self.size,self.size))
    self.visible=True
class Star():
  def __init__(self):
    self.x = randrange(20,WIDTH-20)
    self.y = randrange(20,HEIGHT-20)
    self.size = 30
    self.visible = True
  def drawStar(self):
    screen.blit(star,(self.x,self.y))
  def reset(self):
    self.x = randint(0,WIDTH)
    self.y = randint(0,HEIGHT)
    self.size = 30   
    self.visible=True

#---------------------------------------#
# Functions                             # 
#---------------------------------------#

def redrawScreen(player1, player2, time,obstacleList,chargeList,starList):
  #Redraws the background
  screen.blit(background,(0,0))
  #Extends each of the players, and draws them
  player1.extend()
  player1.drawPlayer(temp1)
  player2.extend()
  player2.drawPlayer(temp2)
  for i in obstacleList:
    i.drawObstacle()
  for i in chargeList:
    if i.visible:
      i.drawCharge()
  for i in starList:
    if i.visible:
      i.drawStar()
  
  player1.lives += player1.move(player2,obstacleList,chargeList,starList)
  player2.lives += player2.move(player1,obstacleList,chargeList,starList)
  text = font.render("Timer: "+str(time), 1, WHITE)
  screen.blit(text,(0, 0))
  text = font.render("Player 1: "+ str(player1.lives),1,BLUE)
  screen.blit(text,(600,0))
  text = font.render("Player 2: "+ str(player2.lives),1,YELLOW)
  screen.blit(text,(200,0))
  text = font.render(" -    LIVES REMAINING    - ",1,WHITE)
  screen.blit(text,(325,0))
  #Converts the speed into a charge based on a scale between 0-100
  text = font.render("Charge: " + str(round(abs(player1.speedX+player1.speedY)*50-150)),1,BLUE)
  screen.blit(text,(600,50))
  text = font.render("Charge: " + str(round(abs(player2.speedX+player2.speedY)*50-150)),1,YELLOW)
  screen.blit(text,(200,50))

def startGameScreen():
  #Display the start screen
  font = pygame.font.SysFont("Ariel Black",30)
  screen.blit(introBackground,(0,0))
  screen.blit(tronLogo,(300,95))
  startTxt=font.render('Controls: ',2,WHITE)
  screen.blit(startTxt,(100,200))
  startTxt=font.render('Player 2: ARROWS',2,YELLOW)
  screen.blit(startTxt,(100,250))
  startTxt=font.render('Player 1: WASD',2,BLUE)
  screen.blit(startTxt,(350,250))
  startTxt=font.render('Instructions: ',2,WHITE)
  screen.blit(startTxt,(100,300))
  font = pygame.font.SysFont("Ariel Black",23)
  startTxt=font.render('Each Player has 7 lives. The first person to lose all of their lives loses! Going outside of the',2,WHITE)
  screen.blit(startTxt,(100,350))
  startTxt=font.render('screen or colliding with yourself subtracts one life. Colliding with the opposite player also',2,WHITE)
  screen.blit(startTxt,(100,375))
  startTxt=font.render('loses you a life. BEWARE of obstacles, if collided with, you lose a life. Charging stations are',2,WHITE)
  screen.blit(startTxt,(100,400))
  startTxt=font.render('scattered around to give a speed boost. The bigger the charging station, the larger the boost!',2,WHITE)
  screen.blit(startTxt,(100,425))
  startTxt=font.render('Stars are also scattered to give invincibility for 10 seconds! Trap your opponent to get the win!!!',2,WHITE)
  screen.blit(startTxt,(100,450))
  font = pygame.font.SysFont("Ariel Black",30)
  startTxt=font.render('Press SPACE to Start the Game',2,WHITE)
  screen.blit(startTxt,(295,500))
  pygame.display.update()

def endGameScreen(winner,loser,name):
  #Display the end game screen
  screen.fill(RED)
  endTxt=font.render('GAME OVER',1,WHITE)            
  screen.blit(endTxt,(350,250))
  endTxt=font.render(name + " won with " + str(winner.lives) + " lives remaining!!",1,WHITE)  
  screen.blit(endTxt,(250,300))
  pygame.display.update()

#---------------------------------------#
# the main program begins here          
#---------------------------------------#
#Play the music
pygame.mixer.music.play(loops=-1)
#Initialize the two players, 7 obstacles, 5 charges, and 2 stars, and put them into their own lists for easy access
playerList = []
playerList.append(Player())
playerList.append(Player(YELLOW,1,1))
obstacleList = []
for i in range(7):
  obstacleList.append(Obstacle())
chargeList=[]
for i in range(5):
  chargeList.append(Charge())
introScreen = True
starList=[]
for i in range(2):
  starList.append(Star())

#Display the intro screen while the space bar has not been pressed
while introScreen:
  for event in pygame.event.get():    
          if event.type == pygame.QUIT:    
                   introScreen = False
  keys = pygame.key.get_pressed()
  if keys[pygame.K_SPACE]:             # Starts game if space key is pressed
    introScreen = False               
  startGameScreen()

#While each player still has lives, run the game screen
while playerList[0].lives>0 and playerList[1].lives>0:
# check for events
    for event in pygame.event.get():         # check for any events
        if event.type == pygame.QUIT:       # If user clicked close
            playerList[0].lives =0                           # Flag that we are done so we exit this loop

        #Depending on the key, the player's corresponding function to the key is called, and the image to be displayed is updated. Ensures player can't go backwards
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and playerList[0].speedY !=0:
            playerList[0].moveLeft()
            temp1 = car1Left       
        if keys[pygame.K_RIGHT] and playerList[0].speedY !=0:
            playerList[0].moveRight()
            temp1 = car1Right  
        if keys[pygame.K_UP] and playerList[0].speedX !=0:
            playerList[0].moveUp()
            temp1 = car1Up        
        if keys[pygame.K_DOWN] and playerList[0].speedX !=0:
            playerList[0].moveDown()
            temp1 = car1Down
        if keys[pygame.K_a] and playerList[1].speedY !=0:
            playerList[1].moveLeft()
            temp2 = car2Left      
        if keys[pygame.K_d] and playerList[1].speedY !=0:
            playerList[1].moveRight()
            temp2 = car2Right 
        if keys[pygame.K_w] and playerList[1].speedX !=0:
            playerList[1].moveUp()
            temp2 = car2Up           
        if keys[pygame.K_s] and playerList[1].speedX !=0:
            playerList[1].moveDown()
            temp2 = car2Down

    time=round(pygame.time.get_ticks()/1000,1)  #Keeps track of how long the players have been playing for
    redrawScreen(playerList[0],playerList[1],time,obstacleList,chargeList,starList)
    pygame.time.delay(10)
    pygame.display.update()  # update the screen

#Display game over screen
gameOver=True
while gameOver:
  for event in pygame.event.get():    
        if event.type == pygame.QUIT:       
                 gameOver = False                # To exit gameOver screen
  if playerList[1].lives == 0:
    endGameScreen(playerList[0], playerList[1], "Player 1")
  if playerList[0].lives == 0:
    endGameScreen(playerList[1], playerList[0], "Player 2")
  pygame.time.delay(100)

pygame.mixer.music.stop()
pygame.quit()