import zmq

from definitions import *

class ConnectionManager:
    def __init__( self, zmq_ctx ):
        self.ctx = zmq_ctx

    def do_connect( self, address, player_id ):
        self.addr, self.pid = address, player_id
        skt_conn = self.ctx.socket( zmq.REQ )
        skt_conn.connect( f'tcp://{self.addr}:{PORT_CONN}' )
        skt_conn.send( self.pid.encode( UTF8 ) )

    def do_init_session( self ):
        self.skt_hand = self.ctx.socket( zmq.PUSH )
        self.skt_hand.connect( f'tcp://{self.addr}:{PORT_HAND}' )
        self.skt_subs = self.ctx.socket( zmq.SUB )
        self.skt_subs.connect( f'tcp://{self.addr}:{PORT_SUBS}' )
        self.skt_subs.setsockopt( zmq.SUBSCRIBE, b"U" )

    def do_disconnect( self ):
        skt_conn = self.ctx.socket( zmq.REQ )
        skt_conn.connect( f'tcp://{self.addr}:{PORT_CONN}' )
        skt_conn.send( self.pid.encode( UTF8 ) )

    def do_subscribe( self ):
        while True:
            try:
                yield self.skt_subs.recv( zmq.NOBLOCK ).decode( UTF8 )[ 2: ]
            except:
                break

    def do_handle( self, action, pos ):
        self.skt_hand.send( f"{self.pid}-{action}-{pos}".encode(UTF8) )
