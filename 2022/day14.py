import re
import time
from contextlib import contextmanager

@contextmanager
def timing():
  start = time.time()
  yield start
  end = time.time()
  print(end - start, "seconds")

def solve(data):
  # data = example
  stone = parse_data(data)
  bottom = max(y for x, y in stone)
  with timing():
    s1 = simulate(stone, bottom)
  with timing():
    s2 = simulate(stone, bottom + 2, bottomless_pit=False)
  return len(s1), len(s2)
  
def simulate(stone, bottom, bottomless_pit=True):
  sand = set()
  x, y = source = 500, 0
  iterations = 0
  while True:
    iterations += 1
    if y >= bottom:
      break
    try:
      x, y = next(
        p for dx in [0, -1, 1] 
        if 
        (p := (x + dx, y + 1)) not in stone
        and p not in sand
        and (bottomless_pit or p[1] < bottom)
      )
    except StopIteration:
      sand.add((x, y))
      if (x, y) == source:
        break
      x, y = source
  print(f"{iterations} iterations")
  return sand

def draw(stone, sand, bottom):
  left = min(x for x, y in stone | sand)
  right = max(x for x, y in stone | sand)
  return "\n".join(
    "".join(
      "#" if (x, y) in stone else "o" if (x, y) in sand else "."
      for x in range(left, right+1)
    ) for y in range(0, bottom+1)
  )

line_re = re.compile("(\d+),(\d+)")

def parse_data(data):
  with timing():
    stone = set()
    for line in data.splitlines():
      stone |= stone_from_line(line)
    return stone

def stone_from_line(line):
  coords = parse_coordinates(line)
  stone = set()
  for (x0, y0), (x1, y1) in zip(coords, coords[1:]):
    x0, x1 = (x0, x1) if x0 < x1 else (x1, x0)
    y0, y1 = (y0, y1) if y0 < y1 else (y1, y0)    
    if x0 == x1:
      stone |= {(x0, y) for y in range(y0, y1+1)}
    elif y0 == y1:
      stone |= {(x, y0) for x in range(x0, x1+1)}
  return stone

def parse_coordinates(line):
  coords = []
  for mo in line_re.finditer(line):
    x, y = mo.groups()
    coords.append((int(x), int(y)))
  return coords

example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""