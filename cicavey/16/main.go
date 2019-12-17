package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func abs(v int) int {
	if v < 0 {
		return -v
	}
	return v
}
func main() {

	raw, _ := ioutil.ReadFile("input")
	input := strings.TrimSpace(string(raw))
	d := make([]int, len(input))
	for i, c := range input {
		d[i] = int(c - 48)
	}

	// Make the big copy for part 2
	longd := make([]int, len(d)*10_000)
	for i := 0; i < 10_000; i++ {
		copy(longd[i*len(d):], d)
	}
	offset, _ := strconv.Atoi(input[:7])
	longd = longd[offset:]

	spat := []int{0, 1, 0, -1}
	newd := make([]int, len(d))
	for phase := 0; phase < 100; phase++ {
		for i := 0; i < len(d); i++ {
			sum := 0
			for j := 0; j < len(d); j++ {
				sum += d[j] * spat[(j+1)/(i+1)%4]
			}
			newd[i] = abs(sum) % 10
		}
		d = newd
	}

	fmt.Println(d[0:8])

	// full disclosure - I need a hint for the partial/cummulative sum business
	for phase := 0; phase < 100; phase++ {
		sum := 0
		for i := len(longd) - 1; i >= 0; i-- {
			sum += longd[i]
			longd[i] = sum % 10
		}
	}
	fmt.Println(longd[:8])
}
