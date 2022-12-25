from collections import deque
import re


def solve(data):
    # data = example

    p1 = play_game(data, 20, True)
    p2 = play_game(data, 10000, False)

    return p1, p2


class Monkey:
    def __init__(self, monkeys, pk, starting_items, operation, divisible_by, a, b):
        self.pk = pk
        self.monkeys = monkeys
        self.items = deque(starting_items)
        self.operation = operation
        self.divisible_by = divisible_by
        self.a = a
        self.b = b
        self.inspected = 0
        self._gcd = None

    @property
    def gcd(self):
        if self._gcd is None:
            gcd = 1
            for m in self.monkeys:
                gcd *= m.divisible_by
            self._gcd = gcd
        return self._gcd

    def take_turn(self, limit_worry_level):
        while self.items:
            item = self.items.popleft()
            item = self.inspect(item)
            item = item % self.gcd
            if limit_worry_level:
                item = item // 3
            monkey = self.test_item(item)
            self.throw(item, monkey)

    def inspect(self, item):
        item = self.operation(item)
        self.inspected += 1
        return item

    def throw(self, item, monkey):
        self.monkeys[monkey].items.append(item)

    def test_item(self, item):
        return self.a if item % self.divisible_by == 0 else self.b

    def __str__(self):
        return f"Monkey {self.pk} {', '.join(str(item) for item in self.items)}"


instruction_re = re.compile(
    r"Monkey (\d+):"
    r"\s*Starting items: (.*?)$"
    r"\s*Operation: (.*?)$"
    r"\s*Test: divisible by (\d+)$"
    r"\s*If true: throw to monkey (\d+)"
    r"\s*If false: throw to monkey (\d+)",
    re.M,
)

operation_re = re.compile(r"new = (old|\d+) ([+*]) (old|\d+)")


def parse_operation(string):
    x, op, y = operation_re.match(string).groups()

    def operation(item):
        a = item if x == "old" else int(x)
        b = item if y == "old" else int(y)
        if op == "+":
            return a + b
        if op == "*":
            return a * b

    return operation


def get_monkeys(data):
    monkeys = list()
    for block in data.split("\n\n"):
        mo = instruction_re.match(block)
        pk, starting_items, operation, divisible_by, a, b = mo.groups()
        starting_items = [int(x) for x in starting_items.split(", ")]
        operation = parse_operation(operation)
        monkey = Monkey(
            monkeys,
            int(pk),
            starting_items,
            operation,
            int(divisible_by),
            int(a),
            int(b),
        )
        monkeys.append(monkey)
    return monkeys


def get_monkey_business(monkeys):
    most_active = sorted(m.inspected for m in monkeys)
    return most_active[-2] * most_active[-1]


def play_game(data, turns, limit_worry_level):
    monkeys = get_monkeys(data)
    for _ in range(turns):
        for monkey in monkeys:
            monkey.take_turn(limit_worry_level)
    return get_monkey_business(monkeys)


example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
