package main

import "fmt"

type point struct {
	x, y int
}

func (p *point) rotateLeft() {
	p.y, p.x = p.x, -p.y
}

func (p *point) rotateRight() {
	p.y, p.x = -p.x, p.y
}

func (p *point) add(t point) {
	p.x += t.x
	p.y += t.y
}

type panel struct {
	color int
	count int
}

func main() {

	rom := loadProgram("input")
	m := newIntCodeMachine(rom)

	pos := point{0, 0}
	facing := point{0, 1}
	grid := make(map[point]panel)

	// Remove for pat 1
	grid[pos] = panel{1, 0}

	var xmax, xmin, ymin, ymax int

	// The program _wants_ read, let's provide a values
	m.stdin.empty = func() []int {
		return []int{grid[pos].color}
	}

	m.stdout.output = func(p *pipe) {
		if len(p.data) < 2 {
			return
		}

		// Consume at least two things and move the robot
		paint, _ := p.pop()
		turn, _ := p.pop()

		curPanel := grid[pos]
		curPanel.color = paint
		curPanel.count++
		grid[pos] = curPanel

		if turn == 0 { // LEFT
			facing.rotateLeft()
		} else {
			facing.rotateRight()
		}

		pos.add(facing)

		if pos.x < xmin {
			xmin = pos.x
		}
		if pos.x > xmax {
			xmax = pos.x
		}
		if pos.y < ymin {
			ymin = pos.y
		}
		if pos.y > ymax {
			ymax = pos.y
		}
	}

	m.run()

	// Part 1
	fmt.Println(len(grid))

	for y := ymax; y >= ymin; y-- {
		for x := xmin; x <= xmax; x++ {
			p := grid[point{x, y}]
			if p.color == 0 {
				fmt.Print(" ")
			} else {
				fmt.Print("#")
			}
		}
		fmt.Println()
	}
}
