import sys


grid = [list(line.strip()) for line in sys.stdin]

width = len(grid[0])
height = len(grid)


def is_bound(x: int, y: int) -> bool:
    return 0 <= x < width and 0 <= y < height


def has_fewer_than_n_rolls_of_papers(x: int, y: int, n: int) -> bool:
    if not is_bound(x, y):
        return False
    rolls_of_papers = 0
    for ny in range(y-1, y+2):
        for nx in range(x-1, x+2):
            if not is_bound(nx, ny) or (nx == x and ny == y):
                continue
            if grid[ny][nx] == '@':
                rolls_of_papers += 1
    return rolls_of_papers < n


################################################################
# 그래프 탐색용 방문 로직 구현
################################################################

stack = []


def is_visitable(x: int, y: int) -> bool:
    if not is_bound(x, y):
        return False
    if grid[y][x] != '@':
        return False
    return has_fewer_than_n_rolls_of_papers(x, y, 4)


def visit(x: int, y: int):
    global stack
    for ny in range(y-1, y+2):
        for nx in range(x-1, x+2):
            if is_visitable(nx, ny):
                stack.append((nx, ny))
                grid[ny][nx] = 'x'


################################################################
# 솔루션
################################################################

def solve_part_1():
    count = 0
    for y in range(height):
        for x in range(width):
            if is_visitable(x, y):
                count += 1
    return count


def solve_part_2() -> int:
    # Graph traverse
    for y in range(height):
        for x in range(width):
            if is_visitable(x, y):
                visit(x, y)

    while stack:
        x, y = stack.pop()
        visit(x, y)

    count = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'x':
                count += 1
    return count


if __name__ == '__main__':
    # print(solve_part_1())
    print(solve_part_2())
