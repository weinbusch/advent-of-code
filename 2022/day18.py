from heapq import heappush, heappop


def solve(data):
    # data = EXAMPLE
    # data = "1,1,1\n2,1,1"
    cubes = parse_data(data)
    M = adjacency(cubes)
    A = sum(len(ns) for _, ns in M)
    trapped = find_trapped_spaces(cubes)
    B = sum(len(ns - trapped) for _, ns in M)
    return A, B


def parse_data(data):
    return set(tuple(map(int, line.split(","))) for line in data.splitlines())


def all_neighbors(cube):
    x, y, z = cube
    return set(
        (x + dx, y + dy, z + dz)
        for dx, dy, dz in [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]
    )


def adjacency(cubes):
    """Neighboring spaces for each cube that are not occupied by another cube"""
    return [(cube, all_neighbors(cube) - cubes) for cube in cubes]


def search_space(cubes):
    """Search space for path finding algorithm"""
    minx = min(x for x, y, z in cubes) - 1
    maxx = max(x for x, y, z in cubes) + 1

    miny = min(y for x, y, z in cubes) - 1
    maxy = max(y for x, y, z in cubes) + 1

    minz = min(z for x, y, z in cubes) - 1
    maxz = max(z for x, y, z in cubes) + 1

    return set(
        (x, y, z)
        for x in range(minx, maxx + 1)
        for y in range(miny, maxy + 1)
        for z in range(minz, maxz + 1)
    )


def find_trapped_spaces(cubes):
    queue = search_space(cubes) - cubes
    start = min(queue)
    distances = {start: 0}
    heap = [(0, start)]
    while heap:
        du, u = heappop(heap)
        queue.discard(u)
        for v in all_neighbors(u):
            if v in queue:
                dv = du + 1
                if v not in distances or dv < distances[v]:
                    distances[v] = dv
                    heappush(heap, (dv, v))
    return queue


EXAMPLE = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
