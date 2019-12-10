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
UPREL= 9
HALT = 99
POS = 0
IMM = 1
REL = 2


class Code(object):
    def __init__(self, code, input):
        self.code = code.copy()
        self.ip = 0
        self.input = input.copy()
        self.terminated = False
        self.rel = 0
        self.last_out = None
    
    def _grow_mem(self, p):
        if p > len(self.code)-1:
            extra = [0] * (p - (len(self.code)-1))
            self.code.extend(extra)
    
    def _get_param(self, p, mode):
        if mode == IMM:
            return p
        if mode == REL:
            pos = p + self.rel
        else:
            pos = p
        return self._read_mem(pos)
    
    def _get_dest(self, p, mode):
        if mode == REL:
            return p + self.rel
        else:
            return p
    
    def _read_mem(self, addr):
        self._grow_mem(addr)
        return self.code[addr]

    def _write_mem(self, addr, val):
        self._grow_mem(addr)
        self.code[addr] = val
    
    def add_input(self, x):
        self.input.append(x)
    
    def has_input(self):
        if self.terminated:
            return False
        if len(self.input) > 0:
            return True
        return False

    def is_termineted(self):
        return self.terminated

    def get_last_out(self):
        return self.last_out
    
    def _breakdown(self, inst, ip):
        mode = [0,0,0]
        mode[2], inst = divmod(inst,10000)
        mode[1], inst = divmod(inst,1000)
        mode[0], inst = divmod(inst,100)
        p1 = self._read_mem(ip+1)
        p2 = self._read_mem(ip+2)
        p3 = self._read_mem(ip+3)
        
        return inst, mode, p1, p2, p3

    
    def run(self):
        last_output = 0
        while True:
            inst = self.code[self.ip]
            opcode, mode, p1, p2, p3 = self._breakdown(inst, self.ip)
            if opcode == HALT:
                self.terminated = True
                break
            if opcode == ADD:
                p3 = self._get_dest(p3, mode[2])
                p2 = self._get_param(p2, mode[1])
                p1 = self._get_param(p1, mode[0])
                self._write_mem(p3, p1 + p2)
                self.ip += 4
            elif opcode == MUL:
                p3 = self._get_dest(p3, mode[2])
                p2 = self._get_param(p2, mode[1])
                p1 = self._get_param(p1, mode[0])
                self._write_mem(p3, p1 * p2)
                self.ip += 4
            elif opcode == IN:
                p1 = self._get_dest(p1, mode[0])
                if len(self.input) == 0:
                    return None
                self._write_mem(p1, self.input.pop(0))
                self.ip += 2
            elif opcode == OUT:
                p1 = self._get_param(p1, mode[0])
                self.last_out = p1
                self.ip += 2
                return last_output
            elif opcode == JMPT:
                p1 = self._get_param(p1, mode[0])
                p2 = self._get_param(p2, mode[1])
                if p1 == 0:
                    self.ip += 3
                else:
                    self.ip = p2
            elif opcode == JMPF:
                p1 = self._get_param(p1, mode[0])
                p2 = self._get_param(p2, mode[1])
                if p1 != 0:
                    self.ip += 3
                else:
                    self.ip = p2
            elif opcode == LESS:
                p3 = self._get_dest(p3, mode[2])
                p2 = self._get_param(p2, mode[1])
                p1 = self._get_param(p1, mode[0])
                if p1 < p2:
                    val = 1
                else:
                    val = 0
                self._write_mem(p3, val)
                self.ip += 4
            elif opcode == EQU:
                p3 = self._get_dest(p3, mode[2])
                p2 = self._get_param(p2, mode[1])
                p1 = self._get_param(p1, mode[0])
                if p1 == p2:
                    val = 1
                else:
                    val = 0
                self._write_mem(p3, val)
                self.ip += 4
            elif opcode == UPREL:
                p1 = self._get_param(p1, mode[0])
                self.rel += p1
                self.ip += 2
            else:
                print("Unknown opself.code %d at %d" % (opcode, self.ip))
                sys.exit()
        return None

with open('input') as f:
    code = f.read()

gold = code.split(',')

for i in range(len(gold)):
    gold[i] = int(gold[i])

boost = Code(gold.copy(), [1])

while (not boost.is_termineted()):
    part1 = boost.run()
    if not boost.is_termineted():
        print(boost.get_last_out())

print("Part 1: ", boost.get_last_out())

boost = Code(gold.copy(), [2])

while (not boost.is_termineted()):
    part1 = boost.run()
    if not boost.is_termineted():
        print(boost.get_last_out())

print("Part 2: ", boost.get_last_out())