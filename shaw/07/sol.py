import sys
import itertools

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

class amp(object):
    def __init__(self, code, input):
        self.code = code.copy()
        self.ip = 0
        self.input = input.copy()
        self.terminated = False
    
    def _get_param(self, p, mode):
        if mode == IMM:
            return p
        return self.code[p]
    
    def add_input(self, x):
        self.input.append(x)
    
    def has_input(self):
        if self.terminated:
            return False
        if len(self.input) > 0:
            return True
        return False
    
    def run(self):
        last_output = 0
        mode = [0,0,0]
        while True:
            opcode = self.code[self.ip]
            mode[2], opcode = divmod(opcode,10000)
            mode[1], opcode = divmod(opcode,1000)
            mode[0], opcode = divmod(opcode,100)
            if opcode == HALT:
                self.terminated = True
                break
            if opcode == ADD:
                p1 = self._get_param(self.code[self.ip+1], mode[0])
                p2 = self._get_param(self.code[self.ip+2], mode[1])
                self.code[self.code[self.ip+3]] = p1 + p2
                self.ip += 4
            elif opcode == MUL:
                p1 = self._get_param(self.code[self.ip+1], mode[0])
                p2 = self._get_param(self.code[self.ip+2], mode[1])
                self.code[self.code[self.ip+3]] = p1 * p2
                self.ip += 4
            elif opcode == IN:
                if len(self.input) == 0:
                    return None
                self.code[self.code[self.ip+1]] = self.input.pop(0)
                self.ip += 2
            elif opcode == OUT:
                last_output = self._get_param(self.code[self.ip+1], mode[0])
                self.ip += 2
                return last_output
            elif opcode == JMPT:
                p1 = self._get_param(self.code[self.ip+1], mode[0])
                p2 = self._get_param(self.code[self.ip+2], mode[1])
                if p1 == 0:
                    self.ip += 3
                else:
                    self.ip = p2
            elif opcode == JMPF:
                p1 = self._get_param(self.code[self.ip+1], mode[0])
                p2 = self._get_param(self.code[self.ip+2], mode[1])
                if p1 != 0:
                    self.ip += 3
                else:
                    self.ip = p2
            elif opcode == LESS:
                p1 = self._get_param(self.code[self.ip+1], mode[0])
                p2 = self._get_param(self.code[self.ip+2], mode[1])
                if p1 < p2:
                    val = 1
                else:
                    val = 0
                self.code[self.code[self.ip+3]] = val
                self.ip += 4
            elif opcode == EQU:
                p1 = self._get_param(self.code[self.ip+1], mode[0])
                p2 = self._get_param(self.code[self.ip+2], mode[1])
                if p1 == p2:
                    val = 1
                else:
                    val = 0
                self.code[self.code[self.ip+3]] = val
                self.ip += 4
            else:
                print("Unknown opself.code %d at %d" % (opcode, self.ip))
                sys.exit()
        return None

with open('input') as f:
    code = f.read()

gold = code.split(',')

for i in range(len(gold)):
    gold[i] = int(gold[i])

part1 = -999999999999

perms = list(itertools.permutations([0, 1, 2, 3, 4]))
for p in perms: 
    amp1 = amp(gold.copy(), [p[0],0])
    amp2 = amp(gold.copy(), [p[1]])
    amp3 = amp(gold.copy(), [p[2]])
    amp4 = amp(gold.copy(), [p[3]])
    amp5 = amp(gold.copy(), [p[4]])
    while True:
        if amp1.has_input():
            op = amp1.run()
            if op != None:
                amp2.add_input(op)
        elif amp2.has_input():
            op = amp2.run()
            if op != None:
                amp3.add_input(op)
        elif amp3.has_input():
            op = amp3.run()
            if op != None:
                amp4.add_input(op)
        elif amp4.has_input():
            op = amp4.run()
            if op != None:
                amp5.add_input(op)
        elif amp5.has_input():
            op = amp5.run()
            if op != None:
                part1 = max(part1, op)
        else:
            break

print('Part 1:', part1)

part2 = -999999999999

perms = list(itertools.permutations([5, 6, 7, 8, 9]))
for p in perms: 
    amp1 = amp(gold.copy(), [p[0],0])
    amp2 = amp(gold.copy(), [p[1]])
    amp3 = amp(gold.copy(), [p[2]])
    amp4 = amp(gold.copy(), [p[3]])
    amp5 = amp(gold.copy(), [p[4]])
    last_out = 0
    while True:
        if amp1.has_input():
            op = amp1.run()
            if op != None:
                amp2.add_input(op)
        elif amp2.has_input():
            op = amp2.run()
            if op != None:
                amp3.add_input(op)
        elif amp3.has_input():
            op = amp3.run()
            if op != None:
                amp4.add_input(op)
        elif amp4.has_input():
            op = amp4.run()
            if op != None:
                amp5.add_input(op)
        elif amp5.has_input():
            op = amp5.run()
            if op != None:
                amp1.add_input(op)
                last_out = op
        else:
            break
    part2 = max(part2, last_out)

print('Part 2:', part2)