import java.io.File

fun hasDouble(digits: List<Char>): Boolean {
    for (i in 0 until digits.size - 1) { // stops 1 short of last char so we don't compare outside of String
        if (digits[i] == digits[i + 1] && digits.count { it == digits[i] } == 2) { // count check is part 2
            return true
        }
    }
    return false
}

fun main(args: Array<String>) {
    val input = File(args.first()).readText().trim().split('-').map { it.toInt() }
    val bounds = input.first()..input.last()

    val availablePasswords = bounds.map { it.toString().toList() }
        .filter { it.sorted() == it }
        .filter { hasDouble(it) }
        .count()

    println(availablePasswords)
}
