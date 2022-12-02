import sys

POINTS = {
    "win": 6,
    "draw": 3,
    "loss": 0,
    "X": 1,
    "Y": 2,
    "Z": 3,
}

BEATS = {
    "A": "Y",
    "B": "Z",
    "C": "X",
}

LOSES = {
    "A": "Z",
    "B": "X",
    "C": "Y",
}

data = sys.stdin.read()

rounds = [tuple(x.split()) for x in data.splitlines(False)]


def outcome(left, right):
    if BEATS[left] == right:
        return "win"
    elif LOSES[left] == right:
        return "loss"
    else:
        return "draw"


def choose_piece(opp, outcome):
    if outcome == "X":
        return LOSES[opp]
    elif outcome == "Y":
        diff = ord("X") - ord("A")
        return chr(ord(opp) + diff)
    else:
        return BEATS[opp]


def part1():
    return sum(POINTS[outcome(left, right)] + POINTS[right] for left, right in rounds)


def part2():
    return sum(
        POINTS[outcome(left, choose_piece(left, right))] + POINTS[choose_piece(left, right)]
        for left, right in rounds
    )


if __name__ == "__main__":
    print(part1())
    print(part2())
