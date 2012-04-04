#!/usr/bin/evn python
import sys
import time

from touch import *
import pygame
from pygame.locals import *
import utils

from animatedshipsprite import *
from bombsprite import *
from shipsprite import *

#Screen dimensions
sd = (800, 600)

clock = pygame.time.Clock()
clock_s = 0

#Set up touchpy stuff
t = touchpy()

#Initialize pygame
pygame.init()

sz = utils.get_sz()

#keeps track of mouse or blob coordinates (x and y) and whether a blob has been touched down or the mouse1 has been pressed
pos = [0, 0, 0]
size = 100
blist = []

#player score
score = 0

ship = ShipSprite([sd[0]/2,sd[1]/2], pos)

class Observer(object):
    def __init__(self, subject):
        subject.push_handlers(self)

laser_pos = [0,0]
shoot_laser = False

class touch_up(Observer):
    def TOUCH_UP(self,blobID, xpos, ypos):
        x = int(round(t.blobs[blobID].xpos * sd[0]))
        y = int(round(t.blobs[blobID].ypos * sd[1]))
        global shoot_laser
        ship.MOVING = False
        if shoot_laser == True:
            shoot_laser = False
            #clock_s = 0
        pos[2] = 0

class touch_down(Observer):
    def TOUCH_DOWN(self,blobID):
        if pos[2] == 1:
            #Already have a blob touch-down somewhere driving the ship
            #Get pos of this blob
            x = int(round(t.blobs[blobID].xpos * sd[0]))
            y = int(round(t.blobs[blobID].ypos * sd[1]))

            laser_pos[0] = x
            laser_pos[1] = y

            global shoot_laser
            shoot_laser = True
            global clock_s
            clock_s = time.time() + .5
            pos[2] = 0

        #x = int(round(t.blobs[blobID].xpos * sd[0]))
        #y = int(round(t.blobs[blobID].ypos * sd[1]))
        pos[2] = 1

class touch_move(Observer):
    def TOUCH_MOVE(self,blobID):
        posx = int(round(t.blobs[blobID].xpos * sd[0]))
        posy = int(round(t.blobs[blobID].ypos * sd[1]))
        shipx = ship.rect.centerx
        shipy = ship.rect.centery
        moveVector = (posx - shipx, posy - shipy)
        degrees = (math.degrees(\
                math.atan2(-1*moveVector[0], -1*moveVector[1])))
        ship.turn(degrees)
        ship.MOVING = True
        #boxes.update(pygame.time.get_ticks(), (posx, posy))
        pos[0] = posx
        pos[1] = posy

tu = touch_up(t)
td = touch_down(t)
tm = touch_move(t)
       
def endGame():
    if pygame.font:
        font = pygame.font.Font(None,50)
        gameOver = font.render("GAME OVER", 1, (255,0,0))
        font = pygame.font.Font(None, 36)
        scoreText = font.render("Score: ", 1, (255,0,0))
        global score
        scorePoints = font.render(str(score), 1, (255,0,0))
        pygame.draw.rect(background, (0,0,0), (text.get_rect().top, 0, text.get_rect().centerx + 75, 30))
        screen.blit(gameOver, (sd[0]/2 - gameOver.get_rect().centerx, sd[1]/2))
        screen.blit(scoreText, (sd[0]/2 - scoreText.get_rect().centerx, sd[1]/2 + 55))
        screen.blit(scorePoints, (sd[0]/2 - scorePoints.get_rect().centerx + 55, sd[1]/2 + 55))
    for bomb in bombs:
        bomb.kill()

boxes = RenderUpdates()

bombs = RenderUpdates()

for location in [[sd[0]/2, sd[1]/2]]:
   boxes.add(ship)

for y in range (0, sd[1] + 50, 50):
    for location in [[0, y]]:
        bomb = BombSprite(location, sd)
        bombs.add(bomb)

screen = pygame.display.set_mode(sd, pygame.HWSURFACE)
background = pygame.image.load("background.jpg")

pygame.display.update()
i=0
while True:
    t.update()

    #screen.fill([0,0,0])
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and \
                                             event.key == pygame.K_ESCAPE):
            sys.exit()          

    if len(boxes) == 0:
        endGame()

    boxes.update(pygame.time.get_ticks(), pos)
    bombs.update(ship)

    clock.tick(50)
    #boxes.clear(screen, background)
    #bombs.clear(screen, background)

    rectlist = boxes.draw(screen)
    rectlist2 = bombs.draw(screen)

    pygame.display.update(rectlist)
    pygame.display.update(rectlist2)
    
    if shoot_laser == True and clock_s >= time.time() and clock_s != 0 and len(boxes) != 0:
        pygame.draw.line(screen, (0,200,0), laser_pos, (ship.getX(), ship.getY()))
        for bomb in bombs:
            #Distance of the laserbeam (from ship center to line end
            #d = math.sqrt(math.pow(ship.getX()-laser_pos[0],2) + math.pow(ship.getY()-laser_pos[1],2))
            a = math.pow(ship.getX() - laser_pos[0],2) + math.pow(ship.getY() - laser_pos[1],2)
            b = 2 * ((ship.getX() - laser_pos[0]) * (laser_pos[0] - bomb.getX()) +\
                         (ship.getY() - laser_pos[1]) * (laser_pos[1] - bomb.getY()))

            c = (math.pow(bomb.getX(),2) + math.pow(bomb.getY(),2) + math.pow(laser_pos[0],2) +\
                     math.pow(laser_pos[1],2) - 2 * (bomb.getX() * laser_pos[0] + bomb.getY() * laser_pos[1]) -\
                     math.pow(bomb.getR(),2))

            i = b * b - 4.0 * a * c
            if i < 0.0:
                pass #no intersections
            elif i > 0:
            #There is an intersection
                #Make sure that the laser beam does not end before the bomb...
                if laser_pos[0] < bomb.getX() and ship.getX() < bomb.getX():
                    pass
                elif laser_pos[1] < bomb.getY() and ship.getY() < bomb.getY():
                    pass
                elif laser_pos[0] > bomb.getX() and ship.getX() > bomb.getX():
                    pass
                elif laser_pos[1] > bomb.getY() and ship.getY() > bomb.getY():
                    pass
                else:
                    #the laser beam cuts across the bomb, destroy it.
                    bomb.kill()
                    score += 1
    else:
        shoot_laser = False

    #render score
    if pygame.font:
        font = pygame.font.Font(None,36)
        text = font.render("Score: ", 1, (0,0,255))
        global score
        textScore = font.render(str(score), 1, (0,0,255))
        pygame.draw.rect(background, (0,0,0), (text.get_rect().top, 0, text.get_rect().centerx + 75, 30))
        screen.blit(text, (0,0))
        screen.blit(textScore, (text.get_rect().centerx + 50, 0))

     

    pygame.display.flip()
