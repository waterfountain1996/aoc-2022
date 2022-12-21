import sys
from itertools import chain, zip_longest
from typing import Any

Packet = list[Any] | int

pairs: list[tuple[Packet, Packet]] = [
    tuple(map(eval, s.strip().splitlines()))
    for s in sys.stdin.read().split("\n\n")
]


def compare(left: Packet, right: Packet, indent: int = 0) -> int:
    # print(f"{' ' * indent}- Compare {left} vs {right}")
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            # print(f"{' ' * indent}  - Left side is smaller, so inputs are in the right order")
            return 1
        elif left > right:
            # print(
            #     f"{' ' * indent}  - Right side is smaller, so inputs are not in the right order"
            # )
            return -1
        else:
            return 0
    elif isinstance(left, list) and isinstance(right, list):
        for a, b in zip_longest(left, right):
            if a is None:
                # print(
                #     f"{' ' * indent}  - Left side ran out of items,"
                #     " so inputs are in the right order"
                # )
                return 1
            elif b is None:
                # print(
                #     f"{' ' * indent}  - Right side ran out of items,"
                #     " so inputs are not in the right order"
                # )
                return -1

            result = compare(a, b, indent+2)
            if result < 0:
                return -1
            elif result > 0:
                return 1

        return 0
    else:
        if isinstance(left, int):
            # print(
            #     f"{' ' * indent}- Mixed types;"
            #     " convert left to {[left]} and retry comparison"
            # )
            return compare([left], right, indent)
        else:
            # print(
            #     f"{' ' * indent}- Mixed types; "
            #     " convert right to {[right]} and retry comparison"
            # )
            return compare(left, [right], indent)


def bubblesort(packets: list[Packet]):
    goon = True
    while goon:
        goon = False
        for i in range(len(packets) - 1):
            if compare(packets[i], packets[i + 1]) < 0:
                goon = True
                packets[i], packets[i + 1] = packets[i + 1], packets[i]


def part1():
    return sum(i for i, pair in enumerate(pairs, 1) if compare(*pair) > 0)


def part2():
    dividers = ([[2]], [[6]])
    packets = [packet for packet in chain(chain.from_iterable(pairs), dividers)]
    bubblesort(packets)
    return (packets.index(dividers[0]) + 1) * (packets.index(dividers[1]) + 1)


if __name__ == "__main__":
    print(part1())
    print(part2())
