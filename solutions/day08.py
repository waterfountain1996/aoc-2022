import sys

grid = [x.strip() for x in sys.stdin]


on_edge = lambda x, grid: x == 0 or x == len(grid) - 1


def get_directions(x: int, y: int, grid: list[str]) -> list[str]:
    return [
        ''.join(map(lambda row: row[x], reversed(grid[:y]))),      # up
        ''.join(reversed(grid[y][:x])),                            # left
        ''.join(map(lambda row: row[x], grid[y+1:])),              # down
        ''.join(grid[y][x+1:]),                                    # right
    ]


def is_visible(tree: tuple[int, int], grid: list[str]) -> bool:
    x, y = tree
    if on_edge(x, grid) or on_edge(y, grid):
        return True

    height = grid[y][x]
    return any(all(h < height for h in d) for d in get_directions(x, y, grid))


def get_scenic_score(tree: tuple[int, int], grid: list[str]) -> int:
    x, y = tree
    height = grid[y][x]
    score = 1
    blocked = False
    for d in get_directions(x, y, grid):
        for i, h in enumerate(d, 1):
            if h >= height:
                score *= i
                blocked = True
                break
        else:
            if not blocked:
                score *= len(d)

        blocked = False

    return score


def part1():
    return sum(
        is_visible((x, y), grid)
        for y, row in enumerate(grid)
        for x in range(len(row))
    )


def part2():
    return max(
        get_scenic_score((x, y), grid)
        for y, row in enumerate(grid)
        for x in range(len(row))
    )


if __name__ == "__main__":
    print(part1())
    print(part2())
