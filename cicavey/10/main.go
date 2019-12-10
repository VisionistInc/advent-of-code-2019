package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
)

type point struct {
	x, y int
	vis  int
}

func (p point) atan2(t point) float64 {
	dx := p.x - t.x
	dy := p.y - t.y
	return math.Atan2(float64(dy), float64(dx))
}

func (p point) distSq(t point) float64 {
	return float64(p.x*t.x + p.y*t.y)
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var pts []point

	var y int

	for scanner.Scan() {
		line := scanner.Text()
		for x, c := range line {
			if c == '#' {
				pts = append(pts, point{x, y, 0})
			}
		}
		y++
	}

	for pidx, p := range pts {
		s := make(map[float64]int)
		for _, t := range pts {
			if p == t {
				continue
			}
			s[p.atan2(t)]++
		}

		pts[pidx].vis = len(s)
	}

	max := 0
	var station point
	for _, p := range pts {
		if p.vis > max {
			max = p.vis
			station = p
		}
	}

	fmt.Println("Part 1", station)

	// Compute the angles to each of the other points relative to station

	aligned := make(map[float64][]point)

	for _, t := range pts {
		if t == station {
			continue
		}
		angle := station.atan2(t)
		aligned[angle] = append(aligned[angle], t)
	}

	// Sort each slice by distance to station
	for _, alignedSlice := range aligned {
		sort.Slice(alignedSlice, func(i, j int) bool {
			di := station.distSq(alignedSlice[i])
			dj := station.distSq(alignedSlice[j])
			return di > dj
		})
	}

	// Sort all angles
	var sortedAngles []float64
	for angle := range aligned {
		sortedAngles = append(sortedAngles, angle)
	}
	sort.Float64s(sortedAngles)
	startIdx := sort.SearchFloat64s(sortedAngles, math.Pi/2)

	var idx = startIdx
	var total = len(pts) - 1
	var n int
	for {

		ts := aligned[sortedAngles[idx]]

		if len(ts) > 0 {
			elim := ts[0]
			//fmt.Println(n+1, elim)
			ts = ts[1:]
			aligned[sortedAngles[idx]] = ts
			n++
			total--

			if n == 200 {
				fmt.Println(elim.x*100 + elim.y)
			}
		}

		idx++
		idx %= len(sortedAngles)

		if total == 0 {
			break
		}
	}

}
