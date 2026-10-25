"""un1's one-Node test of the algebra (integers only): run with PYTHONPATH = the worktree's src (David's engine; the copy's functions are
re-derived here from the same primitives so the test needs no flag).
 1. THE UNIT as one function of the pair: for every pair row of both universe files, David's unit (3 T s with a gap, 3 T den at
    (den, den)) against leg_of's one arithmetic s + den (1 - min(s, 1)) and the residue form sine_den(num mod den, den); the bits.
 2. THE LAY'S SHARE: the share at the vacuum's weight of MS-S1's quarter-turn lay (re_now A, im_before B, A B = T div 2) at one Node
    of the 3-cube board at rest, for EVERY record alike: predicted 3 den (A^2 + B^2), the same integer on every row, the pair absent;
    the share of the rest record (A, A num div den, 0, A s div den) laid uniform: predicted 6 den A^2 s^2 div den^2 to the roundings
    (0 for the massless pair), the Wronskian A^2 s div den; so 3 T s is the share of the rest record carrying W = T div 2 and 3 T den
    the share of the quarter-turn record carrying W = T div 2, and no rest record of the massless pair carries any W.
 3. THE COUPLING c(pair) = min(den - num, 1) on both files, and the turn at c = 0 the identity: turn_pair(re, im, X, 0, X) and the odd
    triple at n = 0 return (re, im) bit for bit on 10,000 signed draws; the Links at c = 1 David's Link records bit for bit.
 4. THE EMITTER: the plane whose pair is the potential's is the plane at the gap 0 on both files (the same object); the emitter's im
    line 0 and its Wronskian and plane current 0 at every Node over 20 intervals of the 3-cube hole seed (so the sums over every plane
    equal the sums over the gapped planes by arithmetic), measured.
 5. THE ORDER: the tuple key (1, shape, 1 - c) sorts both files' rows into David's order_of's order (the same list).
 6. THE LITERALS: HALF_WIDTH = WIDTH div 2 with WIDTH 128 the law's; the amplitude X at the half width less one and its product with a
    level of the half width within 128 bits; TRACE = SIDES AXES^3 = 2 x 27 = 54.
Usage: one_node.py"""

from __future__ import annotations

import json
import os
import random
import sys

import numpy as np

sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "src"))

from event_universe.core.paces import odd_rounded, sine_den  # noqa: E402
from event_universe.core.rule3 import half, quotient, unit_of  # noqa: E402
from event_universe.links import Link, plane_current, turn_pair, wronskian  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.readings import frames  # noqa: E402
from event_universe.rows import HALF_WIDTH, PLANE, POTENTIAL, TRACE, order_of  # noqa: E402
from event_universe.core.ports import AXES  # noqa: E402

WIDTH = 128
SIDES = 2
failures = 0


def check(name: str, ok: bool, *numbers: object) -> None:
    global failures
    failures += 0 if ok else 1
    print(("PASS " if ok else "FAIL ") + name, *numbers)


def leg_of(num: int, den: int) -> int:
    s = sine_den(num, den)
    return s + den * (1 - min(s, 1))


def coupling(num: int, den: int) -> int:
    return min(den - num, 1)


# 1. the unit
for name in ("universe_toy.json", "universe_middle.json"):
    u = json.load(open(os.path.join(HERE, "worlds", name)))
    den, T = int(u["integers"]["den"]), int(u["integers"]["quantum_action"])
    for r in u["rows"]:
        if r.get("pair") is None:
            continue
        num = int(r["pair"][0])
        s = sine_den(num, den)
        david = unit_of(s if den - num else den, T)
        one = unit_of(leg_of(num, den), T)
        residue = unit_of(sine_den(num % den, den), T)
        check(
            f"unit {name} shape {r['shape']} num {num}: David {david} == leg_of {one} == residue {residue}; bits {david.bit_length()}; s {s}; c {coupling(num, den)}",
            david == one == residue,
        )
# the toy den 1,021 (the pair (779, 1021) and the massless pair)
for den, num in ((1021, 779), (1021, 1021)):
    s = sine_den(num, den)
    check(f"unit den 1021 num {num}: 3 T s = {unit_of(leg_of(num, den), 36000)} (s {s}, den {den})", unit_of(leg_of(num, den), 36000) == 3 * 36000 * (s if s else den))

