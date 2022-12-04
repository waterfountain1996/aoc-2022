import sys


def readpairs():
    def torange(x):
        left, right = x.split("-")
        return set(range(int(left), int(right)+1))

    return [tuple(map(torange, x.strip().split(","))) for x in sys.stdin]


pairs = readpairs()


def part1():
    return sum(left.issubset(right) or left.issuperset(right) for left, right in pairs)    


def part2():
    return sum(bool(left & right) for left, right in pairs)    


if __name__ == "__main__":
    print(part1())
    print(part2())
