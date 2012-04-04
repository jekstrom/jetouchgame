import sys
import time

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
    
    def __init__(self, initial_pos, sd):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = initial_pos
        self.originalImage = self.image.copy()
        self.sd = sd
    
    def update(self, ship):
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
