from heapq import heappush, heappop


def solve(data):
    graph = [[int(n) for n in line] for line in data.splitlines()]
    return total_risk_of_shortest_path(graph), None


def total_risk_of_shortest_path(graph):
    start = (0, 0)
    dest = (len(graph) - 1, len(graph[0]) - 1)
    path = dijkstra(graph, start, dest)
    return total_risk(graph, path)


def dijkstra(graph, start, dest):
    costs = {(x, y): c for x, line in enumerate(graph) for y, c in enumerate(line)}
    pending = set(costs.keys())
    distance = {start: 0}
    p = dict()
    queue = []
    heappush(queue, (0, start))
    while queue:
        du, u = heappop(queue)
        pending.remove(u)
        if u == dest:
            break
        x, y = u
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            v = (x + dx, y + dy)
            if v in pending:
                dv = distance.get(v, None)
                c = costs[v]
                d = du + c
                if dv is None or d < dv:
                    distance[v] = d
                    p[v] = u
                    heappush(queue, (d, v))
    return make_path(p, dest)


def make_path(predecessor, dest):
    path = []
    node = dest
    while node:
        path.append(node)
        node = predecessor.get(node)
    return path


def total_risk(graph, path):
    return sum(graph[x][y] for x, y in path if (x, y) != (0, 0))


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
