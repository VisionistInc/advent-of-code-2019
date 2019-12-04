#!/usr/bin/python3

import sys

data = []

with open("input.txt", "r") as infile:
    for line in infile.read().strip().split(","):
        data.append(int(line))

# instruction pointer
eip = 0

data[1] = 12
data[2] = 2
while data[eip] != 99:
    if data[eip] == 1:
        data[data[eip + 3]] = data[data[eip + 1]] + data[data[eip + 2]]
        eip += 4
    elif data[eip] == 2:
        data[data[eip + 3]] = data[data[eip + 1]] * data[data[eip + 2]]
        eip += 4
print(data[0])
