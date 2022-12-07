import sys

DISK_SPACE = 70000000
UNUSED_SPACE = 30000000
THRESHOLD = 100000


class TreeBuilder:
    def __init__(self, terminal: list[str]):
        self._terminal = terminal
        self._ptr = 0
        self._root = {}

        self._curr = None
        self._prev = None

    def build(self):
        while self._ptr < len(self._terminal):
            line = self._terminal[self._ptr]
            self._ptr += 1

            assert line.startswith("$")
            cmd, *args = line.split()[1:]
            if cmd == "cd":
                self.cd(args[0])
            elif cmd == "ls":
                self.ls()
            else:
                assert False, "unexpected cmd"

        return self._root

    def cd(self, arg: str):
        if arg == "/":
            self._curr = self._root
        elif arg == "..":
            assert self._prev is not None
            self._curr = self._prev
            if ".." in self._prev:
                self._prev = self._prev[".."]
            else:
                self._prev = self._root
        else:
            assert self._curr is not None
            self._prev = self._curr
            self._curr = self._curr[arg]

    def ls(self):
        try:
            while not (line := self._terminal[self._ptr]).startswith("$"):
                size, name = line.split()
                assert self._curr is not None
                if size == "dir":
                    self._curr[name] = {"..": self._curr}
                else:
                    self._curr[name] = int(size)

                self._ptr += 1
        except IndexError:
            pass


builder = TreeBuilder([x.rstrip() for x in sys.stdin])
root = builder.build()


def solve():
    underthreshold = 0
    diff = 0
    validsizes = []

    def walk(d) -> int:
        nonlocal underthreshold, diff, validsizes
        total = 0
        for name, entry in d.items():
            if name == "..":
                continue

            if isinstance(entry, int):
                total += entry
            else:
                size = walk(entry)
                if size <= THRESHOLD:
                    underthreshold += size

                total += size

        if total + diff >= UNUSED_SPACE:
            validsizes.append(total)

        return total

    diff = DISK_SPACE - walk(root)
    underthreshold = 0
    walk(root)
    return underthreshold, min(validsizes)


part1, part2 = solve()


if __name__ == "__main__":
    print(part1)
    print(part2)
