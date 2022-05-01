import pygame as pg
from random import randint, uniform
from math import sin, cos, pi

from definitions import *

class Particle:
    def __init__( self, x, y, direction = None ):
        self.x, self.y = x, y
        self.size = randint( 3, 5 )
        self.lifetime = uniform( 0.01, 0.75 )
        if direction is None:
            direction = uniform( 0, 2 * pi )
        direction += uniform( -pi/6, pi/6 )
        power = uniform( 10, 100 )
        self.xvel = power * cos( direction )
        self.yvel = power * sin( direction )

    def update( self, dt ):
        self.lifetime = max( 0, self.lifetime - dt )
        self.x += self.xvel * dt
        self.y += self.yvel * dt
        self.size = max( 0, self.size - dt )

    def draw(self, surf):
        pg.draw.rect( surf, WHITE, pg.Rect( self.x, self.y, self.size, self.size ) )

class Particles:
    def __init__( self ):
        self.buffer = []

    def update( self, dt ):
        for idx, particle in enumerate( self.buffer ):
            particle.update( dt )
            if particle.lifetime == 0:
                self.buffer[ idx ] = None
        self.buffer = [ p for p in self.buffer if p ]

    def emit( self, n, x, y, direction = None ):
        self.buffer += [ Particle( x, y, direction ) for _ in range(n) ]

    def draw(self, surf):
        for particle in self.buffer:
            particle.draw( surf )
