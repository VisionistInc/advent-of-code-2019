package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	opAdd = 1
	opMul = 2
	opInp = 3
	opOut = 4
	opJCT = 5 // Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
	opJCF = 6 // Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
	opCLT = 7 // Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
	opCEQ = 8 // Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
	opEnd = 99
)

type opcodeFunction = func(m *intCodeMachine)

func pFlag(op int, p int) int {
	return op / int(math.Pow10(1+p)) % 10
}

func opAddFunc(m *intCodeMachine) {
	op1 := m.resolve(1)
	op2 := m.resolve(2)
	op3 := m.ram[m.ip+3]
	m.ram[op3] = op1 + op2
	m.ip += 4
}

func opMulFunc(m *intCodeMachine) {
	op1 := m.resolve(1)
	op2 := m.resolve(2)
	op3 := m.ram[m.ip+3]
	m.ram[op3] = op1 * op2
	m.ip += 4
}

func opInpFunc(m *intCodeMachine) {
	dstLoc := m.ram[m.ip+1]
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print(dstLoc, " << ")
	scanner.Scan()
	v, _ := strconv.Atoi(scanner.Text())
	m.ram[dstLoc] = v
	m.ip += 2
}

func opOutFunc(m *intCodeMachine) {
	op1 := m.resolve(1)
	fmt.Println(op1)
	m.ip += 2
}

func opJCTFunc(m *intCodeMachine) {
	op1 := m.resolve(1)
	op2 := m.resolve(2)

	if op1 != 0 {
		m.ip = op2
		return
	}

	m.ip += 3
}

func opJCFFunc(m *intCodeMachine) {
	op1 := m.resolve(1)
	op2 := m.resolve(2)

	if op1 == 0 {
		m.ip = op2
		return
	}

	m.ip += 3
}

func opCLTFunc(m *intCodeMachine) {
	op1 := m.resolve(1)
	op2 := m.resolve(2)
	op3 := m.ram[m.ip+3]

	if op1 < op2 {
		m.ram[op3] = 1
	} else {
		m.ram[op3] = 0
	}

	m.ip += 4
}

func opCEQFunc(m *intCodeMachine) {
	op1 := m.resolve(1)
	op2 := m.resolve(2)
	op3 := m.ram[m.ip+3]

	if op1 == op2 {
		m.ram[op3] = 1

	} else {
		m.ram[op3] = 0
	}

	m.ip += 4
}

func opEndFunc(m *intCodeMachine) {
	m.running = false
	m.ip++
}

var opMap = map[int]opcodeFunction{
	opAdd: opAddFunc,
	opMul: opMulFunc,
	opInp: opInpFunc,
	opOut: opOutFunc,
	opJCT: opJCTFunc,
	opJCF: opJCFFunc,
	opCLT: opCLTFunc,
	opCEQ: opCEQFunc,
	opEnd: opEndFunc,
}

type intCodeMachine struct {
	rom     []int
	ram     []int
	running bool
	ip      int
	op      int
}

func newIntCodeMachine(rom []int, ramSize int) *intCodeMachine {
	if ramSize <= 0 {
		ramSize = len(rom)
	}
	m := &intCodeMachine{
		rom: rom,
		ram: make([]int, ramSize),
	}
	m.reset()
	return m
}

// resolve an operand relative to current opcode and IP
func (m *intCodeMachine) resolve(pos int) int {
	// resolve against current op
	operand := m.ram[m.ip+pos]
	f1 := pFlag(m.op, pos)
	if f1 == 0 {
		operand = m.ram[operand]
	}
	return operand
}

func (m *intCodeMachine) reset() {
	// zero fill ram
	for index := range m.ram {
		m.ram[index] = 0
	}
	copy(m.ram, m.rom)
	m.ip = 0
}

func (m *intCodeMachine) run() {
	m.running = true
	for m.running {
		// fetch
		m.op = m.fetch()
		// decode/exec
		opMap[m.op%100](m)
	}
}

func (m *intCodeMachine) fetch() int {
	return m.ram[m.ip]
}

func (m intCodeMachine) dumpRAM() {
	for i, v := range m.ram {
		if i%16 == 0 {
			fmt.Println()
		}
		fmt.Printf("%4d ", v)
	}
	fmt.Println()
}

func main() {
	content, _ := ioutil.ReadFile("input.txt")
	opcodeStrs := strings.Split(string(content), ",")
	rom := make([]int, len(opcodeStrs))
	for i, s := range opcodeStrs {
		v, _ := strconv.Atoi(s)
		rom[i] = v
	}
	m := newIntCodeMachine(rom, -1)
	m.run()
}
