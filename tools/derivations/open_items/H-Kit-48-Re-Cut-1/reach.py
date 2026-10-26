"""The one-Link reach on the engine (docs/ALGEBRA.md, Only local; the owner's locality law of 2026-10-25), no toy: a world run N intervals, the board copied, one Node's gap-0 level changed on the copy, both run one interval; the births and the refusals of that interval compared Link by Link, each Link named by the least torus L1 distance of its two ends from the changed Node (the births on Links with both ends at distance 2 or more equal bit for bit), and every line's slots (now, before, rem, wr) that differ, counted by the distance of their Node from the changed one: the step reaches one Link (the distances 0 and 1), the lays the Link ends and the packets' width; the farthest distance with a difference is the reach measured, and "no Node's state moved by a second shell" reads as no difference at distance 2 or more on a step without a birth.

Usage: PYTHONPATH=<worktree>/src python reach.py <world.json> <intervals before the change> <x,y,z> <levels added> <out.json> [cube N]
"""

from __future__ import annotations

import copy
import json
import sys
from typing import Any

import numpy as np

sys.set_int_max_str_digits(0)

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402


def arg_after(argv: list[str], key: str, default: str | None) -> str | None:
    return argv[argv.index(key) + 1] if key in argv else default


def distance(node: tuple[int, ...], origin: tuple[int, ...], cube: int) -> int:
    return sum(min(abs(node[k] - origin[k]), cube - abs(node[k] - origin[k])) for k in range(3))


def clicks_of(node: Node, interval: int) -> tuple[dict, dict]:
    found, refused = {}, {}
    for e in node.log:
        if e["i"] != interval:
            continue
        if e["event"] == "birth":
            ends = (tuple(e["minus"]), tuple(e["plus"]))
            key = tuple(sorted(ends))
            found[key] = (e["line_pair"], ends, int(e["taken"]), int(e["booked"]), e["levels"], tuple(e["amplitude"]))
        elif e["event"] == "refused" and "link" in e:
            key = tuple(sorted((tuple(e["node"]), tuple(e["link"]))))
            refused[key] = e["cause"]
    return found, refused


def main(argv: list[str]) -> None:
    world_path, n, p, added, out_path = argv[1], int(argv[2]), tuple(int(x) for x in argv[3].split(",")), int(argv[4]), argv[5]
    universe, world = load_world(world_path)
    cube = int(arg_after(argv, "cube", str(world["shape"][0])))
    world = dict(world, shape=[cube] * 3)
    a = Node(universe, world)
    for _ in range(n):
        a.step()
    b = copy.deepcopy(a)
    light = b.emitter().lines[0]
    light.now[p] = light.now[p] + added
    a.step()
    b.step()
    fa, ra = clicks_of(a, a.interval)
    fb, rb = clicks_of(b, b.interval)
    by: dict[int, dict[str, int]] = {}
    for link in set(fa) | set(fb) | set(ra) | set(rb):
        d = min(distance(link[0], p, cube), distance(link[1], p, cube))
        same = fa.get(link) == fb.get(link) and ra.get(link) == rb.get(link)
        row = by.setdefault(d, {"links": 0, "equal": 0, "apart": 0, "births a": 0, "births b": 0})
        row["links"] += 1
        row["equal" if same else "apart"] += 1
        row["births a"] += link in fa
        row["births b"] += link in fb
    diffs: dict[int, int] = {}
    for row_a, row_b in zip(a.rows(), b.rows(), strict=True):
        for la, lb in zip(row_a, row_b, strict=True):
            for slot in ("now", "before", "rem", "wr"):
                xa, xb = getattr(la, slot), getattr(lb, slot)
                if xa is None:
                    continue
                for at in zip(*np.nonzero(np.asarray(xa != xb))):
                    d = distance(tuple(int(x) for x in at), p, cube)
                    diffs[d] = diffs.get(d, 0) + 1
    result: dict[str, Any] = {
        "world": world_path,
        "cube": cube,
        "changed node": list(p),
        "levels added": added,
        "interval of the change": a.interval,
        "births this interval a/b": [len(fa), len(fb)],
        "links compared by distance of the nearer end": {str(d): r for d, r in sorted(by.items())},
        "farthest distance with a Link apart": max([d for d, r in by.items() if r["apart"]], default=None),
        "links at distance >= 2 equal / of": [
            sum(r["equal"] for d, r in by.items() if d >= 2),
            sum(r["links"] for d, r in by.items() if d >= 2),
        ],
        "line slots differing by distance": {str(d): c for d, c in sorted(diffs.items())},
        "farthest distance with a slot differing": max(diffs, default=None),
        "reach one Link (no slot differing at distance >= 2)": all(d < 2 for d in diffs),
    }
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=1)
    print(json.dumps(result))


if __name__ == "__main__":
    main(sys.argv)
