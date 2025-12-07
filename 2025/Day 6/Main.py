from functools import reduce
from operator import add, mul
from typing import List
import sys


OPERATOR_FN = {
    '+': add,
    '*': mul,
}

args_2d = sys.stdin.readlines()

H = len(args_2d)
W = max(len(row.rstrip('\n')) for row in args_2d)

# (아마도) 에디터 자동 포멧으로 사라진 공백 칸 수 맞춰주기.
args_2d = [row.rstrip('\n').ljust(W) for row in args_2d]


def solve_part_one() -> int:
    # 공백 기준으로 나누기.
    operands_2d = [[*map(int, row.split())] for row in args_2d[:-1]]
    operators_raw = args_2d[-1].split()
    column_count = len(args_2d[0].split())
    grand_sum = 0
    for col_num in range(column_count):
        operands = [operands_2d[y][col_num] for y in range(H-1)]
        grand_sum += reduce(OPERATOR_FN[operators_raw[col_num]], operands)
    return grand_sum


def solve_part_two() -> int:
    # 계산 블록들의 경계선들을 구한다.
    vbars = []  # Vertical bars
    vbars.append(-1)  # padding
    for x in range(W):
        if all(args_2d[y][x] == ' ' for y in range(H)):
            vbars.append(x)
    vbars.append(W)  # padding

    # 경계선대로 숫자들이 있는 공간의 바운딩박스를 구해서 파싱해오자.
    grand_sum = 0
    for i in range(len(vbars)-1):
        x_min = vbars[i]+1
        x_max = vbars[i+1]-1
        operator_fn = OPERATOR_FN[args_2d[-1][x_min]]
        operands = parse_operands_vertical(x_min, 0, x_max, H-2)
        grand_sum += reduce(operator_fn, operands)
    return grand_sum


def parse_operands_vertical(x_min: int, y_min: int, x_max: int, y_max: int) -> List[int]:
    operands = [0] * (x_max-x_min+1)
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            if args_2d[y][x] != ' ':
                operands[x-x_min] *= 10
                operands[x-x_min] += int(args_2d[y][x])
    return operands


print(solve_part_one())
print(solve_part_two())
