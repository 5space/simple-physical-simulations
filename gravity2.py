import pygame
import numpy as np
import random
import math
import time
from typing import Union

CANVAS = pygame.display.set_mode((500, 500))
TRACE_CANVAS = pygame.Surface((500, 500))

G = 0.32

BODIES = []

pygame.font.init()
GUI_FONT = pygame.font.Font("freesansbold.ttf", 20)

clock = pygame.time.Clock()

def acceleration(body, r):
    return G * body.mass / (r * r)

class Body:

    def __init__(self, mass, color, position=None, velocity=None, trace=False, stationary=False, radius=None):
        self.mass = float(mass)
        self.color = np.array(color)

        if type(position) == tuple:
            self.position = np.array(position).astype(float)
        elif position is None:
            self.position = np.array((0.0, 0.0))
        else:
            self.position = position

        if type(velocity) == tuple:
            self.velocity = np.array(velocity).astype(float)
        elif velocity is None:
            self.velocity = np.array((0.0, 0.0))
        else:
            self.velocity = velocity

        self.trace = trace
        self.stationary = stationary
        self.radius = float(radius) or math.sqrt(self.mass) * 2
    
    def update_velocity(self, affected_bodies):
        for body in affected_bodies:
            if body == self:
                continue
            r = np.linalg.norm(body.position - self.position)
            self.velocity += (body.position - self.position) / r * acceleration(body, r)
    
    def update_position(self):
        if self.stationary:
            return
        global TRACE_CANVAS
        old_position = self.position.copy()
        self.position += self.velocity
        if self.trace:
            pygame.draw.line(TRACE_CANVAS, tuple(self.color), tuple(old_position), tuple(self.position))

BODIES.append(Body(70312500000, (255, 255, 0), (0, 0), (0, 0), stationary=True, radius=64000))
BODIES.append(Body(40000000, (0, 255, 0), (500000, 0), (0, 40.9), stationary=False, radius=3200))
BODIES.append(Body(320000000, (0, 255, 0), (1000000, 0), (0, 81.8), stationary=False, radius=6400))
BODIES.append(Body(320000000, (0, 255, 0), (1500000, 0), (0, 122.7), stationary=False, radius=6400))
# BODIES.append(Body(20, (255, 0, 0), (250, 50), (2.3, 0), trace=False, radius=1))
# BODIES.append(Body(1, (0, 255, 0), (250, 32), (2.91, 0), trace=True, radius=1))
t = 0

while True:
    CANVAS.fill((0, 0, 0))
    CANVAS.blit(TRACE_CANVAS, (0, 0))
    for body in BODIES:
        body.update_velocity(BODIES)
    for body in BODIES:
        body.update_position()
    for body in BODIES:
        pygame.draw.circle(CANVAS, tuple(body.color), tuple(map(int, list(body.position/8000 + 250))), int(body.radius/3000))
    
    t1 = GUI_FONT.render(f"{len(BODIES)} bodies - {t}s", True, (255, 255, 255))
    CANVAS.blit(t1, (0, 0))

    t2 = GUI_FONT.render(f"{int(clock.get_fps())} FPS", True, (255, 255, 255))
    CANVAS.blit(t2, (0, 25))

    t += 1

    clock.tick()

    pygame.event.pump()
    pygame.display.flip()