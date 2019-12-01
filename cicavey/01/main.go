package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func massAlg1(origMass int64) int64 {
	return origMass/3 - 2
}

func massAlg2(origMass int64) int64 {
	fuel := massAlg1(origMass)
	if fuel <= 0 {
		return 0
	}
	return fuel + massAlg2(fuel)
}

func main() {
	file, _ := os.Open("input.txt")
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var t1, t2 int64

	for scanner.Scan() {
		mass, _ := strconv.ParseInt(scanner.Text(), 10, 64)
		t1 += massAlg1(mass)
		t2 += massAlg2(mass)
	}
	fmt.Println(t1, t2)
}
