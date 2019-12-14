import java.io.File
import kotlin.math.max

// FIXME this implementation is NOT thread safe!
class IntCodeMachine(val rom: List<Int>, private var ip: Int = 0) {
    private var running = false
    private var ram = rom.toMutableList()
    private var diagnosticCode = Int.MIN_VALUE
    private var valid = 0
    private var errors = 0

    // TODO might move to strings
    enum class Intcodes(val opcode: Int) {
        END(99),
        ADD(1),
        MUL(2),
        SAV(3),
        GET(4),
        JIT(5),
        JIF(6),
        LTN(7),
        EQL(8);

        companion object {
            const val OPCODE_LENGTH = 2
        }
    }

    enum class Parameter(val mode: Int) {
        POSITION(0),
        IMMEDIATE(1);
    }


    // FIXME this might not work (we might need some logic to check if the last parameter should be in position or not!)
    private fun fromParameterMode(modes: String, num: Int, addressLast: Boolean = true): List<Int> {

        println("modes $modes")
        println(ram.subList(ip + 1, ip + num + 1) )

        val values = modes.reversed().mapIndexed{ idx, mode ->
            when (Character.getNumericValue(mode)) { // just using .toInt() returns the ascii value
                Parameter.POSITION.mode -> ram[ram[ip + idx + 1]]
                Parameter.IMMEDIATE.mode -> ram[ip + idx + 1]
                else -> throw IllegalArgumentException("Invalid parameter mode")
            }
        }.toMutableList()

        for (i in values.size until num - 1) { // num - 1 is excluded
            values.add(ram[ram[ip + i + 1]]) // get the missing parameters in position mode
        }

        if (values.size < num) {
            if (addressLast) {
                // last is just a dest address, so only return the immediate value
                values.add(ram[ip + num])
            } else {
                // last can be either immediate or positional, so we need to test for that
                // zero is implied if there isn't anything there
                values.add(when (Character.getNumericValue(modes.elementAtOrElse(num - 1) { '0' })) { // just using .toInt() returns the ascii value
                    Parameter.POSITION.mode -> ram[ram[ip + num]]
                    Parameter.IMMEDIATE.mode -> ram[ip + num]
                    else -> throw IllegalArgumentException("Invalid parameter mode")
                })
            }
        }

        println(values)

        // make it immutable
        return values.toList()
    }

    private fun handleEnd() {
        running = false
        ip++;
    }

    private fun handleAdd(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)
        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2]

        ram[dest] = first + second
        ip += 4
    }

    private fun handleMul(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)

        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2]

        ram[dest] = first * second
        ip += 4
    }

    // default value of 1 because that's what our program is calling for!
    private fun handleSave(input: Int) {
        // TODO will this ever be immediate?
        val address = ram[ip  + 1]
        ram[address] = input
        ip += 2
    }

    private fun handleGet(paramModes: String) {
        // TODO will this ever be immediate?
        val output = fromParameterMode(paramModes, 1, false).first()
//        println(ram.subList(ip, 47))
//
//        println(ram.subList(ip, ip + 3))

        ip += 2

        if (ram[ip] == Intcodes.END.opcode) {
//            println("we're here... oops")
            diagnosticCode = output
        } else if (output == 0) {
            println(output)
            println("all good")
            valid++
        } else {
            println(output)
            println("something went wrong!")
            errors++
        }
    }

    private fun handleJumpIfTrue(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 2, false)

        val test = parameters[0]
        val jumpTo = parameters[1]

        ip = if (test != 0) jumpTo else ip + 3

    }

    private fun handleJumpIfFalse(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 2, false)

        val test = parameters[0]
        val jumpTo = parameters[1]

        ip = if (test == 0) jumpTo else ip + 3
    }

    private fun handleLessThan(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)

        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2]

        ram[dest] = if (first < second) 1 else 0

        ip += 4
    }

    private fun handleEquals(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)

        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2]

        ram[dest] = if (first == second) 1 else 0

        ip += 4
    }

    fun run(initialValues: List<Pair<Int, Int>> = emptyList(), input: Int = 0): Int {
        // TODO we might need to reset more stuff!!
        // TODO do we want a reset instead of this?
        // first, reset the ip and running flag
        // (do we want to be able to configure the start value?)
        ip = 0
        running = true

        // next, reset the ram and provide any modifications
        ram = rom.toMutableList()
        for ((pos, value) in initialValues) {
            ram[pos] = value
        }

        // now, run the machine
        while(running) {

//            println(ram)
//            println(ram.subList(ip, ip + 3))

            val inst = ram[ip].toString()

            val parameterModes = inst.take(max(0, inst.length - Intcodes.OPCODE_LENGTH))

//            println(inst)

            println("opcode ${inst.takeLast(Intcodes.OPCODE_LENGTH)}")

            when (inst.takeLast(Intcodes.OPCODE_LENGTH).toInt()) {
                Intcodes.ADD.opcode -> handleAdd(parameterModes)
                Intcodes.MUL.opcode -> handleMul(parameterModes)
                Intcodes.SAV.opcode -> handleSave(input)
                Intcodes.GET.opcode -> handleGet(parameterModes)
                Intcodes.END.opcode -> handleEnd()
                Intcodes.JIT.opcode -> handleJumpIfTrue(parameterModes)
                Intcodes.JIF.opcode -> handleJumpIfFalse(parameterModes)
                Intcodes.LTN.opcode -> handleLessThan(parameterModes)
                Intcodes.EQL.opcode -> handleEquals(parameterModes)
            }
        }

//        println(ram)

        return diagnosticCode
    }

//    fun diagnosticCode(): Int {
//        return diagnosticCode
//    }
}

fun main(args: Array<String>) {
    // Part 2 test cases
//    val input1 = "3,9,8,9,10,9,4,9,99,-1,8".split(",").map { it.toInt() }
//    println(IntCodeMachine(input1).run(input=1)) // o
//    println(IntCodeMachine(input1).run(input=8)) // 1
//
//    val input2 = "3,9,7,9,10,9,4,9,99,-1,8".split(",").map { it.toInt() }
//    println(IntCodeMachine(input2).run(input=1)) // 1
//    println(IntCodeMachine(input2).run(input=8)) // 0
//
//    val input3 = "3,3,1108,-1,8,3,4,3,99".split(",").map { it.toInt() }
//    println(IntCodeMachine(input3).run(input=1)) // 0
//    println(IntCodeMachine(input3).run(input=8)) // 1
//
//    val input4 = "3,3,1107,-1,8,3,4,3,99".split(",").map { it.toInt() }
//    println(IntCodeMachine(input4).run(input=1)) // 1
//    println(IntCodeMachine(input4).run(input=8)) // 0
//
//    val input5 = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",").map { it.toInt() }
//    println(IntCodeMachine(input5).run(input=0)) // 0
//    println(IntCodeMachine(input5).run(input=8)) // 1
//
//    val input6 = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(",").map { it.toInt() }
//    println(IntCodeMachine(input6).run(input=0)) // 0
//    println(IntCodeMachine(input6).run(input=8)) // 1
//
//    val input7 = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",").map { it.toInt() }
//    println(IntCodeMachine(input7).run(input=0)) // 999
//    println(IntCodeMachine(input7).run(input=8)) // 1000
//    println(IntCodeMachine(input7).run(input=10)) // 1001


//    val dum = "1,0,3,3,1005,2,10,5,1,0,4,1,99".split(",").map {it.toInt()}
//    println(IntCodeMachine(dum).run())

    val input = File(args.first()).readText().trim().split(",").map{ it.toInt() }
    println(IntCodeMachine(input).run(input=5))  // input was 1 for part 1
}
