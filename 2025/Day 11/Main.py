from collections import defaultdict
from functools import lru_cache
from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'

graph = defaultdict(list)

for line in INPUT_FILE.read_text().strip().splitlines():
    in_name, *out_names = line.replace(': ', ' ').split()
    graph[in_name].extend(out_names)


def solve_part_one():
    S = 'you'  # source
    T = 'out'  # sink

    def count_paths(node: str) -> int:
        if node == T:
            return 1
        retval = 0
        for child in graph[node]:
            retval += count_paths(child)
        return retval

    return count_paths(S)


def solve_part_two():
    semaphore = defaultdict(bool)

    @lru_cache(maxsize=1024**3)
    def backtracking(node: str, dac: bool = False, fft: bool = False) -> int:
        if node == 'out':
            return 1 if dac and fft else 0
        retval = 0
        # 이미 진입한 사이클경로에 재진입하는걸 방지하는 장치
        sem_key = (node, dac, fft)
        if not semaphore[sem_key]:
            semaphore[sem_key] = True
            # 계속 탐색 하기
            if node == 'dac':
                dac = True
            if node == 'fft':
                fft = True
            for child in graph[node]:
                retval += backtracking(child, dac, fft)
            semaphore[sem_key] = False
        return retval

    return backtracking('svr')


print(solve_part_one())
print(solve_part_two())
