def solve(data):
    lines = data.splitlines()
    trajectories = [get_trajectory(line) for line in lines]
    a, b = trajectories
    crossings = list(set(a) & set(b))
    distances = [abs(x) + abs(y) for x, y in crossings]
    shortest = distances[distances.index(min(distances))]

    steps = [count_steps(trajectories, crossing) for crossing in crossings]
    nearest = steps[steps.index(min(steps))]

    return shortest, nearest


def count_steps(trajectories, crossing):
    return sum(1 + trajectory.index(crossing) for trajectory in trajectories)


lookup_table = dict(
    [
        ("R", (1, 0)),
        ("L", (-1, 0)),
        ("U", (0, 1)),
        ("D", (0, -1)),
    ]
)


def get_trajectory(line):
    instructions = line.split(",")
    current = (0, 0)
    trajectory = []
    for instruction in instructions:
        dir, dist = instruction[0], int(instruction[1:])
        dx, dy = lookup_table[dir]
        for _ in range(dist):
            a, b = current
            current = (a + dx, b + dy)
            trajectory.append(current)
    return trajectory
