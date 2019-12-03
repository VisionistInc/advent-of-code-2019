var fs = require('fs');

var contents = fs.readFileSync('input.txt', 'utf8');
const lineArray = contents.split('\n')
console.log(lineArray.reduce((total, moduleWeight) => total + (Math.floor(Number(moduleWeight) / 3) - 2), 0))