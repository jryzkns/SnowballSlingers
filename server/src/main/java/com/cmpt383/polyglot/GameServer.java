import java.util.Map;
import java.util.HashMap;

import org.zeromq.ZMQ;
import org.zeromq.ZContext;

import com.cmpt383.polyglot.*;

public class GameServer
{
    public static void main(String[] args) throws Exception
    {
        World game_world = new World();
        try (ZContext zmq_ctx = new ZContext()) {

            ZMQ.Socket skt_conns = zmq_ctx.createSocket(ZMQ.REP);
            skt_conns.bind("tcp://*:5555");

            ZMQ.Socket skt_incs = zmq_ctx.createSocket(ZMQ.PULL);
            skt_incs.bind("tcp://*:5556");

            ZMQ.Socket skt_upd = zmq_ctx.createSocket(ZMQ.PUB);
            skt_upd.bind("tcp://*:5557");
            
            while (!Thread.currentThread().isInterrupted()) {

                while (true) { try {
                    String client_name = new String(
                        skt_conns.recv(ZMQ.NOBLOCK), ZMQ.CHARSET);
                    if (!game_world.is_registered(client_name)) {
                        skt_conns.send("Hello".getBytes(ZMQ.CHARSET));
                        game_world.register_player(client_name);
                    } 
                    else {
                        skt_conns.send("Goodbye".getBytes(ZMQ.CHARSET));
                        game_world.deregister_player(client_name);
                    }
                } catch (Exception e) { break; }}

                while (true) { try {
                    byte[] client_update = skt_incs.recv(ZMQ.NOBLOCK);
                    game_world.process_incoming(new String(client_update, ZMQ.CHARSET));
                } catch (Exception e) { break; } }
 
                game_world.tick();

                for (String out_msg : game_world.tick_updates() ) {
                    skt_upd.send(("U " + out_msg).getBytes(ZMQ.CHARSET)); 
                }

                Thread.sleep(16);
            }
        }
    }
}
