from functools import lru_cache
from pathlib import Path
from sys import setrecursionlimit
from typing import List
import numpy as np


INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'

setrecursionlimit(1024**3)

raw_presents: List[List[str]] = []
raw_regions: List[str] = []


def main():
    # 상태머신으로 선물과 공간을 구분하여 입력받기
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
    # 선물부터 Numpy 행렬로 변환 (원소는 0이면 빈 칸)
    n_presents = len(raw_presents)
    present_mats: List[np.ndarray] = []
    for present_id in range(n_presents):
        raw_present = raw_presents[present_id]
        w, h = len(raw_present[0]), len(raw_present)
        present_mat = np.zeros((w, h), dtype=np.int16)
        for y in range(h):
            for x in range(w):
                if raw_present[y][x] == '#':
                    present_mat[y, x] = 1
        present_mats.append(present_mat)

    @lru_cache
    def find_variants(present_id: int) -> List[np.ndarray]:
        # 선물을 돌리고 뒤집고 한 8가지 경우의 수를 구한다.
        # 효율을 위해 중복된 데이터는 제거한 것을 반환.
        present_mat = present_mats[present_id]
        variants = [
            present_mat,
            np.rot90(present_mat),
            np.rot90(present_mat, 2),
            np.rot90(present_mat, 3),
            np.flip(present_mat, 0),
            np.flip(present_mat, 1),
            np.rot90(np.flip(present_mat, 0)),
            np.rot90(np.flip(present_mat, 0), 3)
        ]
        variants_distinct = []
        for i in range(len(variants)):
            for j in range(i):
                if np.array_equal(variants[i], variants[j]):
                    break
            else:
                variants_distinct.append(variants[i])
        return variants_distinct

    def should_fail_fast(x: int, y: int) -> bool:
        # 앞으로 채울 수 있는 남은 공간에 비해 선물의 부피가 크면 실패
        # -> 이를 선형 시간복잡도로 탐지.
        required_area = 0
        for present_id in range(n_presents):
            present_area = present_counts[present_id] * present_mats[present_id].sum()
            required_area += present_area
        left_area = np.count_nonzero(region_mat[y:, :] == 0)
        left_area -= np.count_nonzero(region_mat[y, :x] == 0)
        return required_area > left_area

    def can_all_fit(x: int = 0, y: int = 0) -> bool:
        if x >= region_width:
            return can_all_fit(0, y+1)
        if y >= region_height:
            return False

        # 지수 시간복잡도 계산을 수행하기 전에, 선형 시간에 Pruning을 시도.
        if should_fail_fast(x, y):
            return False

        if sum(present_counts) == 0:
            return True

        for present_id in range(n_presents):
            if present_counts[present_id] == 0:
                continue
            # find_variants()를 통해 선물을 이리저리 뒤집고 돌려본 것들을 쉽게 가져온다.
            for present_mat in find_variants(present_id):
                # 이 선물을 삽입해도 되는지 검사
                present_height, present_width = present_mat.shape
                if x + present_width > region_width:
                    continue
                if y + present_height > region_height:
                    continue
                region_mat[y:y+present_height, x:x+present_width] += present_mat
                # 겹치는 선물이 있다면 값이 1을 초과할 테니, 이를 검사한 후 넘어간다.
                if region_mat[y:y+present_height, x:x+present_width].max() <= 1:
                    present_counts[present_id] -= 1
                    if can_all_fit(x, y):
                        return True
                    present_counts[present_id] += 1
                region_mat[y:y+present_height, x:x+present_width] -= present_mat

        return can_all_fit(x+1, y)

    # Non-local 변수 스코핑을 위한 더미용 선언부.
    region_width = 1
    region_height = 1
    region_mat = np.zeros((region_height, region_width), dtype=np.int16)
    present_counts = [0] * len(present_mats)

    answer = 0
    # 각 공간별로 그때 그때 답을 구한다.
    for region_id in range(len(raw_regions)):
        print(f'Checking region {region_id + 1}/{len(raw_regions)} {answer=}')
        # 공간도 Numpy 영행렬 형태로 구성해두고, 그 안에 선물 행렬을 더해가며(채워가며)
        # 문제의 조건에 위배되는지 검사(겹치는지, 전부 채울 수 있는지 등 검사)
        raw_size, raw_present_counts = raw_regions[region_id].split(': ')
        region_width, region_height = map(int, raw_size.split('x'))
        region_mat = np.zeros((region_height, region_width), dtype=np.int16)
        present_counts = list(map(int, raw_present_counts.split()))
        if can_all_fit():
            answer += 1
    return answer


def solve_part_two():
    pass


main()
