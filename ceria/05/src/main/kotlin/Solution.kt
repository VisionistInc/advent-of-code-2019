import java.io.File;


fun main(args : Array<String>) {
    val input = File(args.first())
    println("Solution 1: ${solution1(input)}")
    println("Solution 2: ${solution2(input)}")
}

private fun solution1(input: File) :Int {
    var machineList = input.readLines().first().split(",").map { it.trim() }.map{ it.toInt()}.toMutableList()    
    return intComputer(machineList, 1).dropWhile{ it == 0 }.first()
}

private fun solution2(input: File) :Int {
    var machineList = input.readLines().first().split(",").map { it.trim() }.map{ it.toInt()}.toMutableList()    
    return intComputer(machineList, 5).dropWhile{ it == 0 }.first()
}

private fun intComputer(machineList: MutableList<Int>, startValue: Int) :List<Int> {
    val output = mutableListOf<Int>()

    var pointer = 0
    while (true) {
        val instr = machineList.get(pointer) 
        val mode = instr / 100
        when (instr % 100) {
            1 -> { 
                machineList.set(machineList.get(pointer + 3), (getValuesForMode(machineList, pointer, 1, mode) + getValuesForMode(machineList, pointer, 2, mode)))
                pointer += 4
            }

            2 -> {
                machineList.set(machineList.get(pointer + 3), (getValuesForMode(machineList, pointer, 1, mode) * getValuesForMode(machineList, pointer, 2, mode)))
                pointer += 4
            }

            3 -> { 
                machineList.set(machineList.get(pointer + 1), startValue)
                pointer += 2
            }

            4 -> { 
                output.add(getValuesForMode(machineList, pointer, 1, mode))
                pointer += 2
            }

            5 -> { 
                pointer = if (getValuesForMode(machineList, pointer, 1, mode) != 0)
                    getValuesForMode(machineList, pointer, 2, mode) else pointer + 3
            }

            6 -> { 
                pointer = if (getValuesForMode(machineList, pointer, 1, mode) == 0) 
                     getValuesForMode(machineList, pointer, 2, mode) else pointer + 3
            }

            7 -> {   
                machineList.set(machineList.get(pointer + 3), 
                    if (getValuesForMode(machineList, pointer, 1, mode) < getValuesForMode(machineList, pointer, 2, mode)) 1 else 0 )
                pointer += 4
            }
            8 -> { 
                machineList.set(machineList.get(pointer + 3), 
                    if (getValuesForMode(machineList, pointer, 1, mode) == getValuesForMode(machineList, pointer, 2, mode)) 1 else 0 )
                pointer += 4
            }
            99 -> { 
                return output.toList()
            }
        }
    }
}

fun getValuesForMode(machineList: List<Int>, pointer: Int, argNum: Int, m: Int): Int {
    var mode = m
    repeat(argNum - 1) {
        mode /= 10
    }
    mode %= 10

    when (mode) {
        0 -> return machineList.get(machineList.get(pointer + argNum))
        1 -> return machineList.get(pointer + argNum)
    }

    return -1 // Can't happen
}