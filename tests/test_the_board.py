"""The one board test: the 48 (the board run from a seed and from each of its 48 images, the signed permutations of the axes about the origin; the births and the carrier's and the gap-0 line's levels compared through the image, the 24 rotations alike, the 24 reflections apart under the default: A2's standing item, named), the run back exact through births and turns, the chiral seed's births with both hands and the charge summed to 0."""

from __future__ import annotations

import copy
import itertools
import json
from typing import Any

import numpy as np

from event_universe import gates as table
from event_universe import run as writer
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE
from tests.laws import node_of, refused, run_back_exact, world_of

CUBE, INTERVALS, GROUPS, ALIKE = 5, 20, 4, (6, 0, 0, 0)  # rotations alike per part (MS-S1)
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
    """MA-S1 by the fourth form of the file (the owner's word of 17:57 through the Boss, 6401141446; ma2's spelling, the Boss's 6401095909): the pair of the heavy row laid at every Node of the 3-cube at one quantum (tests/worlds/world_pair_3.json, {"lay": "sea", "row": 2, "quanta": 1, "sense": 0}: the amplitude 96, ma1's, re_now 192 the two senses summed, W 0) keeps every Node alike to the integer (400 of 400), turns every Node at once at both tops (27 at 85 and at 252, ma1's), births nothing, and bottoms at 169 and 335; the bottoms 992 and 966 against ma1's exact 1,000 at 168 / 169 and 333 / 334, NOT MET on this head and named: the body at every Node clicks at interval 8 already (PM-S1's unit: the pair stands at a whole quantum from the lay; 27 credits of 6 levels of light each, 162 credits in all against ma1's 27 at 336), and the light taken is the return's shortfall; the run back exact 10 of 10."""
    node = node_of("world_pair_3.json")
    assert int(node.by_index[2].lines[0].now.min()) == int(node.by_index[2].lines[0].now.max()) == 192
    kept = copy.deepcopy(node)
    alike, tops, means = 0, 0, []
    for _ in range(400):
        node.step()
        x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
        alike += min(x) == max(x)
        means.append(sum(x) // len(x))
        if node.turned.any():
            tops += 1
            assert (node.interval, int(node.turned.sum())) in ((85, 27), (252, 27))
    bottoms = [
        (k + 1, means[k]) for k in range(1, 399) if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]
    credits = [e for e in node.log if e["event"] == "credit"]
    assert (alike, tops, node.counts["births"], len(credits)) == (400, 2, 0, 162)
    assert bottoms == [(169, 992), (335, 966)] and sum(1 for c in credits if c["i"] == 8) == 27
    assert run_back_exact(kept, 10) == 10


def test_the_bare_sea_returns_exactly_with_the_whole_board_turning_at_once_bb() -> None:
    """BB-S1 and MA-S1 read by gate 1 from the Node lines (the Boss's 6400540638 and 6400767119 (2); BB_COMPARISON.md section 4): the sea alone on the 3-cube to 240 (tests/worlds/world_sea_3.json, the Universe seed that returns) tops at 58 and 173 with all 27 Nodes turning at once, returns to X = Gamma at every Node exactly at 115 and 230 (the bottoms), the bangs numbered 1, 116 and 231 with no birth and no credit between them; the record read through the table, gate 1 SHOWN, gate 46 NOT SHOWN (no body in the later cycle), the run back exact 10 of 10."""
    universe, world = world_of("world_sea_3.json")
    found = json.loads(json.dumps(writer.record(universe, world, 10, lambda line: None)))
    out = table.gates(found)
    bang = json.loads(json.dumps(out["1 recurring bangs"]))
    assert bang["tops with every Node turning at once (interval)"] == [58, 173]
    assert bang["bottoms (interval, mean X, at Gamma at every Node)"] == [
        [115, 1000, True],
        [230, 1000, True],
    ]
    assert bang["bangs numbered (the interval each begins)"] == [1, 116, 231]
    assert bang["births and body credits between the bangs"] == [[0, 0], [0, 0], [0, 0]]
    assert bang["verdict"].startswith("SHOWN: 2 exact returns")
    assert out["46 the bangs recurring with the same gates"]["verdict"].startswith("NOT SHOWN")
    assert found["run_back"] == {"intervals": 10, "exact": 10} and found["counts"]["births"] == "0"


def test_the_moving_lay_runs_at_its_momentum_over_twice_its_share_mv() -> None:
    """MV-S1 to MV-S3 (the Boss's ledger item 7, MV_COMPARISON.md's section for David): the heavy row's pair of 3 quanta laid under the sea at the centre of the 9-cube with the wave number h = den div 2 along x (k = pi / 3 exactly): W 0 at every Node of every lay, the share centroid's step at each of the first four closes (the paces still the vacuum's, before the sea deepens the board) within 40 milli-Links per interval of (1000 P) div (2 E) by cross multiplication (P_x = 2 num SUM_i (now_(i+x) before_i - now_i before_(i+x)) over the two lines, E the share summed), a top of 3 Nodes above the width-2 value, wave 0 hash-equal to no wave, the refusals by name, the run back exact through 10."""
    universe, world = world_of("world_packet.json")
    den, milli = int(universe["integers"]["den"]), 1000
    packet = {"lay": "at", "row": 2, "centre": [4, 4, 4], "width": 2, "quanta": 3}
    moving = dict(packet, wave=[den // 2, 0, 0])

    def ints(a: Any) -> list[int]:
        return [int(x) for x in a.reshape(-1)]

    def laid(lay: dict[str, Any]) -> tuple[Node, int]:
        node = Node(universe, dict(world, seed=[{"lay": "sea", "row": 0}, lay]))
        row = node.by_index[2]
        re, im = row.lines
        assert row.pair is not None and not any(ints(re.now * im.before - im.now * re.before))
        energy = sum(
            ints(node.share(row.lines, node.rule(row.pair, node.content(), node.link_factors())))
        )
        momentum = sum(
            sum(
                ints(
                    np.roll(line.now, -1, axis=0) * line.before
                    - line.now * np.roll(line.before, -1, axis=0)
                )
            )
            for line in row.lines
        )
        return node, milli * 2 * row.pair[0] * momentum // (2 * energy)

    def centroid(node: Node) -> tuple[int, int]:
        row = node.by_index[2]
        assert row.pair is not None
        share = node.share(row.lines, node.rule(row.pair, node.content(), node.link_factors()))
        return sum(ints(share * np.indices(node.shape)[0])), sum(ints(share))

    node, law = laid(moving)
    assert laid(dict(moving, top=3))[1] > law > 0
    kept = copy.deepcopy(node)
    before = centroid(node)
    for _ in range(4):
        node.step()
        after = centroid(node)
        step, scale = milli * (after[0] * before[1] - before[0] * after[1]), after[1] * before[1]
        assert abs(step - law * scale) <= 40 * scale, (law, step // scale)
        before = after
    assert node.counts["births"] == 0 and run_back_exact(kept, 10) == 10
    rest, zero = laid(packet)[0], laid(dict(packet, wave=[0, 0, 0]))[0]
    for _ in range(2):
        assert rest.state_hash() == zero.state_hash()
        rest.step()
        zero.step()
    for bad, match in (
        (dict(moving, wave=[den + 1, 0, 0]), "beyond the band's edge"),
        (dict(moving, row=0, wave=[0, 0, 0]), "a massless packet at the wave 0"),
        (dict(moving, top=9), "a top is an odd count"),
        (dict(moving, interval=3), "a field of no form"),
    ):
        refused(match, Node, universe, dict(world, seed=[bad]))
