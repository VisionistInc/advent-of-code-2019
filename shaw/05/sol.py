import sys

ADD  = 1
MUL  = 2
IN   = 3
OUT  = 4
JMPT = 5
JMPF = 6
LESS = 7
EQU  = 8
HALT = 99
POS = 0
IMM = 1

code_input = []

def getParam(code, p, mode):
    if mode == IMM:
        return p
    return code[p]

def run(code):
    ip = 0
    last_output = 0
    mode = [0,0,0]
    while code[ip] != HALT:
        mode[2], code[ip] = divmod(code[ip],10000)
        mode[1], code[ip] = divmod(code[ip],1000)
        mode[0], code[ip] = divmod(code[ip],100)
        if code[ip] == ADD:
            p1 = getParam(code, code[ip+1], mode[0])
            p2 = getParam(code, code[ip+2], mode[1])
            code[code[ip+3]] = p1 + p2
            ip += 4
        elif code[ip] == MUL:
            p1 = getParam(code, code[ip+1], mode[0])
            p2 = getParam(code, code[ip+2], mode[1])
            code[code[ip+3]] = p1 * p2
            ip += 4
        elif code[ip] == IN:
            code[code[ip+1]] = code_input.pop()
            ip += 2
        elif code[ip] == OUT:
            last_output = getParam(code, code[ip+1], mode[0])
            print(last_output)
            ip += 2
        elif code[ip] == JMPT:
            p1 = getParam(code, code[ip+1], mode[0])
            p2 = getParam(code, code[ip+2], mode[1])
            if p1 == 0:
                ip += 3
            else:
                ip = p2
        elif code[ip] == JMPF:
            p1 = getParam(code, code[ip+1], mode[0])
            p2 = getParam(code, code[ip+2], mode[1])
            if p1 != 0:
                ip += 3
            else:
                ip = p2
        elif code[ip] == LESS:
            p1 = getParam(code, code[ip+1], mode[0])
            p2 = getParam(code, code[ip+2], mode[1])
            if p1 < p2:
                val = 1
            else:
                val = 0
            code[code[ip+3]] = val
            ip += 4
        elif code[ip] == EQU:
            p1 = getParam(code, code[ip+1], mode[0])
            p2 = getParam(code, code[ip+2], mode[1])
            if p1 == p2:
                val = 1
            else:
                val = 0
            code[code[ip+3]] = val
            ip += 4
        else:
            print("Unknown opcode %d at %d" % (code[ip], ip))
            sys.exit()
    return last_output


with open('input') as f:
    code = f.read()

gold = code.split(',')

for i in range(len(gold)):
    gold[i] = int(gold[i])

code = gold.copy()
code_input.append(1)

part1 = run(code)

print('Part 1: ', part1)

code = gold.copy()
code_input.append(5)

part2 = run(code)

print('Part 2: ', part2)