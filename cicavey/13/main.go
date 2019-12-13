package main

import (
	"fmt"
	tb "github.com/nsf/termbox-go"
	"os"
	_ "os"
	_ "strconv"
	_ "time"
)

type point struct {
	x, y int
}

const (
	EMPTY  = iota
	WALL
	BLOCK
	PADDLE
	BALL

)

var disp = map[int]rune{
	EMPTY: ' ',
	WALL: '#',
	BLOCK: '█',
	PADDLE: '▀',
	BALL: '*',
}

//func drawint(x, y int, v int) {
//	ss := strconv.Itoa(v)
//	for i, c := range ss {
//		tb.SetCell(x + 1 + i, y, c,  tb.ColorRed, tb.ColorBlack)
//	}
//
//}

func main() {
	xmax := 38
	ymax := 21
	//err := tb.Init()
	//if err != nil {
	//	panic(err)
	//}
	//defer tb.Close()

	rom := loadProgram("input")

	m := newIntCodeMachine(rom)

	grid := make(map[point]int)
	score := 0
	defer func() {
		fmt.Println(score)
	}()

	m.stdout.output = func(p *pipe) {
		if len(p.data) < 3 {
			return
		}
		x, _ := p.pop()
		y, _ := p.pop()
		v, _ := p.pop()

		if x == -1 && y == 0 {
			// update score
			score = v
		}

		grid[point{x,y}] = v
	}

	m.stdin.empty = func() []int {

		var ball, paddle point

		tb.Clear(tb.ColorWhite, tb.ColorBlack)
		for y := 0; y < ymax; y++ {
			for x := 0; x < xmax; x++ {
				v := grid[point{x,y}]
				//tb.SetCell(x, y, disp[v], tb.ColorWhite, tb.ColorBlack)
				if v == BALL {
					ball = point{x,y}
				}
				if v == PADDLE {
					paddle = point{x, y}
				}
			}
		}

		//drawint(xmax +1, 0, score)
		//drawint(xmax +1, 1, m.ip)
		//tb.Flush()
		//time.Sleep(1 * time.Millisecond)

		if ball.x < paddle.x {
			return []int{-1}
		}
		if ball.x > paddle.x {
			return []int{1}
		}

		return []int{0}
	}

	m.ram[0] = 2 // free play!

	m.run()

	//tb.Close()

	fmt.Println(score)

	blockCount := 0
	for _, v := range grid {
		if v == 2 {
			blockCount++
		}
	}
	os.Exit(-1)
}
