import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import zmq
import uuid

from definitions import *
from gameSession import GameSession
from connection import Connection

with zmq.Context() as zmq_ctx:

    should_stop = not SHOULD_STOP_GAME
    while not should_stop:

        player_uuid = uuid.uuid4().hex

        Connection.connect(zmq_ctx, player_uuid)

        should_stop = GameSession.run_session(zmq_ctx, player_uuid)

        if should_stop:
            Connection.disconnect(zmq_ctx, player_uuid)

    zmq_ctx.destroy(1000)
