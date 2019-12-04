var fs = require('fs');

const getMethod = (startLoc, symbol) => {
  switch (symbol) {
    case 'U':
      return (key, idx) => [startLoc[0], startLoc[1] + idx + 1]
    case 'D':
      return (key, idx) => [startLoc[0], startLoc[1] - idx - 1]

    case 'L':
      return (key, idx) => [startLoc[0] - idx - 1, startLoc[1]]

    case 'R':
      return (key, idx) => [startLoc[0] + idx + 1, startLoc[1]]
  }
}
var contents = fs.readFileSync('input.txt', 'utf8');

const lineArray = contents.split('\n')

const strArray = contents.split(',')

let points = []

let loc = [0, 0]

const pointArray = strArray.map(key => {
  const num = Number(key.substr(1))
  const newArray = Array.apply(null, Array(num)).map(getMethod(loc, key[0]))

  points = [...points, ...newArray]
  loc = points[points.length]
})

const intersections = pointArray[0].filter(value => -1 !== pointArray[1].indexOf(value))
