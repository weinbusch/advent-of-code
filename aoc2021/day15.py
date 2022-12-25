from heapq import heappop, heappush

example = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def replicate_graph(g, n):
    gs = [[increment_graph(g, x + y) for x in range(n)] for y in range(n)]
    return [[x for line in lines for x in line] for row in gs for lines in zip(*row)]


def increment_graph(g, d):
    return [[(x + d) % 9 or 9 for x in line] for line in g]


def solve(data):
    g = [[int(x) for x in line] for line in data.splitlines()]
    G = replicate_graph(g, 5)
    return dijkstra(g), dijkstra(G)


def dijkstra(g):
    p = dict()
    start = (0, 0)
    dest = (len(g) - 1, len(g[0]) - 1)
    distances = {start: 0}
    costs = {(x, y): c for x, line in enumerate(g) for y, c in enumerate(line)}
    queue = set(costs.keys())
    heap = [(0, start)]
    while queue:
        du, u = heappop(heap)
        if u == dest:
            break
        queue.remove(u)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            v = (u[0] + dx, u[1] + dy)
            if v in queue:
                dv = distances.get(v, None)
                d = du + costs[v]
                if dv is None or d < dv:
                    distances[v] = d
                    heappush(heap, (d, v))
                    p[v] = u
    path = make_path(p, start, dest)
    return total_cost(path, costs, start)


def make_path(p, start, dest):
    path = []
    node = dest
    while node:
        path.append(node)
        node = p.get(node)
    return path


def total_cost(path, costs, start):
    return sum(costs[p] for p in path if p != start)
