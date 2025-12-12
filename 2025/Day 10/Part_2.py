from pathlib import Path
from typing import *
from z3 import *


EXAMPLE_INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
PUZZLE_INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'

INPUT_FILE = PUZZLE_INPUT_FILE


def parse_as_list(raw: str) -> List[int]:
    return list(map(int, raw[1:-1].split(',')))


def convert_indicies_to_flag(indicies: List[int], length: int) -> List[int]:
    retval = [0] * length
    for index in indicies:
        retval[index] = 1
    return retval


def main():
    grand_sum = 0
    for line in INPUT_FILE.read_text().splitlines():
        tokens = line.split()
        joltage = parse_as_list(tokens[-1])
        buttons = [parse_as_list(raw_button) for raw_button in tokens[1:-1]]
        grand_sum += solve(buttons, joltage)
    print(grand_sum)


def solve(buttons: List[List[int]], joltage: List[int]) -> int:
    n_buttons = len(buttons)

    # z3 solver 동작 흐름 (100% 이해하지는 못함)
    # 1. 변수를 선언해준다.
    # 2. 몇 가지 Boolean expression 을 solver에 add() 해준다.
    # 3. solver가 추가된 조건들을 모두 만족하는 변수들을 구해준다.
    solver = Solver()

    # z3 solver에서 사용할 변수 선언 : 각 버튼이 눌린 횟수.
    button_weights = [Int(f'w{i}') for i in range(n_buttons)]

    # 모든 버튼은 0번 이상 눌려야 한다는 조건 제시.
    for w in button_weights:
        solver.add(w >= 0)

    # 만들어진 joltage 의 각 숫자를 구하기 위한 수식
    joltage_expr = [[] for _ in range(len(joltage))]
    for i in range(n_buttons):
        for index in buttons[i]:
            joltage_expr[index].append(button_weights[i])

    for index in range(len(joltage)):
        solver.add(Sum(joltage_expr[index]) == joltage[index])

    # z3 모델이 위 조건을 만족하는 해가 존재하는지 탐색함.
    solver.check()
    model = solver.model()

    # 구해진 각 변수들의 값(버튼을 누른 횟수)을 합산.
    answer = sum(model[w].as_long() for w in button_weights)
    return answer


main()
