import sys

from touch import *
import pygame
from pygame.locals import *

class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('button.png', -1)

    def setCoords(self, pos):
        self.rect.topleft = pos

    def isPressed(self, pos):
        if pos[0] > self.rect.topleft[0]:
            if pos[1] > self.rect.topleft[1]:
                if pos[0] < self.rect.topleft[0]:
                    if pos[1] < self.rect.topleft[1]:
                        return true
                    else: return false
                else: return false
            else: return false
        else: return false

    
