"""Hand dn1: two laws on David's lean toy at a den, from this hand's world files: the cube's 48 (the run from the seed and from each of its 48 images, the births compared through the image and the volume and light rows compared at the last interval; the form of the toy's cube48_test) and the one-Link reach (two boards alike to an interval, one Node's light level changed on one, one interval forward and one back, the farthest Node that differs by the torus's L1 distance; the form of the toy's reach_test). Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Den-Beyond-128-Bits-1/laws.py <world.json> <intervals for the 48> <intervals before the reach's change> <out.json>
"""

from __future__ import annotations

import copy
import itertools
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "toy"))
sys.set_int_max_str_digits(0)

from lean_full import Lean, load_world  # the toy's own program, imported and never edited


def signed_permutations():
    axes = range(3)
    return [np.array([[s[a] if pi[a] == b else 0 for a in axes] for b in axes]) for pi in itertools.permutations(axes) for s in itertools.product((1, -1), repeat=3)]


def image(m, node, cube):
    v = m @ np.array(node, dtype=int)
    return tuple(int(x) % cube for x in v)


def events(b):
    return sorted((e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"])) for e in b.log if e["event"] == "birth")


def mapped(evs, m, cube):
    return sorted((i, image(m, at, cube), s_, image(m, mi, cube), image(m, pl, cube)) for i, at, s_, mi, pl in evs)


def world_image(world, m, cube):
    w = copy.deepcopy(world)
    for lay in w.get("seed", []):
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, tuple(lay[key]), cube))
    return w


def run(universe, world, n):
    b = Lean(universe, world)
    for _ in range(n):
        b.step()
    return b


def the_48(universe, world, n) -> dict:
    cube = int(world["shape"][0])
    t0 = time.monotonic_ns()
    base = run(universe, world_image(world, np.eye(3, dtype=int), cube), n)
    evs = events(base)
    held = 0
    apart = []
    credits_held = 0
    base_credits = sorted((e["i"], tuple(e["node"]), e["line"], e["beat"], e["sense"]) for e in base.log if e["event"] == "credit")
    for m in signed_permutations():
        other = run(universe, world_image(world, m, cube), n)
        same_events = events(other) == mapped(evs, m, cube)
        same_rows = True
        for line_b, line_o in ((base.row(10).lines[0], other.row(10).lines[0]), (base.row(2, gap=0).lines[0], other.row(2, gap=0).lines[0])):
            for at in np.ndindex(cube, cube, cube):
                if int(line_b.now[at]) != int(line_o.now[image(m, at, cube)]) or int(line_b.before[at]) != int(line_o.before[image(m, at, cube)]):
                    same_rows = False
                    break
            if not same_rows:
                break
        other_credits = sorted((i, image(m, at, cube), line, beat, sense) for i, at, line, beat, sense in ((e["i"], tuple(e["node"]), e["line"], e["beat"], e["sense"]) for e in other.log if e["event"] == "credit"))
        credits_held += other_credits == sorted((i, image(m, at, cube), line, beat, sense) for i, at, line, beat, sense in base_credits)
        if same_events and same_rows:
            held += 1
        else:
            apart.append((m.tolist(), "events" if not same_events else "rows"))
    return {"cube": cube, "intervals": n, "births": len(evs), "body_credits": len(base_credits), "turns": base.counts["turns"], "images_holding_births_and_rows": held, "images_holding_credits": credits_held, "of": 48, "apart": apart[:6], "ms": (time.monotonic_ns() - t0) // 10**6}


def distance(node, origin, cube):
    return sum(min(abs(node[k] - origin[k]), cube - abs(node[k] - origin[k])) for k in range(3))


def differences(a, b, p):
    found = []
    for r, (ra, rb) in enumerate(zip(a.rows(), b.rows())):
        for k, (la, lb) in enumerate(zip(ra, rb)):
            for slot in ("now", "before", "rem", "wr"):
                xa, xb = getattr(la, slot), getattr(lb, slot)
                if xa is None:
                    continue
                for node in zip(*np.nonzero(np.asarray(xa != xb))):
                    node = tuple(int(x) for x in node)
                    found.append((distance(node, p, a.cube), r, k, slot, node))
    return found


def the_reach(universe, world, n, added=1) -> dict:
    cube = int(world["shape"][0])
    p = (cube // 2, cube // 2, cube // 2)
    a = run(universe, world, n)
    b = copy.deepcopy(a)
    z = b.row(2, gap=0).lines[0]
    z.now[p] = z.now[p] + added
    assert len(differences(a, b, p)) == 1
    a.step()
    b.step()
    forward = differences(a, b, p)
    by = {}
    for d, r, k, slot, node in forward:
        by.setdefault(d, set()).add((r, k, slot))
    a2 = copy.deepcopy(a)
    b2 = copy.deepcopy(a)
    z2 = b2.row(2, gap=0).lines[0]
    z2.now[p] = z2.now[p] + added
    a2.step_back()
    b2.step_back()
    backward = differences(a2, b2, p)
    by_back = {}
    for d, r, k, slot, node in backward:
        by_back.setdefault(d, set()).add((r, k, slot))
    return {"cube": cube, "intervals_before_change": n, "changed_node": p, "forward": {"differing_lines": len(forward), "farthest_distance": max(by) if by else None, "lines_by_distance": {d: len(v) for d, v in sorted(by.items())}, "log_lines_this_interval_a_b": [len(a.log) - a.stack[-1]["log_from"], len(b.log) - b.stack[-1]["log_from"]]}, "backward": {"differing_lines": len(backward), "farthest_distance": max(by_back) if by_back else None, "lines_by_distance": {d: len(v) for d, v in sorted(by_back.items())}}}


def main() -> None:
    universe, world = load_world(sys.argv[1])
    n48, nreach, out_path = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    found = {"world": sys.argv[1], "den_bits": int(universe["integers"]["den"]).bit_length(), "the_48": the_48(universe, world, n48), "the_reach": the_reach(universe, world, nreach)}
    json.dump(found, open(out_path, "w"), default=str)
    print(json.dumps(found, default=str), flush=True)


if __name__ == "__main__":
    main()
