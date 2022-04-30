import pygame as pg
from definitions import *

class WidgetStyles:
    def __init__( self,
                  fontttf='CaviarDreams.ttf',
                  fontsize=18,
                  fontcolor=BLACK,
                  outline_thickness=2
    ):
        self.font = pg.font.Font( asset( fontttf ), fontsize )
        self.outline_thickness=outline_thickness
        self.fontcolor = fontcolor

class TextMultiline( WidgetStyles ):
    def __init__( self, lines, x, y, linesep=20, **kwargs ):
        WidgetStyles.__init__( self, **kwargs )
        self.rendered = [ ( self.font.render( line, True, self.fontcolor ),
                          ( x, y + i * linesep ) )
                              for i, line in enumerate( lines) ]
    def draw( self, surf ):
        for line, pos in self.rendered:
            surf.blit( line, pos )

class TextBox( pg.Rect, WidgetStyles ):
    def __init__( self, x, y, w, h, matcher = None, **kwargs ):
        pg.Rect.__init__( self, x, y, w, h )
        WidgetStyles.__init__( self, **kwargs )
        self.text_input = ''
        self.text = self.font.render( self.text_input, True, self.fontcolor )
        self.active = False
        self.matcher = matcher
        self.valid = False

    def on_mousebuttondown( self, position ):
        self.active = self.collidepoint( position )

    def on_keydown( self, key ):
        if not self.active:
            return
        if key == pg.K_RETURN:
            return
        if key == pg.K_BACKSPACE:
            self.text_input = self.text_input[ : -1 ]
        else:
            keyname = pg.key.name( key )
            if len( keyname ) > 1:
                return
            self.text_input += pg.key.name( key )
        self.text = self.font.render( self.text_input, True, self.fontcolor )
        self.valid = self.matcher.match( self.text_input ) is not None

    def draw( self, screen ):
        screen.blit( self.text, self.topleft )
        pg.draw.rect( screen, ( ORANGE if self.active else BANANA ), self, self.outline_thickness )

class Button( pg.Rect, WidgetStyles ):
    def __init__( self, w, h, text, position, start_active=True, **kwargs ):
        pg.Rect.__init__( self, *position, w, h )
        WidgetStyles.__init__( self, **kwargs )
        self.text = self.font.render( text, True, BLACK )
        self.active = start_active

    def on_mousebuttondown( self, position ):
        return self.active and pg.mouse.get_pressed()[ 0 ] and self.collidepoint( *position )

    def draw( self, screen ):
        screen.blit( self.text, self.topleft )
        pg.draw.rect(screen, ( ORANGE if self.active else BANANA ), self, self.outline_thickness )
