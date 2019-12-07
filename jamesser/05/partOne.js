var fs = require('fs');
var readlineSync = require('readline-sync')

var contents = fs.readFileSync('input.txt', 'utf8');
const strArray = contents.split(',')

let intArray = strArray.map(key => Number(key))

for (let i = 0; true;) {
  const instruction = intArray[i]
  const instructionNum = Number(instruction)

  const opCode = instructionNum % 100
  const param1Type = Math.floor((instructionNum / 100) % 10)
  const param2Type = Math.floor((instructionNum / 1000) % 10)

  const val1 = param1Type === 1 ? intArray[i + 1] : intArray[intArray[i + 1]]
  const val2 = param2Type === 1 ? intArray[i + 2] : intArray[intArray[i + 2]]
  const outLoc = intArray[i + 3]
  let incAmount = 0
  //console.log("I Pos", i, "inst", instructionNum, "op", opCode, "1t", param1Type, "2t", param2Type, "v1", val1, "v2", val2, "out", outLoc)
  switch (opCode) {
    case 1:
      intArray[intArray[i + 3]] = val1 + val2
      incAmount = 4
      break;
    case 2:
      intArray[intArray[i + 3]] = val1 * val2
      incAmount = 4
      break;
    case 3:
      const val = readlineSync.question("Input?")
      intArray[intArray[i + 1]] = Number(val)
      incAmount = 2
      break;
    case 4:
      console.log(val1)
      incAmount = 2
      break;
    case 5:
      const isTrue = val1 !== 0
      if (isTrue)
        i = val2
      else
        incAmount = 3
      break;
    case 6:
      const isFalse = val1 === 0
      if (isFalse)
        i = val2
      else
        incAmount = 3
      break;
    case 7:
      intArray[intArray[i + 3]] = val1 < val2 ? 1 : 0
      incAmount = 4
      break;
    case 8:
      intArray[intArray[i + 3]] = val1 === val2 ? 1 : 0
      incAmount = 4
      break;
    case 99:
      console.log(intArray[0])
      process.exit()
      break;
  }

  if (outLoc !== i)
    i = i + incAmount
}