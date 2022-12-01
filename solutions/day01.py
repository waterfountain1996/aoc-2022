import sys

data = sys.stdin.read()

calories = sorted([sum(map(int, x.splitlines(False))) for x in data.split("\n\n")], reverse=True)


def part1():
    return calories[0]


def part2():
    return sum(calories[:3])


if __name__ == "__main__":
    print(part1())
    print(part2())
