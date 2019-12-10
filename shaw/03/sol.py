import sys

with open('input') as f:
    lines = f.read()

lines = lines.split()

first = lines[0].split(',')

x = 0
y = 0
s = 0

grid = dict()

for path in first:
    d = int(path[1:])
    if path[0] == 'U':
        for i in range(d):
            y = y + 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if not key in grid:
                grid[key] = s
    if path[0] == 'D':
        for i in range(d):
            y = y - 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if not key in grid:
                grid[key] = s
    if path[0] == 'L':
        for i in range(d):
            x = x - 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if not key in grid:
                grid[key] = s
    if path[0] == 'R':
        for i in range(d):
            x = x + 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if not key in grid:
                grid[key] = s

second = lines[1].split(',')

x = 0
y = 0
s = 0

part1_short = 9999999999999999
part2_short = 9999999999999999

for path in second:
    d = int(path[1:])
    if path[0] == 'U':
        for i in range(d):
            y = y + 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if key in grid:
                part1_short = min(abs(x) + abs(y), part1_short)
                part2_short = min(s + grid[key], part2_short)
                
    if path[0] == 'D':
        for i in range(d):
            y = y - 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if key in grid:
                part1_short = min(abs(x) + abs(y), part1_short)
                part2_short = min(s + grid[key], part2_short)
                
    if path[0] == 'L':
        for i in range(d):
            x = x - 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if key in grid:
                part1_short = min(abs(x) + abs(y), part1_short)
                part2_short = min(s + grid[key], part2_short)
                
    if path[0] == 'R':
        for i in range(d):
            x = x + 1
            s = s + 1
            key = '%d,%d' % (x,y)
            if key in grid:
                part1_short = min(abs(x) + abs(y), part1_short)
                part2_short = min(s + grid[key], part2_short)

print('Part 1: ', part1_short)
print('Part 2: ', part2_short)