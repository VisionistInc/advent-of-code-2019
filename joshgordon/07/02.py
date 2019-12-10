#!/usr/bin/python3
import itertools
from intcode_computer2 import Computer
import multiprocessing
import redis

r = redis.Redis()

choices = [5, 6, 7, 8, 9]
perm = itertools.permutations(choices)

highest_value = 0

for i in perm:

    c1 = Computer(init_args=[i[0], 0], input_topic="aoc:5", output_topic="aoc:1")
    c2 = Computer(init_args=[i[1]], input_topic="aoc:1", output_topic="aoc:2")
    c3 = Computer(init_args=[i[2]], input_topic="aoc:2", output_topic="aoc:3")
    c4 = Computer(init_args=[i[3]], input_topic="aoc:3", output_topic="aoc:4")
    c5 = Computer(init_args=[i[4]], input_topic="aoc:4", output_topic="aoc:5")

    t1 = multiprocessing.Process(target=c1.computer)
    t2 = multiprocessing.Process(target=c2.computer)
    t3 = multiprocessing.Process(target=c3.computer)
    t4 = multiprocessing.Process(target=c4.computer)
    t5 = multiprocessing.Process(target=c5.computer)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    value = int(r.lpop("aoc:5"))
    if value > highest_value:
        highest_value = value

print(highest_value)
