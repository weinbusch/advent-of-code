import re

class Expression:
  def __init__(self, lhs, op, rhs):
    self.lhs = lhs
    self.op = op
    self.rhs = rhs

  def __repr__(self):
    return f"<Expression({self.lhs}, {self.op}, {self.rhs})>"

  def __add__(self, other):
    operator = "+"
    return Expression(self, operator, other)

  def __sub__(self, other):
    operator = "-"
    return Expression(self, operator, other)

  def __mul__(self, other):
    operator = "*"
    return Expression(self, operator, other)

  def __truediv__(self, other):
    operator = "/"
    return Expression(self, operator, other)

  def __radd__(self, other):
    operator = "+"
    return Expression(self, operator, other)

  def __rsub__(self, other):
    operator = "-"
    return Expression(self, operator, other)

  def __rmul__(self, other):
    operator = "*"
    return Expression(self, operator, other)

  def __rtruediv__(self, other):
    operator = "/"
    return Expression(self, operator, other)

class Equality:
  def __init__(self, lhs, rhs):
    self.lhs = lhs
    self.rhs = rhs

  def __repr__(self):
    return f"<Equality({self.lhs}, {self.rhs})>"

  def solve(self):
    ...

class Variable(Expression):
  def __init__(self, name):
    self.name = name
  
  def __repr__(self):
    return f"<Variable({self.name})>"


def solve(data):
  # data = example
  input = parse_data(data)
  t1 = dict(input)
  p1 = evaluate("root", t1)
  t2 = t1.copy()
  t2["humn"] = Variable("humn")
  m1, _, m2 = t2["root"] 
  t2["root"] = (m1, "=", m2)
  return p1, evaluate("root", t2)

def parse_data(data):
  return [parse_line(line) for line in data.splitlines()]

def evaluate(monkey, tree):
  job = tree[monkey]
  if isinstance(job, int):
    return job
  if isinstance(job, Variable):
    return job
  m1, op, m2 = job
  t1 = evaluate(m1, tree)
  t2 = evaluate(m2, tree)
  if op == "+":
    return t1 + t2
  elif op == "-":
    return t1 - t2
  elif op == "*":
    return t1 * t2
  elif op == "/":
    return t1 / t2
  elif op == "=":
    return Equality(t1, t2)

line_re = re.compile(r"([a-z]+): (.*)")
integer_re = re.compile(r"\d+")
operation_re = re.compile(r"([a-z]+) ([-+/*]) ([a-z]+)")

def parse_line(line):
  monkey, job = line_re.match(line).groups()
  if job.isdigit():
    job = int(job)
  else:
    job = operation_re.match(job).groups()
  return monkey, job

example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""