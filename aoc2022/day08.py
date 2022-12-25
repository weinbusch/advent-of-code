from itertools import chain


def solve(data):
    forest = [[int(h) for h in line] for line in data.splitlines()]
    trees = [[(x, y, h) for y, h in enumerate(line)] for x, line in enumerate(forest)]

    visible = set.union(
        *(
            filter_visible(direction)
            for orientation in (trees, zip(*trees))
            for line in orientation
            for direction in (line, reversed(line))
        )
    )

    x_max = len(trees)
    y_max = len(trees[0])
    scores = []
    for x0, y0, h0 in [t for line in trees for t in line]:
        tree_score = 1
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = x0 + dx, y0 + dy
            direction_score = 0
            while x >= 0 and x < x_max and y >= 0 and y < y_max:
                _, _, h = trees[x][y]
                direction_score += 1
                if h >= h0:
                    break
                x, y = x + dx, y + dy
            tree_score *= direction_score
        scores.append(tree_score)

    return len(visible), max(scores)


def filter_visible(line):
    visible = set()
    height = -1
    for x, y, h in line:
        if h > height:
            visible.add((x, y))
            height = h
    return visible
