from pathlib import Path


IS_EXAMPLE = True


def main():
    if IS_EXAMPLE:
        INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
    else:
        INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'

    X = []
    Y = []
    for line in INPUT_FILE.read_text().strip().splitlines():
        x, y = map(int, line.split(','))
        X.append(x)
        Y.append(y)

    print(solve_part_one(X, Y))
    print(solve_part_two(X, Y))


def solve_part_one(X: list[int], Y: list[int]) -> int:
    areas = []
    for j in range(len(X)):
        for i in range(j):
            w = abs(X[i]-X[j])+1
            h = abs(Y[i]-Y[j])+1
            areas.append(w * h)
    return max(areas)


def solve_part_two(X: list[int], Y: list[int]) -> int:
    pass


main()
