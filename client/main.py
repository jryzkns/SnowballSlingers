import os, sys
os.environ[ 'PYGAME_HIDE_SUPPORT_PROMPT' ] = 'hide'

import zmq
import pygame as pg

from definitions import *
from connection import ConnectionManager
from gameSession import gameSession
from prePostSessions import loginPage

pg.init()
game_win = pg.display.set_mode( res )

with zmq.Context() as zmq_ctx:

    cm = ConnectionManager( zmq_ctx )

    if loginPage( game_win, cm ) is None:
        sys.exit()

    gameSession( game_win, cm )

    cm.do_disconnect()

    zmq_ctx.destroy( 1000 )
