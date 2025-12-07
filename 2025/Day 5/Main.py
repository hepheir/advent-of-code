import sys


ing_id_ranges = []
ing_id_list = []

while (line := sys.stdin.readline().strip()):
    s, e = map(int, line.split('-'))
    ing_id_ranges.append((s, e))

while (line := sys.stdin.readline().strip()):
    ing_id_list.append(int(line))

ing_id_ranges.sort()
ing_id_list.sort()


def solve_part_one() -> int:
    fresh_count = 0
    for x in ing_id_list:
        for s, e in ing_id_ranges:
            if s <= x <= e:
                fresh_count += 1
                break
    return fresh_count


def solve_part_two() -> int:
    fresh_count = 0
    fresh_end = -1
    for s, e in ing_id_ranges:
        if fresh_end < s:
            fresh_count += e-s+1
            fresh_end = e
        elif fresh_end < e:
            fresh_count += e-fresh_end
            fresh_end = e
    return fresh_count


# print(solve_part_one())
print(solve_part_two())
