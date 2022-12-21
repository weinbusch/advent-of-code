DIRECTIONS = {
  "R": (1, 0),
  "L": (-1, 0),
  "D": (0, -1),
  "U": (0, 1),
}

example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

larger_example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

def solve(data):
  # data = larger_example
  instructions = [(line[0], int(line[2:])) for line in data.splitlines()]
  head = (0, 0)
  tail = (0, 0)
  path = set()

  for direction, distance in instructions:
    for _ in range(distance):
      head = move_head(head, direction)
      tail = move_tail(head, tail)
      path.add(tail)

  snake_length = 10
  snake = [(0, 0) for _ in range(snake_length)]
  snake_path = set()

  for direction, distance in instructions:
    for _ in range(distance):
      snake[0] = move_head(snake[0], direction)
      for i in range(1, len(snake)):
        snake[i] = move_tail(snake[i-1], snake[i])
      snake_path.add(snake[-1])
  
  return len(path), len(snake_path)

def move_head(head, direction):
  hx, hy = head
  dx, dy = DIRECTIONS[direction]
  hx += dx
  hy += dy
  return (hx, hy)

def move_tail(head, tail):
  hx, hy = head
  tx, ty = tail
  if abs(hy - ty) > 1 and abs(hx - tx) > 1:
    ty += (hy - ty) // abs(hy - ty)
    tx += (hx - tx) // abs(hx - tx)
  elif abs(hy - ty) > 1:
    ty += (hy - ty) // abs(hy - ty)
    tx = hx
  elif abs(hx - tx) > 1:
    tx += (hx - tx) // abs(hx - tx)
    ty = hy
  return (tx, ty)
