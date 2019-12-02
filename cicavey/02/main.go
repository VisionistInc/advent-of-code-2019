package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func run(memory []int, noun int, verb int) int {

	memory[1] = noun
	memory[2] = verb

	ip := 0
	running := true

	for running {
		op := memory[ip]
		switch op {
		case 1:
			memory[memory[ip+3]] = memory[memory[ip+1]] + memory[memory[ip+2]]
			ip += 4
		case 2:
			memory[memory[ip+3]] = memory[memory[ip+1]] * memory[memory[ip+2]]
			ip += 4
		case 99:
			running = false
			ip++
		}

	}

	return memory[0]
}

func main() {
	content, _ := ioutil.ReadFile("input.txt")
	opcodeStrs := strings.Split(string(content), ",")
	memory := make([]int, len(opcodeStrs))
	for i, s := range opcodeStrs {
		v, _ := strconv.Atoi(s)
		memory[i] = v
	}

	working := make([]int, len(memory))
	for noun := 0; noun <= 99; noun++ {
		for verb := 0; verb <= 99; verb++ {
			copy(working, memory)
			result := run(working, noun, verb)

			// Part 1
			if noun == 12 && verb == 2 {
				fmt.Println("Part 1", result)
			}

			if result == 19690720 {
				fmt.Println("Part 2", 100*noun+verb)
			}
		}
	}
}
