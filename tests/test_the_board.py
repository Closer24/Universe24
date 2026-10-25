"""The one board test: the 48 (the board run from a seed and from each of its 48 images, the signed permutations of the axes about the origin; the births and the carrier's and the gap-0 line's levels compared through the image, the 24 rotations alike, the 24 reflections apart under the default: A2's standing item, named), the run back exact through births and turns, the chiral seed's births with both hands and the charge summed to 0."""

from __future__ import annotations

import copy
import itertools
from typing import Any

import numpy as np

from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE
from tests.laws import node_of, run_back_exact, world_of

CUBE, INTERVALS, GROUPS = 5, 20, 4
# the rotations alike per part under A2's digits at 20 intervals on the hole seed (MS-S1, 2026-10-25): the six negating neither y nor z
ALIKE = (6, 0, 0, 0)
IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]


def image(m: Any, node: tuple[int, ...], cube: int) -> tuple[int, ...]:
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def births_of(node: Node) -> list[tuple[Any, ...]]:
    return sorted(
        (e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"]))
        for e in node.log
        if e["event"] == "birth"
    )


def mapped(births: list[tuple[Any, ...]], m: Any, cube: int, exchanged: bool) -> list[tuple[Any, ...]]:
    found = [
        (i, image(m, at, cube), s, image(m, mi, cube), image(m, pl, cube)) for i, at, s, mi, pl in births
    ]
    return sorted((i, at, s, pl, mi) if exchanged else (i, at, s, mi, pl) for i, at, s, mi, pl in found)


def world_image(world: dict[str, Any], m: Any, cube: int) -> dict[str, Any]:
    found = dict(world, shape=[cube] * 3, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key]), cube))
    return found


def run(universe: dict[str, Any], world: dict[str, Any]) -> Node:
    node = Node(universe, world)
    for _ in range(INTERVALS):
        node.step()
    return node


def same_rows(base: Node, other: Node, m: Any) -> bool:
    for line_b, line_o in (
        (base.row(CARRIER).lines[0], other.row(CARRIER).lines[0]),
        (base.row(PLANE, gap=0).lines[0], other.row(PLANE, gap=0).lines[0]),
    ):
        for at in np.ndindex(CUBE, CUBE, CUBE):
            there = image(m, at, CUBE)
            if int(line_b.now[at]) != int(line_o.now[there]) or int(line_b.before[at]) != int(
                line_o.before[there]
            ):
                return False
    return True


def images_hold(group: int) -> None:
    """The images of one part of the 48 (every fourth from the group's first): a rotation that negates no axis runs alike the seed through the image (the rows and the births), a rotation negating the y or the z axis parts under A2's digits (a negated line's remainder mirrors, its digit with it: the standing item, 6 of 24 alike at 20 intervals on the hole seed under MS-S1 against 24 before it), every reflection apart; the counts held by name so that an image coming alike or parting is read."""
    universe, world = world_of("world_hole.json")
    base = run(universe, world_image(world, np.eye(3, dtype=int), CUBE))
    births = births_of(base)
    assert len(births) > 0
    alike = {True: 0, False: 0}
    for m in IMAGES[group::GROUPS]:
        other = run(universe, world_image(world, m, CUBE))
        reflection = int(round(np.linalg.det(m))) == -1
        same = same_rows(base, other, m) and births_of(other) == mapped(births, m, CUBE, reflection)
        alike[reflection] += same
    assert alike[True] == 0 and alike[False] == ALIKE[group]


def test_the_run_back_is_exact_through_births_and_turns() -> None:
    node = node_of("world_hole.json")
    assert run_back_exact(node, 40) == 40
    for _ in range(40):
        node.step()
    assert node.counts["births"] > 0 and node.counts["turns"] > 0


def test_the_chiral_seed_births_both_hands_and_the_charge_sums_to_zero() -> None:
    node = node_of("world_chiral.json")
    for _ in range(60):
        node.step()
    births = [e for e in node.log if e["event"] == "birth"]
    assert len(births) >= 8
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    assert sum(signs) == 0 and 0 not in signs
    assert all(b["taken"] >= b["booked"] for b in births)
    hands = {1 if tuple(b["plus"]) > tuple(b["minus"]) else -1 for b in births}
    assert hands == {1, -1}


def test_the_first_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(0)


def test_the_second_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(1)


def test_the_third_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(2)


def test_the_fourth_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged() -> None:
    images_hold(3)


def test_the_uniform_pair_at_every_node_returns_with_the_whole_board_turning_at_once_ma() -> None:
    """MA-S1 (the Boss's 6400767119 (4), MA_COMPARISON.md section 4 (3)): the pair of the heavy row laid by an `at` of one quantum at every Node of the 3-cube (tests/worlds/world_pair_3.json, the Boss's spelling of the uniform world) keeps every Node alike to the integer (e 0 at 400 of 400), turns every Node at once at its one top (27 at 196, the mean 255,444 at 195), births nothing, credits a body at every Node, and falls to its bottom at 391; the bottom 949 against Gamma, the Boss's 1,000 at 168 / 169 and 27 turned at 85 (ma1's pair at the amplitude 96) NOT MET under the `at` lays: the packets' weights sum to 64 over the 27 Nodes against the centre's 8, so the board holds the eightfold matter (re_now 1,170 against 96 per Node, W 0) and the period lengthens with the write; the run back exact 10 of 10."""
    node = node_of("world_pair_3.json")
    assert int(node.by_index[2].lines[0].now.min()) == int(node.by_index[2].lines[0].now.max()) == 1170
    kept = copy.deepcopy(node)
    alike = tops = 0
    means = []
    for _ in range(400):
        node.step()
        x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
        alike += min(x) == max(x)
        means.append(sum(x) // len(x))
        if node.turned.any():
            tops += 1
            assert (node.interval, int(node.turned.sum())) == (196, 27)
    bottoms = [
        (k + 1, means[k]) for k in range(1, 399) if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]
    assert (alike, tops, node.counts["births"], max(means), means.index(max(means)) + 1) == (
        400,
        1,
        0,
        255444,
        195,
    )
    assert bottoms == [(391, 949)] and node.counts["body_clicks"] == 135
    assert run_back_exact(kept, 10) == 10
