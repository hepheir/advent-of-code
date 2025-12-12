from pathlib import Path
from typing import List


INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
# INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'


raw_presents: List[List[str]] = []
raw_regions: List[str] = []


def main():
    is_present = False
    for line in INPUT_FILE.read_text().strip().splitlines():
        line = line.strip()
        if not line:
            is_present = False
        elif line.endswith(':'):
            is_present = True
            raw_presents.append([])
        elif is_present:
            raw_presents[-1].append(line)
        else:
            raw_regions.append(line)

    print(solve_part_one())
    print(solve_part_two())


def solve_part_one():
    pass


def solve_part_two():
    pass


main()
