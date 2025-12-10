from collections import defaultdict, deque
from pathlib import Path
from sys import maxsize

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
    grand_sum = 0
    for i in range(n):
        machine_mask = machine_to_bitmask(machine[i])
        buttons_mask = list(map(buttons_to_bitmask, buttons[i]))
        grand_sum += solve_part_one_util(machine_mask, buttons_mask)
    return grand_sum


def solve_part_one_util(machine_bits: int, buttons_bits: list[int]) -> int:
    dist = defaultdict(lambda: maxsize)
    queue = deque()
    dist[0] = 0
    queue.append(0)
    while queue:
        for _ in range(len(queue)):
            bits = queue.popleft()
            if bits == machine_bits:
                return dist[bits]
            for button in buttons_bits:
                new_bits = bits ^ button
                if dist[new_bits] > dist[bits] + 1:
                    dist[new_bits] = dist[bits] + 1
                    queue.append(new_bits)
    raise ValueError


def solve_part_two(n: int, machine: list[str], buttons: list[list[str]], joltage: list[str]) -> int:
    pass


def machine_to_bitmask(machine: str) -> int:
    assert machine.startswith('[')
    assert machine.endswith(']')
    retval = 0
    for i, c in enumerate(machine[1:-1]):
        if c == '#':
            retval |= 1 << i
    return retval


def buttons_to_bitmask(buttons: str) -> int:
    assert buttons.startswith('(')
    assert buttons.endswith(')')
    retval = 0
    for i in map(int, buttons[1:-1].split(',')):
        retval |= 1 << i
    return retval


main()
