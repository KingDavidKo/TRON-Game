#########################################
# Programmer: Mrs. G
# Date: 4/05/2022
# File Name: tronTemplate.py
# Description: This program is a template for TRON Game.
#########################################

import pygame
pygame.init()

from random import randint, randrange

HEIGHT = 600
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))

WHITE = (255,255,255)
BLACK = (  0,  0,  0)
outline=0

#---------------------------------------#
# player's properties                    
#---------------------------------------#
BODYSIZE = 15
HSPEED = 10
VSPEED = 10

speedX = 0
speedY = -VSPEED
segx = [WIDTH//2]*3  # playerX is at segx[0]
segy = [HEIGHT, HEIGHT+VSPEED, HEIGHT+2*VSPEED]  # playerY is at segy[0]




#---------------------------------------#
# function that redraws all objects     
#---------------------------------------#
def redrawScreen():
    screen.fill(BLACK)
    
    for i in range(len(segx)):
        segmentCLR = (randint(0,255),randint(0,255),randint(0,255)) 
        pygame.draw.rect(screen, segmentCLR, (segx[i], segy[i], BODYSIZE,BODYSIZE), outline)
    pygame.display.update()             # display must be updated, in order to show the drawings

#---------------------------------------#
# the main program begins here          
#---------------------------------------#
inPlay = True
while inPlay:

# check for events
    for event in pygame.event.get():         # check for any events
        if event.type == pygame.QUIT:       # If user clicked close
            inPlay = False                              # Flag that we are done so we exit this loop


    keys = pygame.key.get_pressed() # act upon key events
    
    if keys[pygame.K_LEFT] and speedY !=0:
        speedX = -HSPEED
        speedY = 0
        
    if keys[pygame.K_RIGHT] and speedY !=0:
        speedX = HSPEED
        speedY = 0
        
    if keys[pygame.K_UP] and speedX !=0:
        speedX = 0
        speedY = -VSPEED
        
    if keys[pygame.K_DOWN] and speedX !=0:
        speedX = 0
        speedY = VSPEED
        
    if keys[pygame.K_SPACE]:       # if space bar is pressed, add a segment:
        segx.append(segx[-1])           # assign the same x and y coordinates
        segy.append(segy[-1])           # as those of the last segment

# move all segments
    for i in range(len(segx)-1,0,-1):   # start from the tail, and go backwards:
        segx[i]=segx[i-1]                     # every segment takes the coordinates of the previous one
        segy[i]=segy[i-1]                     

# move the player
    segx[0] = segx[0] + speedX
    segy[0] = segy[0] + speedY

# update the screen     
    redrawScreen()
    pygame.time.delay(90)
    
pygame.quit()                           
