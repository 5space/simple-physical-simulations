import time
import pygame
from math import sin, cos, pi

CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((500, 500))
TRACE_CANVAS = pygame.Surface((500, 500))
TRACE_CANVAS.fill((255, 255, 255))
SCALE = 100

r1 = 1
r2 = 1

m1 = 1
theta1 = pi
v1 = -2
a1 = 0

m2 = 1
theta2 = pi
v2 = -4
a2 = 0

g = 9.81
trace = True

DELTATIME = time.time()

def energy():
    h1, h2 = -cos(theta1), -cos(theta2)
    ke = (m1 * (r1*v1)**2 + m2 * (r2*v2)**2)/2
    pe = g * (m1*h1 + m2*h2)
    return ke + pe

def delta_time():
    global DELTATIME
    now = time.time()
    offset = now - DELTATIME
    DELTATIME = now
    return offset

def trace(_t1, _t2, t1, t2):
    pygame.draw.line(TRACE_CANVAS, (0, 0, 0),
                     (250 + SCALE*r1*sin(_t1) + SCALE*r2*sin(_t2), 250 + SCALE*r1*cos(_t1) + SCALE*r2*cos(_t2)), 
                     (250 + SCALE*r1*sin(t1) + SCALE*r2*sin(t2), 250 + SCALE*r1*cos(t1) + SCALE*r2*cos(t2)), 2)

def process_physics():
    global theta1, v1, a1, theta2, v2, a2

    dt = delta_time()
    
    a1_numerator = -g*(2*m1+m2)*sin(theta1)-m2*g*sin(theta1-2*theta2)-2*sin(theta1-theta2)*m2*(r2*v2**2+r1*v1**2*cos(theta1-theta2))
    a1_denominator = r1*(2*m1+m2-m2*cos(2*theta1-2*theta2))
    a1 = a1_numerator/a1_denominator

    a2_numerator = 2*sin(theta1-theta2)*(r1*v1**2*(m1+m2)+g*(m1+m2)*cos(theta1)+r2*v2**2*m2*cos(theta1-theta2))
    a2_denominator = r2*(2*m1+m2-m2*cos(2*theta1-2*theta2))
    a2 = a2_numerator/a2_denominator

    v1 += a1 * dt
    v2 += a2 * dt

    _theta1 = theta1
    _theta2 = theta2
    theta1 = (theta1 + v1 * dt) % (2 * pi)
    theta2 = (theta2 + v2 * dt) % (2 * pi)

    if trace:
        trace(_theta1, _theta2, theta1, theta2)

def draw_screen():
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(TRACE_CANVAS, (0, 0))
    pygame.draw.circle(SCREEN, (0, 0, 0), (250, 250), 10)
    pygame.draw.line(SCREEN,
                     (0, 0, 0), (250, 250),
                     (250 + SCALE*r1*sin(theta1), 250 + SCALE*r1*cos(theta1)), 4)
    pygame.draw.line(SCREEN,
                     (0, 0, 0), (250 + SCALE*r1*sin(theta1), 250 + SCALE*r1*cos(theta1)),
                     (250 + SCALE*r1*sin(theta1) + SCALE*r2*sin(theta2), 250 + SCALE*r1*cos(theta1) + SCALE*r2*cos(theta2)), 4)
    pygame.draw.circle(SCREEN, (0, 0, 255), (int(250 + SCALE*r1*sin(theta1)),
                                             int(250 + SCALE*r1*cos(theta1))), 15)
    pygame.draw.circle(SCREEN, (0, 0, 255), (int(250 + SCALE*r1*sin(theta1) + SCALE*r2*sin(theta2)),
                                             int(250 + SCALE*r1*cos(theta1) + SCALE*r2*cos(theta2))), 15)

while True:
    process_physics()
    draw_screen()
    CLOCK.tick(60)
    pygame.event.pump()
    pygame.display.flip()
    print(energy())