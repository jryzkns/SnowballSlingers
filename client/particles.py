import pygame as pg
import random


from definitions import *

class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.size = random.randint(3,5)
        self.lifetime = random.uniform(0.25, 0.75)
        self.xvel = random.uniform(-125, 125)
        self.yvel = random.uniform(-125, 125)

    def update(self, dt):
        self.lifetime = max(0, self.lifetime - dt)
        self.x += self.xvel * dt
        self.y += self.yvel * dt
        self.size = max(0, self.size - dt)

    def draw(self, surf):
        pg.draw.rect(surf, WHITE, pg.Rect(self.x, self.y, self.size, self.size))

class Particles:
    def __init__(self):
        self.buffer = []
    def update(self, dt):
        for idx, particle in enumerate(self.buffer):
            particle.update(dt)
            if particle.lifetime == 0:
                self.buffer[idx] = None
        self.buffer = [particle for particle in self.buffer 
                        if particle is not None]
    def emit(self, n, x, y):
        for _ in range(n):
            self.buffer.append(Particle(x, y))
    def draw(self, surf):
        for particle in self.buffer:
            particle.draw(surf)
