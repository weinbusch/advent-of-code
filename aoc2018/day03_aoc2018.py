import re
from collections import defaultdict

claim_re = re.compile(r"\#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)")


def solve(data):
    claims = [parse_claim(line) for line in data.splitlines()]
    tiles = defaultdict(set)
    unique_pks = set()
    for pk, x, y, w, h in claims:
        unique_pks.add(pk)
        for dx in range(w):
            for dy in range(h):
                tiles[(x + dx, y + dy)].add(pk)
    overlapping = 0
    for pks in tiles.values():
        if len(pks) > 1:
            overlapping += 1
            unique_pks -= pks
    unique_pk = unique_pks.pop()

    return overlapping, unique_pk


def parse_claim(line):
    mo = claim_re.match(line)
    return [int(m) for m in mo.groups()]
