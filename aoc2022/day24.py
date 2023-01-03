import math
from functools import cache
from heapq import heappop, heappush


def solve(data):
    # data = example
    neighbors, start, dest = parse_data(data)
    duration = []
    t = 0
    for s, d in [(start, dest), (dest, start), (start, dest)]:
        t = shortest_path(neighbors, s, d, t)
        duration.append(t)
    return duration[0], duration[-1]


def parse_data(data):
    data = data.strip()
    lines = data.splitlines()
    open_tiles = set(
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c != "#"
    )
    blizzards = [
        ((x, y), c)
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
        if c in "<>v^"
    ]
    height, width = len(lines), len(lines[0])
    start = (lines[0].index("."), 0)
    dest = (lines[-1].index("."), height - 1)

    @cache
    def open_space(t):
        occupied = set()
        for pos, c in blizzards:
            x, y = pos
            if c == ">":
                x = wrap(x + t, 1, width - 2)
            elif c == "<":
                x = wrap(x - t, 1, width - 2)
            elif c == "v":
                y = wrap(y + t, 1, height - 2)
            elif c == "^":
                y = wrap(y - t, 1, height - 2)
            occupied.add((x, y))
        return open_tiles - occupied

    def neighbors(pos, t):
        x, y = pos
        return {
            (x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        } & open_space(t)

    return neighbors, start, dest


def wrap(x, x0, k):
    return x0 + ((x - x0) % k)


def manhattan(p, q):
    x, y = p
    a, b = q
    return abs(x - a) + abs(y - b)


def shortest_path(neighbors, start, dest, t):
    def h(pos):
        return manhattan(pos, dest)

    heap = list()
    heappush(heap, (h(start), (start, t)))
    seen = set()
    while True:
        _, (u, du) = heappop(heap)
        if u == dest:
            return du
        t = du + 1
        for v in neighbors(u, t):
            if (v, t) not in seen:
                heappush(heap, (t + h(v), (v, t)))
                seen.add((v, t))


example = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
