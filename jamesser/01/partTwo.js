var fs = require('fs');

var contents = fs.readFileSync('input.txt', 'utf8');
const lineArray = contents.split('\n')

const getTotalWeight = (moduleWeight) => {
  const newWeight = Math.floor(moduleWeight / 3) - 2

  if (newWeight > 0)
    return newWeight + getTotalWeight(newWeight)

  return 0
}

console.log(lineArray.reduce((total, moduleWeight) => total + getTotalWeight(Number(moduleWeight)), 0))