var fs = require('fs');

var contents = fs.readFileSync('input.txt', 'utf8');

const orbitArray = contents.split('\r\n')

const orbitMap = orbitArray.reduce((total, orbit) => {
  const [home, moon] = orbit.split(')')
  total[moon] = home
  return total
}, {})


const youOrbit = []
const sanOrbit = []

let tmpMoon = 'YOU'
while (orbitMap[tmpMoon] != null) {
  tmpMoon = orbitMap[tmpMoon]
  youOrbit.push(tmpMoon)
}

tmpMoon = 'SAN'
while (orbitMap[tmpMoon] != null) {
  tmpMoon = orbitMap[tmpMoon]
  sanOrbit.push(tmpMoon)
}

const commonMoon = youOrbit.find(moon => sanOrbit.indexOf(moon) != -1)

console.log(youOrbit.indexOf(commonMoon) + sanOrbit.indexOf(commonMoon))