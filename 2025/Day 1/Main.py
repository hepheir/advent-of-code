import sys


answer = 0
arrow = 50

while (line := sys.stdin.readline().strip()):
    direction = line[0]
    clicks = int(line[1:])
    if direction == 'L':
        step = -1
    else:
        step = +1
    for _ in range(clicks):
        arrow += step
        arrow %= 100
        if arrow == 0:
            answer += 1

print(answer)