import sys
from copy import deepcopy
from itertools import chain, repeat, takewhile
from typing import Iterator

SAND_ORIGIN = (499, 0)

Point = tuple[int, int]
Path = list[Point]


paths: list[Path] = [
    [tuple(map(lambda i: i, map(int, x.split(",")))) for x in s.strip().split(" -> ")]
    for s in sys.stdin
]

xmax = max(p[0] for path in paths for p in path)
ymax = max(p[1] for path in paths for p in path)
xmin = min(p[0] for path in paths for p in path)
ymin = min(p[1] for path in paths for p in path)


def connect(p1: Point, p2: Point) -> Iterator[Point]:
    (x1, y1), (x2, y2) = p1, p2
    if y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            yield x, y1
    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            yield x1, y


grid = [list('.' * xmax) for _ in range(ymax)]
rocks = chain.from_iterable(
    connect(p, path[i+1])
    for path in paths
    for i, p in enumerate(path[:-1])
)
for x, y in rocks:
    grid[y-1][x-1] = "#"


def drop_sand(grid: list[list[str]]):
    sx, sy = SAND_ORIGIN
    while sy < ymax - 1:
        if grid[sy + 1][sx] != ".":
            if sx - 1 <= xmin or sx + 1 >= xmax:
                return True

            if grid[sy + 1][sx - 1] != ".":
                if grid[sy + 1][sx + 1] != ".":
                    grid[sy][sx] = "o"
                    return False
                else:
                    sx += 1
            else:
                sx -= 1

        sy += 1

    return True


def part1():
    g = deepcopy(grid)
    return sum(takewhile(lambda _: not drop_sand(g), repeat(1)))


def fill(grid: list[list[str]]):
    nth = lambda i: 1 + (i - 1) * 2

    total = 1
    for y in range(1, len(grid)):
        n = nth(y)
        pos = SAND_ORIGIN[0] - n // 2
        current_row = grid[y - 1]
        low, high = max(pos, 0), min(pos + n, len(current_row))

        rocks = nth(y + 1)
        for x, c in enumerate(current_row[low:high], low):
            if c != ".":
                rocks -= 1
                if x - 1 >= low and x + 1 < high:
                    if current_row[x - 1] == "#" and current_row[x + 1] == "#":
                        grid[y][x] = "#"
            else:
                current_row[x] = "o"

        total += rocks

    return total


def part2():
    g = deepcopy(grid)
    g.append(list("." * xmax))
    g.append(list("#" * xmax))
    return fill(g)


if __name__ == "__main__":
    print(part1())
    print(part2())
