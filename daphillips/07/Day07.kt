import java.io.File
import kotlin.math.max
import kotlin.streams.asStream

// FIXME this implementation is NOT thread safe!
class IntCodeMachine(private val rom: List<Long>, private val phaseSetting: Long, private var ip: Int = 0) {
    private var ram = rom.toMutableList()
    private var diagnosticCode = Long.MIN_VALUE
    private var usePhaseSetting = true
    private var state = RunningState.HALTED

    enum class RunningState {
        RUNNING, SLEEPING, HALTED
    }

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


    private fun fromParameterMode(modes: String, num: Int, addressLast: Boolean = true): List<Long> {

        val values = modes.reversed().mapIndexed{ idx, mode ->
            when (Character.getNumericValue(mode)) { // just using .toInt() returns the ascii value
                Parameter.POSITION.mode -> ram[ram[ip + idx + 1].toInt()]
                Parameter.IMMEDIATE.mode -> ram[ip + idx + 1]
                else -> throw IllegalArgumentException("Invalid parameter mode")
            }
        }.toMutableList()

        if (values.size < num) {
            for (i in values.size until num - 1) { // num - 1 is excluded
                values.add(ram[ram[ip + i + 1].toInt()]) // get the missing parameters in position mode
            }

            if (addressLast) {
                // last is just a dest address, so only return the immediate value
                values.add(ram[ip + num])
            } else {
                // last can be either immediate or positional, so we need to test for that
                // zero is implied if there isn't anything there
                values.add(when (Character.getNumericValue(modes.elementAtOrElse(num - 1) { '0' })) { // just using .toInt() returns the ascii value
                    Parameter.POSITION.mode -> ram[ram[ip + num].toInt()]
                    Parameter.IMMEDIATE.mode -> ram[ip + num]
                    else -> throw IllegalArgumentException("Invalid parameter mode")
                })
            }
        }

        // make it immutable
        return values.toList()
    }

    private fun handleEnd() {
        state = RunningState.HALTED
        ip++
    }

    private fun handleAdd(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)
        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2].toInt()

        ram[dest] = first + second
        ip += 4
    }

    private fun handleMul(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)

        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2].toInt()

        ram[dest] = first * second
        ip += 4
    }

    // default value of 1 because that's what our program is calling for!
    private fun handleInput(input: Long) {
        // TODO will this ever be immediate?
        val address = ram[ip  + 1].toInt()
        ram[address] = if (usePhaseSetting) phaseSetting else input
        usePhaseSetting = false
        ip += 2
    }

    private fun handleOutput(paramModes: String) {
        val output = fromParameterMode(paramModes, 1, false).first()

        ip += 2

        // TODO we need some logic to give an output but still run

        diagnosticCode = output
        if (ram[ip].toInt() != Intcodes.END.opcode) {
            state = RunningState.SLEEPING
        }

//         NOTE this is what we had before (part 1)
//        when {
//            ram[ip].toInt() == Intcodes.END.opcode -> {
//                diagnosticCode = output
//            }
//            output == 0L -> {
//                println(output)
//                println("all good")
//                valid++
//            }
//            else -> {
//                println(output)
//                println("something went wrong!")
//                errors++
//            }
//        }
    }

    private fun handleJumpIfTrue(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 2, false)

        val test = parameters[0]
        val jumpTo = parameters[1].toInt()

        ip = if (test != 0L) jumpTo else ip + 3

    }

    private fun handleJumpIfFalse(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 2, false)

        val test = parameters[0]
        val jumpTo = parameters[1].toInt()

        ip = if (test == 0L) jumpTo else ip + 3
    }

    private fun handleLessThan(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)

        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2].toInt()

        ram[dest] = if (first < second) 1 else 0

        ip += 4
    }

    private fun handleEquals(paramModes: String) {
        val parameters = fromParameterMode(paramModes, 3)

        val first = parameters[0]
        val second = parameters[1]
        val dest = parameters[2].toInt()

        ram[dest] = if (first == second) 1 else 0

        ip += 4
    }


    fun isHalted(): Boolean {
        return state == RunningState.HALTED
    }

    fun run(initialValues: List<Pair<Int, Long>> = emptyList(), input: Long = 0, reset: Boolean = true): Long {
        // TODO we might need to reset more stuff!!
        // TODO do we want a reset instead of this?
        // first, reset the ip and running flag
        // (do we want to be able to configure the start value?)

        // TODO conditionally reset
        if (reset) {
            ip = 0
            usePhaseSetting = true
            ram = rom.toMutableList()
        }

        state = RunningState.RUNNING

        // next, reset the ram and provide any modifications
        for ((pos, value) in initialValues) {
            ram[pos] = value
        }

        // now, run the machine
        while(state == RunningState.RUNNING) {

            val inst = ram[ip].toString()

            val parameterModes = inst.take(max(0, inst.length - Intcodes.OPCODE_LENGTH))

            when (inst.takeLast(Intcodes.OPCODE_LENGTH).toInt()) {
                Intcodes.ADD.opcode -> handleAdd(parameterModes)
                Intcodes.MUL.opcode -> handleMul(parameterModes)
                Intcodes.SAV.opcode -> handleInput(input)
                Intcodes.GET.opcode -> handleOutput(parameterModes)
                Intcodes.END.opcode -> handleEnd()
                Intcodes.JIT.opcode -> handleJumpIfTrue(parameterModes)
                Intcodes.JIF.opcode -> handleJumpIfFalse(parameterModes)
                Intcodes.LTN.opcode -> handleLessThan(parameterModes)
                Intcodes.EQL.opcode -> handleEquals(parameterModes)
            }
        }


        return diagnosticCode
    }

