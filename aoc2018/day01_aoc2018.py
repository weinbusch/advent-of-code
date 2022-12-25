from itertools import cycle


def solve(data):
    instructions = [int(d) for d in data.splitlines()]
    p1 = sum(instructions)

    frequencies = set()
    f = 0

    for df in cycle(instructions):
        f = f + df
        if f in frequencies:
            break
        frequencies.add(f)

    p2 = f

    return p1, p2
