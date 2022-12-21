def solve(data):
    # part 1
    elves = [[int(line) for line in block.splitlines()] for block in data.split("\n\n")]
    weight = [sum(block) for block in elves]
    max_weight = max(weight)

    assert max_weight == 67633

    # part 2
    top_three = sum(list(reversed(sorted(weight)))[:3])

    assert top_three == 199628

    return max_weight, top_three
