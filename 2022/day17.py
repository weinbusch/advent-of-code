from itertools import repeat, zip_longest
from functools import reduce

BOTTOM = 254
LEFT = 256
RIGHT = 1
START = 32

# solutions for example
# 3068
# 1514285714288


def solve(data):
    # data = example
    data = data.strip()
    p1 = part1(data)
    p2 = part2(data)
    return p1, p2


def part1(data):
    simulation = simulate(data)
    t = run_simulation(simulation, 2022)
    return len(t) - 1


def part2(data):
    s = simulate(data)
    seen = dict()
    counter = 0
    limit = 1_000_000_000_000

    while counter < 100_000:
        shape_counter, instruction_counter, tower = next(s)
        counter += 1
        if len(tower) <= 2000:
            continue
        signature = (shape_counter, instruction_counter, tuple(tower[-2000:]))
        if signature in seen:
            break
        seen[signature] = (counter, len(tower))
    else:
        raise Exception(
            "simulation stopped after reaching limit; "
            "could not find any repeating signature"
        )

    c0, h0 = seen[signature]
    c1, h1 = counter, len(tower)

    period = c1 - c0
    height_of_repetition = h1 - h0

    remaining_iterations = limit - c1
    number_of_repetitions, remaining_limit = divmod(remaining_iterations, period)

    h2 = number_of_repetitions * height_of_repetition

    t3 = run_simulation(s, remaining_limit)

    h3 = len(t3) - h1

    return h1 + h2 + h3 - 1


def run_simulation(simulation, limit):
    counter = 0
    while counter < limit:
        _, _, t = next(simulation)
        counter += 1
    return t


def encode_shape(s):
    return tuple(
        reduce(
            lambda x, y: x | y,
            (START >> dx for dx, c in enumerate(line) if c == "#"),
        )
        for line in reversed(s.splitlines())
    )


def shift_left(rock):
    return tuple(r << 1 for r in rock)


def shift_right(rock):
    return tuple(r >> 1 for r in rock)


def collides(rock, obstacle):
    if isinstance(obstacle, int):
        obstacle = repeat(obstacle)
    return any(x & y for x, y in zip(rock, obstacle))


def merge(rock, tower, pos):
    tower[pos:] = [x | y for x, y in zip_longest(rock, tower[pos:], fillvalue=0)]


def simulate(jet_pattern):
    number_of_jets = len(jet_pattern)
    jet_counter = 0

    shapes = tuple(encode_shape(s) for s in SHAPES.split("\n\n"))

    number_of_shapes = len(shapes)
    shape_counter = 0

    tower = [BOTTOM]

    while True:
        pos = len(tower) + 3
        rock = shapes[shape_counter]
        while True:
            jet = jet_pattern[jet_counter]
            jet_counter = (jet_counter + 1) % number_of_jets
            r = shift_left(rock) if jet == "<" else shift_right(rock)
            if not any(collides(r, o) for o in (LEFT, RIGHT, tower[pos:])):
                rock = r
            if collides(rock, tower[pos - 1 :]):
                break
            pos -= 1
        merge(rock, tower, pos)
        yield shape_counter, jet_counter, tower
        shape_counter = (shape_counter + 1) % number_of_shapes


def render(tower):
    return "\n".join(
        "{:0>9}".format(bin(lvl)[2:]).replace("1", "#").replace("0", ".")
        for lvl in reversed(tower)
    )


example = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

SHAPES = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""
