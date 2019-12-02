import json


def puzzle1(fuelz):
    return sum(fuelz)


def recurse(fuel):
    if fuel <= 0:
        return 0
    return fuel + recurse(fuel//3-2)


def puzzle2(fuelz):
    answer = 0
    for f in fuelz:
        answer += recurse(f)
    return answer


if __name__ == "__main__":
    fuelz = [int(line.rstrip('\n'))//3-2 for line in open('input.txt')]
    answer = {"puzzle_1_answer": puzzle1(
        fuelz), "puzzle_2_answer": puzzle2(fuelz)}
    with open('answers.json', 'w') as out:
        json.dump(answer, out)
