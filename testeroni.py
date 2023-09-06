#!/usr/bin/env python3
import pygame, sys
from pygame.locals import *
from math import sin, cos, tan, radians, atan, degrees, sqrt
pygame.init()
origin = pygame.math.Vector2(200,200)
t = pygame.time.Clock()
font = pygame.font.SysFont('Courier New', 14, True, False)
pygame.display.set_caption('Hello World!')
DISPLAYSURF = pygame.display.set_mode((400, 400))

def mag(deg):
    return (450 - deg) % 360

FPS = 60
TIMERATE = 10
ihdg = mag(30)
hdg = (ihdg + 180) % 360

ibrg = 120
brg = (ibrg % 360)

icrs = 216
crs = (icrs % 360)

rang = 21
speed = 282

crs_dev = (crs ) - (brg)
OWN_AC = [0, 390]
def mag(deg):
    return (450 - compassDegrees) % 360

def tick_from_angle(th, l):
    a = th
    vec1 = pygame.math.Vector2.from_polar((150 -l,a))+pygame.math.Vector2(200, 200)
    vec2 = pygame.math.Vector2.from_polar((150, a))+pygame.math.Vector2(200,200)
    return (vec1, vec2)

labels = ['N', '3', '6', 'E', '12', '15', 'S', '21', '24', 'W', '30', '33']
crs = 0
while True:
    tick = tick_from_angle(crs, 20 )
    DISPLAYSURF.fill((0,0,0,))
    pygame.draw.circle(DISPLAYSURF, (0,255,0), OWN_AC, 20)
    pygame.draw.aaline(DISPLAYSURF, (0,255,0), tick[0], tick[1])
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEWHEEL:
           crs += [-1, 1][event.y > 0] * 1
    pygame.display.update()
    t.tick(FPS)
