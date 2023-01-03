from collections import deque, Counter


def solve(data):
    # data = example2
    elves = parse_data(data)
    t1, p1 = play_game(elves, limit=10)
    t2, _ = play_game(elves)
    return (t1, empty_tiles(p1)), t2


def draw(elves):
    x0 = min(x for x, _ in elves)
    x1 = max(x for x, _ in elves)
    y0 = min(y for _, y in elves)
    y1 = max(y for _, y in elves)
    return "\n".join(
        "".join("#" if (x, y) in elves else "." for x in range(x0, x1 + 1))
        for y in range(y0, y1 + 1)
    )


def empty_tiles(elves):
    x0 = min(x for x, _ in elves)
    x1 = max(x for x, _ in elves)
    y0 = min(y for _, y in elves)
    y1 = max(y for _, y in elves)
    total = (x1 - x0 + 1) * (y1 - y0 + 1)
    return total - len(elves)


def play_game(elves, limit=None):
    directions = DIRECTIONS.copy()
    turn = 0
    while True:
        turn += 1
        new_elves = play_round(elves, directions)
        if new_elves is None:
            break
        elves = new_elves
        if limit is not None and turn == limit:
            break
    return turn, elves


def play_round(elves, directions):
    proposals = [(elf, propose(elf, elves, directions)) for elf in elves]
    if all(q is None for _, q in proposals):
        return None
    counter = Counter(p for _, p in proposals)
    new_elves = {p if q is None or counter[q] > 1 else q for p, q in proposals}
    directions.rotate(-1)
    return new_elves


def parse_data(data):
    elves = {
        (x, y)
        for y, line in enumerate(data.splitlines())
        for x, c in enumerate(line)
        if c == "#"
    }
    return elves


DIRECTIONS = deque(
    [
        lambda x, y: ({(x + dx, y - 1) for dx in [-1, 0, 1]}, (x, y - 1)),  # north
        lambda x, y: ({(x + dx, y + 1) for dx in [-1, 0, 1]}, (x, y + 1)),  # south
        lambda x, y: ({(x - 1, y + dy) for dy in [-1, 0, 1]}, (x - 1, y)),  # west
        lambda x, y: ({(x + 1, y + dy) for dy in [-1, 0, 1]}, (x + 1, y)),  # east
    ]
)


def propose(elf, elves, directions):
    x, y = elf
    neighbors = {
        (x + dx, y + dy)
        for dy in [-1, 0, 1]
        for dx in [-1, 0, 1]
        if not (dx == 0 and dy == 0)
    }
    if neighbors.isdisjoint(elves):
        return None
    for f in directions:
        positions, proposal = f(x, y)
        if positions.isdisjoint(elves):
            return proposal


example2 = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""

example1 = """.....
..##.
..#..
.....
..##.
.....
"""
