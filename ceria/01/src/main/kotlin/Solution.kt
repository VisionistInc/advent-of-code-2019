import java.io.File;


fun main(args : Array<String>) {
    val input = File(args.first())
    println("Solution 1: ${solution1(input)}")
    println("Solution 2: ${solution2(input)}")
}

private fun solution1(input: File) :Int {
    return input.readLines().map{ (it.toInt() / 3) - 2 }.sum()
}

private fun solution2(input: File) :Int {
    return input.readLines().map{ totalFuelForModule(it.toInt(), 0) }.sum()
}

private fun totalFuelForModule(module :Int, total :Int) :Int {
    val newTotal  = (module / 3) - 2
    return when(newTotal > 0) {
        true -> totalFuelForModule(newTotal, total + newTotal)
        false -> total
    }
}