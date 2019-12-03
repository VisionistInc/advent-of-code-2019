var fs = require('fs');

var contents = fs.readFileSync('input.txt', 'utf8');
const strArray = contents.split(',')

const intArray = strArray.map(key => Number(key))

intArray[1] = 12
intArray[2] = 2

for (let i = 0; true; i = i + 4) {
  const opCode = intArray[i]
  switch (opCode) {
    case 1:
      intArray[intArray[i + 3]] = intArray[intArray[i + 1]] + intArray[intArray[i + 2]]
      break;
    case 2:
      intArray[intArray[i + 3]] = intArray[intArray[i + 1]] * intArray[intArray[i + 2]]
      break;
    case 99:
      console.log(intArray[0])
      process.exit()
  }
}