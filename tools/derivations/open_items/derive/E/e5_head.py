"""Draft E, probe e5: the head's own acts, read with no engine change.

  /home/user/Universe24/venv314/bin/python -I e5_head.py <t24 src>

1. The head's turnover (Clock.reverse, hands.signs) on twin hands: S of the now after = (Sx, -Sy, Sz) of the before
   at every Node-clock, bit for bit: K, not the phase reversal T (which gives -S).
2. The head's pawl signs (meshes.pawls) are a pure gauge: every plaquette's product is +1.
3. The head's lay jam (click.jam) on a world whose sprung trains are twin hands (the head's own test's world): each
   jammed or kept fitting read against the occupant-frame sizes of draft E at its two ends.
Integers only; the head's arrays hold Python integers.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

SRC = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SRC))

import numpy as np  # noqa: E402

from event_universe import click, hands, meshes  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core.spokes import SPOKE_SIDES, across, spoke_of  # noqa: E402
from event_universe.trains import HAND  # noqa: E402

WORLDS = SRC.parent / "tests" / "worlds"
FAIL = []


def check(name, ok, count=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if count is None else f": {count}"))


def twin_clock(ticks):
    calibre, piece = read_piece(WORLDS / "world_nature.json")
    rim = int(calibre["integers"]["den"])
    four = [
        dict(t, shape=HAND + HAND) if t.get("pair") and t["shape"] == HAND and t["pair"][0] < rim else t
        for t in calibre["rows"]
    ]
    return Clock(dict(calibre, rows=four), {**piece, "intervals": ticks})


def z_at(gears, slot, at):
    three, twelve = gears
    return (int(getattr(three, slot)[at]), int(getattr(twelve, slot)[at]))


def spin(up, down):
    c = (up[0] * down[0] + up[1] * down[1], up[0] * down[1] - up[1] * down[0])  # conj(up) down
    return (2 * c[0], 2 * c[1], up[0] ** 2 + up[1] ** 2 - down[0] ** 2 - down[1] ** 2)


def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gn(a):
    return a[0] * a[0] + a[1] * a[1]


def det(u, v):
    p, q = gm(u[0], v[1]), gm(u[1], v[0])
    return (p[0] - q[0], p[1] - q[1])


def inner(u, v):
    p = gm((u[0][0], -u[0][1]), v[0])
    q = gm((u[1][0], -u[1][1]), v[1])
    return (p[0] + q[0], p[1] + q[1])


def part1():
    print("1. The head's turnover on twin hands is K: S(now after) = (Sx, -Sy, Sz)(before), not -S")
    clock = twin_clock(30)
    for _ in range(10):
        clock.tick()
    held = [[g.copy() for g in train] for train in clock.trains()]
    pairs = hands.twin_pairs(clock.hands())
    idx = {id(r): k for k, r in enumerate(clock.trains_)}
    hand_trains = clock.hands()
    clock.reverse(np.ones(clock.size, dtype=bool), held)
    k_ok = t_diff = sites = nonzero = 0
    for up, down in pairs:
        hu, hd = idx[id(hand_trains[up])], idx[id(hand_trains[down])]
        for at in np.ndindex(*clock.size):
            before = spin(z_at(held[hu], "before", at), z_at(held[hd], "before", at))
            after = spin(z_at(hand_trains[up].gears, "now", at), z_at(hand_trains[down].gears, "now", at))
            sites += 1
            k_ok += after == (before[0], -before[1], before[2])
            if before != (0, 0, 0):
                nonzero += 1
                t_diff += after != tuple(-x for x in before)
    check("every Node-clock of every twin pair: S(now after) = (Sx, -Sy, Sz) of the before", k_ok == sites, f"{k_ok} of {sites}")
    check("where S is not 0, the head's image differs from T's -S", t_diff > 0, f"{t_diff} of {nonzero}")


def part2():
    print("2. The head's pawl signs are a pure gauge (no flux)")
    clock = twin_clock(2)
    rng = random.Random(5)
    bad = total = 0
    for _ in range(20):
        fine = np.array([[[rng.randint(0, 1) for _ in range(clock.size[2])] for _ in range(clock.size[1])] for _ in range(clock.size[0])], dtype=object)
        f = meshes.pawls(fine)
        for a in range(3):
            for b in range(3):
                if a == b:
                    continue
                pa, pb = spoke_of(a, 0), spoke_of(b, 0)
                # the plaquette at x: x -> x + a -> x + a + b, and x -> x + b -> x + a + b
                prod_ = f[pa] * across(f[pb], pa) * f[pb] * across(f[pa], pb)
                bad += int((prod_ != 1).sum())
                total += prod_.size
    check("plaquette products of the head's pawl signs that are not +1", bad == 0, f"{bad} of {total}")


def part3():
    print("3. The head's lay jam on the twin world, against the occupant-frame sizes at each end")
    clock = twin_clock(20)
    rows = []
    original = click.jam

    def jam_read(clock_, fits, winds):
        kept = original(clock_, fits, winds)
        hs = clock_.start_gears
        all_hands = clock_.hands()
        kept_set = set(kept)
        for k in fits:
            hand = all_hands[k.gear_ratio]
            if hand.twin is None:
                continue
            up, down = k.gear_ratio, hands.twin_of(all_hands, k.gear_ratio)
            standing = int(winds[up][k.minus]) > 0 or int(winds[down][k.plus]) > 0
            a_ = clock_.A
            ends = []
            for where, child in ((k.minus, ((-a_, 0), (0, 0))), (k.plus, ((0, 0), (a_, 0)))):
                occ = (z_at(hs[up], "now", where), z_at(hs[down], "now", where))
                room = (gn(occ[0]) + gn(occ[1])) * (gn(child[0]) + gn(child[1]))
                free, blocked = gn(det(occ, child)), gn(inner(occ, child))
                ends.append((free, blocked, room, occ != ((0, 0), (0, 0))))
            rows.append((k in kept_set, standing, ends))
        return kept

    click.jam = jam_read
    try:
        for _ in range(20):
            clock.tick()
    finally:
        click.jam = original
    lagrange = all(f + b == r for _k, _s, e in rows for f, b, r, _o in e)
    check("at every end read, free + blocked = the room (Lagrange)", lagrange, sum(len(e) for _k, _s, e in rows))
    by_standing = [e for kept, st, e in rows if not kept and st]
    by_crowding = [e for kept, st, e in rows if not kept and not st]
    kept = [e for kept, _st, e in rows if kept]
    blocked_full = sum(1 for e in by_standing if any(f == 0 and o for f, _b, _r, o in e))
    drawable = sum(1 for e in by_standing if all(f > 0 or not o for f, _b, _r, o in e))
    sure = sum(1 for e in by_standing if all(f == r for f, _b, r, _o in e))
    kept_blocked = sum(1 for e in kept if any(b > 0 for _f, b, _r, _o in e))
    print(f"  twin fittings read: {len(rows)}; kept by the head {len(kept)}; refused by the standing test {len(by_standing)}, by the crowding test alone {len(by_crowding)}")
    print(f"  refused by the standing test where an occupied end's free size is 0 (the derived act refuses too): {blocked_full}")
    print(f"  refused by the standing test although every occupied end leaves a free size above 0 (the derived act could lay): {drawable}")
    print(f"    of them with every end's free size the whole room (the derived act lays for sure): {sure}")
    print(f"  kept by the head although an end's occupant has a blocked size above 0: {kept_blocked}")
    check("every twin fitting was read at both ends", all(len(e) == 2 for _k, _s, e in rows), len(rows))


if __name__ == "__main__":
    part1()
    part2()
    part3()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)
