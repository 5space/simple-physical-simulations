import time
import pygame
import math

CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((500, 500))
SCALE = 200

r = 0.78

v = 0
a = 0
theta = -math.pi/3

g = 9.81
m = 1

DELTATIME = time.time()

def energy():
    ke = m * (r*v) ** 2 / 2
    pe = m * g * -math.cos(theta)
    return ke + pe

def delta_time():
    global DELTATIME
    now = time.time()
    offset = now - DELTATIME
    DELTATIME = now
    return offset

def process_physics():
    global theta, v, a
    dt = delta_time()
    a = -g/r * math.sin(theta)
    v += a * dt
    theta += v * dt

def draw_screen():
    SCREEN.fill((255, 255, 255))
    pygame.draw.circle(SCREEN, (0, 0, 0), (250, 250), 10)
    pygame.draw.line(SCREEN,
                     (0, 0, 0), (250, 250),
                     (250 + SCALE * r * math.sin(theta), 250 + SCALE * r * math.cos(theta)), 5)
    pygame.draw.circle(SCREEN, (0, 0, 255), (int(250 + SCALE * r * math.sin(theta)),
                                             int(250 + SCALE * r * math.cos(theta))), 20)

while True:
    process_physics()
    draw_screen()
    pygame.event.pump()
    pygame.display.flip()
    print(energy())