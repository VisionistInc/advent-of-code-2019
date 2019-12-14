import java.io.File

// I really could have just made this its own class that wraps a map, but these extension functions were neat to write so ¯\_(ツ)_/¯

// extend default MutableMap interface to allow for this conditional insert
// (means i have to type less than if i made a wrapper class)
// limited to our problem scope (list of children keyed by the parent's name)
private fun MutableMap<String, MutableList<String>>.insert(parent: String, name: String) {
    // add an entry for the orbit we're adding (in case it has future direct orbits)
    putIfAbsent(name, mutableListOf())
    // append the new orbit if we have an existing map, or create the map now with this orbit
    compute(parent) { _, directOrbits -> directOrbits?.also { it.add(name) } ?: mutableListOf(name) }
}

private fun Map<String, MutableList<String>>.recursiveCount(root: String = "COM", parentSum: Int = 0): Int {
    // everything directly orbiting us is one step farther from COM
    // we need to add our distance to the sum of distances of things directly orbiting us 
    // use of !! because if an entry is null, something went wrong
    return get(root)!!.stream().mapToInt { recursiveCount(it, parentSum + 1) }.sum() + parentSum
}

private fun MutableMap<String, MutableList<String>>.closestParent(
    parent: String = "COM",
    child1: String = "YOU",
    child2: String = "SAN"
): String {
    // see what our best child is
    // since children only have 1 direct orbit (us) there is at most one child that can lead us to child1 and child2
    val bestChild = get(parent)!!.stream().filter { distanceTo(child1, it) != 0 && distanceTo(child2, it) != 0 }
        .findFirst().orElse("")

    return if (bestChild.isEmpty()) parent else closestParent(bestChild, child1, child2)
}

private fun MutableMap<String, MutableList<String>>.distanceTo(child: String, parent: String = "COM"): Int {
    // if the value of parent is null, we have an input problem
    val children = get(parent)!!
    return when {
        children.contains(child) -> 1
        children.isEmpty() -> 0
        else -> {
            val sum = children.stream().mapToInt { distanceTo(child, it) }.sum()
            // only step if one of our children had the thing we were looking for
            // NOTE implicit return
            if (sum == 0) sum else sum + 1
        }
    }
}

fun main(args: Array<String>) {
//    // test input
//    var testInput = "COM)B\n" +
//            "B)C\n" +
//            "C)D\n" +
//            "D)E\n" +
//            "E)F\n" +
//            "B)G\n" +
//            "G)H\n" +
//            "D)I\n" +
//            "E)J\n" +
//            "J)K\n" +
//            "K)L"
//
//    var testOrbitMap: MutableMap<String, MutableList<String>> = mutableMapOf()
//    testInput.split("\n").map { it.split(")") }.forEach { testOrbitMap.insert(it[0], it[1])}
//    println(testOrbitMap.recursiveCount())
//
//    // part 2 tests
//    testInput = "\n" +
//    "K)YOU\n" +
//    "I)SAN)"
//    testOrbitMap = mutableMapOf()
//    testInput.split("\n").map { it.split(")") }.forEach { testOrbitMap.insert(it[0], it[1])}
//
//    val testClosestParent = testOrbitMap.closestParent()
//    val testDistanceToYou = testOrbitMap.distanceTo("YOU", testClosestParent) - 1
//    val testDistanceToSan = testOrbitMap.distanceTo("SAN", testClosestParent) - 1
//    println(testDistanceToYou + testDistanceToSan)

    val orbits: MutableMap<String, MutableList<String>> = mutableMapOf()
    File(args.first()).readLines().map { it.split(")") }.forEach { orbits.insert(it[0], it[1]) }
    println(orbits.recursiveCount())

    val closestParent = orbits.closestParent()
    val distanceToYou = orbits.distanceTo("YOU", closestParent) - 1
    val distanceToSan = orbits.distanceTo("SAN", closestParent) - 1
    println(distanceToYou + distanceToSan)
}
