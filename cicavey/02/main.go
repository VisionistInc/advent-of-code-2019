package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const (
	opAdd = 1
	opMul = 2
	opEnd = 99
)

type opcodeFunction = func(m *intCodeMachine)

func opAddFunc(m *intCodeMachine) {
	dstLoc := m.ram[m.ip+3]
	op1Loc := m.ram[m.ip+1]
	op2Loc := m.ram[m.ip+2]
	m.ram[dstLoc] = m.ram[op1Loc] + m.ram[op2Loc]
	m.ip += 4
}

func opMulFunc(m *intCodeMachine) {
	dstLoc := m.ram[m.ip+3]
	op1Loc := m.ram[m.ip+1]
	op2Loc := m.ram[m.ip+2]
	m.ram[dstLoc] = m.ram[op1Loc] * m.ram[op2Loc]
	m.ip += 4
}

func opEndFunc(m *intCodeMachine) {
	m.running = false
	m.ip++
}

var opMap = map[int]opcodeFunction{
	opAdd: opAddFunc,
	opMul: opMulFunc,
	opEnd: opEndFunc,
}

type intCodeMachine struct {
	rom     []int
	ram     []int
	running bool
	ip      int
	// TODO registers, pointers/indirection, offsets. I know it's coming.
}

func newIntCodeMachine(rom []int) *intCodeMachine {
	return &intCodeMachine{
		rom: rom,
		ram: make([]int, len(rom)),
	}
}

func (m *intCodeMachine) reset() {
	copy(m.ram, m.rom)
	m.ip = 0
}

func (m *intCodeMachine) patch(noun, verb int) {
	// Patch
	m.ram[1] = noun
	m.ram[2] = verb
}

func (m *intCodeMachine) run() {
	m.running = true
	for m.running {
		// fetch
		op := m.fetch()
		// decode
		opMap[op](m)
	}
}

func (m *intCodeMachine) fetch() int {
	return m.ram[m.ip]
}

func main() {
	content, _ := ioutil.ReadFile("input.txt")
	opcodeStrs := strings.Split(string(content), ",")
	rom := make([]int, len(opcodeStrs))
	for i, s := range opcodeStrs {
		v, _ := strconv.Atoi(s)
		rom[i] = v
	}

	m := newIntCodeMachine(rom)

	m.reset()
	m.patch(12, 2)
	m.run()

	fmt.Println("Part 1", m.ram[0])

terminate:
	for noun := 0; noun <= 99; noun++ {
		for verb := 0; verb <= 99; verb++ {
			m.reset()
			m.patch(noun, verb)
			m.run()
			if 19690720 == m.ram[0] {
				fmt.Println("Part 2", 100*noun+verb)
				break terminate
			}
		}
	}
}
