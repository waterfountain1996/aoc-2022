import re
import sys
from copy import deepcopy


def readdata():
    rawstacks, rawsteps = map(
        lambda x: x.splitlines(False),
        sys.stdin.read().rstrip().split("\n\n")
    )
    
    indexes = [i for i, c in enumerate(rawstacks[-1]) if not c.isspace()]
    stacks = []
    for index in indexes:
        stacks.append(Stack())
        for line in rawstacks[::-1][1:]:
            if line[index].isspace():
                break

            stacks[-1].push(line[index])

    p = re.compile(r"move (\d+) from (\d+) to (\d+)")
    steps = []
    for i in rawsteps:
        m = p.match(i)
        assert m is not None
        steps.append(tuple(map(int, m.groups())))

    return stacks, steps


class Stack:
    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        return self.__items.pop(-1)

    def peek(self):
        return self.__items[-1]


stacks, steps = readdata()


def part1():
    global stacks
    localstacks = deepcopy(stacks)

    for n, fr, to in steps:
        for _ in range(n):
            localstacks[to-1].push(localstacks[fr-1].pop())

    return ''.join(s.peek() for s in localstacks)


def part2():
    global stacks
    localstacks = deepcopy(stacks)

    q = Stack()
    for n, fr, to in steps:
        for _ in range(n):
            q.push(localstacks[fr-1].pop())

        for _ in range(n):
            localstacks[to-1].push(q.pop())

    return ''.join(s.peek() for s in localstacks)


if __name__ == "__main__":
    print(part1())
    print(part2())
