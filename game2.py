#!/usr/bin/evn python
import sys

from touch import *
import pygame
from pygame.locals import KEYDOWN
import utils
from dirty import *
from oru import *
from animatedshipsprite import *

#Screen dimensions
sd = (800, 600)

clock = pygame.time.Clock()

#Set up touchpy stuff
t = touchpy()

#Initialize pygame
pygame.init()

sz = utils.get_sz()

#keeps track of mouse or blob coordinates (x and y) and whether a blob has been touched down or the mouse1 has been pressed
pos = [0, 0, 0]
size = 100
blist = []

mouseO = [0, 0, 0]

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
        pos[2] = 0

class touch_down(Observer):
    def TOUCH_DOWN(self,blobID):
        if pos[2] == 1:
            #Already have a blob touch-down somewhere driving the ship
            #Get pos of this blob
            x = int(round(t.blobs[blobID].xpos * sd[0]))
            y = int(round(t.blobs[blobID].ypos * sd[1]))

            print "shipx = ", ship.getX()
            print "shipy = ", ship.getY()
            print "x = ", x
            print "y = ", y
            d = math.sqrt(math.pow(ship.getX()-laser_pos[0],2) + math.pow(ship.getY()-laser_pos[1],2))
            #Direction vector from laserbeam center to end
            dx = (ship.getX() - laser_pos[0])/d
            dy = (ship.getY() - laser_pos[1])/d

            if (dx > 100):
                if x > ship.getX():
                    x = ship.getX() + 100
                else:
                    x = ship.getX() - 100
            if (dy > 100):
                if y > ship.getY():                
                    y = ship.getY() + 100
                else:
                    y = ship.getY() - 100

            laser_pos[0] = x
            laser_pos[1] = y

            global shoot_laser
            shoot_laser = True

        x = int(round(t.blobs[blobID].xpos * sd[0]))
        y = int(round(t.blobs[blobID].ypos * sd[1]))
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
        self.image = pygame.transform.rotate(self.originalImage, rotation)
        self.rect.size = self.image.get_rect().size
        if self.rect.centerx == self.sd[0]:
            self.rect.centerx = 0

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos[2] = 1
            pos[0] = event.pos[0]
            pos[1] = event.pos[1]

            x = ship.rect.centerx
            y = ship.rect.centery

            moveVector = (pos[0]-x, pos[1]-y)
            degrees = (math.degrees(\
                    math.atan2(-1*moveVector[0], -1*moveVector[1])))
            ship.turn(degrees)
            ship.MOVING = True

        if event.type == pygame.MOUSEBUTTONUP:
            pos[2] = 0
            ship.MOVING = False

        elif event.type == pygame.MOUSEMOTION and pos[2] == 1:
            pos[0] = event.pos[0]
            pos[1] = event.pos[1]

            x = ship.rect.centerx
            y = ship.rect.centery

            moveVector = (pos[0]-x, pos[1]-y)
            degrees = (math.degrees(\
                    math.atan2(-1*moveVector[0], -1*moveVector[1])))

            ship.turn(degrees)            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.turn(10)
            elif event.key == pygame.K_RIGHT:
                ship.turn(-10)

    boxes.update(pygame.time.get_ticks(), pos)
    i += 1
    if (i >= 360):
        i = 0
    bombs.update(i)

    rectlist = boxes.draw(screen)
    rectlist2 = bombs.draw(screen)

    pygame.display.update(rectlist)
    pygame.display.update(rectlist2)

    clock.tick(60)
    #boxes.clear(screen, background)
    #bombs.clear(screen, background)

    #only draw a line for 30 frames.
    if i % 30 != 0 and shoot_laser == True:
        pygame.draw.line(screen, (255,0,0), laser_pos, (ship.getX(), ship.getY()))
        for bomb in bombs:
            #Distance of the laserbeam (from ship center to line end
            d = math.sqrt(math.pow(ship.getX()-laser_pos[0],2) + math.pow(ship.getY()-laser_pos[1],2))
            #Direction vector from laserbeam center to end
            dx = (ship.getX() - laser_pos[0])/d
            dy = (ship.getY() - laser_pos[1])/d
            #closest point to the circle center
            closestPoint = dx*(bomb.getX() - laser_pos[0]) + dy*(bomb.getY() - laser_pos[1])
            ex = closestPoint * dx + laser_pos[0]
            ey = closestPoint * dy + laser_pos[1]
            de = math.sqrt( math.pow(ex - bomb.getX(), 2) + math.pow(ey - bomb.getY(), 2) )
            #Check if the line intersects the bomb
            if (de < bomb.getR()):
                bomb.kill()

    else:
        global shoot_laser
        shoot_laser = False

    pygame.display.flip()