# 2. the lay's share at one Node, every record alike
universe, world = load_world(os.path.join(HERE, "worlds", "world_node.json"))
node = Node(universe, dict(world, seed=[]))
den, T = node.den, node.T
A = max(d for d in range(1, half(T) + 1) if half(T) % d == 0 and d * d <= half(T))
B = half(T) // A
c0 = node.content()
factors = node.link_factors()
at = (1, 1, 1)
shares = []
for rec, row in enumerate(node.records()):
    re, im = row.lines
    re.now[at] += A
    im.before[at] += B
    rule = node.rule_of(row, c0, factors)
    sh = int((node.share(re, rule, vacuum=True) + node.share(im, rule, vacuum=True))[at])
    w = int(wronskian(re, im)[at])
    shares.append(sh)
    re.now[at] -= A
    im.before[at] -= B
    check(f"quarter-turn lay (A {A}, B {B}, A B {A * B} = T div 2 {half(T)}) on record {rec} pair num {row.pair[0]}: share {sh}, predicted 3 den (A^2 + B^2) = {3 * den * (A * A + B * B)}, W {w}, 3 den T = {3 * den * T}", sh == 3 * den * (A * A + B * B) and w == A * B)
check("the lay's share one integer on every record (the pair absent)", len(set(shares)) == 1, shares)
# the rest record laid uniform at amplitude A_r
A_r = 10**6  # large against den div s, so the roundings of A num div den and A s div den stay below one per mille of the share
for rec, row in enumerate(node.records()):
    num = row.pair[0]
    s = sine_den(num, den)
    re, im = row.lines
    re.now[:] = A_r
    re.before[:] = quotient(A_r * num, den)
    im.now[:] = 0
    im.before[:] = quotient(A_r * s, den)
    rule = node.rule_of(row, c0, factors)
    sh = int((node.share(re, rule, vacuum=True) + node.share(im, rule, vacuum=True))[at])
    w = int(wronskian(re, im)[at])
    a_, b_, d_ = A_r, quotient(A_r * num, den), quotient(A_r * s, den)
    predicted = 3 * den * (a_ * a_ + b_ * b_ + d_ * d_) - 6 * num * a_ * b_  # exact from the laid integers (S = 0 at the vacuum); 6 den A^2 sin^2 with b = A cos, d = A sin
    algebra = quotient(6 * den * A_r * A_r * s * s, den * den)
    re.now[:] = 0
    re.before[:] = 0
    im.before[:] = 0
    off = abs(sh - predicted)
    check(f"rest record A {A_r} on record {rec} (s {s}): share {sh} == 3 den (a^2 + b^2 + d^2) - 6 num a b = {predicted} exactly (b = A num div den, d = A s div den); the algebra's 6 den A^2 sin^2 = {algebra}, apart {abs(sh - algebra) * 1000000 // (algebra + 1)} per million by the two roundings; W {w} == a d = {a_ * d_}", off == 0 and w == a_ * d_)
# the unit as the share of the record carrying W = T div 2: at rest 6 den A^2 s^2/den^2 with A^2 s/den = T/2 -> 3 den T s/den = 3 T s; at the quarter turn 3 den (A^2 + B^2) with A B = T/2, A = B -> 3 den T
for rec, row in enumerate(node.records()):
    s = sine_den(row.pair[0], den)
    rest = quotient(3 * T * s, 1) if s else None
    check(f"record {rec}: the rest record at W = T div 2 has the share 3 T s = {rest} (none for s = 0: no rest record of the massless pair carries a W); the quarter-turn record at W = T div 2 has the share 3 den T = {3 * den * T} on every row; David's unit {node.units[rec]}", node.units[rec] == (3 * T * s if s else 3 * den * T))

# 3. the coupling and the identity turn at c = 0
for name in ("universe_toy.json", "universe_middle.json"):
    u = json.load(open(os.path.join(HERE, "worlds", name)))
    den_u = int(u["integers"]["den"])
    cs = [coupling(int(r["pair"][0]), den_u) for r in u["rows"] if r.get("pair") is not None]
    check(f"coupling c(pair) on {name}: {cs} (0 at the two (den, den) rows, 1 elsewhere)", cs.count(0) == 2 and set(cs) <= {0, 1})
