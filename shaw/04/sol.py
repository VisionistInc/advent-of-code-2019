import sys

def validPart1(s):
    for i in range(1,6):
        if s[i] == s[i-1]:
            return True
    return False

def validPart2(s):
    i = 1
    c = s[0]
    n = 1
    while i < 6:
        if s[i] == c:
            n += 1
        else:
            if n == 2:
                return True
            c = s[i]
            n = 1        
        i += 1

    if n == 2:
        return True
    return False

with open('input') as f:
    lines = f.read()

numbers = lines.split('-')

low = int(numbers[0])
hi = int(numbers[1])

inc_list = []

for x in range(low, hi+1):
    s = '%d' % x
    decrease = False
    for i in range(1,6):
        if s[i] < s[i-1]:
            decrease = True
            break
    
    if not decrease:
        inc_list.append(s)

count = 0

for i in inc_list:
    if validPart1(i):
        count += 1

print('Part 1: ' , count)

count = 0

for i in inc_list:
    if validPart2(i):
        count += 1

print('Part 2: ' , count)