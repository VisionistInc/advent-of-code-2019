var fs = require('fs');

var contents = fs.readFileSync('input.txt', 'utf8');

const isBetween = (v, a, b) => (v - a) * (v - b) <= 0

const lineArray = contents.split('\n')

const strArray = lineArray.map(key => key.split(','))

let loc = [0, 0]

const pointArray = strArray.map(stuff => {
  let x = 0
  let y = 0
  return stuff.reduce((total, key) => {
    let num = Number(key.substr(1))
    switch (key[0]) {
      case 'U':
        y = y + num
        break;
      case 'D':
        y = y - num
        break;
      case 'L':
        x = x - num
        break;
      case 'R':
        x = x + num
        break
    }
    total[total.length] = [x, y]
    return total
  }, [])
})

const intersections = []
for (let pa1Idx = 0; pa1Idx < pointArray[0].length - 1; pa1Idx = pa1Idx + 1) {
  let wire1Start = pointArray[0][pa1Idx]
  let wire1End = pointArray[0][pa1Idx + 1]
  let wire1IsHorizontal = wire1Start[1] === wire1End[1]

  for (let pa2Idx = 0; pa2Idx < pointArray[1].length - 1; pa2Idx = pa2Idx + 1) {

    let wire2Start = pointArray[1][pa2Idx]
    let wire2End = pointArray[1][pa2Idx + 1]
    let wire2IsHorizontal = wire2Start[1] === wire2End[1]

    if (wire1IsHorizontal === wire2IsHorizontal)
      continue;

    if (wire1IsHorizontal && isBetween(wire2Start[0], wire1Start[0], wire1End[0]) && isBetween(wire1Start[1], wire2Start[1], wire2End[1])) {
      intersections.push([wire2Start[0], wire1Start[1]])
    }

    if (!wire1IsHorizontal && isBetween(wire2Start[1], wire1Start[1], wire1End[1]) && isBetween(wire1Start[0], wire2Start[0], wire2End[0])) {
      intersections.push([wire1Start[0], wire2Start[1]])
    }
  }
}

console.log("Processing distances")
const distances = intersections.map(key => Math.abs(key[0]) + Math.abs(key[1])).sort((a, b) => a - b)

console.log("Shortest Distance:")
console.log(distances[0])
