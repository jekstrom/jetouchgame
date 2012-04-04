import sys

from touch import *
import pygame
from pygame.locals import *

from animatedshipsprite import *

images = (pygame.image.load("spaceship1.png"), pygame.image.load("spaceship2.png"), pygame.image.load("spaceship3.png"))

class ShipSprite(AnimatedShipSprite, pygame.sprite.Sprite):
    image = None

    def __init__(self, initial_pos, pos):
        AnimatedShipSprite.__init__(self, images, pos)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = initial_pos
