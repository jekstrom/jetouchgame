#!/usr/bin/env python

import sys
import math

import pygame
from pygame.locals import *

from touch import *
import utils

def make_rectlist(pos, size):
    print pos
    print "\n"
    print pos[0]
    print "\n"
    print pos[1]
    print "\n"
    return (pos, (pos[0] + size, pos[1]), (pos[0] + size, pos[1] + size), (pos[0], pos[1] + size))

def get_distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

#screenSize = utils.get_sz()
screenSize = (1920, 1080)

pygame.init()
screen = pygame.display.set_mode(screenSize, pygame.DOUBLEBUF)

pos = [(x/2) - 50 for x in screenSize]
size = 100
blist = []

t = touchpy()

@t.event
def TOUCH_DOWN(blobID):
    global blist
    blist.append(t.blobs[blobID])

@t.event
def TOUCH_MOVE(blobID):
    global blist, screenSize, size
    if len(blist) == 1:
        pos[0] += int(round(t.blobs[blobID].xmot * (screenSize[0])))
        pos[1] += int(round(t.blobs[blobID].ymot * (screenSize[1])))

    elif len(blist) == 2:
        oDist = get_distance(blist[0].oxpos * screenSize[0], blist[1].oxpos * screenSize[0], blist[0].oypos * screenSize[1], blist[1].oypos * screenSize[1])

        cDist = get_distance(blist[0].xpos * screenSize[0], blist[1].xpos * screenSize[0], blist[0].ypos * screenSize[1], blist[1].ypos * screenSize[1])

        z = round(oDist / cDist, 1)
        if z >= .5:
            size /= z

@t.event
def TOUCH_UP(blobID, xpos, ypos):
    global blist
    blist.remove(t.blobs[blobID])

while 1:
    screen.fill((0, 0, 0))
    pygame.draw.aalines(screen, (0, 255, 0), True, make_rectlist(pos, size))
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        
    t.update()
    pygame.display.flip()
