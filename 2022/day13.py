import re
from itertools import chain
from functools import cmp_to_key

def solve(data):
  # data = example
  pairs = [tuple(p.splitlines()) for p in data.split("\n\n")]
  comparisons = [compare_pair(*pair) for pair in pairs]
  ordered_pairs = [i for i, c in enumerate(comparisons, 1) if c < 0]
  packets = [packet for pair in pairs for packet in pair] + ["[[2]]", "[[6]]"]
  ordered_packets = sorted(packets, key=cmp_to_key(compare_pair))
  return sum(ordered_pairs), (ordered_packets.index("[[6]]") + 1) * (ordered_packets.index("[[2]]") + 1)
  
def compare_pair(left, right):
  return -1 if compare(parse(left), parse(right)) else 1

def compare(left, right):
  try:
    l = next(left)
  except StopIteration:
    return True
    
  r = next(right)

  if isinstance(l, int) and isinstance(r, int):
    if l == r:
      return compare(left, right)
    return l < r

  if (l == "[" and r == "[") or (l == "]" and r == "]"):
    return compare(left, right)

  if l == "]":
    return True

  if r == "]":
    return False

  if isinstance(l, int):
    return compare(chain(("[", l, "]"), left), chain(r, right))

  if isinstance(r, int):
    return compare(chain(l, left), chain(("[", r, "]"), right))
    
  raise Exception(f"Cannot compare {l} and {r}")

message_re = re.compile("|".join((
  r"(\d+)",
  r"(\[)",
  r"(\])",
)))

def parse(string):
  for mo in message_re.finditer(string):
    s = mo.group()
    yield int(s) if s.isdigit() else s


example = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""