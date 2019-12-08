import sys

with open('input') as f:
    orbits = f.read()

gold = orbits.split()
orbits = gold.copy()
orbit_count = 0
multi = 1

bodies = ['COM']
next_bodies = []

while True:
    removes = []
    while len(bodies) > 0:
        body = bodies.pop()
        s = '%s)' % body
        for o in orbits:
            if s in o:
                removes.append(o)
                a,b = o.split(')')
                next_bodies.append(b)
    if len(next_bodies) == 0:
        break
    for r in removes:
        orbits.remove(r)
    orbit_count += len(next_bodies) * multi
    multi += 1
    bodies = list(next_bodies)
    next_bodies = []

print('Part 1:', orbit_count)

orbits = gold.copy()
orbit_count = 0

bodies = ['YOU']
next_bodies = []

while True:
    removes = []
    while len(bodies) > 0:
        body = bodies.pop()
        if body == 'SAN':
            print('Part 2:', orbit_count-2)
            sys.exit()
        s = '%s)' % body
        t = ')%s' % body
        for o in orbits:
            if s in o:
                removes.append(o)
                a,b = o.split(')')
                next_bodies.append(b)
            if t in o:
                removes.append(o)
                a,b = o.split(')')
                next_bodies.append(a)
    if len(next_bodies) == 0:
        break
    for r in removes:
        orbits.remove(r)
    orbit_count += 1
    bodies = list(next_bodies)
    next_bodies = []