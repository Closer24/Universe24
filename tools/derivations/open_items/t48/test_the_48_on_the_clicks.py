"""The cube's 48 on the clicks: a world run from its seed and from its images under the signed permutations
of the axes about the origin (the torus wrapped), the births compared through the image by the law's criterion.

The law (ALGEBRA.md, the cube's 48; A48-S1 of 2026-10-25): the reflected world is the base's conjugate, so
the clicks of a rotated world are the base's clicks carried by the rotation, equal to the bit, and the clicks
of a reflected world are the base's carried by the reflection with every sense exchanged; none is apart.

The criterion (a48b's B, the kit's clicks_48_example.py, pa2's): a birth is the tuple (interval, the take's
Node, the plane, the children as a map Node -> sense), the minus child's sense -1, the plus child's +1; the
image's births are mapped back through g inverse; a rotation's lawful image is the same map, a reflection's
is the same map with every sense negated (the two children's Nodes exchanged).

The correction of pm2's criterion (tools/derivations/open_items/pm2/clicks_48.py, kept untouched as a record):
pm2 compares a birth as (take Node, plane, minus Node, plus Node, sign W at minus, sign W at plus) and tests
"senses exchanged" by negating the two signs with the two Nodes left in place.  A child's Wronskian at its own
Node is always negative at the minus end and positive at the plus end, so the negated tuple names a birth no
engine can write: under pm2's criterion every reflection reads apart whatever the draw does, and the standing
"24 reflections apart" of PM and MS is in part the test's.  The lawful image of a reflected birth exchanges
the two children's Nodes, which is the map Node -> sense with every sense negated; that is the comparison
written here (`births_through`), and under it the default engine still parts by the digits of the one-Link
read (a48b's REPORT.md, section 1) while A48-S1's draw in the laid frame does not.

The world: tests/worlds/world_node.json's 3-cube with a48b's chiral seed (the hole at the origin and three
quanta at (1,0,0), (0,2,1), (2,1,0): no mirror plane keeps the seed), run INTERVALS intervals, the shortest
run with a birth after a turned Node on which the default engine parts on a rotation and on a reflection.
Integers only: the matrices are signed permutations held as a permutation and three signs, the determinant
the permutation's parity times the product of the signs.
"""

from __future__ import annotations

import itertools
import os
from typing import Any

import event_universe.take as take
from event_universe.node import Node

from tests.laws import world_of

CUBE = 3
INTERVALS = 7
CHIRAL_SEED = [
    {"lay": "sea", "row": 0},
    {"lay": "hole", "at": [0, 0, 0]},
    {"lay": "at", "row": 0, "centre": [1, 0, 0], "quanta": 1},
    {"lay": "at", "row": 0, "centre": [0, 2, 1], "quanta": 1},
    {"lay": "at", "row": 0, "centre": [2, 1, 0], "quanta": 1},
]

Image = tuple[tuple[int, int, int], tuple[int, int, int]]  # (pi, signs): axis a goes to axis pi[a] with sign signs[a]


def signed_permutations() -> list[Image]:
    """The 48 signed permutations of the three axes, in the order of pm2's and a48b's scripts."""
    return [(pi, s) for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def det(g: Image) -> int:
    pi, s = g
    inversions = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
    return (-1) ** inversions * s[0] * s[1] * s[2]


def inverse(g: Image) -> Image:
    pi, s = g
    pi_inv = [0, 0, 0]
    s_inv = [0, 0, 0]
    for a in range(3):
        pi_inv[pi[a]] = a
        s_inv[pi[a]] = s[a]
    return (tuple(pi_inv), tuple(s_inv))  # type: ignore[return-value]


def image(g: Image, x: Any, cube: int) -> tuple[int, int, int]:
    pi, s = g
    y = [0, 0, 0]
    for a in range(3):
        y[pi[a]] = (s[a] * int(x[a])) % cube
    return (y[0], y[1], y[2])


def world_image(world: dict[str, Any], g: Image, cube: int) -> dict[str, Any]:
    seed = []
    for lay in world["seed"]:
        lay = dict(lay)
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(g, lay[key], cube))
        seed.append(lay)
    return {**world, "seed": seed}


