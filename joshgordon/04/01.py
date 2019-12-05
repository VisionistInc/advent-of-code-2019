#!/usr/bin/python3

with open("input.txt", "r") as infile:
    data = [int(n) for n in infile.read().strip().split("-")]


def check_number(num):
    numstr = str(num)
    # six digit number. Assumed based on input.
    # Within range of puzzle input. Assumed based on input.
    # Two adjacent digits are the same
    adjacents = False
    for i in range(len(numstr) - 1):
        # adjacents
        if numstr[i] == numstr[i + 1]:
            adjacents = True
            break

    for i in range(len(numstr) - 1):
        if numstr[i] > numstr[i + 1]:
            return False

    if not adjacents:
        return False

    return True


# do some sanity checks:
print(f"111111: {check_number(111111)}")
print(f"223450: {check_number(223450)}")
print(f"123789: {check_number(123789)}")

print(data)
valids = [i for i in range(data[0], data[1] + 1) if check_number(i)]
print(len(valids))
