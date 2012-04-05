import sys
import time
import random
from math import sqrt

from touch import *
import pygame
from pygame.locals import *
import utils
from dirty import *
from oru import *
from animatedshipsprite import *

bombImage = (pygame.image.load("bomb.png"))

class BombSprite(pygame.sprite.Sprite):
    image = bombImage
    
    def __init__(self, initial_pos, sd, speed):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = initial_pos
        self.originalImage = self.image.copy()
        self.sd = sd

        x = random.random()*sd[1]
        y = random.random()*sd[0]
        dx = random.random()*sd[1] - x
        dy = random.random()*sd[0] - y

        if x >= 3*sd[1]/4:
            self.x_a = x + sd[0]/4 + 50
        elif x < 3*sd[1]/4 and x >= sd[1]/2:
            self.x_a = x + sd[1]/2 + 50
        elif x < sd[1]/2 and x >= sd[1]/4:
            self.x_a = x - sd[1]/2 - 50
        elif x < sd[1]/4:
            self.x_a = x - sd[1]/4 - 50
        if y >= sd[0]/2:
            self.y_a = y + sd[0]/2 + 50
        elif y < sd[0]/2:
            self.y_a = y - sd[0]/2 - 50

        d = sqrt(dx*dx + dy*dy)
        v = random.randrange(speed[0], speed[1])
        self.dx = dx*v/d
        self.dy = dy*v/d
    
    def update(self, ship):
        self.rect = self.rect.move(self.dx, self.dy)
        #self.image = pygame.transform.rotate(self.originalImage, rotation)
        #self.rect.size = self.image.get_rect().size
        if self.rect.centerx >= self.sd[0]:
            self.dx *= -1
        elif self.rect.centerx <= 0:
            self.dx *= -1
        elif self.rect.centery >= self.sd[1]:
            self.dy *= -1
        elif self.rect.centery <= 0:
            self.dy *= -1
            
        #See if a bomb collides with the ship.
        if self.rect.colliderect(ship.rect):
            ship.kill()

    def getX(self):
        return self.rect.centerx

    def getY(self):
        return self.rect.centery

    def getR(self):
        return self.rect.w 
