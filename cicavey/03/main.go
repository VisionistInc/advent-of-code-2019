package main

import (
	"bufio"
	"fmt"
	"math"
	"math/bits"
	"os"
	"strconv"
	"strings"
)

func abs(v int) int {
	if v < 0 {
		return -v
	}
	return v
}

type point struct {
	x, y int
}

func (p *point) add(v point) {
	p.x += v.x
	p.y += v.y
}

func (p point) md() uint64 {
	return uint64(abs(p.x) + abs(p.y))
}

func walk(seq string, grid map[point]uint64, mask uint64, target *point) uint64 {
	pos := point{0, 0}
	steps := uint64(0)
	grid[pos] |= mask
	ins := strings.Split(seq, ",")
	for _, ins := range ins {
		dir := string(ins[0])
		q, _ := strconv.Atoi(ins[1:])
		var v point
		switch dir {
		case "U":
			v = point{0, 1}
		case "D":
			v = point{0, -1}
		case "L":
			v = point{-1, 0}
		case "R":
			v = point{1, 0}
		}

		for i := 0; i < q; i++ {
			pos.add(v)
			steps++

			if target != nil && *target == pos {
				return steps
			}

			grid[pos] |= mask
		}
	}

	return steps
}

func main() {
	grid := make(map[point]uint64)

	file, _ := os.Open("input")
	defer file.Close()

	scanner := bufio.NewScanner(file)
	mask := uint64(1)
	var seqs []string
	for scanner.Scan() {
		line := scanner.Text()
		seqs = append(seqs, line)
		walk(line, grid, mask, nil)
		mask <<= 1
	}

	var intersections []point
	var min uint64 = math.MaxUint64
	for k, v := range grid {

		// exclude self-intersection
		if bits.OnesCount64(v) < 2 {
			continue
		}

		// exclude zero
		md := k.md()
		if md == 0 {
			continue
		}

		intersections = append(intersections, k)

		if md < min {
			min = md
		}
	}
	fmt.Println("Part 1:", min)

	// For each intersection, re-calculate the steps to get there
	// This is super inefficient. I should only need to iterate once
	var minSteps uint64 = math.MaxUint64
	for _, p := range intersections {
		ts := uint64(0)
		for _, seq := range seqs {
			// mask of 0 won't modify the _grid_
			ts += walk(seq, grid, 0, &p)
		}
		if ts < minSteps {
			minSteps = ts
		}
	}
	fmt.Println("Part 2:", minSteps)
}
