import json
from collections import Counter


def is_increasing(n):
    return int(''.join(sorted([str(d) for d in str(n)]))) == n


def has_double(n):
    return len(str(n)) > len(set(str(n)))


def has_perfect_double(n):
    cnts = Counter([d for d in str(n)]).values()
    return any(c == 2 for c in cnts)


def puzzle1(rng):
    cnt = 0
    for n in range(rng[0]+1, rng[1]):
        if has_double(n) and is_increasing(n):
            cnt += 1
    return cnt


def puzzle2(rng):
    cnt = 0
    for n in range(rng[0]+1, rng[1]):
        if has_perfect_double(n) and is_increasing(n):
            cnt += 1
    return cnt


if __name__ == "__main__":
    answer = {"puzzle_1_answer": puzzle1(
        [146810, 612564]), "puzzle_2_answer": puzzle2([146810, 612564])}
    with open('answers.json', 'w') as out:
        json.dump(answer, out)
