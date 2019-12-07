package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type node struct {
	name     string
	parent   *node
	children []*node
}

func (n node) String() string {

	var sb strings.Builder

	for _, c := range n.children {
		sb.WriteString(c.name)
	}

	return n.name + " -> " + sb.String()
}

func (n *node) direct() int {
	if n.parent != nil {
		return 1
	}
	return 0
}

func (n *node) indirect() int {
	cur := n.parent
	i := 0
	for cur != nil {
		cur = cur.parent
		i++
	}
	return i
}

func (n *node) path() []*node {
	var p []*node
	cur := n.parent
	for cur != nil {
		p = append(p, cur)
		cur = cur.parent
	}
	return p
}

type orbitalMap struct {
	nodes map[string]*node
}

func newOrbitalMap() *orbitalMap {
	return &orbitalMap{
		nodes: make(map[string]*node),
	}
}

func (o *orbitalMap) getOrCreate(name string) (*node, bool) {
	n, ok := o.nodes[name]
	if !ok {
		n = &node{name: name}
		o.nodes[name] = n
	}
	return n, ok
}

func (o *orbitalMap) define(src, dst string) {
	srcNode, _ := o.getOrCreate(src)
	dstNode, _ := o.getOrCreate(dst)
	dstNode.parent = srcNode
	srcNode.children = append(srcNode.children, dstNode)
}

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	om := newOrbitalMap()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		s := strings.Split(scanner.Text(), ")")
		om.define(s[0], s[1])
	}

	total := 0
	for _, node := range om.nodes {
		total += node.indirect()
	}
	fmt.Println(total)

	u, _ := om.getOrCreate("YOU")
	uPath := u.path()

	s, _ := om.getOrCreate("SAN")
	sPath := s.path()

found:
	for ui, un := range uPath {
		for si, sn := range sPath {
			if un == sn {
				fmt.Println(ui + si)
				break found
			}
		}
	}
}
