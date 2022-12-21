import re
from collections import deque 

def solve(data):
  drawing, instructions = data.split("\n\n")

  instructions = [parse_instruction(line) for line in instructions.splitlines()]

  # part 1
  stacks = parse_drawing(drawing)
  for instruction in instructions:
    stacks = execute_instruction(stacks, *instruction)
  top_crates = [stack[0] for stack in stacks]

  p1 = "".join(top_crates)
  assert p1 == "CWMTGHBDW"

  # part 1
  stacks = parse_drawing(drawing)
  for instruction in instructions:
    stacks = execute_instruction(stacks, *instruction, new_model=True)
  top_crates = [stack[0] for stack in stacks]

  p2 = "".join(top_crates)
  assert p2 == "SSCGWJCRB"

  return p1, p2


def parse_drawing(drawing):
  lines = drawing.splitlines()
  
  number_of_stacks = len(lines[-1].split())

  line_length = len(lines[0]) - number_of_stacks + 1
  
  field_width = line_length // number_of_stacks
  stacks = [deque() for _ in range(number_of_stacks)]
  
  for line in lines[:-1]:
    crates = [line[n:n+field_width] for n in range(0, len(line), field_width+1)]
    for index, crate in enumerate(crates):
      symbol = crate.strip()
      if symbol:
        stacks[index].append(symbol[1:-1])
  
  return stacks

instruction_re = re.compile(r"move (\d+) from (\d+) to (\d+)")

def parse_instruction(line):
  mo = instruction_re.match(line)
  numbers = [int(match) for match in mo.groups()]
  return numbers

def execute_instruction(stacks, n, src, dest, new_model=False):
  if new_model:
    block = deque()
    for _ in range(n):
      element = stacks[src-1].popleft()
      block.append(element)
    block.extend(stacks[dest-1])
    stacks[dest-1] = block
  else:
    for _ in range(n):
      element = stacks[src-1].popleft()
      stacks[dest-1].appendleft(element)
  return stacks