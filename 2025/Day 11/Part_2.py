from collections import defaultdict
from functools import lru_cache
from pathlib import Path

INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'

directed_graph = defaultdict(list)

for line in INPUT_FILE.read_text().strip().splitlines():
    in_name, *out_names = line.replace(': ', ' ').split()
    directed_graph[in_name].extend(out_names)


visited = defaultdict(bool)


@lru_cache(maxsize=1024**3)
def dfs(node: str, dac: bool = False, fft: bool = False) -> int:
    if node == 'out':
        return 1 if dac and fft else 0
    retval = 0
    cache_key = (node, dac, fft)
    if not visited[cache_key]:
        visited[cache_key] = True
        if node == 'dac':
            dac = True
        if node == 'fft':
            fft = True
        for child in directed_graph[node]:
            retval += dfs(child, dac, fft)
        visited[cache_key] = False
    return retval

print(dfs('svr'))
