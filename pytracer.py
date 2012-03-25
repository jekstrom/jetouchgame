#!/usr/bin/env python

import sys
import random
from math import *
import cProfile

import pygame
from touch import *
import utils

screen_dimensions = (640, 480)

pygame.init()
screen = pygame.display.set_mode(screen_dimensions, pygame.HWSURFACE)
clock = pygame.time.Clock()

player1Score = 0
player2Score = 0

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

#Player labels
font = pygame.font.Font(None, 36)
text_player1 = font.render("Player 1", 1, (255, 255, 255))
textpos1 = text_player1.get_rect(centerx=50)
text_player2 = font.render("Player 2", 1, (255, 255, 255))
textpos2 = text_player2.get_rect(centerx=background.get_width()-50)

#Player score
text_player1Score = font.render(str(player1Score), 1, (255,255,255))
text_player2Score = font.render(str(player2Score), 1, (255,255,255))

#player paddles
player1rect = pygame.Rect(0, screen_dimensions[1]/2-20, 10, 40)
player2rect = pygame.Rect(screen_dimensions[0]-10, screen_dimensions[1]/2-20, 10, 40)

#ball coords
ballrect = pygame.Rect(screen_dimensions[0]/2, screen_dimensions[1]/2, 10, 10)

class Ball():
    vector = [0,0]
    vx = vector[0]
    vy = vector[1]
    pos = [screen_dimensions[0]/2,screen_dimensions[1]/2]
    x = pos[0]
    y = pos[1]

ball = Ball()

def serve_ball():
    ball.x = screen_dimensions[0] / 2
    ball.y = screen_dimensions[1] / 2
    ball.vx = 4
    ball.vy = 0

def move_ball():
    ball.x += ball.vx
    ball.y += ball.vy

def make_rectlist(pos, size):
    return (pos, (pos[0] + size, pos[1]), (pos[0] + size, pos[1] + size), (pos[0], pos[1] + size))

def get_distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

t = touchpy()
sz = utils.get_sz()
pos = []
size = 100
blist = []

@t.event
def TOUCH_UP(blobID, xpos, ypos):
    global blist
    blist.remove(t.blobs[blobID])

@t.event                              
def TOUCH_DOWN(blobID):
    global blist
    blist.append(t.blobs[blobID])

#@t.event
#def TOUCH_MOVE(blobID):
#    global blist, sz, size
#    pos[0] += t.blobs[blobID].xmot*sz[0]
#    pos[1] += t.blobs[blobID].ymot*sz[1]
                             

serve_ball()
################################################################################
#
#MAIN GAME LOOP
#
################################################################################
#def main():
mouse = [0, 0, 0]
while 1:
    clock.tick(60)
    #screen.fill((0, 0, 0))
    background.fill((0,0,0))
    t.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and \
                                             event.key == pygame.K_ESCAPE):
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse[2] = 1
            mouse[0] = event.pos[0]
            mouse[1] = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse[2] = 0
            mouse[0] = event.pos[0]
            mouse[1] = event.pos[1]
        elif event.type == pygame.MOUSEMOTION:
            mouse[0] = event.pos[0]
            mouse[1] = event.pos[1]
        
    if mouse[2] == 1:
        if mouse[0] < screen_dimensions[0] / 2:
            player1rect.centerx = 5
            player1rect.centery = mouse[1]
        else:
            player2rect.centerx = screen_dimensions[0] - 5
            player2rect.centery = mouse[1]

    background.blit(text_player1, textpos1)
    background.blit(text_player2, textpos2)
    background.blit(text_player2Score, (screen_dimensions[0]-50, screen_dimensions[1]-50))
    background.blit(text_player1Score, (50, screen_dimensions[1]-50))

    pygame.draw.circle(background, (100,0,0), (ball.x, ball.y), 10)
    
    player1 = pygame.draw.rect(background, (0,0,200), player1rect)
    player2 = pygame.draw.rect(background, (200,0,0), player2rect)  
    
    move_ball()
    
    #Detect collisions
    if (ball.y+10 < 0) or (ball.y+10 > screen_dimensions[1]):
        ball.vy *= -1
    if (player1rect.collidepoint(ball.x-10, ball.y)):
        offset = (ball.y - player1rect.centery)/(player1rect.height/2)
        bounced = (-1*ball.vx, ball.vy)
        vel = bounced[0] * 1.1, bounced[1] * 1.1
        ball.vx = vel[0]
        ball.vy = vel[1] + offset
    if (player2rect.collidepoint(ball.x+10, ball.y)):
        offset = (ball.y - player2rect.centery)/(player2rect.height/2)
        bounced = (-1*ball.vx, ball.vy)
        vel = bounced[0] * 1.1, bounced[1] * 1.1
        ball.vx = vel[0]
        ball.vy = vel[1] + offset
    elif ball.x < 0:
        player2Score += 1
        text_player2Score = font.render(str(player2Score), 1, (255,255,255))
        serve_ball()
    elif ball.x > screen_dimensions[0]:
        player1Score += 1
        text_player1Score = font.render(str(player1Score), 1, (255,255,255))
        serve_ball()

    for blobid in blist:
         x = int(round(blobid.xpos * screen_dimensions[0]))
         y = int(round(blobid.ypos * screen_dimensions[1]))
 
         if x < screen_dimensions[0]/2:
            #player1rect = pygame.Rect(0, y, 10, 40)
             player1rect.centerx = 5
             player1rect.centery = y
         else:
            #player2rect = pygame.Rect(screen_dimensions[0]-10, y, 10, 40)
             player2rect.centerx = screen_dimensions[0] - 5
             player2rect.centery = y
        
    #print clock.get_fps()
    screen.blit(background, (0,0))
    pygame.display.flip()
    

#cProfile.run('main()')

