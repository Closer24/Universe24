"""ag1, item (4), the 48 on the clicks of the engine (ALGEBRA.md, The cube's symmetry; the kit's clicks_48_example re-posed on
src/event_universe): the world is run from its seed and from each of its 48 images (the signed permutations about the origin on
the torus); the record (the births with the take's Node, the children's Nodes and record, taken and booked; the credits with the
Node, the record, the sense, the beat and the take) and the end state (the carrier's time line X and the gap-0 re line) are
compared through the image: EQUAL, or the senses exchanged (the births' two children swapped and every credit's sense negated: the
conjugate record) or APART; the counts over the 24 rotations and the 24 reflections.
tw3: ag1's clicks_48.py (H-Algebra-Of-The-Whole-1) with ONE line changed for this head, the gap-0 plane read as node.emitter(); run under PYTHONPATH=src_tw3 with TW3_TRACE set.
Usage: clicks_48.py <world.json> <intervals> <out.json>"""

from __future__ import annotations

import copy
import itertools
import json
import sys
import time

import numpy as np

sys.set_int_max_str_digits(0)

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE  # noqa: E402


def signed_permutations() -> list[np.ndarray]:
    axes = range(3)
    return [
        np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes], dtype=int)
        for pi in itertools.permutations(axes)
        for s in itertools.product((1, -1), repeat=3)
    ]


def det(m: np.ndarray) -> int:
    """The determinant of a 3 x 3 integer matrix by Leibniz's six terms, integers alone."""
    a = [[int(x) for x in row] for row in m]
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def image(m: np.ndarray, node: tuple[int, ...], cube: int) -> tuple[int, ...]:
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def world_image(world: dict, m: np.ndarray, cube: int) -> dict:
    w = copy.deepcopy(world)
    for lay in w.get("seed", []):
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key]), cube))
    return w


def run(universe: dict, world: dict, n: int) -> Node:
    node = Node(universe, world)
    for _ in range(n):
        node.step()
    return node


def record_of(node: Node, m: np.ndarray, cube: int, conj: bool) -> tuple[list, list]:
    births, credits = [], []
    for e in node.log:
        if e["event"] == "birth":
            mi, pl = image(m, tuple(e["minus"]), cube), image(m, tuple(e["plus"]), cube)
            if conj:
                mi, pl = pl, mi
            births.append((e["i"], image(m, tuple(e["node"]), cube), e["line_pair"], mi, pl, e["taken"], e["booked"], e["levels"]))
        elif e["event"] == "credit":
            sense = -e["sense"] if conj else e["sense"]
            credits.append((e["i"], image(m, tuple(e["node"]), cube), e["line"], sense, e["beat"], e["taken"], e["levels"]))
    return sorted(births), sorted(credits)


def board_of(node: Node, m: np.ndarray, cube: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """The end state's two scalar lines read through the image: X at g x and the gap-0 re line at g x, in the base's order."""
    x = node.row(CARRIER).lines[0].now
    re = node.emitter().lines[0].now  # tw3: the gap-0 plane on this head is node.emitter() (the gap-0 finders, a796f299c)
    xs, res = [], []
    for at in np.ndindex(*node.shape):
        g = image(m, tuple(int(v) for v in at), cube)
        xs.append(int(x[g]))
        res.append(int(re[g]))
    return tuple(xs), tuple(res)


def main(argv: list[str]) -> None:
    t0 = time.monotonic_ns()
    universe, world0 = load_world(argv[1])
    n, out_path = int(argv[2]), argv[3]
    cube = int(world0["shape"][0])
    identity = np.eye(3, dtype=int)
    base = run(universe, world_image(world0, identity, cube), n)
    base_rec = record_of(base, identity, cube, False)
    base_board = board_of(base, identity, cube)
    tallies = {"rotations": {"EQUAL": 0, "SENSES EXCHANGED": 0, "APART": 0}, "reflections": {"EQUAL": 0, "SENSES EXCHANGED": 0, "APART": 0}}
    boards = {"rotations": [0, 0], "reflections": [0, 0]}
    apart: list[dict] = []
    for m in signed_permutations():
        kind = "rotations" if det(m) == 1 else "reflections"
        node = run(universe, world_image(world0, m, cube), n)
        back = m.T  # the inverse of a signed permutation is its transpose
        rec = record_of(node, back, cube, False)
        verdict = "EQUAL" if rec == base_rec else ("SENSES EXCHANGED" if record_of(node, back, cube, True) == base_rec else "APART")
        tallies[kind][verdict] += 1
        boards[kind][0] += board_of(node, m, cube) == base_board  # the image's state at m x against the base's at x
        boards[kind][1] += 1
        if verdict == "APART":
            b0, c0 = base_rec
            b1, c1 = rec
            b2, c2 = record_of(node, back, cube, True)
            apart.append({"m": m.tolist(), "births base/image": [len(b0), len(b1)], "credits base/image": [len(c0), len(c1)],
                          "first differing birth": next(((a, b) for a, b in zip(b0, b1, strict=False) if a != b), None),
                          "first differing credit": next(((a, b) for a, b in zip(c0, c1, strict=False) if a != b), None),
                          "births differing under the conjugation": sum(1 for a, b in zip(b0, b2, strict=False) if a != b),
                          "credits differing under the conjugation": sum(1 for a, b in zip(c0, c2, strict=False) if a != b),
                          "first differing birth under the conjugation": next(((a, b) for a, b in zip(b0, b2, strict=False) if a != b), None),
                          "first differing credit under the conjugation": next(((a, b) for a, b in zip(c0, c2, strict=False) if a != b), None)})
    found = {"world": argv[1], "intervals": n, "births": len(base_rec[0]), "credits": len(base_rec[1]),
             "clicks through the image": tallies, "end state (X, gap-0 re) equal through the image, of": boards,
             "apart (first three)": apart[:3], "seconds": (time.monotonic_ns() - t0) // 10**9}
    print(json.dumps(found))
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main(sys.argv)
