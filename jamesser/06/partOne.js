var fs = require('fs');

var contents = fs.readFileSync('input.txt', 'utf8');

const orbitArray = contents.split('\r\n')

const orbitMap = orbitArray.reduce((total, orbit) => {
  const [home, moon] = orbit.split(')')
  total[moon] = home
  return total
}, {})


const count = Object.keys(orbitMap).reduce((total, moon) => {
  let tmpTotal = total
  let tmpMoon = moon;

  while (orbitMap[tmpMoon] != null) {
    tmpTotal = tmpTotal + 1
    tmpMoon = orbitMap[tmpMoon]
  }

  return tmpTotal
}, 0)

console.log("Total:", count)