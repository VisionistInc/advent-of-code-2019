#!/usr/bin/python3
import itertools
from intcode_computer import Computer
import threading
import redis
from collections import defaultdict

r = redis.Redis()
# start with a clean slate.
r.flushall()

ship = defaultdict(lambda: b"0")

# up, right, down, left
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def handle_computer():
    # the computer does a brpop on input, so we need to do an lpush, and vice versa
    input_keyname = "input"
    output_keyname = "output"

    x = 0
    y = 0
    # start facing up (0)
    direction = 0

    # start the loop
    while True:
        # tell the ship what color we're on.
        r.lpush(input_keyname, ship[(x, y)])
        # print(f"Telling the computer the current color is {ship[(x, y)]}")

        # get instructions back from the computer.
        color = r.brpop(output_keyname)[1]
        newdir = r.brpop(output_keyname)[1]

        ship[(x, y)] = color

        if newdir == b"0":
            newdir = -1
        else:
            newdir = 1

        direction += newdir
        direction %= 4
        x, y = x + directions[direction][0], y + directions[direction][1]


c1 = Computer(init_args=[], input_topic="input", output_topic="output")

t1 = threading.Thread(target=c1.computer)
t2 = threading.Thread(target=handle_computer, daemon=True)

t1.start()
t2.start()

t1.join()

print(f"Part 1: {len(ship)}")
