from functools import cache
from pathlib import Path


# INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'


GRID = INPUT_FILE.read_text().strip().splitlines()
H = len(GRID)
W = len(GRID[0].rstrip())


def solve_part_one():
    # +2칸 해준 것은 -1, W 번 인덱스를 위한 padding.
    split_count = 0
    curr_row = list(GRID[0])
    for y in range(1, H):
        prev_row = curr_row
        curr_row = list(GRID[y])
        for x in range(W):
            # 히히 case works
            if prev_row[x] == 'S':
                if curr_row[x] == '.':
                    curr_row[x] = '|'
            elif prev_row[x] == '|':
                if curr_row[x] == '.':
                    curr_row[x] = '|'
                elif curr_row[x] == '^':
                    split_count += 1
                    if (0 < x) and curr_row[x-1] == '.':
                        curr_row[x-1] = '|'
                    if (x+1 < W) and curr_row[x+1] == '.':
                        curr_row[x+1] = '|'
    return split_count


def solve_part_two():
    for x in range(W):
        if GRID[0][x] == 'S':
            return count_timelines_BT(x, 1)
    raise ValueError


@cache
def count_timelines_BT(x: int, y: int) -> int:
    # Backtracking
    if y == H:
        return 1
    count = 0
    if GRID[y][x] == '.':
        count += count_timelines_BT(x, y+1)
    if GRID[y][x] == '^':
        if (0 < x) and GRID[y][x-1] == '.':
            count += count_timelines_BT(x-1, y+1)
        if (x+1 < W) and GRID[y][x+1] == '.':
            count += count_timelines_BT(x+1, y+1)
    return count


print(solve_part_one())
print(solve_part_two())
