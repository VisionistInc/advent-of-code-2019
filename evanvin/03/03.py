import json


def calculateSteps(ps, hm):
    for p in range(len(ps)):
        step = -1
        for i in range(len(ps[p])):
            step += 1
            if tuple(ps[p][i]) in hm:
                hm[tuple(ps[p][i])]['steps'] += step
                hm[tuple(ps[p][i])]['done'][p] = True


def getIntersections(paths):
    a = set(map(tuple, paths[0]))
    b = set(map(tuple, paths[1]))
    return a & b


def getPathCoords(d):
    path, x, y = [[0, 0]], 0, 0
    for i in range(len(d)):
        xx, yy = 0, 0
        if d[i][0] == 'R':
            xx = 1
        elif d[i][0] == 'D':
            yy = 1
        elif d[i][0] == 'L':
            xx = -1
        else:
            yy = -1
        num = int(d[i][1:])
        for j in range(num):
            x += xx
            y += yy
            path.append([x, y])
    return path


def getPaths(dirs):
    paths = []
    for i in range(len(dirs)):
        paths.append(getPathCoords(dirs[i]))
    return paths


def puzzle1(dirs):
    paths = getPaths(dirs)
    c = getIntersections(paths)
    minDist = float("inf")
    for (i, j) in list(c):
        if i != 0 or j != 0:
            dist = abs(0-i) + abs(0-j)
            minDist = dist if dist < minDist else minDist
    return minDist


def puzzle2(dirs):
    paths = getPaths(dirs)
    intersections = getIntersections(paths)
    intersections.discard((0, 0))
    hashmap = {c: {'steps': 0, 'done': [False, False]} for c in intersections}
    calculateSteps(paths, hashmap)
    return sorted([c['steps'] for c in hashmap.values()])[0]


if __name__ == "__main__":
    directions = []
    with open('input.txt', 'r') as fp:
        for line in fp:
            directions.append([x for x in line.split(',')])
        answer = {"puzzle_1_answer": puzzle1(
            directions), "puzzle_2_answer": puzzle2(directions)}
        with open('answers.json', 'w') as out:
            json.dump(answer, out)
