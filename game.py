#!/usr/bin/env python

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

#Set up pygame screen
pygame.init()

screen = pygame.display.set_mode(sd)
clock = pygame.time.Clock()

#background = pygame.Surface(screen.get_size())
#background = background.convert()
#background.fill((0, 0, 0))

#Set up touchpy stuff
t = touchpy()
sz = utils.get_sz()
pos = []
size = 100
blist = []

#Sprite test
class BallSprite(pygame.sprite.Sprite):
    image = None
    
    def __init__(self, initial_pos):
        pygame.sprite.Sprite.__init__(self)
        if (BallSprite.image is None):
            BallSprite.image = pygame.image.load("spaceship1.png")
        self.image = BallSprite.image.convert(BallSprite.image)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = initial_pos
        self.going_down = True # start going downwards
        self.next_update_time = 0 # update hasn't beeen called yet

    def update(self, current_time):
        #update every 10 ms
        if self.next_update_time < current_time:
            if self.rect.bottom == (sd[1] - 1):
                self.going_down = False
            elif self.rect.top == 0:
                self.going_down = True
            if self.going_down:
                self.rect.top += 1
            else:
                self.rect.top -= 1

            self.next_update_time = current_time + 10

boxes = pygame.sprite.RenderUpdates()
for location in [[0, 0], [60, 60], [120, 200]]:
    boxes.add(BallSprite(location))

background = pygame.Surface(sd)
background.fill([0,0,0])
screen.blit(background, [0,0])
while pygame.event.poll().type != KEYDOWN:
    boxes.update(pygame.time.get_ticks())
    rectlist = boxes.draw(screen)
    pygame.display.update(rectlist)
    pygame.time.delay(10)
    boxes.clear(screen, background)

# while 1:                         
#     clock.tick(60)              
#     #screen.fill((0, 0, 0))
#     background.fill((0,0,0))
#     t.update()
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and \ 
#                                              event.key == pygame.K_ESCAPE):
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             mouse[2] = 1
#             mouse[0] = event.pos[0]
#             mouse[1] = event.pos[1]
#         elif event.type == pygame.MOUSEBUTTONUP:
#             mouse[2] = 0
#             mouse[0] = event.pos[0]
#             mouse[1] = event.pos[1]
#         elif event.type == pygame.MOUSEMOTION:
#             mouse[0] = event.pos[0]
#             mouse[1] = event.pos[1]
        
#     if mouse[2] == 1:
#         if mouse[0] < sd[0] / 2:
            
#         else:
            


