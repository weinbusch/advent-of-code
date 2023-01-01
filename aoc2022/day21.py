import operator
import re


class EvaluationError(Exception):
    pass


def solve(data):
    # data = example
    t1 = parse_data(data)
    p1 = evaluate("root", t1)
    t2 = t1.copy()
    t2["humn"] = Variable("humn")
    t2["root"] = Equation(t2["root"].lhs, t2["root"].rhs)
    p2 = solve_equation("root", t2)
    return p1, p2


def parse_data(data):
    return dict([parse_line(line) for line in data.splitlines()])


line_re = re.compile(r"^([a-z]+): (.*)$")
expression_re = re.compile(r"([a-z]+) ([-+/*]) ([a-z]+)")


def parse_line(line):
    monkey, job = line_re.match(line).groups()
    if job.isdigit():
        job = Number(int(job))
    else:
        lhs, op, rhs = expression_re.match(job).groups()
        job = OPERATIONS[op](Pointer(lhs), Pointer(rhs))
    return monkey, job


def evaluate(name, tree):
    t = tree[name]
    t = t.resolve(tree)
    return t.evaluate()


def solve_equation(name, tree):
    eq = tree[name]
    eq = eq.resolve(tree)
    return eq.solve()


OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def resolve(self, tree):
        return self

    def __repr__(self):
        return f"Number({self.value})"


class BinOp:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self):
        lhs = self.lhs.evaluate()
        rhs = self.rhs.evaluate()
        return self.op(lhs, rhs)

    def resolve(self, tree):
        lhs = self.lhs.resolve(tree)
        rhs = self.rhs.resolve(tree)
        return self.__class__(lhs, rhs)

    def separate_constant(self):
        try:
            const = self.rhs.evaluate()
            var = self.lhs
            f = self.rhs_f(const)
        except EvaluationError:
            const = self.lhs.evaluate()
            var = self.rhs
            f = self.lhs_f(const)
        return var, f

    def __repr__(self):
        return f"{self.__class__.__name__}({self.rhs, self.lhs})"


class Add(BinOp):
    op = operator.add

    def rhs_f(self, x):
        return lambda o: o - x

    def lhs_f(self, x):
        return self.rhs_f(x)


class Sub(BinOp):
    op = operator.sub

    def rhs_f(self, x):
        return lambda o: o + x

    def lhs_f(self, x):
        return lambda o: x - o


class Mul(BinOp):
    op = operator.mul

    def rhs_f(self, x):
        return lambda o: o / x

    def lhs_f(self, x):
        return self.rhs_f(x)


class Div(BinOp):
    op = operator.truediv

    def rhs_f(self, x):
        return lambda o: o * x

    def lhs_f(self, x):
        return lambda o: x / o


OPERATIONS = {
    "+": Add,
    "-": Sub,
    "*": Mul,
    "/": Div,
}


class Pointer:
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        raise Exception("Pointer cannot be evaluated, call .resolve(tree) first")

    def resolve(self, tree):
        return tree[self.name].resolve(tree)

    def __repr__(self):
        return f"Pointer({self.name})"


class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        raise EvaluationError

    def resolve(self, tree):
        return self

    def __repr__(self):
        return f"Variable({self.name})"


class Equation:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self):
        raise Exception("Equation cannot be evaluated, call .solve() instead")

    def resolve(self, tree):
        lhs = self.lhs.resolve(tree)
        rhs = self.rhs.resolve(tree)
        return self.__class__(lhs, rhs)

    def solve(self):
        # assume that variable is in lhs and rhs can always be evaluated
        rhs = self.rhs.evaluate()
        lhs = self.lhs
        while hasattr(lhs, "separate_constant"):
            lhs, f = lhs.separate_constant()
            rhs = f(rhs)
        return Equation(lhs, rhs)

    def __repr__(self):
        return f"Equation({self.lhs}, {self.rhs})"


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
