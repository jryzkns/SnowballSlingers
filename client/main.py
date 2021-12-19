import os
from typing import Text
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import zmq
import uuid
import pygame as pg

import pygame as pg

from definitions import *
from gameSession import GameSession
from connection import Connection
from textBox import *
from buttonPress import *

pg.init()

# done = False
# while not done:
#     for event in pg.event.get():
#         print(event)
#         input_box.on_user_input(event)
#         done = True

pg.init()
game_win = pg.display.set_mode(res)

with zmq.Context() as zmq_ctx:

    should_stop = not SHOULD_STOP_GAME

    while not should_stop:

        player_uuid = uuid.uuid4().hex

        Connection.connect(zmq_ctx, player_uuid)

        pg.display.set_caption(f'Playing as: {player_uuid}')

        should_stop = GameSession.run_session(zmq_ctx, game_win, player_uuid)

        if should_stop:
            Connection.disconnect(zmq_ctx, player_uuid)

    zmq_ctx.destroy(1000)
