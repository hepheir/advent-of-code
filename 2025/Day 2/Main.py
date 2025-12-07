
def main():
    # 탐색 범위가 1,780,119 개 숫자밖에 안된다.
    answer = 0
    for raw_range in input().strip().split(','):
        start, end = map(int, raw_range.split('-'))
        for number in range(start, end+1):
            # if is_repeated_twice(number): # <- Part One
            if is_repeated(number):  # <- Part Two
                answer += number
    print(answer)


def is_repeated_twice(x: int) -> bool:
    raw_number = str(x)
    length = len(raw_number)
    if length % 2 == 1:
        return False
    return raw_number[:length//2] == raw_number[length//2:]


def is_repeated(x: int) -> bool:
    # O(log x log x)
    number_string = str(x)
    number_length = len(number_string) # O(log x)

    def is_repeated_util(chunk_size: int) -> bool:
        """chunk_size 길이의 패턴이 반복되는 숫자인지 검사.

        O(number_length)
        """
        if number_length % chunk_size != 0:
            return False
        for offset in range(chunk_size, number_length, chunk_size):
            for i in range(chunk_size):
                if number_string[i] != number_string[offset+i]:
                    return False
        return True


    for chunk_size in range(1, number_length//2+1):
        if is_repeated_util(chunk_size):
            return True

    return False



if __name__ == '__main__':
    main()
