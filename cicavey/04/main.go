package main

import (
	"fmt"
	"strconv"
)

func hasDouble(s string) bool {
	for i := 0; i < 5; i++ {
		if s[i] == s[i+1] {
			return true
		}
	}
	return false
}

func hasStrictDouble(s string) bool {
	// find a histogram of all sequences
	// seqHist[2] counts all strictly 2 digit seqs, this MUST be > 0
	var seqHist [7]int
	ss := 0
	c := s[0]

done:
	for i := 1; i < 6; i++ {
		for s[i] == c {
			i++
			if i == 6 {
				seqHist[i-ss]++
				break done
			}
		}
		seqHist[i-ss]++
		c = s[i]
		ss = i
	}
	return seqHist[2] > 0
}

func isMono(s string) bool {
	for i := 0; i < 5; i++ {
		if s[i] > s[i+1] {
			return false
		}
	}
	return true
}

func main() {
	min := 197487
	max := 673251

	count1 := 0
	count2 := 0
	for i := min; i <= max; i++ {
		s := strconv.Itoa(i)
		if isMono(s) {
			if hasDouble(s) {
				count1++
			}
			if hasStrictDouble(s) {
				count2++
			}
		}
	}

	fmt.Println(count1)
	fmt.Println(count2)
}
