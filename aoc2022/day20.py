KEY = 811589153


def solve(data):
    # data = example
    numbers = list(map(int, data.splitlines()))
    r1 = mix_numbers(numbers)
    r2 = mix_numbers([n * KEY for n in numbers], 10)
    c1 = get_grove_coordinates(r1)
    c2 = get_grove_coordinates(r2)
    return sum(c1), sum(c2)


def get_grove_coordinates(a):
    k = len(a)
    i0 = a.index(0)
    return [a[(i0 + offset) % k] for offset in (1000, 2000, 3000)]


def mix_numbers(numbers, repetitions=1):
    k = len(numbers)
    tuples = list(enumerate(numbers))
    a = tuples.copy()
    for _ in range(repetitions):
        for t in tuples:
            x = a.index(t)
            (_, dx) = a.pop(x)
            y = (x + dx) % (k - 1)
            a.insert(y, t)
    result = [n for _, n in a]
    return result


example = """1
2
-3
3
-2
0
4
"""

expected = [
    [2, 1, -3, 3, -2, 0, 4],
    [1, -3, 2, 3, -2, 0, 4],
    [1, 2, 3, -2, -3, 0, 4],
    [1, 2, -2, -3, 0, 3, 4],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 4, 0, 3, -2],
]
