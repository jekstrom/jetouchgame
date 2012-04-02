#!/usr/bin/evn python
import sys
import time

from touch import *
import pygame
from pygame.locals import *
import utils
from dirty import *
from oru import *
from animatedshipsprite import *

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

images = (pygame.image.load("spaceship1.png"), pygame.image.load("spaceship2.png"), pygame.image.load("spaceship3.png"))

class ShipSprite(AnimatedShipSprite, pygame.sprite.Sprite):
    image = None

    def __init__(self, initial_pos, mouse, sd):
        AnimatedShipSprite.__init__(self, images, pos)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = initial_pos

ship = ShipSprite([sd[0]/2,sd[1]/2], pos, sd)

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
       
bombImage = (pygame.image.load("bomb.png"))

class BombSprite(pygame.sprite.Sprite):
    image = bombImage
    
    def __init__(self, initial_pos, sd):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = initial_pos
        self.originalImage = self.image.copy()
        self.sd = sd
    
    def update(self, rotation):
        self.rect.centerx += 1
        #self.image = pygame.transform.rotate(self.originalImage, rotation)
        #self.rect.size = self.image.get_rect().size
        if self.rect.centerx == self.sd[0]:
            self.rect.centerx = 0
            
        #See if a bomb collides with the ship.
        if self.rect.colliderect(ship.rect):
            ship.kill()

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery

    def getR(self):
        return self.rect.w 

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

    boxes.update(pygame.time.get_ticks(), pos)
    i += 1
    if i > 60:
        i = 0
    bombs.update(i)

    clock.tick(50)
    #boxes.clear(screen, background)
    #bombs.clear(screen, background)

    rectlist = boxes.draw(screen)
    rectlist2 = bombs.draw(screen)

    pygame.display.update(rectlist)
    pygame.display.update(rectlist2)
    
    if shoot_laser == True and clock_s >= time.time() and clock_s != 0:
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
