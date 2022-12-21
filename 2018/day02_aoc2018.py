from collections import Counter
from itertools import product


def solve(data):
    boxes = data.splitlines()
    counts = [Counter(box) for box in boxes]
    selected = [[box for box in counts if has_counts(box, n)] for n in (2, 3)]
    a, b = [len(x) for x in selected]
    checksum = a * b

    prototype = next(pair for pair in product(boxes, boxes) if is_prototype(pair))
    common = common_characters(prototype)

    return checksum, common


def has_counts(counter, n):
    return any(value == n for value in counter.values())


def is_prototype(pair):
    return number_of_differences(pair) == 1


def number_of_differences(pair):
    return sum(1 for a, b in zip(*pair) if a != b)


def common_characters(pair):
    return "".join(a for a, b in zip(*pair) if a == b)
