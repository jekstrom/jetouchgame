import pygame
import math

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, mouse, sd = (640, 480), fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self._images = images
        self.originalImage = self._images[0]
        self.image = self.originalImage.copy()

        # Track the time we started and between updates
        # Then we can figure out when we have to switch the image
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.originalRect = self.originalImage.get_rect()
        self.rect = self.originalRect.copy()

        self.sd = sd
        self.mouse = mouse

        self.rotation = 0
        self.MOVING = False
        self.speed = 5
        # Call update to set our first image.
        self.update(pygame.time.get_ticks(), mouse)


    def update(self, t, mouse):
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images):
                self._frame = 0
            self.image = self._images[self._frame]
            self.originalImage = self.image
            self._last_update = t

        if self.rotation:
            self.image = pygame.transform.rotate(self.originalImage,\
                                         (self.rotation))
            self.rect.size = self.image.get_rect().size

        self.M_POSITION = (mouse[0], mouse[1])
            
        dx = self.M_POSITION[0] - self.rect.centerx
        dy = self.M_POSITION[1] - self.rect.centery

        self.d = math.sqrt(dx*dx + dy*dy)
        if (self.d > 20):
            self.dx_s = dx * self.speed / self.d
            self.dy_s = dy * self.speed / self.d

        if self.d > 20:
            if self.MOVING:
                self.rect.centerx += self.dx_s
                self.rect.centery += self.dy_s
                    
    def turn(self, amt):
        self.rotation = amt
