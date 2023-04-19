import sys
import pygame as pg
from math import *
import time
import random
import numpy as np

mode = int(input("Vpisite nacin, ki bi ga radi videli (0 - simulacija osoncja, 1 - sumulacija krozenja Zemlje z razdaljo, 2 - preprosta simulacija trkov): "))
pg.init()
pg.font.init()
text = pg.font.Font(None, 25)
clock = pg.time.Clock()
size = width, height = 1920, 1080
black = 0, 0, 0
yellow = 255, 255, 0
red = 255, 0, 0
white = (255, 255, 255)
blue = 0, 0, 255
mass_mult = 10**24
G = 6.673 * (10**(-11))
SCALE = 10**9
nSCALE = SCALE
planetarni_podatki = {'masa': [0.330, 4.87, 5.97, 0.642, 1898, 568, 86.8, 102, 0.0130], 
                      'premer': [4879, 12104, 12756, 6792, 142984, 120536, 51118, 49528, 2376], 
                      'razdalja': [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0, 5906.4],
                      'hitrost': [47.4, 35.0, 29.8, 24.1, 13.1, 9.7, 6.8, 5.4, 4.7]
                      }
screen = pg.display.set_mode(size)
x = 0
zoom = 10**8
xzoom = zoom
yzoom = zoom
nplanets = []
FPS = 60
SPD = 10*(1/FPS)*60*60*24
speed_multiplier = SPD/SCALE

class planet():
    def __init__(self, mass, x, y, x_vel, y_vel, colour, rad):
        self.mass = mass
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.colour = colour
        self.irad = rad*695700/2
        self.rad = rad

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        pg.draw.circle(screen, self.colour, (self.x, self.y), self.rad if self.rad > 2 else 2)

    def pos(self):
        return self.x, self.y

def distance(item1, item2):
    x1, y1 = item1.pos()
    try:
        x2, y2 = item2.pos()
    except:
        x2 = width/2
        y2 = height/2
    vect = sqrt((x1-x2)**2 + (y1-y2)**2)
    length = vect*SCALE
    dist = [length, (x1-x2)/vect, (y1-y2)/vect]
    return dist

def grav_effect(pl1, pl2, r):
    m1 = pl1.mass
    m2 = pl2.mass
    v1 = G*m2*SPD/(r[0]**2)
    v2 = G*m1*SPD/(r[0]**2)
    s1 = [v1*r[1]*SPD/SCALE, v1*r[2]*SPD/SCALE]
    s2 = [v2*r[1]*SPD/SCALE, v2*r[2]*SPD/SCALE]
    if r[0]/SCALE <= (pl1.rad + pl2.rad):
        planets.remove(pl1)
        planets.remove(pl2)
        pl1.x_vel -= s1[0]
        pl1.y_vel -= s1[1]
        pl2.x_vel += s2[0]
        pl2.y_vel += s2[1]
        if pl1.mass > pl2.mass:
            vx = (m1*pl1.x_vel + m2*pl2.x_vel)/(m1+m2)
            vy = (m1*pl1.y_vel + m2*pl2.y_vel)/(m1+m2)
            planets.append(planet(pl1.mass + pl2.mass, pl1.x, pl1.y, vx, vy, pl1.colour, pl1.rad + pl2.rad/10))
        else:
            vx = (m2*pl2.x_vel + m1*pl1.x_vel)/(m1+m2)
            vy = (m2*pl2.y_vel + m1*pl1.y_vel)/(m1+m2)
            planets.append(planet(pl1.mass + pl2.mass, pl2.x, pl2.y, vx, vy, pl2.colour, pl2.rad + pl1.rad/10))
        del pl1
        del pl2
        return 1
    else:
        pl1.x_vel -= s1[0]
        pl1.y_vel -= s1[1]
        pl2.x_vel += s2[0]
        pl2.y_vel += s2[1]
        return 0

