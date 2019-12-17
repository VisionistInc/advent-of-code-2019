package main

import (
	"fmt"
	"strings"
)

type vec2 struct {
	x, y int
}

func (v vec2) add(u vec2) vec2 {
	return vec2{v.x + u.x, v.y + u.y}
}

func (v vec2) abs() vec2 {
	new := v
	if new.x < 0 {
		new.x = -new.x
	}
	if new.y < 0 {
		new.y = -new.y
	}
	return new
}

func main() {
	rom := loadProgram("input")
	m := newIntCodeMachine(rom)

	grid := make(map[vec2]int)

	go m.run()

	var x, y, xmax, ymax int
	var bot vec2

done:
	for {
		select {
		case output := <-m.c:
			if output == 10 {
				fmt.Println()
				y++
				ymax = y
				x = 0
			} else {

				if output == '^' || output == 'v' || output == '<' || output == '>' {
					bot = vec2{x, y}
				}

				grid[vec2{x, y}] = output
				fmt.Print(string(output))
				x++
				if x > xmax {
					xmax = x
				}
			}
		case <-m.halt:
			break done
		}
	}

	directions := []vec2{
		vec2{0, 1},
		vec2{0, -1},
		vec2{-1, 0},
		vec2{1, 0},
	}

	intersections := make(map[vec2]bool)

	// given start, find adjacent path, travel
	var direction vec2
	for _, d := range directions {
		if v, ok := grid[bot.add(d)]; ok && v == '#' {
			direction = d
			break
		}
	}

exhausted:
	for {

		// intersection?
		intersection := true
		for _, d := range directions {
			if v, ok := grid[bot.add(d)]; ok && v == '#' {
				continue
			}
			intersection = false
			break
		}

		if intersection {
			intersections[bot] = true
		}

		// Look ahead in direction, if path then move there
		if grid[bot.add(direction)] == '#' {
			bot = bot.add(direction)
		} else {
			// find a new direction that wasn't the previos or opposite
			found := false
			for _, d := range directions {
				if d.abs() == direction.abs() {
					continue
				}

				if v, ok := grid[bot.add(d)]; ok && v == '#' {
					direction = d
					found = true
					break
				}
			}
			if !found {
				break exhausted
			}
		}
	}

	for i := 0; i < ymax; i++ {
		for j := 0; j < xmax; j++ {
			p := vec2{j, i}
			if p == bot {
				fmt.Print("M")
			} else if intersections[p] {
				fmt.Print("O")
			} else {
				fmt.Print(string(grid[p]))
			}
		}
		fmt.Println()
	}

	sum := 0
	for o := range intersections {
		sum += o.x * o.y
	}
	fmt.Println(sum)

	m = newIntCodeMachine(rom)
	m.ram[0] = 2

	go m.run()

	var last int
	for {
		output := <-m.c
		if output == 10 {
			fmt.Println()
			if last == 10 {
				break
			}
		} else {
			fmt.Print(string(output))
		}
		last = output
	}

	// By visual inspection
	A := "R,4,R,10,R,8,R,4"
	B := "R,4,L,12,R,6,L,12"
	C := "R,10,R,6,R,4"
	MAIN := "A,C,A,C,B,C,B,A,C,B"
	CODE := []string{MAIN, A, B, C}

	// Load up programs
	for _, src := range CODE {
		fmt.Print(readLine(m.c))
		fmt.Println(src)
		writeLine(m.c, src)
	}

	fmt.Print(readLine(m.c))
	fmt.Println("n")
	writeLine(m.c, "n")

	output := 0
done2:
	for {
		select {
		case output = <-m.c:
		case <-m.halt:
			break done2
		}
	}
	fmt.Println(output)
}

func readLine(c chan int) string {
	var b strings.Builder
	output := 0
	for output != 10 {
		output = <-c
		if output != 10 {
			b.WriteRune(rune(output))
		}
	}
	return b.String()
}

func writeLine(c chan int, src string) {
	for _, i := range src {
		c <- int(i)
	}
	c <- 10
}
