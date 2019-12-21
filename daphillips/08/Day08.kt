import java.io.File

enum class PixelColor(val digit: Char) {
    BLACK('0'),
    WHITE('1'),
    TRANS('2')
}

fun main(args: Array<String>) {
    val imageWidth = 25
    val imageHeight = 6

    val pixelsInLayer = imageHeight * imageWidth

    // read the input and split by the number of pixels in layer
    val input = File(args.first()).readText().trim().chunked(pixelsInLayer)

    // !! enforces non-null (throws npe if not null)
    val smallest = input.minBy { it.count { digit -> digit == '0' } }!!
    println(smallest.count { it == '1' } * smallest.count { it == '2' })

    // initialize the array to 2 (transparent)
    val result: Array<Char> = Array(pixelsInLayer) { PixelColor.TRANS.digit }

    for (line in input) {
        result.withIndex().forEach { (index, value) ->
            if (value == PixelColor.TRANS.digit) {
                result[index] = line[index]
            }
        }
    }

    // for each row, print the unicode full if white or a space if black
    result.toList().chunked(imageWidth).forEach{ row -> row.forEach {
            print(if (it == PixelColor.WHITE.digit) "\u2588" else " ")
        }
        // done row; don't forget to provide newline!
        print("\n")
    }
}
