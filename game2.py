#!/usr/bin/evn python
import sys

from touch import *
import pygame
from pygame.locals import KEYDOWN
import utils
from dirty import *
from oru import *
from animatedsprite import *

#Screen dimensions
sd = (640, 480)

clock = pygame.time.Clock()

#Set up touchpy stuff
t = touchpy()
sz = utils.get_sz()
pos = []
size = 100
blist = []

mouse = [0, 0, 0]
mouseO = [0, 0, 0]

images = ((pygame.image.load("spaceship2.png")), (pygame.image.load("spaceship2.png")))

class ShipSprite(AnimatedSprite, pygame.sprite.Sprite):
    image = None

    def __init__(self, initial_pos, mouse, sd):
        AnimatedSprite.__init__(self, images, mouse)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = initial_pos

pygame.init()

boxes = RenderUpdates()

ship = ShipSprite([sd[0]/2,sd[1]/2], mouse, sd)

for location in [[sd[0]/2, sd[1]/2]]:
   boxes.add(ship)

screen = pygame.display.set_mode(sd, pygame.HWSURFACE)
background = pygame.image.load("background.png")

screen.blit(background, (0,0))
pygame.display.update()
while True:
    #screen.fill([100,0,0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and \
                                             event.key == pygame.K_ESCAPE):
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse[2] = 1
            mouse[0] = event.pos[0]
            mouse[1] = event.pos[1]

            x = ship.rect.centerx
            y = ship.rect.centery

            moveVector = (mouse[0]-x, mouse[1]-y)
            degrees = (math.degrees(\
                    math.atan2(-1*moveVector[0], -1*moveVector[1])))

            ship.turn(degrees)
            ship.MOVING = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse[2] = 0
            ship.MOVING = False

        elif event.type == pygame.MOUSEMOTION and mouse[2] == 1:
            mouse[0] = event.pos[0]
            mouse[1] = event.pos[1]

            x = ship.rect.centerx
            y = ship.rect.centery

            moveVector = (mouse[0]-x, mouse[1]-y)
            degrees = (math.degrees(\
                    math.atan2(-1*moveVector[0], -1*moveVector[1])))

            ship.turn(degrees)            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.turn(10)
            elif event.key == pygame.K_RIGHT:
                ship.turn(-10)

    mouseO[0] = mouse[0]
    mouseO[1] = mouse[1] + 23
    mouseO[2] = mouse[2]

    boxes.update(pygame.time.get_ticks(), mouse)
    rectlist = boxes.draw(screen)
    pygame.display.update(rectlist)
    clock.tick(50)
    boxes.clear(screen, background)


    #pygame.display.flip()
