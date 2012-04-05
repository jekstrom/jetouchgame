import sys
import time

from touch import *
import pygame
from pygame.locals import *
import utils

class Button(pygame.sprite.Sprite):
    def __init__(self, imageLoc1, imageLoc2):
        pygame.sprite.Sprite.__init__(self)
        
        self._images = (pygame.image.load(imageLoc1), pygame.image.load(imageLoc2))
        self.originalImage = self._images[0]
        self.image = self.originalImage.copy()
        self.rect = self.image.get_rect()

        self.clock = pygame.time.Clock()
        self.clock_d = 0
        self.clock_u = 0

    def setCoords(self, pos):
        self.rect.topleft = pos

    def isPressed(self, pos):
        if pos[0] > self.rect.topleft[0]:
            if pos[1] > self.rect.topleft[1]:
                if pos[0] < self.rect.bottomright[0]:
                    if pos[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
        
    def update(self, pos):
        buttonClicked = False
        if self.isPressed(pos):
            self.image = self._images[1]
            self.clock_d = time.time()
            buttonClicked = True
        else:
            self.image = self._images[0]
            self.clock_u = time.time()

        if self.clock_d - self.clock_u < 1.0 and buttonClicked and pos[2] != 2:
            #the button was pressed
            return True
        else:
            return False

    
