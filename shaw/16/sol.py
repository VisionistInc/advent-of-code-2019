import time

def summer(l, a, b):
    s = 0
    for x in range(a,b):
        s += l[x]
        
with open('input') as f:
    nums = f.read()

gold = [int(num) for num in nums]

nums = gold.copy()
len_nums = len(nums)


for x in range(100):
    nxt = []
    i = 0
    while i < len_nums:
        mul = i + 1
        adders = []
        subs = []
        tot = 0
        j = 0
        while j <= len_nums-i:
            o = j + i
            tot += sum(nums[o:o+mul])
            j += (4 * mul)
        j = 2 * mul
        while j <= len_nums-i:
            o = j + i
            tot -= sum(nums[o:o+mul])
            j += (4 * mul)
        nxt.append(abs(tot) % 10)
        i += 1
    nums = nxt

print('Part 1: ', ''.join([str(n) for n in nums[0:8]]))

nums = []

for i in range(10000):
    nums.extend(gold.copy())
len_nums = len(nums)

print('Part 2: ', 'Not solved')