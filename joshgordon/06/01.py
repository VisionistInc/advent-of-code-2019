#!/usr/bin/python3

import sys


data = {}

with open("input.txt", "r") as infile:
    for line in infile:
        data[line.split(")")[1].strip()] = line.split(")")[0]


def find_depth(planet):
    if planet == "COM":
        return 0
    return find_depth(data[planet]) + 1


count = 0
for f in data:
    count += find_depth(f)

print(count)