rng = random.Random(24)
X = node.X
wl = 4 * node.gamma
bad = 0
for _ in range(10000):
    re_, im_ = rng.randint(-(2**60), 2**60), rng.randint(-(2**60), 2**60)
    a, b = turn_pair(re_, im_, X, 0, X)
    a2, b2 = turn_pair(a, b, wl * wl, 0, wl * wl)
    bad += (a2, b2) != (re_, im_)
check(f"the turn at the coupling 0 is the identity on 10000 signed draws to 2^60: {10000 - bad} of 10000 (X {X}, W {wl})", bad == 0)
# the Links at c: a Link record (f, cos, sin, n) -> (1 + c (f - 1), X + c (cos - X), c sin, c n)
for c in (0, 1):
    f, cosv, sinv, n = -1, 123456789, 987654321, 17
    got = (1 + c * (f - 1), X + c * (cosv - X), c * sinv, c * n)
    want = (f, cosv, sinv, n) if c else (1, X, 0, 0)
    check(f"the Link's record at c = {c}: {got} == {want}", got == want)

# 4. the emitter and its im line
for name in ("world_node.json", "world_bodies.json"):
    universe, world = load_world(os.path.join(HERE, "worlds", name))
    n2 = Node(universe, dict(world, intervals=20))
    potential = n2.row(POTENTIAL)
    emitter = next(r for r in n2.rows_ if r.shape == PLANE and r.pair == potential.pair)
    check(f"{name}: the plane of the potential's pair is the plane at the gap 0 (the same object), index {n2.records().index(emitter)} of {len(n2.records())}", emitter is n2.row(PLANE, gap=0))
    if name == "world_node.json":
        im_max = w_max = j_max = 0
        for _ in range(20):
            n2.step()
            re, im = emitter.lines
            im_max = max(im_max, max(abs(int(x)) for x in im.now.reshape(-1)), max(abs(int(x)) for x in im.before.reshape(-1)))
            w_max = max(w_max, max(abs(int(x)) for x in wronskian(re, im).reshape(-1)))
            fr = frames(n2, n2.walled().lines[0].rem)
            j_max = max(j_max, max(abs(int(x)) for j in plane_current(re, im, fr) for x in j.reshape(-1)))
        check(f"the emitter's im line, Wronskian and plane current over 20 intervals of the 3-cube hole seed: max |im| {im_max}, max |W| {w_max}, max |J| {j_max}; births {n2.counts['births']}, turns {n2.counts['turns']}", im_max == 0 and w_max == 0 and j_max == 0)

# 5. the order key
for name in ("universe_toy.json", "universe_middle.json"):
    universe, world = load_world(os.path.join(HERE, "worlds", "world_node.json" if name == "universe_toy.json" else "world_bodies.json"))
    n3 = Node(universe, world)
    david = [n3.by_index.index(r) for r in n3.rows_]
    tup = sorted(n3.by_index, key=lambda r: (0, 0, 0) if r.wall is not None else (1, r.shape, 1 - min(r.pair[1] - r.pair[0], 1)))
    mine = [n3.by_index.index(r) for r in tup]
    check(f"{name}: the tuple key's order {mine} == David's order_of {david}", mine == david)

# 6. the literals
check(f"HALF_WIDTH {HALF_WIDTH} == WIDTH div 2 = {WIDTH // 2}; the phase amplitude X {X} at {HALF_WIDTH - 1} bits has {X.bit_length()} bits; X times a level of {HALF_WIDTH - 1} bits has {(X * (2 ** (HALF_WIDTH - 1) - 1)).bit_length()} bits (within {WIDTH})", HALF_WIDTH == WIDTH // 2 and (X * (2 ** (HALF_WIDTH - 1) - 1)).bit_length() <= WIDTH)
check(f"TRACE {TRACE} == SIDES x AXES^3 = {SIDES * AXES**3} (2 x 27: the doubled wall's 2, W_c's 3, the trace over 3, the traceless part's 3)", TRACE == SIDES * AXES**3)
print("failures", failures)
sys.exit(1 if failures else 0)
