def solve(data):
    pairs = [line.split(",") for line in data.splitlines()]
    assignments = [[get_assignment(elf) for elf in pair] for pair in pairs]
    fully_contained = [
        assignment_pair
        for assignment_pair in assignments
        if fully_contains(assignment_pair)
    ]

    p1 = len(fully_contained)
    assert p1 == 528

    overlapping = [
        assignment_pair for assignment_pair in assignments if overlaps(assignment_pair)
    ]

    p2 = len(overlapping)
    assert p2 == 881

    return p1, p2


def fully_contains(assignment_pair):
    a, b = assignment_pair
    return a <= b or a >= b


def overlaps(assignment_pair):
    a, b = assignment_pair
    return a & b


def get_assignment(string):
    limits = [int(number) for number in string.split("-")]
    assignment = set(range(limits[0], limits[1] + 1))
    return assignment