def births_through(node: Node, g: Image, cube: int, negate: bool) -> list[tuple[Any, ...]]:
    """Criterion B: every birth as (interval, take Node, plane, the children as a sorted map Node -> sense), the Nodes carried by g, every sense negated where asked."""
    s = -1 if negate else 1
    found = []
    for e in node.log:
        if e["event"] == "birth":
            kids = tuple(sorted([(image(g, e["minus"], cube), -s), (image(g, e["plus"], cube), s)]))
            found.append((e["i"], image(g, e["node"], cube), e["line_pair"], kids))
    return sorted(found)


def run(universe: dict[str, Any], world: dict[str, Any], intervals: int) -> tuple[Node, int]:
    """The Node run `intervals` intervals; beside it the first interval at which a Node turned (0 for none)."""
    node = Node(universe, world)
    first_turn = 0
    for _ in range(intervals):
        node.step()
        if first_turn == 0 and node.counts["turns"] > 0:
            first_turn = node.interval
    return node, first_turn


def verdict(base: list[tuple[Any, ...]], img: Node, g: Image, cube: int) -> str:
    """The image's births carried back by g inverse against the base's: equal, senses exchanged, or apart."""
    back = births_through(img, inverse(g), cube, False)
    if back == base:
        return "equal"
    if births_through(img, inverse(g), cube, True) == base:
        return "senses exchanged"
    return "apart"


def the_48_on_the_clicks(intervals: int, images: list[Image]) -> dict[str, Any]:
    """The verdict of every image, the counts by the sign of the determinant, and the base's births and turns."""
    universe, world = world_of("world_node.json")
    world = {**world, "shape": [CUBE, CUBE, CUBE], "intervals": intervals, "seed": CHIRAL_SEED}
    base, first_turn = run(universe, world, intervals)
    identity: Image = ((0, 1, 2), (1, 1, 1))
    base_births = births_through(base, identity, CUBE, False)
    counts = {d: {"equal": 0, "senses exchanged": 0, "apart": 0} for d in ("rotations", "reflections")}
    verdicts = []
    for g in images:
        img, _ = run(universe, world_image(world, g, CUBE), intervals)
        v = verdict(base_births, img, g, CUBE)
        counts["rotations" if det(g) == 1 else "reflections"][v] += 1
        verdicts.append((g, det(g), v, img.counts["births"]))
    births_after_turn = sum(1 for b in base_births if first_turn and b[0] > first_turn)
    return {"counts": counts, "verdicts": verdicts, "base_births": len(base_births), "first_turn": first_turn, "births_after_turn": births_after_turn}


def test_the_48_on_the_clicks() -> None:
    """Rotations equal, reflections with the senses exchanged, 0 apart (the law); the base run has a birth after a turned Node (the premise)."""
    images = signed_permutations()
    print("engine", take.__file__, "A48B_FOLD", os.environ.get("A48B_FOLD", ""))
    got = the_48_on_the_clicks(INTERVALS, images)
    print("intervals", INTERVALS, "base births", got["base_births"], "first turn", got["first_turn"], "counts", got["counts"])
    rotations = sum(1 for g in images if det(g) == 1)
    reflections = len(images) - rotations
    assert got["births_after_turn"] >= 1, f"the premise: no birth after a turned Node in {INTERVALS} intervals, {got}"
    lawful = {
        "rotations": {"equal": rotations, "senses exchanged": 0, "apart": 0},
        "reflections": {"equal": 0, "senses exchanged": reflections, "apart": 0},
    }
    assert got["counts"] == lawful, f"the 48 on the clicks: {got['counts']} (base births {got['base_births']}, first turn at interval {got['first_turn']}); {[(g, d, v) for g, d, v, _ in got['verdicts'] if v != ('equal' if d == 1 else 'senses exchanged')]}"
