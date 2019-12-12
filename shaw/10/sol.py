import sys

with open('input') as f:
    maps = f.read()

total_asteroids = maps.count('#')

rows = maps.split()
num_rows = len(rows)
num_cols = len(rows[0])

already_blocking = []

def sight_blocked(rows, r, c, dr, dc):
    global already_blocking
    b = 0
    found = False
    while True:
        r += dr
        c += dc
        if r >= num_rows or r < 0:
            break
        if c >= num_cols or c < 0:
            break
        if [r,c] in already_blocking:
            continue
        if rows[r][c] == '#':
            already_blocking.append([r,c])
            if found:
                b += 1
            else:
                found = True
    return b

def get_blocked(rows, r, c):
    b = 0
    for dr in range(0, -num_rows, -1):
        for dc in range(0, -num_cols, -1):
            if dr == 0 and dc == 0:
                continue
            b += sight_blocked(rows, r, c, dr, dc)
    for dr in range(0, -num_rows, -1):
        for dc in range(0, num_cols, 1):
            if dr == 0 and dc == 0:
                continue
            b += sight_blocked(rows, r, c, dr, dc)
    for dr in range(0, num_rows, 1):
        for dc in range(0, -num_cols, -1):
            if dr == 0 and dc == 0:
                continue
            b += sight_blocked(rows, r, c, dr, dc)
    for dr in range(0, num_rows, 1):
        for dc in range(0, num_cols, 1):
            if dr == 0 and dc == 0:
                continue
            b += sight_blocked(rows, r, c, dr, dc)
    return b

for i in range(num_rows):
    rows[i] = list(rows[i])

blocked = total_asteroids
_r = -1
_c = -1

for r in range(num_rows):
    for c in range(num_cols):
        if rows[r][c] == '#':
            already_blocking = []
            b = get_blocked(rows, r, c)
            if b < blocked:
                blocked = b
                _r = r
                _c = c

print("Part 1: ", total_asteroids-blocked-1)

blown_up = 0

def blow_up(rows, r, c):
    global blown_up
    rows[r][c] = '.'
    blown_up += 1
    print(blown_up, c,r)
    if blown_up == 200:
        print("Part 2: ", (c*100)+r)
        sys.exit()

def wipe_out_quad(rows, d, r, c):
    for deg in sorted(d.keys()):
        closest = None
        dis = 99999999999
        for a in d[deg]:
            _dis = abs(a[0] - r) + abs(a[1] - c)
            if _dis < dis:
                dis = _dis
                closest = [a[0], a[1]]
        blow_up(rows, closest[0], closest[1])

def upper_right(rows, r, c):

    for y in range(r-1, 0, -1):
        if rows[y][c] == '#':
            blow_up(rows, y, c)
            break
    
    d = {}
    for y in range(r-1, -1, -1):
        for x in range(c+1, num_cols, 1):
            if rows[y][x] == '#':
                b = r-y
                t = x-c
                if t/b in d:
                    d[t/b].append([y,x])
                else:
                    d[t/b] = [[y,x]]

    wipe_out_quad(rows, d, r, c)

def lower_right(rows, r, c):
    for x in range(c+1, num_cols, 1):
        if rows[r][x] == '#':
            blow_up(rows, r, x)
            break
    
    d = {}
    for y in range(r+1, num_rows, 1):
        for x in range(c+1, num_cols, 1):
            if rows[y][x] == '#':
                b = x-c
                t = y-r
                if t/b in d:
                    d[t/b].append([y,x])
                else:
                    d[t/b] = [[y,x]]
    
    wipe_out_quad(rows, d, r, c)

def lower_left(rows, r, c):
    for y in range(r+1, num_rows, 1):
        if rows[y][c] == '#':
            blow_up(rows, y, c)
            break
    
    d = {}
    for y in range(r+1, num_rows, 1):
        for x in range(c-1, -1, -1):
            if rows[y][x] == '#':
                b = y-r
                t = c-x
                if t/b in d:
                    d[t/b].append([y,x])
                else:
                    d[t/b] = [[y,x]]
    
    wipe_out_quad(rows, d, r, c)

def upper_left(rows, r, c):
    for x in range(c-1, -1, -1):
        if rows[r][x] == '#':
            blow_up(rows, r, x)
            break
    
    d = {}
    for y in range(r-1, -1, -1):
        for x in range(c-1, -1, -1):
            if rows[y][x] == '#':
                b = c-x
                t = r-y
                if t/b in d:
                    d[t/b].append([y,x])
                else:
                    d[t/b] = [[y,x]]
    
    wipe_out_quad(rows, d, r, c)

while True:
    upper_right(rows, _r, _c)
    lower_right(rows, _r, _c)
    lower_left(rows, _r, _c)
    upper_left(rows, _r, _c)