from definitions import *
import pygame as pg
import re

from widgets import Button, TextBox, TextMultiline

def loginPage( screen ):
    address_regex = re.compile( r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|localhost)$" )
    input_box = TextBox( 50, 80, 200, 32, address_regex )
    button = Button( 90, 30, "Connect", ( 50, 130 ), start_active=False )
    text = TextMultiline( [ "Welcome to Snowball Slingers.",
                            "Please enter the server IP address into the text box below.",
                            "Click the Connect button after you have entered the IP address",
                          ], 20, 10 )

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            elif event.type == pg.MOUSEBUTTONDOWN:
                input_box.on_mousebuttondown( event.pos )
                if button.on_mousebuttondown( event.pos ):
                    return input_box.text_input
            elif event.type == pg.KEYDOWN:
                if input_box.active:
                    input_box.on_keydown( event.key )
                    button.active = input_box.valid
        screen.fill( INDIGO )
        text.draw( screen )
        input_box.draw( screen )
        button.draw( screen )
        pg.display.flip()

REJOIN = True
def endScreen( screen ):
    button_rejoin = Button( 90, 30, "Rejoin", ( 50,130 ) )
    back_to_login = Button( 200, 30, "Return to Login Screen", ( 50,180 ) )

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_rejoin.collidepoint( event.pos ):
                    if button_rejoin.on_mousebuttondown( event.pos ):
                        return REJOIN
                elif back_to_login.collidepoint( event.pos ):
                    if back_to_login.on_mousebuttondown(event.pos):
                        return not REJOIN
        screen.fill( INDIGO )
        button_rejoin.draw( screen )
        back_to_login.draw( screen )
        pg.display.flip()
