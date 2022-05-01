import scala.util.matching.Regex
import collection.JavaConverters._
import scala.math.hypot

class World {

    private val msg_regex = raw"([\da-f]{32})-(.*)".r
    private val cast_regex = raw"cast-\((\d{1,3}),\s+(\d{1,3})\)".r
    private val click_regex = raw"click-\((\d{1,3}),\s+(\d{1,3})\)".r
    private val register_regex = raw"([\da-f]{32}):([\d\w]{1,12})".r

    private var _refresh_time = System.currentTimeMillis()

    private var _players = scala.collection.mutable.Map[ String, Player ]()
    private var _snowballs = scala.collection.mutable.MutableList[ Snowball ]()
    private val _updates = scala.collection.mutable.Queue[ String ]()

    private val _rng = new scala.util.Random
    def rand_range( min: Int, max: Int ) : Int = min + _rng.nextInt( ( max - min ) + 1 )

    def register_player ( id : String, name : String ) : Unit = {
        val player_x = rand_range( Definitions._world_left, Definitions._world_right )
        val player_y = rand_range( Definitions._world_top , Definitions._world_bottom )
        _players += ( id -> new Player( id, name, player_x, player_y, None ) )
        println( s"$id is now registered in the game as $name!" )
    }

    def deregister_player ( id : String ) : Unit = {
        if ( _players.contains( id ) ) {
            _players -= id
            _updates.enqueue(s"$id-disconn")
            println(s"Player $id have left the game")
        } else {
            println(s"Player $id was not here to begin with")
        }
    }

    def is_registered( id : String ) : Boolean = _players.contains( id )

    def process_register( msg : String ) : String = {
        msg match {
            case register_regex ( uuid, name ) => {
                val registered = is_registered( uuid )
                if ( registered ) {
                    deregister_player( uuid )
                } else {
                    register_player( uuid, name )
                }
                if ( registered ) {
                    return "Hello"
                } else {
                    return "Goodbye"
                }
            }
            case _ => return "wtf bro"
        }
    }

    def get_uuid() : String = java.util.UUID.randomUUID.toString.replace("-", "")

    def process_incoming( msg : String ) : Unit = {
        msg match {
            case msg_regex(player, body) => {
                if (!is_registered(player)) { return }
                body match {
                    case cast_regex(x, y) =>
                        var caster = _players( player )
                        if (caster.attempt_cast()) {
                            _updates.enqueue(s"$player-ack")
                            _snowballs += new Snowball( get_uuid(),
                                player, caster.x, caster.y, (x.toInt, y.toInt))
                        }
                    case click_regex(x, y) =>
                        _players(player).intent = Some((x.toInt, y.toInt))
                }
            }
            case _ => return
        }
    }

    def tick() : Unit = {
        val now = System.currentTimeMillis()
        val dt = (now - _refresh_time)/1000.0
        _players foreach ( { case (_, player) => player.tick(dt)})
        _snowballs foreach ( snowball => {
            snowball.tick(dt)
            val this_caster = snowball.caster
            // check if this snowball collides with any players
            _players foreach ( { case (p_name, player) => {
                val dist = hypot(player.x - snowball.x, player.y - snowball.y)
                if ( this_caster != p_name && dist < Definitions._snowball_player_collide_dist) {
                    snowball.lifetime = 0
                    player.hp = math.max(0, player.hp - 1)
                    _updates.enqueue(s"$p_name-hit")
                }
            }})
            // check if this snowbal lcollides with any other snowballs
            _snowballs foreach ( other_snowball => {
                if (this_caster != other_snowball.caster && other_snowball.lifetime != 0) {
                    val dist = hypot(   other_snowball.x - snowball.x,
                                        other_snowball.y - snowball.y)
                    if (dist < Definitions._snowball_snowball_collide_dist) {
                        snowball.lifetime = 0
                        other_snowball.lifetime = 0
                    }
                }

            })
        })

        _snowballs.filter(_.lifetime == 0) foreach {
            snowball => _updates.enqueue(s"${snowball.uuid}-d")
        }

        _snowballs = _snowballs.filterNot(_.lifetime == 0)

        _players foreach ( { case (p_name, player) => {
            if (player.hp == 0) {
                deregister_player(p_name)
            }
        }})

        _refresh_time = now
    }

    def tick_updates() : java.util.List[String] = {
        var out_updates = List[String]()
        out_updates = _updates.dequeueAll(_ => true).toList ::: out_updates
        out_updates = (for ((id, player) <- _players) yield
                        s"${id}-${player.name}-(${player.x.toInt}, ${player.y.toInt})"
                        ).toList ::: out_updates
        out_updates = (for (snowball <- _snowballs) yield
                        s"${snowball.uuid}-(${snowball.x.toInt}, ${snowball.y.toInt})"
                        ).toList ::: out_updates
        out_updates.asJava
    }
}
