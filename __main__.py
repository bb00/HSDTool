#!/usr/bin/env python3
import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from pygame.locals import *
from math import sin, cos, tan, radians, atan, degrees, sqrt, atan2
pygame.init()
origin = pygame.math.Vector2(200,200)
t = pygame.time.Clock()
font = pygame.font.SysFont('Courier New', 14, True, False)
pygame.display.set_caption('Hello World!')
DISPLAYSURF = pygame.display.set_mode((400, 400))
def mag(deg):
    return (450 - deg) % 360
plt.ion()
fig = plt.axes(projection='polar')

fig= plt.figure()
FPS = 60
TIMERATE = 60

hdg = mag(270)
brg = mag(90)

icrs = 0
crs = (icrs % 360)

rang = 25
speed = 250

crs_dev = (crs ) - (brg)

def tick_from_angle(th, l):
    a = hdg + th + 180
    vec1 = pygame.math.Vector2.from_polar((150 -l,a))+pygame.math.Vector2(200, 200)
    vec2 = pygame.math.Vector2.from_polar((150, a))+pygame.math.Vector2(200,200)
    return (vec1, vec2)

targets = [[0, 12], [90, 180],[0, 25], [-90, 315],[0,7], [-90,360], [0,1.7],[90, 180], [0,4],[90,360],[0,4],[0,21]]
target_index = 0
disp = targets[0][1]
labels = ['N', '3', '6', 'E', '12', '15', 'S', '21', '24', 'W', '30', '33']
target = targets[target_index]
data = []
while True:
    xos,yos = (rang * f(radians(brg)) for f in (cos,sin))
    
    dx, dy = ((speed / (3600 * (FPS / TIMERATE)))  * f(radians(hdg)) for f in (cos, sin))
    brg = ((degrees(atan2(yos+dy,xos+dx))))

    rang = sqrt(((xos+dx) ** 2) + ((yos+dy)**2))
    plt.polar(atan2(yos+dy,xos+dx), rang, 'g.')
    data.append((radians(brg),rang))
    crs_dev = ((crs ) - (mag(brg)) + 180) % 360 - 180
    target_type = target[0]
    
    hdg_target_dev = (((target[1]) - mag(hdg))) % 360
    target_reached = [(abs(hdg_target_dev) < 0.01), (disp) < 0.1][target_type == 0]
    if not target_reached:
        if target_type != 0:
            dev_sign = (abs(hdg_target_dev)/hdg_target_dev)
            hdg += (target[0]/60) / (FPS / TIMERATE)
        else:
            disp -= (sqrt((dx**2)+(dy**2)))
    else:
        print("Target {0} reached".format(target_index))
        if target_index == len(targets) - 1:
            break
        else:
            target_index += 1
            target = targets[target_index]
            disp = target[1]
    crs %= 360
    
    crs_dev = (crs ) - (mag(brg))
    crs_dev = (crs_dev + 180) % 360 - 180
    crs_dev_reciprocal_agnostic = (crs_dev + 90) % 180 - 90
    
    
    tacan_brg = brg % 360
    DISPLAYSURF.fill((0,0,0,))
    for i in range(0, 360, 30):   
        s = font.render(labels[i // 30], True, (0,255,0))
        #s = pygame.transform.rotate(s, (hdg + i))
        ctr = s.get_rect(center=origin+pygame.math.Vector2.from_polar((140, (hdg + i + 180))))
        DISPLAYSURF.blit(s, ctr)

    s = font.render('RNG', True, (0,255,0))
    ctr = s.get_rect(center=pygame.math.Vector2.from_polar((50, 45)))
    DISPLAYSURF.blit(s, ctr)
    s = font.render('%05.1f' % rang, True, (0,255,0))
    ctr = s.get_rect(center=pygame.math.Vector2.from_polar((30, 20))+pygame.math.Vector2.from_polar((15, 90)))
    DISPLAYSURF.blit(s, ctr)

    s = font.render('CRS', True, (0,255,0))
    ctr = s.get_rect(center=pygame.math.Vector2(400,0)+pygame.math.Vector2.from_polar((30, 160)))
    DISPLAYSURF.blit(s, ctr)
    s = font.render('%d' % (crs), True, (0,255,0))
    ctr = s.get_rect(center=pygame.math.Vector2(400, 0)+pygame.math.Vector2.from_polar((30, 160))+pygame.math.Vector2.from_polar((15, 90)))
    DISPLAYSURF.blit(s, ctr)

    s = font.render('TCN', True, (0,255,0))
    ctr = s.get_rect(center=pygame.math.Vector2(400,0)+pygame.math.Vector2.from_polar((30, 160))+pygame.math.Vector2(-80, 0))
    DISPLAYSURF.blit(s, ctr)
    s = font.render('%0.06f' % (mag(brg + 180) ), True, (0,255,0))
    ctr = s.get_rect(center=pygame.math.Vector2(400, 0)+pygame.math.Vector2.from_polar((30, 160))+pygame.math.Vector2.from_polar((15, 90))+pygame.math.Vector2(-80, 0))
    DISPLAYSURF.blit(s, ctr)
#    pygame.draw.circle(DISPLAYSURF, (0, 255, 0,), (200, 200), 150, 2)
    for i in range(0, 360, 10):
        if i % 30 == 0:
           continue;
        tick = tick_from_angle(i , 20)
        pygame.draw.aaline(DISPLAYSURF, (0,255,0), tick[0], tick[1])
    for i in range(5, 360, 10):
        tick = tick_from_angle(i, 15)
        pygame.draw.aaline(DISPLAYSURF, (0,255,0), tick[0], tick[1])

    # TACAN BRG INDICATOR
    pygame.draw.aalines(DISPLAYSURF, (0, 128, 0), True, (
        origin+pygame.math.Vector2.from_polar((170, hdg + mag(brg))),
        origin+pygame.math.Vector2.from_polar((155, hdg + mag(brg)))+pygame.math.Vector2.from_polar((10, hdg + mag(brg) - 90)),
        origin+pygame.math.Vector2.from_polar((155, hdg + mag(brg)))+pygame.math.Vector2.from_polar((10, hdg + mag(brg) + 90))
        ) 
    )

    # TACAN BRG RECIPROCAL
    pygame.draw.line(DISPLAYSURF, (0, 255, 0), 
        origin+pygame.math.Vector2.from_polar((172, hdg + mag(brg) + 180)),
        origin+pygame.math.Vector2.from_polar((156, hdg + mag(brg) + 180)),
        
    )
    pygame.draw.aaline(
        DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((164, hdg + mag(brg) + 180))  + pygame.math.Vector2.from_polar((8, hdg + mag(brg) - 90 )),
        origin+pygame.math.Vector2.from_polar((164, hdg + mag(brg) + 180)) + pygame.math.Vector2.from_polar((8, hdg + mag(brg) + 90 )),
        
    )
    pygame.draw.line(DISPLAYSURF, (0,255,0),
        origin+pygame.math.Vector2(0, 20),
        origin+pygame.math.Vector2(0, -16)
    )
    pygame.draw.line(DISPLAYSURF, (0,255,0),
        origin+pygame.math.Vector2(16, 0),
        origin+pygame.math.Vector2(-16, 0)
    )
    pygame.draw.line(DISPLAYSURF, (0,255,0),
        origin+pygame.math.Vector2(-2, 18),
        origin+pygame.math.Vector2(2, 18)
    )
    # SET 1 OF WITNESS MARKS -- 12°
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs + 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs)),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs + 90))+pygame.math.Vector2.from_polar((16, hdg + crs)),2
    )
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs + 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs + 180)),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs + 90))+pygame.math.Vector2.from_polar((16,  hdg + crs + 180)),2
    )
    # SET 1 OF WITNESS MARKS -- 6°
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs+ 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs)),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs + 90))+pygame.math.Vector2.from_polar((16, hdg + crs)),2
    )
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs + 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs + 180)),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs + 90))+pygame.math.Vector2.from_polar((16, hdg + crs + 180)),2
    )

    # SET 2 OF WITNESS MARKS -- 12°
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs - 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs)),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs - 90))+pygame.math.Vector2.from_polar((16, hdg + crs)),
        2
    )
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs - 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs + 190)),
        origin+pygame.math.Vector2.from_polar((75, hdg + crs - 90))+pygame.math.Vector2.from_polar((16,  hdg + crs + 180)),
        2
    )
    # SET 2 OF WITNESS MARKS -- 6°
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs - 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs)),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs - 90))+pygame.math.Vector2.from_polar((16, hdg + crs)),
        2
    )
    pygame.draw.line(DISPLAYSURF, (0, 255, 0),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs - 90))+pygame.math.Vector2.from_polar((5.3, hdg + crs + 180)),
        origin+pygame.math.Vector2.from_polar((37.5, hdg + crs - 90))+pygame.math.Vector2.from_polar((16, hdg + crs + 180)),2
    )

    aaaa = abs(crs_dev)
    vtr_sign = [1, -1][abs(crs_dev) > 90]
    vtr_s2 = [1, -1][abs(crs_dev_reciprocal_agnostic) > 90]
    # Course Deviation Vector
    crs_dev_vtr = pygame.math.Vector2.from_polar(
        (
            (
             [abs(crs_dev_reciprocal_agnostic) / 12, 1][(abs(crs_dev_reciprocal_agnostic) / 12 > 1)] * 75
            ),
            (hdg+ crs + 180 + [-1, 1][((abs(crs_dev) == crs_dev))] * 90)
        )
    )
    
    pygame.draw.aalines(DISPLAYSURF, (0,255,0), False, (
                     origin+crs_dev_vtr+pygame.math.Vector2.from_polar((50, hdg+ crs + 90 + vtr_sign * 90)),
                     origin+crs_dev_vtr+pygame.math.Vector2.from_polar((50, hdg+ crs + 90 - vtr_sign * 90)),
                     origin+crs_dev_vtr+pygame.math.Vector2.from_polar((50, hdg+ crs + 90 - vtr_sign * 90))+pygame.math.Vector2.from_polar((10, hdg+ crs + 90 + vtr_sign * 90 + 30))
    )
    )
    pygame.draw.aalines(DISPLAYSURF, (0,255,0), False, (
                     origin+crs_dev_vtr+pygame.math.Vector2.from_polar((50, hdg+ crs + 90 + vtr_sign * 90)),
                     origin+crs_dev_vtr+pygame.math.Vector2.from_polar((50, hdg+ crs + 90 - vtr_sign * 90)),
                     origin+crs_dev_vtr+pygame.math.Vector2.from_polar((50, hdg+ crs + 90 - vtr_sign * 90))+pygame.math.Vector2.from_polar((10, hdg+ crs + 90 + vtr_sign * 90 - 30))
    )
    )
    # Course Indicator Arrow (Front)
    pygame.draw.aalines(DISPLAYSURF, (0,255,0), False, (
                     origin+pygame.math.Vector2.from_polar((55,  hdg + crs + 180)),
                     origin+pygame.math.Vector2.from_polar((130, hdg + crs + 180)),
                     origin+pygame.math.Vector2.from_polar((130, hdg + crs + 180))+pygame.math.Vector2.from_polar((10, hdg + crs + 30))
    )
    )
    pygame.draw.aalines(DISPLAYSURF, (0,255,0), False, (
                     origin+pygame.math.Vector2.from_polar((55,  hdg + crs + 180)),
                     origin+pygame.math.Vector2.from_polar((130, hdg + crs + 180)),
                     origin+pygame.math.Vector2.from_polar((130, hdg + crs + 180))+pygame.math.Vector2.from_polar((10, hdg + crs - 30))
    )
    )
    # Course Indicator Arrow (Rear)
    pygame.draw.aaline(DISPLAYSURF, (0,255,0), 
            origin+pygame.math.Vector2.from_polar((55, hdg+crs)),
            origin+pygame.math.Vector2.from_polar((130, hdg+crs)) 
    )
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEWHEEL:
           crs += [-1, 1][event.y > 0] * 1
    pygame.display.update()
    t.tick(FPS)
