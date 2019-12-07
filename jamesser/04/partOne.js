

const start = 136760
const end = 595730

const isNotUnique = (value) => {
  const strVal = `${value}`
  valueSplit = strVal.split('')

  const set = new Set(valueSplit)
  return (Array.from(set)).length != valueSplit.length
}

const loop = (digits) => {
  if (digits.length === 6)
    return [digits]
  let lastDigit = digits[digits.length - 1]
  let outArray = []
  for (let i = lastDigit; i < 10; i++)
    outArray = [...outArray, ...loop([...digits, i])]

  return outArray
}

let count = 0
for (let i = Math.floor(start / 100000); i < Math.floor(end / 100000) + 1; i++) {
  const loopVal = loop([i])
  const values = loopVal.map(digits => digits[0] * 100000 + digits[1] * 10000 + digits[2] * 1000 + digits[3] * 100 + digits[4] * 10 + digits[5])
  count = count + values.filter(value => value < end && value > start && isNotUnique(value)).length
}

console.log("Value Count:", count)