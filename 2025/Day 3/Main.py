import functools
import sys


@functools.cache
def solve(rating: str, amount: int = 12) -> str:
    "offset번째 인덱스 부터 amount개의 숫자를 골라 수를 형성할 때 최대 값."
    if amount == 0:
        return ''
    retval = '0'
    for i in range(len(rating)-amount+1):
        retval = max(retval, rating[i]+solve(rating[i+1:], amount-1))
    return retval


answer = 0

while (rating := sys.stdin.readline().strip()):
    answer += int(solve(rating))

print(answer)
