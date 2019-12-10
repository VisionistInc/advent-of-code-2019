import sys

with open('input') as f:
    pix = f.read()

X = 25
Y = 6
SIZE = X * Y
zeros = SIZE
value = 0

i = 0
while i < len(pix):
    if pix[i:i+SIZE].count('0') < zeros:
        zeros = pix[i:i+SIZE].count('0')
        value = pix[i:i+SIZE].count('1') * pix[i:i+SIZE].count('2')
    i += SIZE

print('Part 1', value)

final = ['2'] * SIZE

for i in range(SIZE):
    j = i
    while j < len(pix):
        if pix[j] != '2':
            final[i] = pix[j]
            break
        j += SIZE

print('Part 2')
i = 0
while (i < SIZE):
    s = ''
    for c in final[i:i+X]:
        if c == '0':
            s += ' '
        else:
            s += '*'
    print(s)
    i += X