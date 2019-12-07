import networkx as nx
import json


def createTree(orbits):
    tree = nx.Graph()
    planets = set()
    for o in orbits:
        tree.add_edge(o[0], o[1])
        tree.add_edge(o[1], o[0])
        planets.add(o[0])
        planets.add(o[1])
    return tree, planets


def puzzle1(tree, planets):
    answer = 0
    for p in planets:
        answer += nx.shortest_path_length(tree, "COM", p)
    return answer


def puzzle2(tree):
    return nx.shortest_path_length(tree, "YOU", "SAN")-2


if __name__ == "__main__":
    orbits = [x.strip().split(')') for x in open('input.txt').readlines()]
    tree, planets = createTree(orbits)
    answer = {"puzzle_1_answer": puzzle1(
        tree, planets), "puzzle_2_answer": puzzle2(tree)}
    with open('answers.json', 'w') as out:
        json.dump(answer, out)
