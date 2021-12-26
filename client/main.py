import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import zmq
import uuid
import pygame as pg

from definitions import *
from gameSession import GameSession
from connection import Connection
from login import loginPage
from end import endScreen

pg.init()
game_win = pg.display.set_mode(res)

with zmq.Context() as zmq_ctx:

    rejoin = False
    should_stop = not SHOULD_STOP_GAME

    while not should_stop:
        if not rejoin:
            address = loginPage(game_win)   
            player_uuid = uuid.uuid4().hex
            pg.display.set_caption(f'Playing as: {player_uuid}')
        Connection.connect(zmq_ctx, player_uuid, address)

        should_stop = GameSession.run_session(zmq_ctx, game_win, player_uuid, address)

        if should_stop:
            Connection.disconnect(zmq_ctx, player_uuid, address)

        if not should_stop:
            rejoin = endScreen(game_win)
            should_stop = rejoin is None

    zmq_ctx.destroy(1000)