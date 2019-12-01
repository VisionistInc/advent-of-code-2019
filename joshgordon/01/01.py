#!/usr/bin/python3


data = []
with open('input.txt', 'r') as infile:
    for line in infile:
        data.append(int(line))

print(sum([point // 3 - 2 for point in data]))
