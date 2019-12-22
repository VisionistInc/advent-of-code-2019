import copy

QTY = 0
PARTS = 1

class Equ:
    def __init__(self, q, s):
        self.qty = q
        self.parts = {}
        s = s.split(', ')
        for p in s:
            q,n = p.split(' ')
            self.parts[n] = int(q)

with open('input') as f:
    reactions = f.read()

gold = reactions.split('\n')

def get_dis(d, k):
    if len(d[k].parts) == 1:
        if 'ORE' in d[k].parts:
            return 1
    n = 0
    for _k in d[k].parts.keys():
        n += (get_dis(d, _k) + 1)
    return n


d = {}

for g in gold:
    l,r = g.split(' => ')
    q,n = r.split(' ')
    d[n] = Equ(int(q), l)

gold = copy.deepcopy(d)

def get_ore(d):
    while True:
        if len(d['FUEL'].parts) == 1:
            if 'ORE' in d['FUEL'].parts:
                return d['FUEL'].parts['ORE']
        longest = ''
        n = 0
        for k in d['FUEL'].parts.keys():
            if k == 'ORE':
                continue
            dis = get_dis(d, k)
            if dis > n:
                n = dis
                longest = k
        needed = d['FUEL'].parts[longest]
        makes = d[longest].qty
        multi = needed // makes
        if ((needed % makes) != 0):
            multi += 1
        del d['FUEL'].parts[longest]
        for k in d[longest].parts.keys():
            if not k in d['FUEL'].parts:
                d['FUEL'].parts[k] = 0
            d['FUEL'].parts[k] += (d[longest].parts[k] * multi)

part1 = get_ore(copy.deepcopy(gold))
print("Part 1: ", part1)

ore = 0
fuel = 1000000000000 // part1

while True:
    d = copy.deepcopy(gold)
    d['FUEL'].qty *= fuel
    for k in d['FUEL'].parts:
        d['FUEL'].parts[k] *= fuel
    ore = get_ore(d)
    if (ore > 1000000000000):
        break
    add = (1000000000000 - ore) // part1
    if add == 0:
        add = 1
    fuel += add

while True:
    fuel -= 1
    d = copy.deepcopy(gold)
    d['FUEL'].qty *= fuel
    for k in d['FUEL'].parts:
        d['FUEL'].parts[k] *= fuel
    ore = get_ore(d)
    if (ore <= 1000000000000):
        break

print("Part 2: ", fuel)

