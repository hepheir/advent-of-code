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
    pass


def solve_part_two(X: list[int], Y: list[int]) -> int:
    pass


main()
