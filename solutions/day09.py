import sys
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

steps = [(x[0], int(x.split()[1])) for x in sys.stdin.read().splitlines(False)]


def touches(tail: Point, head: Point) -> bool:
    return head.x in (tail.x-1, tail.x, tail.x+1) and head.y in (tail.y-1, tail.y, tail.y+1)


def move(pt: Point, direction: str, n: int) -> Point:
    if direction == "U":
        return Point(x=pt.x, y=pt.y-n)
    elif direction == "L":
        return Point(x=pt.x-n, y=pt.y)
    elif direction == "D":
        return Point(x=pt.x, y=pt.y+n)
    else:
        return Point(x=pt.x+n, y=pt.y)


def follow(tail: Point, head: Point) -> Point:
    dx = dy = 0
    if tail.x != head.x:
        dx = 1 if head.x > tail.x else -1

    if tail.y != head.y:
        dy = 1 if head.y > tail.y else -1

    return Point(x=tail.x+dx, y=tail.y+dy)


def solve(steps: list[tuple[str, int]], nknots: int) -> int:
    assert nknots > 1
    knots = [Point(x=0, y=0) for _ in range(nknots)]
    visited = {knots[-1]}
    for direction, n in steps:
        for _ in range(n):
            knots[0] = move(knots[0], direction, 1)
            for i in range(1, nknots):
                if not touches(knots[i], knots[i-1]):
                    knots[i] = follow(knots[i], knots[i-1])
                    if i == len(knots) - 1:
                        visited.add(knots[i])

    return len(visited)


def part1():
    return solve(steps, 2)


def part2():
    return solve(steps, 10)


if __name__ == "__main__":
    print(part1())
    print(part2())
