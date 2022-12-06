import sys

stream = sys.stdin.read().strip()


def findmarker(n):
    for i in range(0, len(stream)):
        if len(set(stream[i:i+n])) == n:
            return i + n


def part1():
    return findmarker(4)


def part2():
    return findmarker(14)


if __name__ == "__main__":
    print(part1())
    print(part2())
