import re
from itertools import combinations, permutations, chain
from collections import namedtuple
from heapq import heappop, heappush
from utils import timing

def solve(data):
  # data = example
  start = "AA"
  distance_matrix, rates = parse_data(data)
  print(f"Searching {len(rates)} valves")
  if len(rates) < 11:
    with timing("Brute force"):
      bf = brute_force(start, distance_matrix, rates)
      print(bf)
  with timing("Branch and bound search"):
    p1 = single_agent(start, distance_matrix, rates)
  with timing("Branch and bound search for two agents"):
    p2 = double_agent(start, distance_matrix, rates)
  
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
  rates = {v: r for v, r in rates.items() if r > 0}
  distance_matrix = calculate_distance_matrix(graph)
  return distance_matrix, rates

def brute_force(start, distance_matrix, rates):
  limit = 30
  valves = rates.keys()
  def pressure_released(route):
    ts = (1 + distance_matrix[src][dest] for src, dest in zip(chain([start], route), route))
    rs = (rates[v] for v in route)
    t = 0
    p = 0
    for r, dt in zip(rs, ts):
      t += dt
      if not t < limit:
        break
      p += r * (limit - t)
    return p
  p_max = 0
  optimal = None
  for route in permutations(valves):
    p = pressure_released(route)
    if p > p_max:
      p_max = p
      optimal = route
  return p_max, optimal

def partitions(s):
  """Return all possible ways of splitting s in half"""
  r = len(s) // 2
  ps = set()
  for c in combinations(s, r):
    a = frozenset(c)
    b = s - a
    ps.add(frozenset((a, b)))
  return ps
    
def double_agent(start, distance_matrix, rates):
  limit = 26
  valves = frozenset(rates.keys())
  return max(
    sum(
      single_agent(start, distance_matrix, rs, limit)
      for rs in ({v: r for v, r in rates.items() if v in p} for p in ps)
    )
    for ps in partitions(valves)
  )
  
def single_agent(start, distance_matrix, rates, limit=30):
  sorted_rates = sorted(((r, v) for v, r in rates.items()), reverse=True)
  valves = frozenset(v for v, r in rates.items() if r > 0)
  
  Solution = namedtuple("Solution", "total_pressure_released current_valve current_time remaining_valves path")
  
  initial = Solution(
    total_pressure_released=0, 
    current_valve=start, 
    current_time=0, 
    remaining_valves=valves, 
    # path is only included for debugging purposes, 
    # it is not needed for the algorithm to work
    path=[],
  )
  
  def reward(solution):
    return solution.total_pressure_released

  def branch(solution):
    for v in solution.remaining_valves:
      dt = 1 + distance_matrix[solution.current_valve][v]
      t = solution.current_time + dt
      if t < limit:
        dp = rates[v] * (limit - t)
        p = solution.total_pressure_released + dp
        vs = frozenset(x for x in solution.remaining_valves if x != v)
        h = solution.path.copy()
        h.append(v)
        yield Solution(
          total_pressure_released=p, 
          current_valve=v, 
          current_time=t, 
          remaining_valves=vs, 
          path=h,
        )
        
  def bound(solution):
    rs = (r for r, v in sorted_rates if v in solution.remaining_valves)
    t0 = solution.current_time + 2
    ts = range(t0, limit, 2)
    p = sum(r * (limit - t) for r, t in zip(rs, ts))
    return solution.total_pressure_released + p

  solution = branch_and_bound(initial, reward, branch, bound)
  return solution.total_pressure_released

def branch_and_bound(initial, reward, branch, bound):
  N, R = initial, reward(initial)
  heap = [(-R, N)]
  while heap:
    _, n = heappop(heap)
    r = reward(n)
    if r > R:
      N, R = n, r
    for m in branch(n):
      b = bound(m) 
      if b > R:
        heappush(heap, (-b, m))
  return N

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