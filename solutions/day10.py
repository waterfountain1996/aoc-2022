import sys
from itertools import accumulate

cycles = [1] + [
    x for xs in [
        (0,) if x.startswith("noop") else (0, int(x.strip().split()[1]))
        for x in sys.stdin
    ] for x in xs
]


def part1():
    return sum(
        cycle * reg
        for cycle, reg in enumerate(accumulate(cycles), 1)
        if cycle in range(20, 221, 40)
    )


def part2():
    rows = [list(" " * 40) for _ in range(6)]
    for cycle, reg in enumerate(accumulate(cycles)):
        row, col = divmod(cycle, 40)
        if col in (reg - 1, reg, reg  + 1):
            rows[row][col] = "#"

    return "\n".join("".join(row) for row in rows)


if __name__ == "__main__":
    print(part1())
    print(part2())
