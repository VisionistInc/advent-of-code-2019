import math
import json


def getDLS(ms, rocks):
    dls = set()  # Direct line of sight
    for a in rocks:
        if a != ms:
            dist = [a[0]-ms[0], a[1]-ms[1]]
            gcd = abs(math.gcd(dist[0], dist[1]))
            dls.add((math.floor(dist[0]/gcd), math.floor(dist[1]/gcd)))
    return dls


def getDetections(rocks):
    detections = []
    for ms in rocks:
        dls = getDLS(ms, rocks)
        detections.append((len(dls), ms, dls))
    detections.sort(reverse=True)
    return detections


def puzzle1(detections):
    return detections[0][0]


# Fiance wrote this
def puzzle2(detections):
    detected, ms, dls = detections[0]
    # Got a little help from my math nerd fiance
    # Still don't know/don't care what atan is
    vaporized = [(math.atan2(y, x), (x, y)) for x, y in dls]
    vaporized.sort(reverse=True)
    dx, dy = vaporized[200-1][1]

    x, y = ms[0]+dx, ms[1]+dy
    while (x, y) not in rocks:
        x, y = x+dx, y+dy
    return y * 100 + x


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().split('\n')
        rocks = set((x, y) for x, row in enumerate(data)
                    for y, _ in enumerate(row) if data[x][y] == '#')
        detections = getDetections(rocks)
        answer = {"puzzle_1_answer": puzzle1(
            detections), "puzzle_2_answer": puzzle2(detections)}
        with open('answers.json', 'w') as out:
            json.dump(answer, out)
