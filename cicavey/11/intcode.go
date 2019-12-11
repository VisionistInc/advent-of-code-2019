package main

import (
	"io/ioutil"
	"math"
	"strconv"
	"strings"
)

const (
	opAdd = 1
	opMul = 2
	opInp = 3
	opOut = 4
	opJCT = 5
	opJCF = 6
	opCLT = 7
	opCEQ = 8
	opRBO = 9
	opEnd = 99
)

type opcodeFunction = func(m *intCodeMachine)

func pFlag(op int, p int) int {
	return op / int(math.Pow10(1+p)) % 10
}

func opAddFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	op2 := m.resolveRead(2)
	op3 := m.resolveWrite(3)
	m.ram[op3] = op1 + op2
	m.ip += 4
}

func opMulFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	op2 := m.resolveRead(2)
	op3 := m.resolveWrite(3)
	m.ram[op3] = op1 * op2
	m.ip += 4
}

func opInpFunc(m *intCodeMachine) {
	op1 := m.resolveWrite(1)
	v, ok := m.stdin.pop()
	if !ok {
		m.running = false
		return
	}
	m.ram[op1] = v
	m.ip += 2
}

func opOutFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	m.stdout.push(op1)
	m.ip += 2
}

func opJCTFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	op2 := m.resolveRead(2)

	if op1 != 0 {
		m.ip = op2
		return
	}

	m.ip += 3
}

func opJCFFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	op2 := m.resolveRead(2)

	if op1 == 0 {
		m.ip = op2
		return
	}

	m.ip += 3
}

func opCLTFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	op2 := m.resolveRead(2)
	op3 := m.resolveWrite(3)

	if op1 < op2 {
		m.ram[op3] = 1
	} else {
		m.ram[op3] = 0
	}

	m.ip += 4
}

func opCEQFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	op2 := m.resolveRead(2)
	op3 := m.resolveWrite(3)
	if op1 == op2 {
		m.ram[op3] = 1

	} else {
		m.ram[op3] = 0
	}

	m.ip += 4
}

func opRBOFunc(m *intCodeMachine) {
	op1 := m.resolveRead(1)
	m.rb += op1
	m.ip += 2
}

func opEndFunc(m *intCodeMachine) {
	m.running = false
	m.halt = true
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
	opRBO: opRBOFunc,
	opEnd: opEndFunc,
}

type intCodeMachine struct {
	rom     []int
	ram     map[int]int
	running bool
	halt    bool
	ip      int
	op      int
	rb      int
	stdin   *pipe
	stdout  *pipe
}

func newIntCodeMachine(rom []int) *intCodeMachine {
	m := &intCodeMachine{
		rom:    rom,
		ram:    make(map[int]int),
		stdin:  &pipe{},
		stdout: &pipe{},
	}
	m.reset()
	return m
}

// resolve an operand relative to current opcode and IP
func (m *intCodeMachine) resolveRead(pos int) int {
	// resolve against current op
	operand := m.ram[m.ip+pos]
	f := pFlag(m.op, pos)
	if f == 0 {
		operand = m.ram[operand]
	}
	if f == 2 {
		operand = m.ram[m.rb+operand]
	}
	return operand
}

// resolve an operand relative to current opcode and IP
func (m *intCodeMachine) resolveWrite(pos int) int {
	// resolve against current op
	operand := m.ram[m.ip+pos]
	f := pFlag(m.op, pos)
	if f == 2 {
		operand = m.rb + operand
	}
	return operand
}

func (m *intCodeMachine) reset() {
	// clear ram
	m.ram = make(map[int]int)
	// copy rom into ram
	for i, v := range m.rom {
		m.ram[i] = v
	}
	m.ip = 0
	m.rb = 0
	m.stdout.clear()
}

func (m *intCodeMachine) run() {
	m.running = true
	for m.running {
		// fetch
		m.op = m.fetch()

		// decode/exec
		opMap[m.op%100](m)

		// bufio.NewReader(os.Stdin).ReadBytes('\n')
	}
}

func (m *intCodeMachine) fetch() int {
	return m.ram[m.ip]
}

type pipeinputfunc func() []int
type pipeoutputfunc func(p *pipe)

type pipe struct {
	data   []int
	empty  pipeinputfunc
	output pipeoutputfunc
}

func (p *pipe) push(v ...int) {
	p.data = append(p.data, v...)
	if p.output != nil {
		p.output(p)
	}
}

func (p *pipe) pop() (int, bool) {
	if len(p.data) == 0 {
		if p.empty != nil {
			p.data = append(p.data, p.empty()...)
			return p.pop()
		}
		return 0, false
	}
	v := p.data[0]
	p.data = p.data[1:]
	return v, true
}

func (p *pipe) clear() {
	p.data = nil
}

func (p *pipe) peek() int {
	return p.data[0]
}

func loadProgram(file string) []int {
	content, _ := ioutil.ReadFile(file)
	opcodeStrs := strings.Split(string(content), ",")
	rom := make([]int, len(opcodeStrs))
	for i, s := range opcodeStrs {
		v, _ := strconv.Atoi(s)
		rom[i] = v
	}
	return rom
}
