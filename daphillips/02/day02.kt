import java.io.File

enum class Intcodes(val code: Int) {
    END(99),
    ADD(1),
    MUL(2)
}

// part 2 solution
fun calculateResult(lines: MutableList<Int>, noun: Int, verb: Int): Int {
    var position = 0

    // update the initial conditions of the intcodes
    lines[1] = noun
    lines[2] = verb

    while(true) {
        val first = lines[position + 1]
        val second = lines[position + 2]
        val dest = lines[position + 3]
        when (lines[position]) {
            Intcodes.ADD.code -> lines[dest] = lines[first] + lines[second]
            Intcodes.MUL.code -> lines[dest] = lines[first] * lines[second]
            Intcodes.END.code -> return lines[0]
        }
        position += 4
    }
}

fun main(args: Array<String>) {
    val targetValue = 19690720

    // only read from the file once and clone later
    val linesMaster: List<Int> = File(args.first()).readText().trim().split(",").map{ it.toInt() }

    val pairs: MutableList<Pair<Int, Int>> = mutableListOf()

    // construct a list of all the possible matches
    for (i in 0..99) {
        for (j in 0..99) {
            pairs.add(Pair(i, j))
        }
    }

    // iterate over the pairs, and find the first (only) one that matches the target value
    // parallel because 10k values with a filter seems to fit the mold for a potential performance bump
    val result: Pair<Int, Int> = pairs.parallelStream().filter { calculateResult(linesMaster.toMutableList(), it.first, it.second) == targetValue }.findFirst().get()
    println(100 * result.first + result.second)
}


// part 1 solution
//fun main(args: Array<String>) {
//    var position = 0
//    val lines: MutableList<Int> = File(args.first()).readText().trim().split(",").map{ it.toInt() }.toMutableList()
//
//    // update the initial conditions of the intcodes
//    lines[1] = 12
//    lines[2] = 2
//
//    var exit = false
//
//    while(!exit) {
//        val first = lines[position + 1]
//        val second = lines[position + 2]
//        val dest = lines[position + 3]
//        when (lines[position]) {
//            Intcodes.ADD.code -> lines[dest] = lines[first] + lines[second]
//            Intcodes.MUL.code -> lines[dest] = lines[first] * lines[second]
//            Intcodes.END.code -> exit = true
//        }
//        position += 4
//    }
//
//    println(lines[0])
//}
