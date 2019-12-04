import json


def runProgram(opcode):
    oc = opcode[:]
    idx = 0
    while idx < len(oc):
        if oc[idx] is 1:
            # addition
            oc[oc[idx+3]] = oc[oc[idx+1]]+oc[oc[idx+2]]
        elif oc[idx] is 2:
            # multiplication
            oc[oc[idx+3]] = oc[oc[idx+1]]*oc[oc[idx+2]]
        elif oc[idx] is 99:
            break
        idx += 4

    return oc


def puzzle1(opcode):
    opcode[1] = 12
    opcode[2] = 2
    return runProgram(opcode)[0]


def puzzle2(opcode):
    n = 0
    v = 0
    while runProgram(opcode)[0] != 19690720 and n != 100:
        if v == 99:
            n += 1
            v = 0
        else:
            v += 1
        opcode[1] = n
        opcode[2] = v
    return 100*n+v


if __name__ == "__main__":
    input = open('input.txt', 'r')
    for line in input.readlines():
        opcode = [int(x) for x in line.split(',')
        answer = {"puzzle_1_answer": puzzle1(
            opcode), "puzzle_2_answer": puzzle2(opcode)}
        with open('answers.json', 'w') as out:
            json.dump(answer, out)
