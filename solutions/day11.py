import re
import sys
from copy import deepcopy
from functools import reduce
from typing import Callable, Optional


def gcd(a: int, b: int) -> int:
    if b == 0:
        return a

    return gcd(b, a % b)


def lcm(a: int, b: int):
    return (a * b) // gcd(a, b)


class Monkey:
    _RE_STARTING_ITEMS = re.compile(r"\s*Starting items: \d+(?:,\ \d+)*", re.MULTILINE)
    _RE_OPERATION = re.compile(r"new = (.*)", re.MULTILINE)
    _RE_TEST = re.compile(r"divisible by (\d+)", re.MULTILINE)
    _RE_TEST_CONDITION = re.compile(r"If (\w+): throw to monkey (\d)", re.MULTILINE)

    _holding: int
    _test_result: bool

    def __init__(
        self,
        items: list[int],
        operation: Callable[[int], int],
        test: int,
        throw_to: tuple[int, int],
    ):
        self._items = items
        self._operation = operation
        self._test = test
        self._throw_to = throw_to
        self._inspected = 0

    @property
    def inspected(self) -> int:
        return self._inspected

    @property
    def throwing_to(self) -> int:
        return self._throw_to[self._test_result]

    @property
    def has_items(self) -> bool:
        return bool(self._items)

    def inspect(self, n: Optional[int] = None):
        self._inspected += 1
        if n is None:
            self._holding = self._operation(self._items.pop(0)) // 3
        else:
            self._holding = self._operation(self._items.pop(0)) % n

        self._test_result = self._holding % self._test == 0

    def catch(self, item: int):
        self._items.append(item)

    def throw(self) -> int:
        return self._holding

    @classmethod
    def from_note(cls, note: str) -> "Monkey":
        m = cls._RE_STARTING_ITEMS.search(note)
        assert m is not None
        items = list(map(int, note[m.start():m.end()].split(": ")[1].split(", ")))

        m = cls._RE_OPERATION.search(note)
        assert m is not None
        operation = eval(f"lambda old: {m.groups()[0]}")

        m = cls._RE_TEST.search(note)
        assert m is not None
        test = int(m.groups()[0])

        m = cls._RE_TEST_CONDITION.findall(note)
        assert m is not None
        throw_to = (int(m[1][1]), int(m[0][1]))

        return cls(
            items=items,
            operation=operation,
            test=test,
            throw_to=throw_to,
        )


monkeys = [Monkey.from_note(note) for note in sys.stdin.read().split("\n\n")]


def get_monkey_business(monkeys: list[Monkey]) -> int:
    x = sorted(monkeys, key=lambda m: m.inspected, reverse=True)
    return x[0].inspected * x[1].inspected


def stuff_slinging_simian_shenanigans(
    monkeys: list[Monkey], nrounds: int, relief: bool = True
) -> int:
    if relief:
        n = None
    else:
        n = reduce(lcm, map(lambda m: m._test, monkeys))

    for _ in range(nrounds):
        for monkey in monkeys:
            while monkey.has_items:
                monkey.inspect(n)
                monkeys[monkey.throwing_to].catch(monkey.throw())

    return get_monkey_business(monkeys)


def part1():
    return stuff_slinging_simian_shenanigans(deepcopy(monkeys), 20, True)


def part2():
    return stuff_slinging_simian_shenanigans(deepcopy(monkeys), 10000, False)


if __name__ == "__main__":
    print(part1())
    print(part2())
