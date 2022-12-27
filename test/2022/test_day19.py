import pytest
from aoc2022.day19 import (
    EXAMPLE,
    parse_blueprints,
    GameState,
    Robots,
    maximum_required_robots,
)


def test_parse_blueprints():
    blueprints = parse_blueprints(EXAMPLE)
    assert blueprints == {
        1: (
            (4, 0, 0, 0),
            (2, 0, 0, 0),
            (3, 14, 0, 0),
            (2, 0, 7, 0),
        ),
        2: (
            (2, 0, 0, 0),
            (3, 0, 0, 0),
            (3, 8, 0, 0),
            (3, 0, 12, 0),
        ),
    }


def test_initial_game_state():
    s = GameState()
    assert s.minute == 0
    assert s.robots.ore == 1
    assert s.robots.clay == 0
    assert s.robots.obsidian == 0
    assert s.robots.geode == 0
    assert s.resources == (0, 0, 0, 0)


def test_game_state_as_tuple():
    s = GameState()
    assert s.tuple() == (0, (1, 0, 0, 0), (0, 0, 0, 0))


def test_game_state_collect():
    s = GameState(resources=(1, 0, 0, 0), robots=(1, 2, 3, 0))
    s.collect()
    assert s.resources == Robots(2, 2, 3, 0)


def test_game_state_spend():
    s = GameState(resources=(2, 4, 0, 0))
    costs = (1, 3, 0, 0)
    s.spend(costs)
    assert s.resources == (1, 1, 0, 0)


def test_game_state_can_build():
    s = GameState()
    s.resources = (2, 4, 0, 0)
    costs = (1, 3, 0, 0)
    assert s.can_build(costs)
    costs = (3, 3, 0, 0)
    assert s.can_build(costs) is False


def test_game_state_build():
    s = GameState()
    s.build("geode")
    assert s.robots == (1, 0, 0, 1)
    s.build("ore")
    assert s.robots == (2, 0, 0, 1)
    s.build("clay")
    assert s.robots == (2, 1, 0, 1)
    s.build("obsidian")
    assert s.robots == (2, 1, 1, 1)


def test_game_state_advance():
    s = GameState()
    s.advance()
    assert s.minute == 1
    assert s.resources == (1, 0, 0, 0)


def test_game_state_advance_and_build():
    s = GameState()
    s.resources = (3, 0, 12, 0)
    costs = (3, 0, 12, 0)
    s.advance_and_build("geode", costs)
    assert s.minute == 1
    assert s.robots == (1, 0, 0, 1)
    assert s.resources == (1, 0, 0, 0)


def test_game_state_reward():
    s = GameState()
    assert s.reward == 0
    s.build("geode")
    s.collect()
    assert s.reward == 1


def test_game_state_bound():
    limit = 24
    s = GameState()
    b0 = s.bound(limit)
    assert b0 > 0
    s.advance()
    b1 = s.bound(limit)
    assert b1 < b0
    s.build("geode")
    b2 = s.bound(limit)
    assert b2 > b1


def test_game_state_copy():
    s = GameState()
    s.advance()
    t = s.copy()
    s.build("geode")
    assert s is not t
    assert s.minute == t.minute
    assert s.robots.geode == 1
    assert t.robots.geode == 0


@pytest.mark.parametrize(
    "game_state, branches",
    [
        (
            # if you can't build anything, just advance
            GameState(),
            [GameState(minute=1, robots=(1, 0, 0, 0), resources=(1, 0, 0, 0))],
        ),
        (
            # if you can build geode, do only that
            GameState(resources=(4, 8, 12, 0)),
            [GameState(minute=1, robots=(1, 0, 0, 1), resources=(2, 8, 0, 0))],
        ),
        (
            # if you have enough robots of a kind, don't build those,
            # but build all others and advance
            GameState(robots=(4, 0, 0, 0), resources=(4, 8, 0, 0)),
            [
                GameState(minute=1, robots=(4, 0, 0, 0), resources=(8, 8, 0, 0)),
                GameState(minute=1, robots=(4, 1, 0, 0), resources=(5, 8, 0, 0)),
                GameState(minute=1, robots=(4, 0, 1, 0), resources=(5, 0, 0, 0)),
            ],
        ),
        (
            # if you reach the time limit, stop
            GameState(minute=24),
            [],
        ),
    ],
)
def test_game_state_branch(game_state, branches):
    blueprint = (
        (4, 0, 0, 0),  # ore
        (3, 0, 0, 0),  # clay
        (3, 8, 0, 0),  # obsidian
        (3, 0, 12, 0),  # geode
    )
    required = maximum_required_robots(blueprint)
    limit = 24
    assert game_state.branch(limit, blueprint, required) == branches


def test_maximum_required_robots():
    bp = parse_blueprints(EXAMPLE)[1]
    robots = maximum_required_robots(bp)
    assert robots.ore == 4
    assert robots.clay == 14
    assert robots.obsidian == 7
