from pathlib import Path


IS_EXAMPLE = True


def main():
    if IS_EXAMPLE:
        INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
    else:
        INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'

    MACHINE = []
    BUTTONS = []
    JOLTAGE = []

    N = 0
    for line in INPUT_FILE.read_text().splitlines():
        tokens = line.split()
        MACHINE.append(tokens[0])
        BUTTONS.append(tokens[1:-1])
        JOLTAGE.append(tokens[-1])
        N += 1

    print(solve_part_one(N, MACHINE, BUTTONS, JOLTAGE))
    print(solve_part_two(N, MACHINE, BUTTONS, JOLTAGE))


def solve_part_one(n: int, machine: list[str], buttons: list[list[str]], joltage: list[str]) -> int:
    pass


def solve_part_two(n: int, machine: list[str], buttons: list[list[str]], joltage: list[str]) -> int:
    pass


main()
