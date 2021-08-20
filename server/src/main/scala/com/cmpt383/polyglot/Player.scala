import scala.math.hypot

class Player (
    val name : String,
    var x : Double,
    var y : Double,
    var intent : Option[(Int, Int)],
) {
    private var _cd_countdown = 0.0
    var hp = 3

    def tick (dt : Double) = {
        _cd_countdown -= dt
        _cd_countdown = math.max(0, _cd_countdown)
        intent match {
            case None => {}
            case Some((dst_x, dst_y)) => move_towards(dt, dst_x, dst_y)
        }
    }

    def move_towards(dt : Double, dst_x : Int, dst_y : Int) : Unit = {
        val (x_diff, y_diff) = (dst_x - x, dst_y - y)
        val dst = hypot(x_diff, y_diff)
        if (dst > dt * Definitions._player_velocity) {
            val move = dt * Definitions._player_velocity / dst
            val (dx, dy) = (x_diff * move, y_diff * move)
            x += dx
            y += dy
        } else {
            x = dst_x
            y = dst_y
            intent = None
        }
    }

    def attempt_cast() : Boolean = {
        val castable = _cd_countdown == 0.0
        if (castable) {
            _cd_countdown = Definitions._cd_duration
        }
        castable
    }
}
