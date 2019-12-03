package `01`

import java.io.File

fun calculateFuel(mass : Int): Int {
    val neededFuel = Math.floorDiv(mass, 3) - 2
    if (neededFuel <= 0) {
        return 0
    } else {
        // because recursion is fun
        return neededFuel + calculateFuel(neededFuel)
    }
}

fun main(args : Array<String>) {
    var totalFuel = 0

//    part 1
//    File(args.first()).forEachLine { totalFuel += Math.floorDiv(it.toInt(), 3) - 2 }
//    println(totalFuel)

    File(args.first()).forEachLine { totalFuel += calculateFuel(it.toInt()) }
    println(totalFuel)
}