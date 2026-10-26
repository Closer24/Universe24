"""The 48 on the clicks, on the engine's own log (src/event_universe, no toy): a world file and a count of intervals in; the board run from the seed and from each of its 48 images (the signed permutations of the axes about the origin, as tests/test_the_board.py builds them: 24 proper rotations, det +1, and 24 reflections, det -1); the click record of each image (the births with the children's Nodes and senses, the credits with line, sense and beat, the takes taken / booked / levels of both, the turned Nodes per interval) carried back through the image and compared with the base's: the verdict per image is EQUAL (bit for bit under the image), CONJUGATE (every sense negated, the children exchanged) or APART, with the first interval apart per part (births, credits, takes, turns). Integers only.

Usage: PYTHONPATH=<worktree>/src python clicks_48.py <world.json> <intervals> <out.json> [cube N] [src <path>]
  cube N  the world run on the N-cube instead of the file's shape (the 3-cube for the fast reference).
Prints one JSON line per image and the summary (the counts by verdict and by det) last.
"""

from __future__ import annotations

import itertools
import json
import sys
from typing import Any

import numpy as np


def arg_after(argv: list[str], key: str, default: str | None) -> str | None:
    return argv[argv.index(key) + 1] if key in argv else default


SRC = arg_after(sys.argv, "src", None)
if SRC:
    sys.path.insert(0, SRC)
sys.set_int_max_str_digits(0)

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

IMAGES = [
    np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
    for pi in itertools.permutations(range(3))
    for s in itertools.product((1, -1), repeat=3)
]


def det_of(m: np.ndarray) -> int:
    """The determinant of a signed permutation as an integer: the permutation's parity times the signs' product."""
    pi = [int(np.nonzero(m[:, a])[0][0]) for a in range(3)]
    signs = [int(m[pi[a], a]) for a in range(3)]
    inversions = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
    return (-1) ** inversions * signs[0] * signs[1] * signs[2]


def image(m: np.ndarray, node: Any, cube: int) -> tuple[int, ...]:
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(world: dict, m: np.ndarray, cube: int) -> dict:
    found = dict(world, shape=[cube] * 3, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, lay[key], cube))
    return found


def run(universe: dict, world: dict, intervals: int) -> tuple[Node, list[list[tuple[int, ...]]]]:
    """The board run, the turned Nodes of every interval kept beside the Node (the log holds no turn line)."""
    node = Node(universe, world)
    turned = []
    for _ in range(intervals):
        node.step()
        turned.append([tuple(int(x) for x in at) for at in zip(*np.nonzero(node.turned))])
    return node, turned


def click_record(
    node: Node, turned: list[list[tuple[int, ...]]], m: np.ndarray, cube: int, s: int
) -> dict[str, list[tuple]]:
    """The clicks under the image m with the senses times s: four sorted lists, the births, the credits, the takes (taken, booked, levels per click) and the turns."""
    births, credits, takes, turns = [], [], [], []
    for e in node.log:
        if e["event"] == "birth":
            kids = tuple(sorted([(image(m, e["minus"], cube), -s), (image(m, e["plus"], cube), s)]))
            births.append((e["i"], image(m, e["node"], cube), e["line_pair"], kids))
            takes.append(("birth", e["i"], image(m, e["node"], cube), int(e["taken"]), int(e["booked"]), e["levels"]))
        elif e["event"] == "credit":
            credits.append((e["i"], image(m, e["node"], cube), e["line"], s * e["sense"], e["beat"]))
            takes.append(("credit", e["i"], image(m, e["node"], cube), int(e["taken"]), int(e["booked"]), e["levels"]))
    for i, nodes in enumerate(turned):
        turns.append((i + 1, tuple(sorted(image(m, at, cube) for at in nodes))))
    return {"births": sorted(births), "credits": sorted(credits), "takes": sorted(takes), "turns": sorted(turns)}


def first_apart(a: list[tuple], b: list[tuple], at: int) -> int | None:
    """The first interval at which the two sorted lists part (the interval read at the tuple's index `at`)."""
    odd = set(a) ^ set(b)
    return None if not odd else min(x[at] for x in odd)


def compare(base: dict[str, list[tuple]], other: dict[str, list[tuple]]) -> dict[str, int | None]:
    where = {"births": 0, "credits": 0, "takes": 1, "turns": 0}
    return {part: first_apart(base[part], other[part], where[part]) for part in base}


def main(argv: list[str]) -> None:
    world_path, intervals, out_path = argv[1], int(argv[2]), argv[3]
    universe, world = load_world(world_path)
    cube = int(arg_after(argv, "cube", str(world["shape"][0])))
    world = dict(world, intervals=intervals)
    eye = np.eye(3, dtype=int)
    base, base_turned = run(universe, world_image(world, eye, cube), intervals)
    base_rec = click_record(base, base_turned, eye, cube, 1)
    rows = []
    counts = {"EQUAL": 0, "CONJUGATE": 0, "APART": 0}
    for k, m in enumerate(IMAGES):
        img, img_turned = run(universe, world_image(world, m, cube), intervals)
        back = click_record(img, img_turned, m.T, cube, 1)
        back_x = click_record(img, img_turned, m.T, cube, -1)
        plain, conjugate = compare(base_rec, back), compare(base_rec, back_x)
        verdict = (
            "EQUAL"
            if all(v is None for v in plain.values())
            else "CONJUGATE"
            if all(v is None for v in conjugate.values())
            else "APART"
        )
        counts[verdict] += 1
        firsts = [v for v in plain.values() if v is not None]
        row = {
            "image": k,
            "det": det_of(m),
            "verdict": verdict,
            "first_apart": min(firsts) if firsts else None,
            "first_apart_by_part": plain,
            "first_apart_by_part_conjugate": conjugate,
            "births": int(img.counts["births"]),
            "credits": int(img.counts["body_clicks"]),
            "turns": int(img.counts["turns"]),
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
    summary = {
        "world": world_path,
        "cube": cube,
        "intervals": intervals,
        "counts": counts,
        "by_det": {
            str(d): {v: sum(1 for r in rows if r["det"] == d and r["verdict"] == v) for v in counts}
            for d in (1, -1)
        },
        "base": {
            "births": len(base_rec["births"]),
            "credits": len(base_rec["credits"]),
            "takes": len(base_rec["takes"]),
            "turns": int(base.counts["turns"]),
            "counts": {k: int(v) for k, v in base.counts.items()},
        },
        "first_apart_intervals": sorted({r["first_apart"] for r in rows if r["verdict"] == "APART"}),
    }
    print(json.dumps(summary), flush=True)
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump({"summary": summary, "rows": rows}, out, default=str)


if __name__ == "__main__":
    main(sys.argv)
