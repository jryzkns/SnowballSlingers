import zmq

from definitions import *

class Connection:
    def connect(zmq_ctx, player_uuid, address):
        skt_conn = zmq_ctx.socket(zmq.REQ)
        skt_conn.connect(f"tcp://{address}:{PORT_CONN}")
        skt_conn.send(player_uuid.encode(UTF8))

    def disconnect(zmq_ctx, player_uuid, address):
        skt_conn = zmq_ctx.socket(zmq.REQ)
        skt_conn.connect(f"tcp://{address}:{PORT_CONN}")
        skt_conn.send(player_uuid.encode(UTF8))
