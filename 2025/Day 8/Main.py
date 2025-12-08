from collections import Counter
from functools import reduce
from math import hypot
from operator import mul
from pathlib import Path


IS_EXAMPLE = True
PART_ONE_EDGES = 10
V = []
E = []


def main():
    global V, E, PART_ONE_EDGES
    if IS_EXAMPLE:
        INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
    else:
        INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'
        PART_ONE_EDGES = 1000

    for line in INPUT_FILE.read_text().strip().splitlines():
        x, y, z = map(int, line.split(','))
        V.append((x, y, z))

    for j in range(len(V)):
        for i in range(j):
            x1, y1, z1 = V[i]
            x2, y2, z2 = V[j]
            dist = hypot(x1-x2, y1-y2, z1-z2)
            E.append((dist, i, j))

    print(solve_part_one())


# Disjoint set via union-find
rank = {}


def union(i: int, j: int):
    i = find(i)
    j = find(j)
    if i != j:
        rank[j] = i


def find(i: int) -> int:
    rank[i] = rank.get(i, i)
    if i != rank[i]:
        rank[i] = find(rank[i])
    return rank[i]


def solve_part_one():
    E.sort()
    for i in range(PART_ONE_EDGES):
        _, u, v = E[i]
        union(u, v)

    counter = Counter()
    for i in range(len(V)):
        counter[find(i)] += 1

    return reduce(mul, [v for k, v in counter.most_common(3)])


main()
