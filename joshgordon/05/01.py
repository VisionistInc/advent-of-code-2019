#!/usr/bin/python3

import sys


data = []

with open("input.txt", "r") as infile:
    for line in infile.read().strip().split(","):
        data.append(int(line))

# instruction pointer
eip = 0


# TODO implement support for 3 immediate operands (??? maybe ???)
def get_params(data, eip):
    # two params
    immediate = f"{data[eip]:05d}"
    if immediate[2] == "1":
        eax = data[eip + 1]
    else:
        eax = data[data[eip + 1]]
    if data[eip] % 100 in [1, 2, 5, 6, 7, 8]:
        if immediate[1] == "1":
            ebx = data[eip + 2]
        else:
            ebx = data[data[eip + 2]]
        return eax, ebx
    return eax


while data[eip] != 99:
    # print(f"data[{eip}+] = {data[eip:eip+4]}")
    # add operands
    if data[eip] % 100 == 1:
        eax, ebx = get_params(data, eip)

        data[data[eip + 3]] = eax + ebx
        eip += 4

    # multiply operands
    elif data[eip] % 100 == 2:
        eax, ebx = get_params(data, eip)

        data[data[eip + 3]] = eax * ebx
        eip += 4

    # read from stdin
    elif data[eip] % 100 == 3:
        valid_int = False
        while not valid_int:
            eax = input("> ")
            try:
                eax = int(eax)
                valid_int = True
            except ValueError:
                print("Not a valid int!")
                pass

        data[data[eip + 1]] = eax
        eip += 2

    # write to stdout
    elif data[eip] % 100 == 4:
        eax = get_params(data, eip)
        print(f"output: {eax}")
        eip += 2

    # jump if true
    elif data[eip] % 100 == 5:
        eax, ebx = get_params(data, eip)

        if eax != 0:
            eip = ebx
        else:
            eip += 3

    # jump if false
    elif data[eip] % 100 == 6:
        eax, ebx = get_params(data, eip)

        if eax == 0:
            eip = ebx
        else:
            eip += 3

    # less than
    elif data[eip] % 100 == 7:
        eax, ebx = get_params(data, eip)

        if eax < ebx:
            data[data[eip + 3]] = 1
        else:
            data[data[eip + 3]] = 0

        eip += 4

    # equals
    elif data[eip] % 100 == 8:
        eax, ebx = get_params(data, eip)

        if eax == ebx:
            data[data[eip + 3]] = 1
        else:
            data[data[eip + 3]] = 0

        eip += 4

    else:
        print(f"INVALID OPCODE {data[eip]}")
        sys.exit(1)
