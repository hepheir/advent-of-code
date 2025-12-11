from collections import defaultdict, deque
from pathlib import Path
from sys import maxsize

EXAMPLE_INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
PUZZLE_INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'


def main():
    input_file = PUZZLE_INPUT_FILE

    raw_machines = []
    raw_buttons = []
    raw_joltages = []

    for line in input_file.read_text().splitlines():
        tokens = line.split()
        raw_machines.append(tokens[0])
        raw_buttons.append(tokens[1:-1])
        raw_joltages.append(tokens[-1])

    print(solve_part_one(raw_machines, raw_buttons, raw_joltages))
    print(solve_part_two(raw_machines, raw_buttons, raw_joltages))


def solve_part_one(raw_machines: list[str], raw_buttons: list[list[str]], raw_joltages: list[str]) -> int:
    grand_sum = 0
    for raw_machine, raw_button in zip(raw_machines, raw_buttons):
        machine_mask = machine_to_bitmask(raw_machine)
        buttons_mask = list(map(buttons_to_bitmask, raw_button))
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


def solve_part_two(raw_machines: list[str], raw_buttons: list[list[str]], raw_joltages: list[str]) -> int:
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