def rad_draw(pl1, czoom):
    pg.draw.aaline(screen, white, (pl1.x, pl1.y), (width/2, height/2), 1)
    img = text.render(str((distance(pl1,0)[0]*czoom/SCALE).__round__(3)), 1, white)
    screen.blit(img, ((pl1.x + width/2)/2, (pl1.y + height/2)/2))

planets = []
Sun = planet(1.988500*(10**30), width/2, height/2, 0, 0, yellow, 1)
if mode == 1:
    SPD = 10*(1/FPS)*60*60*24
    Earth = planet(5.97*mass_mult, width/2, height/2 + 147.1, 30.29*10**3*SPD/SCALE, 0, blue, 1/5)
    planets = [Sun, Earth]
elif mode == 0:
    planets = [Sun]
    for i in range(len(planetarni_podatki['masa'])):
        if i % 2 == 0:
            planets.append(planet(planetarni_podatki['masa'][i]*mass_mult, width/2 - planetarni_podatki['razdalja'][i]*(10**9)/SCALE, height/2, 0, planetarni_podatki['hitrost'][i]*speed_multiplier*10**3, (random.randint(100, 255),random.randint(100, 255),random.randint(100, 255)), planetarni_podatki['premer'][i]/695700))
        else:
            planets.append(planet(planetarni_podatki['masa'][i]*mass_mult, width/2 + planetarni_podatki['razdalja'][i]*(10**9)/SCALE, height/2, 0, -planetarni_podatki['hitrost'][i]*speed_multiplier*10**3, (random.randint(100, 255),random.randint(100, 255),random.randint(100, 255)), planetarni_podatki['premer'][i]/695700))
elif mode == 2:
    planets.append(planet(1000000*mass_mult, width/2, height/2, 0, 0, red, 10))
    planets.append(planet(1000000*mass_mult, width/2 + 100, height/2 + 100, 0, 0, white, 10))
    planets.append(planet(1000000*mass_mult, width/2 + 200, height/2 - 400, 0, 0, blue, 10))
    planets.append(planet(1000000*mass_mult, width/2 - 500, height/2 - 600, 0, 0, yellow, 10))


t0 = time.time()
while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.MOUSEWHEEL:
            if event.y < 1:
                xzoom = zoom
                nSCALE = SCALE + yzoom
                for p in planets:
                    p.x_vel = p.x_vel*SCALE/nSCALE
                    p.y_vel = p.y_vel*SCALE/nSCALE
                    p.x = (p.x-width/2)*SCALE/nSCALE + width/2
                    p.y = (p.y-height/2)*SCALE/nSCALE + height/2
                    p.rad = p.rad * SCALE/nSCALE
                SCALE = nSCALE
                yzoom = yzoom * 1.1
            else:
                yzoom = zoom
                if SCALE > xzoom:
                    nSCALE = SCALE - xzoom
                    for p in planets:
                        p.x_vel = p.x_vel*SCALE/nSCALE
                        p.y_vel = p.y_vel*SCALE/nSCALE
                        p.x = (p.x-width/2)*SCALE/nSCALE + width/2
                        p.y = (p.y-height/2)*SCALE/nSCALE + height/2
                        p.rad = p.rad*SCALE/nSCALE
                    SCALE = nSCALE
                    xzoom = xzoom * 1.1

    if len(planets) != 1:
        for i in range(len(planets)-1):
            for ii in range(i+1,len(planets)):
                x = grav_effect(planets[i], planets[ii], distance(planets[i], planets[ii]))
                if x == 1:
                    break   
    
    screen.fill(black)

    if mode == 1:
        for x in planets:
            if x.x != width/2 or x.y != height/2:
                rad_draw(x, nSCALE)

    for p in planets:
        p.update()
    img2 = text.render(str((time.time() - t0).__round__(2)), 1, white)
    screen.blit(img2, (10, 10))
    pg.display.update()

pg.quit()