//    fun diagnosticCode(): Int {
//        return diagnosticCode
//    }
}

private fun runAmpCircuit(rom: List<Long>, phaseSettings: List<Long>, initialInput: Long = 0): Long {
    val ampA = IntCodeMachine(rom, phaseSettings[0])
    val ampB = IntCodeMachine(rom, phaseSettings[1])
    val ampC = IntCodeMachine(rom, phaseSettings[2])
    val ampD = IntCodeMachine(rom, phaseSettings[3])
    val ampE = IntCodeMachine(rom, phaseSettings[4])

    var outA = ampA.run(input=initialInput)
    var outB = ampB.run(input=outA)
    var outC = ampC.run(input=outB)
    var outD = ampD.run(input=outC)
    var outE = ampE.run(input=outD)

    while (!ampE.isHalted()) {
        outA = ampA.run(input=outE, reset=false)
        outB = ampB.run(input=outA, reset=false)
        outC = ampC.run(input=outB, reset=false)
        outD = ampD.run(input=outC, reset=false)
        outE = ampE.run(input=outD, reset=false)
    }

    return outE
}

// Taken from MarchinMoskala's `KotlinDiscreteMathToolkit library`
fun <T> List<T>.permutations(): Set<List<T>> = when {
    isEmpty() -> setOf()
    size == 1 -> setOf(listOf(get(0)))
    else -> {
        val element = get(0)
        drop(1).permutations().flatMap { sublist -> (0..sublist.size).map { i -> sublist.plusAt(i, element) } }.toSet()
    }
}

// also taken from MarchinMoskala's `KotlinDiscreteMathToolkit library`
internal fun <T> List<T>.plusAt(index: Int, element: T): List<T> = when {
    index !in 0..size -> throw Error("Cannot put at index $index because size is $size")
    index == 0 -> listOf(element) + this
    index == size -> this + element
    else -> dropLast(size - index) + element + drop(index)
}

fun main(args: Array<String>) {
//    val testInput1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(",").map { it.toInt() }
//
//    // each amp needs a copy of the ROM
//    val testAmpA1 = IntCodeMachine(testInput1,4)
//    val testOutA1 = testAmpA1.run(input=0)
//    val testAmpB1 = IntCodeMachine(testInput1, 3)
//    val testOutB1 = testAmpB1.run(input=testOutA1)
//    val testAmpC1 = IntCodeMachine(testInput1, 2)
//    val testOutC1 = testAmpC1.run(input=testOutB1)
//    val testAmpD1 = IntCodeMachine(testInput1, 1)
//    val testOutD1 = testAmpD1.run(input=testOutC1)
//    val testAmpE1 = IntCodeMachine(testInput1, 0)
//    println(testAmpE1.run(input=testOutD1))

//    val testInput2 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(",").map { it.toLong() }
//    println(runAmpCircuit(testInput2, listOf(9,8,7,6,5)))

    val input = File(args.first()).readText().trim().split(",").map{ it.toLong() }
    (5..9L).toList().permutations().parallelStream().mapToLong { runAmpCircuit(input, it) }.max().asLong.also{ println(it) }


}
