import string
from functools import reduce


def solve(data):
    rucksacks = data.splitlines()
    compartments = [divide(rucksack) for rucksack in rucksacks]
    common = [find_common(compartment) for compartment in compartments]

    p1 = sum(get_priority(element) for element in common)
    assert p1 == 8123

    groups = [rucksacks[n : n + 3] for n in range(0, len(rucksacks), 3)]
    badges = [find_common(group) for group in groups]

    p2 = sum(get_priority(badge) for badge in badges)
    p2 == 2620

    return p1, p2


def divide(line):
    n = len(line) // 2
    return line[:n], line[n:]


def find_common(groups):
    sets = (set(group) for group in groups)
    common = reduce(lambda a, b: a & b, sets)
    return common.pop()


def get_priority(character):
    return 1 + string.ascii_letters.find(character)
