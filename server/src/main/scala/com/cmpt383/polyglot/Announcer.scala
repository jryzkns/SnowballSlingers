abstract class AnnounceEvent

case class KillEvent( killer : String, killee : String ) extends AnnounceEvent
case class JoinEvent( player : String ) extends AnnounceEvent
case class QuitEvent( player : String ) extends AnnounceEvent

class Announcer {

    private var _event_buffer = scala.collection.mutable.Queue[ AnnounceEvent ]()

    def register_kill_event( killer : String, killee : String ) : Unit = {
        println( s"$killer killed $killee" )
        _event_buffer += new KillEvent( killer, killee )
    }

    def register_join_event( player : String ) : Unit = {
        println( s"$player joined" )
        _event_buffer += new JoinEvent( player )
    }

    def register_quit_event( player : String ) : Unit = {
        println( s"$player quit" )
        _event_buffer += new QuitEvent( player )
    }

    def emit_announcement() : Option[ String ] = {
        if ( _event_buffer.isEmpty ) {
            None
        }
        Some( _event_buffer.dequeue() match {
            case KillEvent( killer, killee ) =>
                s"a-k-$killer-$killee"
            case JoinEvent( player ) =>
                s"a-j-$player"
            case QuitEvent( player ) =>
                s"a-q-$player"
        } )
    }
}
