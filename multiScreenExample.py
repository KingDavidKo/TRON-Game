import pygame
import random
pygame.init()

HEIGHT = 600
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))
font=pygame.font.SysFont('Ariel Black',60)    #Resize the current font
    
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED =(255,0,0)
GREEN =(0,255,0)
YELLOW = (255,255,0)
ORANGE = (255, 102, 0)
BLUE = (0,0,255)
BROWN = (26, 9, 0)

########################## FUNCTIONS #####################################

def endGameScreen():
         screen.fill(BROWN)
         endTxt=font.render('GAME OVER',1,YELLOW)            
         screen.blit(endTxt,(20,150))
         pygame.display.update()

def startGameScreen():
         screen.fill(ORANGE)
         startTxt=font.render('Press SPACE to Start the Game ',1,BLUE)            
         screen.blit(startTxt,(10,150))
         pygame.display.update()


def redraw():
         screen.fill(RED)
         gameTxt=font.render('GAME ON Click the mouse to exit',1,BLACK)            
         screen.blit(gameTxt,(10,150))
         pygame.display.update()
         

######################## INTRO & INSTRUCTION SECTION ##########################
introScreen = True
while introScreen:
         for event in pygame.event.get():    
                  if event.type == pygame.QUIT:    
                           introScreen = False
       
         keys = pygame.key.get_pressed()
         if keys[pygame.K_SPACE]:             # Starts game if space key is pressed
                  introScreen = False
                     
         startGameScreen()

######################## MAIN GAME SECTION ##############################

inPlay = True                                                      # mainLoopBoolean       
while inPlay:                                                       # While loop for while game is in progress
                                            
         for event in pygame.event.get():    
                  if event.type == pygame.QUIT:    
                           inPlay = False

                  if event.type == pygame.MOUSEBUTTONDOWN:  # end game when the mouse is clicked
                           gameOver=True              
                           inPlay = False
         redraw()
         pygame.time.delay(60)
         
####################### GAMER OVER SECTION ###############################
while gameOver:
         for event in pygame.event.get():    
                  if event.type == pygame.QUIT:       
                           gameOver = False                # To exit gameOver screen

         endGameScreen()
         pygame.time.delay(60)
         
pygame.quit() 
