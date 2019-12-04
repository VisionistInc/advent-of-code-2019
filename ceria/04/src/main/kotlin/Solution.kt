import java.io.File;

fun main(args : Array<String>) {
    val input = File(args.first())
    println("Solution 1: ${solution1(input)}")
    println("Solution 2: ${solution2(input)}")
}

private fun solution1(input: File) :Int {
    val i = input.readLines().first().split("-")
    var start = i[0].toInt()
    return generateSequence { (start++).takeIf { it < i[1].toInt() } }
          .toMutableList().filter{ checkPassword(it) }.size
}

private fun solution2(input: File) :Int {
    val i = input.readLines().first().split("-")
    var start = i[0].toInt()
    return generateSequence { (start++).takeIf { it < i[1].toInt() } }
          .toMutableList().filter{ checkPassword(it) }.filter{ checkPasswordAgain(it) }.size
}

private fun checkPassword(candidate: Int) :Boolean {
    var divider = 100000
    var previous = 0
    var hasAdjacentMatch = false
   
    while ((candidate / divider) % 10  >= previous && divider > 1) {
        if ((candidate / divider) % 10 == previous){
            hasAdjacentMatch = true
        }

        previous = (candidate / divider) % 10
        divider = divider / 10
    }
   
    if (divider == 1) {
        if (candidate % 10 == previous || hasAdjacentMatch){
            return candidate % 10 >= previous
        }
    }
   
    return false
}

private fun checkPasswordAgain(candidate: Int) :Boolean {
    var divider = 100000
    var previous = 0
    var adjacents = mutableMapOf<Int, Int>()
  
   while (divider > 1) {
       var test = (candidate / divider) % 10
       if (test == previous) {
           if (adjacents.containsKey(test)) {
               var count = adjacents.get(test)!!
               count++
               adjacents.put(test, count)
           } else {
           adjacents.put(test, 2)
           }
       }
       previous = test
       divider = divider / 10
   }
  
   if (divider == 1) {
       var test = candidate % 10
       if (test == previous) {
           if (adjacents.containsKey(test)) {
               var count = adjacents.get(test)!!
               count++
               adjacents.put(test, count)
           } else {
           adjacents.put(test, 2)
           }
       }
   }
  
   val tooLarge = adjacents.filterValues{it > 2 }.size
   val justRight = adjacents.filterValues{it == 2 }.size
   if (tooLarge != 0 && tooLarge > justRight ) {
      return false
   }

   return true
}

