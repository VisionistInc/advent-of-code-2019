import java.io.File;


fun main(args : Array<String>) {
    val input = File(args.first())
    println("Solution 1: ${solution1(input)}")
    println("Solution 2: ${solution2(input)}")
}

private fun solution1(input: File) :Int {
    var machineList = input.readLines().first().split(",").map { it.trim() }.map{ it.toInt()}.toMutableList()    
    loop@ for (x in 0..machineList.size step 4) {
        when (machineList.get(x)) {
            1 -> machineList.set(machineList.get(x+3), machineList.get(machineList.get(x+1)) + machineList.get(machineList.get(x+2)))
            2 -> machineList.set(machineList.get(x+3), machineList.get(machineList.get(x+1)) * machineList.get(machineList.get(x+2)))
            99 -> break@loop
        }
    }
    return machineList.get(0)
}

private fun solution2(input: File) :Int {
    val finalOutputVal = 19690720
    val originalMachineList = input.readLines().first().split(",").map { it.trim() }.map{ it.toInt()}.toMutableList()    

    for (noun in 0..99) {
        for (verb in 0..99) {
            var machineList = originalMachineList.toMutableList()
            machineList.set(1, noun)
            machineList.set(2, verb)
            loop@ for (x in 0..machineList.size step 4) {
                when (machineList.get(x)) {
                    1 -> machineList.set(machineList.get(x+3), machineList.get(machineList.get(x+1)) + machineList.get(machineList.get(x+2)))
                    2 -> machineList.set(machineList.get(x+3), machineList.get(machineList.get(x+1)) * machineList.get(machineList.get(x+2)))
                    99 -> break@loop
                }
            }

             if (machineList.get(0) == finalOutputVal) {
                 return (100 * noun + verb)
             }
        }
    }

    return 0 // noot found but need a return value
}