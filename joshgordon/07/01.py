#!/usr/bin/python3
import itertools
from intcode_computer import computer

choices = [0, 1, 2, 3, 4]
perm = itertools.permutations(choices)

highest_output = 0

# it's a bit janky and takes a couple of seconds to run (at least on my laptop) but this feels like the
# easiest way to do this.

for i in perm:
    last_output = "0"

    for j in i:
        result = computer(args=[j, last_output])
        last_output = result.strip()

    last_output = int(last_output)
    if last_output > highest_output:
        highest_output = last_output

print(highest_output)
