from pathlib import Path
from sys import setrecursionlimit


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
    # 좌표를 압축하고 실제로 그리그 그래프 구성하기.
    # 입력에서 주어진 총 정점 수가 500개 미만이므로
    # 좌표 쌍의 개수는 약 (2*500)^2 정도.
    COLOR_NONE = '_'
    COLOR_LINE = '#'
    COLOR_INNER = 'X'
    COLOR_OUTTER = '.'

    N = len(X)
    x_unique = sorted(set(map(float, X)))
    y_unique = sorted(set(map(float, Y)))

    # 나이퀴스트 샘플링 이론에 따라 2배의 주파수로 샘플링하여 빈 칸을 탐지
    for i in range(len(x_unique)-1):
        x_unique.append((x_unique[i]+x_unique[i+1])/2)
    x_unique.append(min(X)-1) # padding
    x_unique.append(max(X)+1) # padding
    x_unique.sort()
    for i in range(len(y_unique)-1):
        y_unique.append((y_unique[i]+y_unique[i+1])/2)
    y_unique.append(min(Y)-1) # padding
    y_unique.append(max(Y)+1) # padding
    y_unique.sort()

    # 좌표 압축을 위한 매핑 생성
    x_mapper = {x: i for i, x in enumerate(x_unique)}
    y_mapper = {y: i for i, y in enumerate(y_unique)}
    w = len(x_unique)
    h = len(y_unique)
    color_grid = [[COLOR_NONE] * w for _ in range(h)]

    # 테두리 그리기
    for i in range(N):
        dx = (X[i]-X[i-1])
        dy = (Y[i]-Y[i-1])
        if dx:
            y = y_mapper[Y[i]]
            for x in range(x_mapper[X[i-1]], x_mapper[X[i]], dx//abs(dx)):
                color_grid[y][x] = COLOR_LINE
        if dy:
            x = x_mapper[X[i]]
            for y in range(y_mapper[Y[i-1]], y_mapper[Y[i]], dy//abs(dy)):
                color_grid[y][x] = COLOR_LINE

    # 바깥쪽과 안쪽 색상을 채우기.
    def flood_fill(x: int, y: int, fill_value: str):
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < w and 0 <= ny < h and color_grid[ny][nx] == COLOR_NONE:
                color_grid[ny][nx] = fill_value
                flood_fill(nx, ny, fill_value)

    setrecursionlimit(w*h+1000)

    # 바깥쪽 영역 채우기 (=2)
    flood_fill(0, 0, COLOR_OUTTER) # padding 으로 넣은 좌표이므로 무조건 바깥에 해당.

    # 안쪽 영역 채우기 (=3)
    for x in range(w):
        for y in range(h):
            if color_grid[y][x] == COLOR_NONE:
                flood_fill(x, y, COLOR_INNER)
                break
        else:
            continue
        break

    # Bruteforcing 영역 매칭
    def is_valid(i: int, j: int) -> bool:
        "i번 좌표와 j번 좌표로 만드는 박스 영역이 적녹색으로만 채워져있는가."
        x_min = min(x_mapper[X[i]], x_mapper[X[j]])
        x_max = max(x_mapper[X[i]], x_mapper[X[j]])
        y_min = min(y_mapper[Y[i]], y_mapper[Y[j]])
        y_max = max(y_mapper[Y[i]], y_mapper[Y[j]])
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                if color_grid[y][x] == COLOR_OUTTER:
                    return False
        return True

    areas = []
    for j in range(N):
        for i in range(j):
            if is_valid(i, j):
                w = abs(X[i]-X[j])+1
                h = abs(Y[i]-Y[j])+1
                areas.append(w*h)
    return max(areas)


main()
