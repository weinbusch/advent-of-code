from heapq import heappop, heappush

example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

def elevation(char):
  if char == "S":
    return elevation("a")
  if char == "E":
    return elevation("z")
  return ord(char) - ord("a")

def solve(data):
  # data = example
  elevation_map = {(x, y): elevation(c) for x, line in enumerate(data.splitlines()) for y, c in enumerate(line)}
  poi = {c: (x, y) for x, line in enumerate(data.splitlines()) for y, c in enumerate(line) if c in "SE"}
  start = poi["S"]
  dest = poi["E"]

  distance = dijkstra(elevation_map, start, dest)

  starting_points = [k for k, v in elevation_map.items() if v == elevation("a")]
  distances = filter(None, (dijkstra(elevation_map, s, dest) for s in starting_points))

  return distance, min(distances)

def dijkstra(e, start, dest):
  p = dict()
  cost = 1
  distances = {start: 0}
  queue = set(e.keys())
  heap = [(0, start)]
  while queue:
    try:
      du, u = heappop(heap)
    except IndexError:
      # no path can be found
      return None
    if u == dest:
      break
    queue.remove(u)
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      v = (u[0] + dx, u[1] + dy)
      if v in queue and e[v] - e[u] < 2:
        dv = distances.get(v, None)
        d = du + cost
        if dv is None or d < dv:
          distances[v] = d
          heappush(heap, (d, v))
          p[v] = u
  return distances[dest]
