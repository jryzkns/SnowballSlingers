import java.util.Map;
import java.util.HashMap;

import org.zeromq.ZMQ;
import org.zeromq.ZContext;

import com.cmpt383.polyglot.*;

public class GameServer {
    public static void main( String[] args ) throws Exception {

        World game_world = new World();

        try ( ZContext zmq_ctx = new ZContext() ) {

            ZMQ.Socket skt_conns = zmq_ctx.createSocket( ZMQ.REP );
            skt_conns.bind( "tcp://*:5555" );

            ZMQ.Socket skt_incs = zmq_ctx.createSocket( ZMQ.PULL );
            skt_incs.bind( "tcp://*:5556" );

            ZMQ.Socket skt_upd = zmq_ctx.createSocket( ZMQ.PUB );
            skt_upd.bind( "tcp://*:5557" );

            while ( !Thread.currentThread().isInterrupted() ) {

                for ( ;; ) {
                    try {
                        String result = game_world.process_register(
                            new String( skt_conns.recv( ZMQ.NOBLOCK ), ZMQ.CHARSET ) );
                        skt_conns.send( result.getBytes( ZMQ.CHARSET ) );
                    } catch ( Exception e ) {
                        break;
                    }
                }

                for ( ;; ) {
                    try {
                        byte[] client_update = skt_incs.recv( ZMQ.NOBLOCK );
                        game_world.process_incoming(
                            new String( client_update, ZMQ.CHARSET ) );
                    } catch ( Exception e ) {
                        break;
                    }
                }

                game_world.tick();

                for (String out_msg : game_world.tick_updates() ) {
                    skt_upd.send( ( "U " + out_msg ).getBytes( ZMQ.CHARSET ) );
                }

                Thread.sleep( 16 );

            }
        }
    }
}
