import java.io.File
import kotlin.math.absoluteValue
import kotlin.streams.toList

// represents a path of a wire using a list of ranges representing the wire's moves
class Wire(path: String) {
    enum class Direction(val dir: Char) {
        UP('U'),
        DOWN('D'),
        LEFT('L'),
        RIGHT('R')
    }

    val route: MutableList<Triple<IntProgression, IntProgression, Int>> = mutableListOf(Triple(0..0, 0..0, 0))

    init {
        val moves = path.split(",")
        for (move in moves) {
            val lastX = route.last().first.last
            val lastY = route.last().second.last
            // TODO should we make this the distance of the move or the total distance?
            val dist = move.drop(1).toInt()
            val totalDist = route.last().third + dist
            when (move.first()) {
                Direction.UP.dir -> route.add(Triple(lastX..lastX, lastY..lastY + dist, totalDist))
                Direction.DOWN.dir -> route.add(Triple(lastX..lastX, lastY downTo lastY - dist, totalDist))
                Direction.LEFT.dir -> route.add(Triple(lastX downTo lastX - dist, lastY..lastY, totalDist))
                Direction.RIGHT.dir -> route.add(Triple(lastX..lastX + dist, lastY..lastY, totalDist))
            }
        }
    }
}

// use set to eliminate duplicates
fun getIntersections(wire1: Wire, wire2: Wire): Set<Triple<Int, Int, Int>> {
    // basically, we need to loop over one of the wires and see if there are any intersection points
    val results: MutableSet<Triple<Int, Int, Int>> = mutableSetOf()

    for (move in wire1.route) {
        val x = move.first
        val y = move.second
        val dist = move.third

        results.addAll(wire2.route.parallelStream()
            .map{
                val xInt = it.first.intersect(x)
                val yInt = it.second.intersect(y)

                // the full distance scaled based on where the intersection was in the range
                // one axis will always be zero
                // note this only adjusts it for the distance of wire2
                val adjustedDist = it.third - (it.first.last - xInt.ifEmpty { setOf(it.first.last) }.first()).absoluteValue - (it.second.last - yInt.ifEmpty { setOf(it.second.last) }.first()).absoluteValue

                // bundle the result into a triple
                Triple(xInt, yInt, adjustedDist)
            }
            .filter{ it.first.isNotEmpty() && it.second.isNotEmpty() }
            .map{
                // we are comparing 1 move of each wire at a time, so there should only be 1 intersection at most
                val xInt = it.first.first()
                val yInt = it.second.first()

                // this time, we adjust it with the distance of wire1
                val adjustedDist = dist - (x.last - xInt).absoluteValue - (y.last - yInt).absoluteValue
                Triple(xInt, yInt, it.third + adjustedDist)
            }
            .filter{ !(it.first == 0 && it.second == 0) } // remove intersections at the origin
            .toList())
    }

    return results.toSet()
}

fun main(args: Array<String>) {
    val wires = File(args.first()).readLines().map{ Wire(it) }
    val result = getIntersections(wires.first(), wires[1])

    // part 1 - closest to origin
    // manhattan dist is abs(xIntersection) + abs(yIntersection)
    val closest = result.stream()
        .mapToInt{it.first.absoluteValue + it.second.absoluteValue} // summing absolute values of x and y is manhattan
        .min().asInt

    // part 2 - shortest route to intersection
    val shortest = result.stream()
        .mapToInt { it.third }
        .min().asInt

    println(closest)
    println(shortest)
}
