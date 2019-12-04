#!/usr/bin/python3

import sys


def main():
    data_orig = []

    with open("input.txt", "r") as infile:
        for line in infile.read().strip().split(","):
            data_orig.append(int(line))
    with open("target.txt", "r") as infile:
        target = int(infile.read().strip())

    # instruction pointer

    for i in range(100):
        for j in range(100):
            eip = 0
            data = data_orig.copy()
            data[1] = i
            data[2] = j
            while data[eip] != 99:
                if data[eip] == 1:
                    data[data[eip + 3]] = data[data[eip + 1]] + data[data[eip + 2]]
                    eip += 4
                elif data[eip] == 2:
                    data[data[eip + 3]] = data[data[eip + 1]] * data[data[eip + 2]]
                    eip += 4
            if data[0] == target:
                print(f"noun: {i}, verb: {j}, output: {data[0]}")
                return


if __name__ == "__main__":
    main()
