import sys

rucksacks = list(map(lambda x: x.strip(), sys.stdin.readlines()))

priority = lambda c: (ord(c) - ord('a') + 1) if c.islower() else (ord(c) - ord('A') + 27)


def part1():
    return sum(
        priority(c)
        for rs in rucksacks
        for c in set(rs[:len(rs)//2]) & set(rs[len(rs)//2:])
    )


def part2():
    return sum(
        priority(c)
        for i in range(0, len(rucksacks), 3)
        for c in set(rucksacks[i]) & set(rucksacks[i+1]) & set(rucksacks[i+2])
    )


if __name__ == "__main__":
    print(part1())
    print(part2())
