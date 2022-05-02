import pygame as pg
from pygame.freetype import Font

from definitions import *

class Announcer:
    def __init__( self, x, y ):
        self.x, self.y = x - RIBBON_W//2, y - RIBBON_H//2
        self.buffer, self.timer = [], 0
        self.font = Font( asset( 'orange-kid.regular.ttf' ), 16 )
        self.texth = self.font.render( 'A', True, WHITE )[ 0 ].get_rect().h
    def register_join( self, player ):
        canvas = pg.Surface( ( RIBBON_W, RIBBON_H ), pg.SRCALPHA )
        canvas.fill( ( *WHITE, 50 ) )
        self.font.render_to( canvas,
                             (10, ( RIBBON_H - self.texth )/2 ),
                             f"{player:12} JOINED THE FIGHT!",
                             WHITE )
        self.buffer += canvas,
    def register_quit( self, player ):
        canvas = pg.Surface( ( RIBBON_W, RIBBON_H ), pg.SRCALPHA )
        canvas.fill( ( *WHITE, 50 ) )
        self.font.render_to( canvas,
                             (10, ( RIBBON_H - self.texth )/2 ),
                             f"{player:12} LEFT THE FIGHT!",
                             WHITE )
        self.buffer += canvas,
    def register_kill( self, killer, killee ):
        canvas = pg.Surface( ( RIBBON_W, RIBBON_H ), pg.SRCALPHA )
        canvas.fill( ( *WHITE, 50 ) )
        self.font.render_to( canvas,
                             (10, ( RIBBON_H - self.texth )/2 ),
                             f"{killer:12} KILLED {killee:12}",
                             WHITE )
        self.buffer += canvas,
    def register_event( self, action, subject ):
        self.timer = 0
        if action == JOIN:
            self.register_join( *subject )
        elif action == QUIT:
            self.register_quit( *subject )
        elif action == KILL:
            self.register_kill( *subject )
    def update( self, dt ):
        if len( self.buffer ) > 0:
            self.timer += dt
            if self.timer > RIBBON_TIME:
                self.buffer.pop( 0 )
                self.timer = 0
    def draw( self, surf ):
        for i, canvas in enumerate( self.buffer[ : MAX_RIBBONS ] ):
            surf.blit( canvas, (self.x, self.y + i * ( RIBBON_H + RIBBON_SPACING ) ) )
