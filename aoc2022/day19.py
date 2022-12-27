import re
from heapq import heappop, heappush
from dataclasses import dataclass
from collections import namedtuple
from functools import reduce


def product(iterator):
    return reduce(lambda x, y: x * y, iterator)


def solve(data):
    # data = EXAMPLE
    limit = 24
    blueprints = parse_blueprints(data)
    game_states = [
        simulate(bp, limit) for bp in blueprints.values()
    ]  # takes > 60 seconds :(
    quality_level = sum(n * s.reward for n, s in zip(blueprints.keys(), game_states))
    top_three = [
        simulate(blueprints[x], 32) for x in [1, 2, 3]
    ]  # takes ~ 150 seconds :(
    top_product = product(s.reward for s in top_three)
    return quality_level, top_product


blueprint_re = r"Blueprint (\d+):"

robot_re = r"Each ([a-z]+) robot costs ([^.]+)\."

master_re = re.compile("|".join((blueprint_re, robot_re)))

costs_re = re.compile(r"(\d+) ([a-z]+)")


Robots = namedtuple("Robots", "ore clay obsidian geode")


def parse_blueprints(s):
    blueprints = dict()
    current = None
    for mo in master_re.finditer(s):
        bp, typ, cost_string = mo.groups()
        if bp:
            current = int(bp)
            blueprints[current] = dict()
        elif current and typ:
            blueprints[current][typ] = parse_costs(cost_string)
    return {n: Robots(**d) for n, d in blueprints.items()}


def parse_costs(s):
    kwargs = dict(ore=0, clay=0, obsidian=0, geode=0)
    for mo in costs_re.finditer(s):
        amount, name = mo.groups()
        kwargs[name] = int(amount)
    return Robots(**kwargs)


ROBOTS = {
    "ore": (1, 0, 0, 0),
    "clay": (0, 1, 0, 0),
    "obsidian": (0, 0, 1, 0),
    "geode": (0, 0, 0, 1),
}


@dataclass
class GameState:
    minute: int = 0
    robots: Robots = Robots(1, 0, 0, 0)
    resources: Robots = Robots(0, 0, 0, 0)

    def tuple(self):
        return (self.minute, self.robots, self.resources)

    def copy(self):
        return GameState(*self.tuple())

    def can_build(self, costs):
        return all(x - y >= 0 for x, y in zip(self.resources, costs))

    def collect(self):
        self.resources = Robots(*(x + y for x, y in zip(self.resources, self.robots)))

    def spend(self, costs):
        self.resources = Robots(*(x - y for x, y in zip(self.resources, costs)))

    def build(self, robot):
        self.robots = Robots(*(x + y for x, y in zip(self.robots, ROBOTS[robot])))

    def advance(self):
        self.collect()
        self.minute += 1

    def advance_and_build(self, robot, costs):
        self.spend(costs)
        self.advance()
        self.build(robot)

    @property
    def reward(self):
        return self.resources.geode

    def bound(self, limit):
        return sum(
            [
                self.resources.geode,
                self.robots.geode * (limit - self.minute),
                sum(x for x in range(limit - self.minute)),
            ]
        )

    def branch(self, limit, blueprint, required_robots):
        if self.minute == limit:
            return []

        s = self.copy()
        s.advance()
        branches = [s]

        for robot, built, required, costs in zip(
            Robots._fields, self.robots, required_robots, blueprint
        ):
            if robot != "geode" and built >= required:
                continue
            if not self.can_build(costs):
                continue
            s = self.copy()
            s.advance_and_build(robot, costs)
            if robot == "geode":
                branches = [s]
                break
            branches.append(s)

        return branches


def maximum_required_robots(blueprint):
    maximum = map(max, zip(*blueprint))
    return Robots(*maximum)


def simulate(blueprint, limit):
    initial_solution = GameState()
    required_robots = maximum_required_robots(blueprint)

    def reward(solution):
        return solution.reward

    def branch(solution):
        return solution.branch(limit, blueprint, required_robots)

    def bound(solution):
        return solution.bound(limit)

    return dfs(initial_solution, reward, branch, bound)


def dfs(initial, reward, branch, bound):
    """Depth first search with pruning based on expected reward (upper bound)"""
    N, R = initial, reward(initial)
    queue = [initial]
    seen = set()
    while queue:
        n = queue.pop()
        seen.add(n.tuple())
        if reward(n) >= R:
            N, R = n, reward(n)
        for m in branch(n):
            if bound(m) < R or m.tuple() in seen:
                continue
            queue.append(m)
    return N


def branch_and_bound(initial, reward, branch, bound):
    """Basic branch and bound algorithm for finding solution N with maximum reward

    see also day 16
    and https://en.wikipedia.org/wiki/Branch_and_bound
    """
    N, R = initial, reward(initial)
    heap = [(-R, N)]
    while heap:
        _, n = heappop(heap)
        r = reward(n)
        if r >= R:
            N, R = n, r
        for m in branch(n):
            b = bound(m)
            if b >= R:
                heappush(heap, (-b, m))
    return N


EXAMPLE = """Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
"""
