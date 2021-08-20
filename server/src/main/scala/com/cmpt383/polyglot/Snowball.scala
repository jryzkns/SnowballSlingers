import scala.math.hypot

class Snowball (
    val uuid : String,
    val caster : String,
    var x : Double,
    var y : Double,
    var dst : (Int, Int)
) {
    var lifetime = 0.75

    def tick (dt: Double) = {
        lifetime -= dt
        lifetime = math.max(0, lifetime)
        move_towards(dt, dst._1, dst._2)
    }

    def move_towards(dt : Double, dst_x : Int, dst_y : Int) : Unit = {
        val (x_diff, y_diff) = (dst_x - x, dst_y - y)
        val dst = hypot(x_diff, y_diff)
        if (dst > dt * Definitions._snowball_velocity) {
            val move = dt * Definitions._snowball_velocity / dst
            val (dx, dy) = (x_diff * move, y_diff * move)
            x += dx
            y += dy
        } else {
            x = dst_x
            y = dst_y
            lifetime = 0
        }
    }
}
