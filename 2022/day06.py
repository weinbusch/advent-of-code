def solve(data):
  # part 1
  p1 = find_position(data, 4)
  assert p1 == 1598

  # part 2
  p2 = find_position(data, 14)
  assert p2 == 2414

  return p1, p2

def find_position(data, width):
  for n in range(width, len(data)):
    if is_unique(data[n-width:n]):
      return n

def is_unique(characters):
  return len(set(characters)) == len(characters)