import re
from itertools import zip_longest


def solve(data):
    data = example
    world, path = parse_data(data)
    player = Player(world)
    for instruction in path:
        player.go(instruction)
    return player.password(), None


def parse_data(data):
    world_map, path = data.split("\n\n")
    world = get_world(world_map)
    path = list(mo.group() for mo in re.finditer(r"(\d+)|([RL])", path))
    return world, path


def get_world(string):
    m = get_matrix(string)
    walls = get_walls(m)
    row_boundaries = get_boundaries(m)
    column_boundaries = get_boundaries(transpose(m))
    return (walls, row_boundaries, column_boundaries)


def get_matrix(string):
    return list(map(list, string.splitlines()))


def get_walls(m):
    return {(x, y) for y, line in enumerate(m) for x, c in enumerate(line) if c == "#"}


def get_boundaries(m):
    b = []
    for line in m:
        xs = [x for x, c in enumerate(line) if c != " "]
        x0 = min(xs)
        k = len(xs)
        b.append((x0, k))
    return b


def transpose(m):
    return list(zip_longest(*m, fillvalue=" "))


def move(x, dx, x0, k):
    return x0 + ((x + dx - x0) % k)


class WallCollision(Exception):
    pass


class Player:
    def __init__(self, world):
        self.walls, self.row_boundaries, self.column_boundaries = world
        self.facing = 0
        self.x, self.y = (self.row_boundaries[0][0], 0)
        self.m = self.get_adjacency_matrix()

    def get_adjacency_matrix(self):
        m = dict()
        for y, (x0, k) in enumerate(self.row_boundaries):
            for x in range(x0, x0 + k):
                y0, l = self.column_boundaries[x]
                neighbors = [
                    (move(x, 1, x0, k), y),
                    (x, move(y, 1, y0, l)),
                    (move(x, -1, x0, k), y),
                    (x, move(y, -1, y0, l)),
                ]
                m[(x, y)] = neighbors
        return m

    def move(self):
        # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        x, y = self.m[(self.x, self.y)][self.facing]
        if (x, y) in self.walls:
            raise WallCollision
        self.x, self.y = x, y

    def turn_left(self):
        self.facing = (self.facing - 1) % 4

    def turn_right(self):
        self.facing = (self.facing + 1) % 4

    def go(self, instruction):
        if instruction.isdigit():
            n = int(instruction)
            for _ in range(n):
                try:
                    self.move()
                except WallCollision:
                    break
        elif instruction == "R":
            self.turn_right()
        elif instruction == "L":
            self.turn_left()

    def password(self):
        # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
        column = self.x + 1
        row = self.y + 1
        return 1000 * row + 4 * column + self.facing


example = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
