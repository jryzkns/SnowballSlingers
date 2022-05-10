import pygame as pg
from pygame.freetype import Font
from math import sin, atan2

from definitions import *
from utils import *

class Entity:
    def __init__( self, uuid, x, y ):
        self.uuid, self.x, self.y = uuid, x, y
    def goto( self, x, y ):
        self.px, self.py = self.x, self.y
        self.x, self.y = x, y

class Player( Entity ):
    def __init__( self, uuid, name, x, y, is_self=False ):
        Entity.__init__( self, uuid, x, y )
        self.name = name
        self.cd_countdown = 0
        self.hp = 3
        self.canvas = pg.Surface( ( PLAYER_WIDTH, PLAYER_HEIGHT ) )
        self.render()
        self.hp_sprite = pg.image.load( asset( 'hp.png' ) )
        self.is_self = is_self
        if self.is_self:
            self.counter = 0
            self.marker_sprite = pg.image.load( asset( 'marker.png' ) )
            self.marker_offset = 0

        self.font = Font( asset( 'orange-kid.regular.ttf' ), 12 )
        self.ns, _ = self.font.render( self.name, True, GREEN )
        self.textw, self.texth = self.ns.get_size()

    def render( self ):
        self.canvas.fill( WHITE )
        head = self.uuid[ :30 ]
        for idx, offset in enumerate( range( 0, 30, 6 ) ):
            color_str = head[ offset:offset + 6 ]
            pg.draw.rect(   self.canvas,
                            colorstr2triple( color_str ),
                            pg.Rect(    PLAYER_RENDER_PADDING,
                                        PLAYER_HEIGHT - ( idx + 1 ) * 5 + PLAYER_RENDER_PADDING,
                                        PLAYER_WIDTH - 2 * PLAYER_RENDER_PADDING,
                                        5 ) )
    def hit( self ):
        self.hp = max( 0, self.hp - 1 )
    def update( self, dt ):
        if self.cd_countdown != 0:
            self.cd_countdown = max( 0, self.cd_countdown - dt )
        if self.is_self:
            self.counter += dt
            self.marker_offset = 2 * sin( 5 * self.counter )
    def draw(self, surf):
        surf.blit( self.canvas,
                   ( self.x - PLAYER_WIDTH//2,
                     self.y - PLAYER_HEIGHT//2 ) )

        progress = ( 1 - self.cd_countdown / CD_DURATION )
        progress_height = progress * PLAYER_HEIGHT
        pg.draw.rect( surf,
                      ( 255 * progress, 255 * progress, 255 * progress ),
                      pg.Rect(
                          self.x - ( PLAYER_WIDTH//2 + 4 ),
                          self.y - PLAYER_HEIGHT//2 + ( PLAYER_HEIGHT - progress_height ),
                          4,
                          progress_height ) )

        pg.draw.rect( surf,
                      WHITE,
                      pg.Rect(
                          self.x - ( PLAYER_WIDTH//2 + 4 ),
                          self.y - PLAYER_HEIGHT//2,
                          4,
                          PLAYER_HEIGHT ), 1 )

        for i in range( self.hp ):
            surf.blit( self.hp_sprite,
                       ( self.x + PLAYER_WIDTH//2 + 4,
                         self.y - PLAYER_HEIGHT//2 + i * 6 ) )

        self.font.render_to( surf,
                             ( self.x - ( PLAYER_WIDTH + self.textw )//2,
                               self.y - ( PLAYER_HEIGHT//2 + self.texth + 5 ) ),
                             self.name,
                             GREEN if self.is_self else RED )

        if self.is_self:
            surf.blit( self.marker_sprite,
                       ( self.x - ( PLAYER_WIDTH//2 ),
                         self.y - ( PLAYER_HEIGHT//2 + self.texth + 10 ) + self.marker_offset ) )

class Snowball( Entity ):
    def __init__( self, uuid, x, y ):
        Entity.__init__( self, uuid, x, y )
        self.px, self.py = x, y
    def draw( self, surf ):
        pg.draw.circle( surf, WHITE, ( self.x, self.y ), 5 )
    def direction( self ):
        return atan2( self.y - self.py, self.x - self.px )
