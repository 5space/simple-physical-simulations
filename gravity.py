import pygame
import numpy as np
import random
import math
import time
from typing import Union

CANVAS = pygame.display.set_mode((500, 500))
TRACE_CANVAS = pygame.Surface((500, 500))

G = 5

BODIES = []

pygame.font.init()
GUI_FONT = pygame.font.Font("freesansbold.ttf", 20)

clock = pygame.time.Clock()

def acceleration(body, r):
    return G * body.mass / (r * r)

def get_center_of_mass(bodies):
    total = V((0, 0))
    mass_sum = 0
    for body in bodies:
        total += body.position * body.mass
        mass_sum += body.mass
    return total/mass_sum

class V:

    def __init__(self, tup):
        self.x, self.y = tup
    
    def copy(self):
        return V((self.x, self.y))
    
    def __add__(self, other):
        return V((self.x + other.x, self.y + other.y))
    
    def __sub__(self, other):
        return V((self.x - other.x, self.y - other.y))
    
    def __mul__(self, other):
        return V((self.x * other, self.y * other))
    
    def __truediv__(self, other):
        return V((self.x / other, self.y / other))
    
    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def tup(self):
        return (self.x, self.y)
    
    def norm(self):
        a = self.__abs__()
        if a == 0:
            return self.copy()
        else:
            return self.__truediv__(a)
    
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

class Body:

    def __init__(self, mass, color, position=None, velocity=None, trace=False, stationary=False, radius=None):
        self.mass = mass
        self.color = np.array(color)

        if type(position) == tuple:
            self.position = V(position)
        elif position is None:
            self.position = V((0, 0))
        else:
            self.position = position

        if type(velocity) == tuple:
            self.velocity = V(velocity)
        elif velocity is None:
            self.velocity = V((0.0, 0.0))
        else:
            self.velocity = velocity

        self.trace = trace
        self.stationary = stationary
        self.radius = radius or math.sqrt(self.mass) * 2
    
    def update_velocity(self, affected_bodies):
        for body in affected_bodies:
            if body == self:
                continue
            r = abs(body.position - self.position)
            self.velocity += (body.position - self.position).norm() * acceleration(body, r)
    
    def update_position(self):
        if self.stationary:
            return
        global TRACE_CANVAS
        old_position = self.position.copy()
        self.position += self.velocity
        if self.trace:
            pygame.draw.line(TRACE_CANVAS, tuple(self.color), old_position.tup(), self.position.tup())
    
    def check_collisions(self, affected_bodies):
        global BODIES
        for body in affected_bodies:
            if body == self:
                continue
            r = abs(body.position - self.position)
            if r <= max(self.radius, body.radius, abs(self.velocity - body.velocity) - max(self.radius, body.radius), 0):
                BODIES.remove(self)
                BODIES.remove(body)
                BODIES.append(Body(self.mass + body.mass,
                                   (self.color*self.mass + body.color*body.mass)/(self.mass + body.mass),
                                   (self.position*self.mass + body.position*body.mass)/(self.mass + body.mass),
                                   (self.velocity*self.mass + body.velocity*body.mass)/(self.mass + body.mass),
                                   trace = self.trace or body.trace))
                return

for _ in range(150):
    BODIES.append(Body(1, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    (random.random()*500, random.random()*500),
    (random.random()*2-1, random.random()*2-1)))
BODIES[1].trace = True
# BODIES.append(Body(1000, (255, 255, 0), (250, 250), (0, 0)))
# BODIES.append(Body(20, (255, 0, 0), (250, 50), (2.3, 0), trace=False, radius=1))
# BODIES.append(Body(1, (0, 255, 0), (250, 32), (2.91, 0), trace=True, radius=1))

while True:
    CANVAS.fill((0, 0, 0))
    CANVAS.blit(TRACE_CANVAS, (0, 0))
    for body in BODIES:
        body.update_velocity(BODIES)
    for body in BODIES:
        body.update_position()
    for body in BODIES:
        body.check_collisions(BODIES)
    for body in BODIES:
        pygame.draw.circle(CANVAS, tuple(body.color), tuple(map(int, list(body.position.tup()))), int(body.radius))

    pygame.draw.circle(CANVAS,
                       (255, 255, 255),
                       tuple(map(int, list(get_center_of_mass(BODIES).tup()))),
                       5, 1)
    t1 = GUI_FONT.render(f"{len(BODIES)} bodies", True, (255, 255, 255))
    CANVAS.blit(t1, (0, 0))

    t2 = GUI_FONT.render(f"{int(clock.get_fps())} FPS", True, (255, 255, 255))
    CANVAS.blit(t2, (0, 25))

    clock.tick()

    pygame.event.pump()
    pygame.display.flip()