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


def find_parents(planet):
    if planet == "COM":
        return list(["COM"])
    return [planet] + find_parents(data[planet])


santa_parents = find_parents("SAN")
you_parents = find_parents("YOU")

common_ancestor = None
for parent in you_parents:
    if parent in santa_parents:
        print(f"Found common ancestor: {parent}")
        common_ancestor = parent
        break

print(
    f"Distance between YOU and {common_ancestor}: {you_parents.index(common_ancestor)}"
)
print(
    f"Distance between SAN and {common_ancestor}: {santa_parents.index(common_ancestor)}"
)
print(
    f"Transfers: {you_parents.index(common_ancestor) + santa_parents.index(common_ancestor) - 2}"
)
