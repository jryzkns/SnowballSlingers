import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import zmq
import uuid
import pygame as pg

from end import endScreen
from definitions import *
from gameSession import GameSession
from connection import Connection
from login import loginPage

pg.init()
game_win = pg.display.set_mode(res)

with zmq.Context() as zmq_ctx:

    address = loginPage(game_win)
    should_stop = not SHOULD_STOP_GAME

    while not should_stop:

        player_uuid = uuid.uuid4().hex

        Connection.connect(zmq_ctx, player_uuid, address)

        pg.display.set_caption(f'Playing as: {player_uuid}')

        should_stop = GameSession.run_session(zmq_ctx, game_win, player_uuid, address)

        if should_stop:
            #Connection.disconnect(zmq_ctx, player_uuid, address)
            result = endScreen(game_win, address)
            if result:
                Connection.connect(zmq_ctx, player_uuid, address)
                should_stop = GameSession.run_session(zmq_ctx, game_win, player_uuid, address)
            else:
                address = loginPage(game_win)
                should_stop = not SHOULD_STOP_GAME

    zmq_ctx.destroy(1000)
