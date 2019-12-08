package main

import (
	"fmt"
	"io/ioutil"
	"sort"
)

type layer struct {
	data []byte
	hist [3]int
}

func (l *layer) ck() int {
	return l.hist[1] * l.hist[2]
}

func (l *layer) dump(lx, ly int) {
	for y := 0; y < ly; y++ {
		for x := 0; x < lx; x++ {
			offset := x + y*lx
			if l.data[offset] == 0 {
				fmt.Print(" ")
				continue
			}
			fmt.Print(l.data[offset])
		}
		fmt.Println()
	}
}

func main() {
	content, _ := ioutil.ReadFile("input")

	for i, v := range content {
		content[i] = v - '0'
	}

	lx, ly := 25, 6
	size := lx * ly
	nl := len(content) / (size)
	var layers []*layer

	// Parition layers
	for l := 0; l < nl; l++ {
		offset := l * (size)
		layers = append(layers, &layer{data: content[offset : offset+size]})
	}

	// Hist layers
	for _, layer := range layers {
		for _, v := range layer.data {
			layer.hist[v]++
		}
	}

	sortedLayers := make([]*layer, len(layers))
	copy(sortedLayers, layers)
	sort.SliceStable(sortedLayers, func(i, j int) bool {
		return sortedLayers[i].hist[0] < sortedLayers[j].hist[0]
	})

	fmt.Println(sortedLayers[0].ck())

	// Combine layers
	fl := layer{data: make([]byte, size)}

	for x := 0; x < lx; x++ {
		for y := 0; y < ly; y++ {
			offset := x + y*lx
			for _, l := range layers {
				if l.data[offset] == 2 {
					continue
				}
				fl.data[offset] = l.data[offset]
				break
			}

		}
	}

	fl.dump(lx, ly)
}
