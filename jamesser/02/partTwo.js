var fs = require('fs');

var contents = fs.readFileSync('input.txt', 'utf8');
const strArray = contents.split(',')

const intArray = strArray.map(key => Number(key))

const runProgram = (noun, verb, array) => {
  const newArray = [...array]
  newArray[1] = noun
  newArray[2] = verb
  for (let i = 0; true; i = i + 4) {
    const opCode = newArray[i]
    switch (opCode) {
      case 1:
        newArray[newArray[i + 3]] = newArray[newArray[i + 1]] + newArray[newArray[i + 2]]
        break;
      case 2:
        newArray[newArray[i + 3]] = newArray[newArray[i + 1]] * newArray[newArray[i + 2]]
        break;
      case 99:
        return newArray[0]
    }
  }
}

let testValue = 19690720

for (let n = 0; n < 100; n = n + 1) {
  for (let v = 0; v < 100; v = v + 1) {
    if (testValue == runProgram(n, v, intArray))
      console.log(n * 100 + v)
  }
}