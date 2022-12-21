import re
from itertools import chain, pairwise, tee
from heapq import heappop, heappush, heapify
from utils import timing, cumsum


def solve(data):
    data = example
    start = "AA"
    rates, graph = parse_data(data)
    distance_matrix = calculate_distance_matrix(graph)
    with timing("Branch and bound search"):
        p1, _ = branch_and_bound(start, distance_matrix, rates)

    with timing("With elephant"):
        p2, _ = with_elephant(start, distance_matrix, rates)

    return p1, p2


valve_re = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ((?:[A-Z]+(?:, )?)+)*"
)


def parse_data(data):
    rates = dict()
    graph = dict()
    for mo in valve_re.finditer(data):
        name, rate, ns = mo.groups()
        rates[name] = int(rate)
        graph[name] = ns.split(", ")
    return rates, graph


def timestamps_for_route(start, route, distance_matrix):
    return cumsum(
        distance_matrix[src][dest] + 1 for src, dest in pairwise(chain([start], route))
    )


def reward_for_route(start, route, timestamps, rates, limit):
    return sum((limit - t) * rates[v] for t, v in zip(timestamps, route) if t < limit)


def branch_and_bound(start, distance_matrix, rates):
    valves = set(v for v, r in rates.items() if r > 0)
    limit = 30

    def reward(route):
        timestamps = timestamps_for_route(start, route, distance_matrix)
        return reward_for_route(start, route, timestamps, rates, limit)

    def branch(route):
        visited_nodes = set(route)
        for v in valves - visited_nodes:
            yield route + [v]

    def bound(route):
        timestamps = timestamps_for_route(start, route, distance_matrix)
        r0 = reward_for_route(start, route, timestamps, rates, limit)
        t0 = max(timestamps, default=0)
        ts = range(t0 + 2, limit, 2)
        rs = sorted((r for v, r in rates.items() if v not in route), reverse=True)
        r1 = sum((limit - t) * r for t, r in zip(ts, rs) if t < limit)
        return r0 + r1

    return _branch_and_bound(reward, branch, bound)


def with_elephant(start, distance_matrix, rates):
    valves = set(v for v, r in rates.items() if r > 0)
    limit = 26

    def reward(routes):
        timestamps = [
            timestamps_for_route(start, route, distance_matrix) for route in routes
        ]
        return sum(
            reward_for_route(start, r, t, rates, limit)
            for r, t in zip(routes, timestamps)
        )

    def branch(routes):
        a, b = routes if routes else ([], [])
        visited_nodes = set(chain(*routes))
        for v in valves - visited_nodes:
            yield [a + [v], b]
            yield [a, b + [v]]

    def bound(routes):
        timestamps = [
            timestamps_for_route(start, route, distance_matrix) for route in routes
        ]
        r0 = sum(
            reward_for_route(start, r, t, rates, limit)
            for r, t in zip(routes, timestamps)
        )
        visited_nodes = set(chain(*routes))
        rs = sorted(
            (r for v, r in rates.items() if v not in visited_nodes), reverse=True
        )
        ts = list(sorted(map(lambda ts: max(ts, default=0), timestamps)))
        for r in rs:
            t = heappop(ts) + 2
            heappush(ts, t)
            if t < limit:
                r0 += (limit - t) * r
        return r0

    return _branch_and_bound(reward, branch, bound)


def _branch_and_bound(reward, branch, bound):
    N, R = [], 0
    heap = [(-R, N)]
    while heap:
        _, n = heappop(heap)
        r = reward(n)
        if r > R:
            N, R = n, r
        for m in branch(n):
            b = bound(m)
            if b >= R:
                heappush(heap, (-b, m))
    return R, N


def calculate_distance_matrix(graph):
    return {src: shortest_distances(graph, src) for src in graph}


def shortest_distances(graph, src):
    heap = [(0, src)]
    distances = {src: 0}
    queue = set(graph.keys())
    while queue:
        du, u = heappop(heap)
        queue.remove(u)
        for v in graph[u]:
            if v in queue:
                dv = distances.get(v, None)
                d = du + 1
                if dv is None or d < dv:
                    distances[v] = d
                    heappush(heap, (d, v))
    return distances


example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
