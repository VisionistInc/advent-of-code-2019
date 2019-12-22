from copy import deepcopy
POS = 0
VEL = 1

class Moon(object):
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.xv = 0
        self.yv = 0
        self.zv = 0
    
    def change_vel(self, moon):
        if moon.x > self.x:
            moon.xv -= 1
            self.xv += 1
        elif moon.x < self.x:
            moon.xv += 1
            self.xv -= 1
        if moon.y > self.y:
            moon.yv -= 1
            self.yv += 1
        elif moon.y < self.y:
            moon.yv += 1
            self.yv -= 1
        if moon.z > self.z:
            moon.zv -= 1
            self.zv += 1
        elif moon.z < self.z:
            moon.zv += 1
            self.zv -= 1
    
    def update(self):
        self.x += self.xv
        self.y += self.yv
        self.z += self.zv
    
    def energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.xv) + abs(self.yv) + abs(self.zv))
    
    def show(self):
        print(self.x, self.y, self.z, self.xv, self.yv, self.zv)


with open('input') as f:
    lines = f.read()

lines = lines.split('\n')

moons = []

for line in lines:
    x,y,z = line.split(', ')
    x = int(x[3:])
    y = int(y[2:])
    z = int(z[2:len(z)-1])
    moons.append(Moon(x,y,z))

gold = deepcopy(moons)

for i in range(1000):
    for j in range(0, len(moons)-1):
        for k in range(j, len(moons)):
            moons[j].change_vel(moons[k])
    for j in range(0, len(moons)):
        moons[j].update()

energy = 0
for i in range(len(moons)):
    energy += moons[i].energy()

print('Part 1: ', energy)

moons = deepcopy(gold)
orig = deepcopy(gold)
x_rep = 0
y_rep = 0
z_rep = 0
cnt = 0

while(x_rep == 0 or y_rep == 0 or z_rep == 0):
    cnt += 1
    for j in range(0, len(moons)-1):
        for k in range(j, len(moons)):
            moons[j].change_vel(moons[k])
    for j in range(0, len(moons)):
        moons[j].update()
    
    if (x_rep == 0):
        match = True
        for i in range(len(moons)):
            if orig[i].x != moons[i].x or orig[i].xv != moons[i].xv:
                match = False
        if match:
            x_rep = cnt

    if (y_rep == 0):
        match = True
        for i in range(len(moons)):
            if orig[i].y != moons[i].y or orig[i].yv != moons[i].yv:
                match = False
        if match:
            y_rep = cnt

    if (z_rep == 0):
        match = True
        for i in range(len(moons)):
            if orig[i].z != moons[i].z or orig[i].zv != moons[i].zv:
                match = False
        if match:
            z_rep = cnt
            
# find lcm of x and y (xy)
# find lcm of x and z (xz)
# find lcm of xy and xz (solution)

x = x_rep
y = y_rep
z = z_rep

while x != y:
    if x < y:
        x += x_rep
    else:
        y += y_rep

xy = x
xy_rep = x

x = x_rep
y = y_rep
z = z_rep

while x != z:
    if x < z:
        x += x_rep
    else:
        z += z_rep

xz = x
xz_rep =x

while xy != xz:
    if xy < xz:
        xy += xy_rep
    else:
        xz += xz_rep

print('Part 2: ', xz)