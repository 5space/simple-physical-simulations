import time
import pygame
import math

CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((500, 500))
SCALE = 50

m = 0.4
k = 320

x = 3
v = 0
a = 0
L = 4

t = 0

y = 0.5

DELTATIME = time.time()

def delta_time():
    global DELTATIME
    now = time.time()
    offset = now - DELTATIME
    DELTATIME = now
    return offset

def process_physics():
    global x, v, a, t
    dt = delta_time()
    a = (-k*x - y*v)/m
    v += a * dt
    x += v * dt
    t += dt

def draw_screen():
    SCREEN.fill((255, 255, 255))
    y = -10
    x1 = 0
    length = (L+x)*SCALE
    print(t)
    for n in range(20):
        x1 += length/20
        pygame.draw.line(SCREEN, (0, 0, 0), (x1, 250+y), (x1+length/20, 250-y), 5)
        y *= -1
    pygame.draw.circle(SCREEN, (0, 0, 255), (int(length), 250), 20)
    CLOCK.tick(60)

while True:
    process_physics()
    draw_screen()
    pygame.event.pump()
    pygame.display.flip()