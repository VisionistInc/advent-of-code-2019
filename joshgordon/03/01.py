#!/usr/bin/python3

import sys


class Point:
    """yup this is probably overkill"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __int__(self):
        return abs(self.x) + abs(self.y)

    def __lt__(self, other):
        return int(self) < int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Wire:
    def __init__(self, instructions):
        self.instructions = instructions
        self.x = 0
        self.y = 0
        self.points = set()

        for inst in instructions.split(","):
            direction = inst[0]
            dist = int(inst[1:])
            if direction == "U":
                self.up(dist)
            elif direction == "D":
                self.down(dist)
            elif direction == "L":
                self.left(dist)
            elif direction == "R":
                self.right(dist)

    def up(self, distance):
        for i in range(distance):
            self.y += 1
            self.points.add(Point(self.x, self.y))

    def down(self, distance):
        for i in range(distance):
            self.y -= 1
            self.points.add(Point(self.x, self.y))

    def left(self, distance):
        for i in range(distance):
            self.x -= 1
            self.points.add(Point(self.x, self.y))

    def right(self, distance):
        for i in range(distance):
            self.x += 1
            self.points.add(Point(self.x, self.y))

    def find_intersections(self, other):
        return self.points.intersection(other.points)


wires = []

with open("input.txt", "r") as infile:
    for line in infile.read().strip().split("\n"):
        print(line)
        wires.append(Wire(line))

intersections = list(wires[0].find_intersections(wires[1]))
intersections.sort()
print(int(intersections[0]))
