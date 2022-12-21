import re
from pprint import pprint
from collections import deque
import time
from contextlib import contextmanager

@contextmanager
def timing():
  start = time.time()
  yield start
  end = time.time()
  print(end - start, "seconds")

# part 1: 4951427

def solve(data):
  # data = example
  # line_of_interest = 10
  # limit = 20
  line_of_interest = 2000000
  limit = 4000000
  sensors, beacons = parse_data(data)
  covered_tiles = covered_tiles_in_line(sensors, beacons, line_of_interest)
  position = find_free_position(sensors, limit)
  # freq = position[0] * 4000000 + position[1] if position else None
  return covered_tiles, None # freq

instruction_re = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

def parse_data(data):
  sensors = set()
  beacons = set()
  for line in data.splitlines():
    mo = instruction_re.match(line)
    x, y, a, b = map(int, mo.groups())
    r = abs(x - a) + abs(y - b)
    sensors.add((x, y, r))
    beacons.add((a, b))
  return sensors, beacons

def covered_tiles_in_line(sensors, beacons, line):
  with timing():
    ranges = nonoverlapping_ranges_for_line(sensors, line)
  covered_tiles = sum(hi - lo for lo, hi in ranges)
  # subtract beacons on that line
  covered_tiles -= sum(1 for a, b in beacons if b == line)
  return covered_tiles

def nonoverlapping_ranges_for_line(sensors, line):
  ranges = []
  for x, y, r in sensors:
    dy = abs(line - y)
    dx = r - dy
    if dx < 0:
      continue
    s = x - dx, x + dx + 1
    ranges.append(s)
  return merge_list_of_ranges(ranges)

def ranges_overlap(x, y):
  xl, xh = x
  yl, yh = y
  return (xh >= yl and xl <= yh) 

def merge_pair_of_ranges(x, y):
  xl, xh = x
  yl, yh = y
  return min(xl, yl), max(xh, yh)

def merge_list_of_ranges(ranges):
  r = deque(sorted(ranges))
  m = []
  while r:
    x = r.popleft()
    if not m or not ranges_overlap(m[-1], x):
      m.append(x)
    else:
      m[-1] = merge_pair_of_ranges(m[-1], x)
  return m

def find_free_positions(sensors, limit):
  for line in range(limit):
    range = (0, limit + 1)
    ranges = nonoverlapping_ranges_for_line(sensors, line)
    for r in ranges:
      range = subtract_range(range, r)
      
      
example = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""