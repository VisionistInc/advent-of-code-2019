package main

import (
	"fmt"
)

const (
	COLLISON     = 0
	MOVED        = 1
	FOUND_OXYGEN = 2

	NORTH = 1
	SOUTH = 2
	WEST  = 3
	EAST  = 4

	WALL = 0
	EXP  = 1
	UNK  = 2
)

type vec2 struct {
	x, y int
}

func (v vec2) add(u vec2) vec2 {
	return vec2{v.x + u.x, v.y + u.y}
}

type bot struct {
	pos vec2
}

var vMap = map[int]vec2{
	NORTH: vec2{0, 1},
	SOUTH: vec2{0, -1},
	WEST:  vec2{-1, 0},
	EAST:  vec2{1, 0},
}

var rMap = map[int]int{
	NORTH: SOUTH,
	SOUTH: NORTH,
	WEST:  EAST,
	EAST:  WEST,
}

func drawGrid(g map[vec2]int, b vec2, o vec2) {
	var xmin, xmax, ymin, ymax int

	for p := range g {
		if p.x < xmin {
			xmin = p.x
		}
		if p.x > xmax {
			xmax = p.x
		}
		if p.y < ymin {
			ymin = p.y
		}
		if p.y > ymax {
			ymax = p.y
		}
	}

	for y := ymin; y <= ymax; y++ {
		for x := xmin; x <= xmax; x++ {
			if b.x == x && b.y == y {
				fmt.Print("B")
				continue
			}
			if o.x == x && o.y == y {
				fmt.Print("O")
				continue
			}
			switch g[vec2{x, y}] {
			case WALL:
				fmt.Print("▉")
			case UNK:
				fmt.Print("░")
			default:
				fmt.Print(" ")
			}
		}
		fmt.Println()
	}

}

func main() {

	rom := loadProgram("input")
	m := newIntCodeMachine(rom)

	go m.run()

	grid := make(map[vec2]int)

	bot := bot{}

	var oxygen vec2

	grid[bot.pos] = EXP

	var undoPath []int

outer:
	for {

		for direction, dvec := range vMap {

			next := bot.pos.add(dvec)

			// Already been there
			if _, ok := grid[next]; ok {
				continue
			}

			m.c <- direction // attempt to go in that direction
			status := <-m.c  // get staus right back! magic of channels
			grid[next] = status

			if status == COLLISON {
				// Didn't move, marked, try a different way
				continue outer
			}

			if status == FOUND_OXYGEN {
				oxygen = next
			}

			bot.pos = next
			undoPath = append(undoPath, rMap[direction]) // track the opposite/inverse moves

			continue outer
		}

		if len(undoPath) < 1 {
			break
		}

		// No valid moves, need to step back, pop from reversePath
		reverseLast := undoPath[len(undoPath)-1]
		undoPath = undoPath[:len(undoPath)-1]
		m.c <- reverseLast
		<-m.c // ignore output, we were just there
		bot.pos = bot.pos.add(vMap[reverseLast])
	}

	drawGrid(grid, bot.pos, oxygen)

	// Now do BFS to find shortest from O to (0,0)
	q := []vec2{oxygen}
	dist := map[vec2]int{oxygen: 0} // track distances
	var curr vec2
	for len(q) > 0 {
		curr = q[0]
		q = q[1:]

		// enqueue all the neighbors of curr that are not walls
		for _, dvec := range vMap {
			target := curr.add(dvec)
			_, ok := dist[target]
			if !ok && grid[target] != WALL {
				dist[target] = dist[curr] + 1
				q = append(q, target)
			}
		}
	}

	// Distance to starting point
	fmt.Println(dist[vec2{0, 0}], dist[curr])
}
