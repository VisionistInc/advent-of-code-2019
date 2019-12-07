#!/usr/bin/python3


class Point:
    """yup this is probably overkill, but it's awesome because it makes things downstream a lot nicer."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __int__(self):
        return abs(self.x) + abs(self.y)

    def __lt__(self, other):
        return int(self) < int(other)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Wire:
    """one wire based on a set of points passed to the constructor."""

    def __init__(self, instructions):
        self.instructions = instructions
        self.x = 0
        self.y = 0
        self.points = set()
        self.steps = {}
        self.count = 0

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
            self.count += 1
            self.y += 1
            point = Point(self.x, self.y)
            if point not in self.steps:
                self.steps[point] = self.count
            self.points.add(point)

    def down(self, distance):
        for i in range(distance):
            self.count += 1
            self.y -= 1
            point = Point(self.x, self.y)
            if point not in self.steps:
                self.steps[point] = self.count
            self.points.add(point)

    def left(self, distance):
        for i in range(distance):
            self.count += 1
            self.x -= 1
            point = Point(self.x, self.y)
            if point not in self.steps:
                self.steps[point] = self.count
            self.points.add(point)

    def right(self, distance):
        for i in range(distance):
            self.count += 1
            self.x += 1
            point = Point(self.x, self.y)
            if point not in self.steps:
                self.steps[point] = self.count
            self.points.add(point)

    def find_intersections(self, other):
        return self.points.intersection(other.points)


wires = []

with open("input.txt", "r") as infile:
    for line in infile.read().strip().split("\n"):
        wires.append(Wire(line))

intersections = list(wires[0].find_intersections(wires[1]))
intersections.sort()
print(f"part 1: {int(intersections[0])}")

# part 2!
min_steps = float("inf")
# go through the intersections and figure out how many steps each one takes.
for intersection in intersections:
    steps = wires[0].steps[intersection] + wires[1].steps[intersection]
    if steps < min_steps:
        min_steps = steps

print(f"Part 2: {min_steps}")
