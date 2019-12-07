#!/usr/bin/python3

with open("input.txt", "r") as infile:
    data = [int(n) for n in infile.read().strip().split("-")]


def check_number(num):
    # treat this sucker as a string.
    numstr = str(num)
    # six digit number. Assumed based on input.
    # Within range of puzzle input. Assumed based on input.
    # Two adjacent digits are the same
    adjacents = False
    # Variable for storing the value of digits that are 3+ adjacent together so
    # we can keep ignoring them.
    super_adjacents = None
    for i in range(len(numstr) - 1):
        # adjacents
        if numstr[i] == numstr[i + 1]:
            if super_adjacents and numstr[i] == super_adjacents:
                continue
            # reset super_adjacents if we're past the end of it.
            elif super_adjacents:
                super_adjacents = None

            # check for 3+ adjacent same numbers.
            try:
                if numstr[i + 2] == numstr[i]:
                    super_adjacents = numstr[i]
            # but just ignore if we go past the end of the string
            except IndexError:
                pass

            # if we've made it to this point it passes this part of the test.
            if not super_adjacents or super_adjacents != numstr[i]:
                adjacents = True
                break

    if not adjacents:
        return False

    # make sure the numbers are always increasing.
    for i in range(len(numstr) - 1):
        if numstr[i] > numstr[i + 1]:
            return False

    return True


# do some sanity checks:
print(f"111111: {check_number(111111)}")
print(f"223450: {check_number(223450)}")
print(f"123789: {check_number(123789)}")
print(f"112233: {check_number(112233)}")
print(f"123444: {check_number(123444)}")
print(f"111122: {check_number(111122)}")

valids = [i for i in range(data[0], data[1] + 1) if check_number(i)]
print(f"The answer is {len(valids)}")
