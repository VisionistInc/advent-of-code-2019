package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

type vec struct {
	x, y, z int
}

type body struct {
	p, v vec
}

func abs(i int) int {
	if i < 0 {
		return -i
	}
	return i
}

func (b body) pot() int {
	return abs(b.p.x) + abs(b.p.y) + abs(b.p.z)
}

func (b body) kin() int {
	return abs(b.v.x) + abs(b.v.y) + abs(b.v.z)
}

func (b body) te() int {
	return b.pot() * b.kin()
}

func (b *body) step() {
	b.p.x += b.v.x
	b.p.y += b.v.y
	b.p.z += b.v.z
}

func (b body) compare(ob body, i int) bool {
	switch i {
	case 0:
		return b.p.x == ob.p.x && b.v.x == ob.v.x
	case 1:
		return b.p.y == ob.p.y && b.v.y == ob.v.y
	case 2:
		return b.p.z == ob.p.z && b.v.z == ob.v.z
	}

	return false

}

func step(bodies []body) {
	// Apply gravity
	for i := range bodies {
		a := &bodies[i]
		for j := range bodies {
			b := &bodies[j]
			if i == j {
				continue
			}
			if a.p.x < b.p.x {
				a.v.x++
				b.v.x--
			}
			if a.p.y < b.p.y {
				a.v.y++
				b.v.y--
			}
			if a.p.z < b.p.z {
				a.v.z++
				b.v.z--
			}
		}
	}

	// Apply velocity
	for i := range bodies {
		bodies[i].step()
	}
}

func gcd(x, y int) int {
	for y != 0 {
		x, y = y, x%y
	}
	return x
}

func lcm(a, b int, integers ...int) int {
	result := a * b / gcd(a, b)

	for i := 0; i < len(integers); i++ {
		result = lcm(result, integers[i])
	}

	return result
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var b1 []body

	ex := regexp.MustCompile(`[xyz]=([+-]?\d+)`)
	for scanner.Scan() {
		a := ex.FindAllStringSubmatch(scanner.Text(), -1)
		x, _ := strconv.Atoi(a[0][1])
		y, _ := strconv.Atoi(a[1][1])
		z, _ := strconv.Atoi(a[2][1])
		b1 = append(b1, body{p: vec{x, y, z}})
	}

	// Copy original position for part 2
	b2 := make([]body, len(b1))
	copy(b2, b1)
	b2orig := make([]body, len(b1))
	copy(b2orig, b1)

	// Run 1000 steps, print energy
	for t := 0; t < 100; t++ {
		step(b1)
	}

	e := 0
	for _, a := range b1 {
		e += a.te()
	}
	fmt.Println(e)

	var allFound int
	var found [3]bool
	var atStep [3]int

	// Run 3000 steps, print energy
	for t := 0; allFound != 3; t++ {
		step(b2)

		// Check and see if the x comps all line up with orig

		for j := 0; j < 3; j++ {
			all := true
			for i := range b2 {
				all = all && b2[i].compare(b2orig[i], j)
			}
			if all && !found[j] {
				found[j] = true
				atStep[j] = t + 1
				allFound++
			}
		}
	}

	fmt.Println(lcm(atStep[0], atStep[1], atStep[2]))

}
