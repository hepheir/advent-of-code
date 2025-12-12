from collections import defaultdict
from pathlib import Path


INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'example.in'
INPUT_FILE = Path(__file__).parent.resolve() / 'data' / 'puzzle.in'

graph = defaultdict(list)

for line in INPUT_FILE.read_text().strip().splitlines():
    in_name, *out_names = line.replace(': ', ' ').split()
    graph[in_name].extend(out_names)


S = 'you' # source
T = 'out' # sink


def count_paths(node: str) -> int:
    if node == T:
        return 1
    retval = 0
    for child in graph[node]:
        retval += count_paths(child)
    return retval

print(count_paths(S))
