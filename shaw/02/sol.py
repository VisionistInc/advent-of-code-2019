import sys

def run(code):
    ip = 0
    while code[ip] != 99:
        if code[ip] == 1:
            code[code[ip+3]] = code[code[ip+2]] + code[code[ip+1]]
        elif code[ip] == 2:
            code[code[ip+3]] = code[code[ip+2]] * code[code[ip+1]]
        else:
            print("Unknown opcode %d at %d" % (code[ip], ip))
            sys.exit()
        ip = ip + 4
    return code[0]


with open('input') as f:
    code = f.read()

gold = code.split(',')

for i in range(len(gold)):
    gold[i] = int(gold[i])

code = gold.copy()

code[1] = 12
code[2] = 2

print("Part 1: ", run(code))

for noun in range(100):
    for verb in range(100):
        code = gold.copy()
        code[1] = noun
        code[2] = verb
        if run(code) == 19690720:
            print("Part 2: ", noun*100+verb)
            sys.exit()
