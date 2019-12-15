package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
)

type chemical struct {
	name  string
	value int
}

type reaction struct {
	reagent []chemical
	result  chemical
}

type environment struct {
	rxs   map[string]reaction
	waste map[string]int
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	rxs := make(map[string]reaction)

	r, _ := regexp.Compile(`(\d+) (\w+)`)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		s := r.FindAllStringSubmatch(line, -1)

		var temp []chemical

		for _, sub := range s {
			v, _ := strconv.Atoi(sub[1])
			temp = append(temp, chemical{sub[2], v})
		}

		rx := reaction{temp[0 : len(temp)-1], temp[len(temp)-1]}
		rxs[rx.result.name] = rx
	}

	e := &environment{rxs, make(map[string]int)}

	fmt.Println(e.cost("FUEL", 1))

	ore := 1_000_000_000_000

	max := 1_000_000_000
	min := 0
	fuel := (max - min) / 2

	cost := e.cost("FUEL", fuel)

	for min != fuel || max != fuel {
		if cost-ore > 0 {
			max = fuel - 1
		} else {
			min = fuel + 1
		}

		fuel = min + (max-min)/2

		cost = e.cost("FUEL", fuel)
	}

	fmt.Println(fuel, e.cost("FUEL", max-1))
}

func ceil(a, b int) int {
	return int(math.Ceil(float64(a) / float64(b)))
}

func (e *environment) cost(name string, q int) int {
	e.waste = make(map[string]int)
	return e.costHelper(name, q)
}

func (e *environment) costHelper(name string, q int) int { //target chemical) int {

	// What reaction creates target?
	rx := e.rxs[name]

	spare := e.waste[name]
	factor := ceil(q-spare, rx.result.value)
	created := rx.result.value * factor
	waste := created - (q - spare)
	e.waste[name] = waste

	// Iterate over reagents and cost them
	total := 0
	for _, reagent := range rx.reagent {
		if reagent.name == "ORE" {
			total += factor * reagent.value
		} else {
			total += e.costHelper(reagent.name, reagent.value*factor)
		}
	}

	return total
}
