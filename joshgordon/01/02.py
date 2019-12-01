#!/usr/bin/python3

def compute_fuel(weight):
    next_fuel = weight // 3 - 2
    # did you mean recursion?
    if next_fuel > 0:
        return next_fuel + compute_fuel(next_fuel)
    return 0


data = []
with open('input.txt', 'r') as infile:
    for line in infile:
        data.append(int(line))

total_weight = sum(data)
fuel = sum([compute_fuel(point) for point in data])

print(fuel)
