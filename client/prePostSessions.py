from definitions import *
import pygame as pg
import re

import uuid
import connection
from widgets import Button, TextBox, TextMultiline

def loginPage( screen, cm ):
    address_regex = re.compile( r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|localhost)$" )
    input_box = TextBox( 50, 80, 200, 32, address_regex )
    input_box.active = True
    button = Button( 90, 30, "Connect", ( 50, 130 ), start_active=False )
    text = TextMultiline( [ "Welcome to Snowball Slingers.",
                            "Please enter the server IP address into the text box below.",
                            "Click the Connect button after you have entered the IP address",
                          ], 20, 10 )

    should_stop = False
    while not should_stop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            elif event.type == pg.MOUSEBUTTONDOWN:
                input_box.on_mousebuttondown( event.pos )
                if button.on_mousebuttondown( event.pos ):
                    should_stop = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN and input_box.valid:
                    should_stop = True
                if input_box.active:
                    input_box.on_keydown( event.key )
                    button.active = input_box.valid
        screen.fill( INDIGO )
        text.draw( screen )
        input_box.draw( screen )
        button.draw( screen )
        pg.display.flip()

    player_uuid = uuid.uuid4().hex
    cm.do_connect( input_box.text_input, player_uuid )
    pg.display.set_caption( f'{input_box.text_input} : {player_uuid}' )

    return 0
