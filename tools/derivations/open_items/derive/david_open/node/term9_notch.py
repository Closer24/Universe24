"""Term 9, the volume's notch: a spring on the metric family's scalar slots, and what it does on the act.

Whole numbers alone, on the act (engine/step.py, mesh.py and contract.py at main 0df0e8385), the reads laid by hand as
in g2_static.py: the rows matter, light and the metric family in the square's basis (00; 0x 0y 0z; xx yy zz; yz zx xy).
Every row but the 00 row reads its teeth from the 00 slot (W = rest + c00, term 2); the 00 row stands at the rest
teeth, so no row's teeth read its own count. Every Spoke's grip reads its axis's ii slot at both ends (term 3). The
board: 4 by 4 by 4, wrapped on every axis. The notch is laid as plan monomials (the vertex law, contract.pushes):
f9 c00 c00 on the 00 slot, and (f9 / 2) on the ii trace squared, so each Node-clock's 00 slot stands on a spring 2 f9
of its own and the trace of its ii slots on 3 f9 per slot; the E part (xx - yy, yy - zz) and the T2 part (yz, zx, xy)
get none.

(a) a source pinned at one Node-clock (matter held still there, pushing its 00 slot by J times its count each round),
    no notch: the 00 slot's sum over the board and its least at rounds 500, 1,000, 2,000 and 4,000: the board's mean
    runs off;
(b) the same with the notch: the 00 slot's sum swings about J's total over 2 f9 times the Node-clocks and returns: its
    largest and least over 4,000 rounds, its sign changes about that rest against 4,000 omega / pi from
    4 sin^2 (omega / 2) = 2 f9 / W (computed in whole numbers);
(c) which slots the notch holds: each of the 00 slot, the ii trace, the E part and the T2 part laid uniform at 10^9
    on the whole board, no source, sign changes over 4,000 rounds: the 00 slot swings at the notch's beat and the
    trace at root(3 / 2) of it; the E and T2 parts, with no notch and no gradient, stand still (no rest beat);
(d) the run back with the notch and the source: 2,000 rounds out and 2,000 unticks back, bit for bit.

Usage: python3 -I term9_notch.py <src of main at 0df0e8385>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

GRIP = 15162856759112389 * 1000 * 1000
REST = 6 * GRIP
matter_row, light_row, slot00, slot_xx, slot_yz = 0, 1, 2, 6, 9
ROWS = 12
UNIT = 5 * ROWS  # the readings' unit row: the value rows, three gradients, the force, then the unit
F9 = carry(REST, 16200, 0)[0]  # the notch's monomial factor: the spring 2 f9 = W div 8100, a beat of about 400 rounds
J = 3

nb = board((4, 4, 4))
sites = nb.shape[1]
spokes, meshes = geometry(nb, 3)
grips = np.full((ROWS, 3 * sites), GRIP, dtype=object)
grips[matter_row, :] = 0  # matter held still: no grip
clock = Read(np.full(ROWS - 1, slot00, dtype=np.intp), np.ones(ROWS - 1, dtype=object),
             np.array([r for r in range(ROWS) if r != slot00], dtype=np.intp))
stretch = Read(np.array([slot_xx, slot_xx, slot_xx + 1, slot_xx + 1, slot_xx + 2, slot_xx + 2], dtype=np.intp),
               np.ones(6, dtype=object), np.arange(6, dtype=np.intp))
gearing = Gearing(REST * np.ones((ROWS, 1), dtype=object), *(np.ones((ROWS, 1), dtype=object),) * 3)


def plan_of(source, notch):
    parts = []
    if source:
        parts.append(Plan(np.array([matter_row], dtype=np.intp), np.array([UNIT], dtype=np.intp),
                          np.array([UNIT], dtype=np.intp), np.array([J], dtype=object), np.array([slot00], dtype=np.intp)))
    if notch:
        factors, legs = [F9], [(slot00, slot00)]
        half, _ = carry(F9, 2, 0)
        for i in range(3):
            factors.append(half)
            legs.append((slot_xx + i, slot_xx + i))
            for j in range(i + 1, 3):
                factors.append(F9)
                legs.append((slot_xx + i, slot_xx + j))
        parts.append(pushes(np.array(factors, dtype=object),
                            tuple(np.array(x, dtype=np.intp) for x in (
                                [a for a, _ in legs], [b for _, b in legs], [-1] * len(legs), [-1] * len(legs)))))
    if not parts:
        return Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
    return Plan(*(np.concatenate([p[k] for p in parts]) for k in range(5)))


def layout(source, notch):
    return Layout(nb, spokes, meshes, grips, gearing, plan_of(source, notch), clock, stretch)


def laid(rows):
    a = np.zeros((ROWS, sites), dtype=object)
    for row, value in rows.items():
        a[row, :] = value
    return State(a, a.copy(), np.full((ROWS, sites), carry(REST, 2, 0)[0], dtype=object),
                 np.zeros((ROWS, sites), dtype=object))


def pinned():
    s = laid({})
    s.a[matter_row, 0] = 10**22
    s.b[matter_row, 0] = 10**22
    return s


SCALE = 10**40


def arctan_inverse(m):
    total, power, j, sign = 0, carry(SCALE, m, 0)[0], 0, 1
    while power:
        total += sign * carry(power, 2 * j + 1, 0)[0]
        power = carry(power, m * m, 0)[0]
        j, sign = j + 1, -sign
    return total


PI = 16 * arctan_inverse(5) - 4 * arctan_inverse(239)


def sine(x):
    total, term, j, sign = 0, x, 0, 1
    while term:
        total += sign * term
        j, sign = j + 1, -sign
        term = carry(carry(term * x, SCALE, 0)[0] * x, SCALE * (2 * j) * (2 * j + 1), 0)[0]
    return total


def beats_expected(spring, teeth, rounds=4000):
    lo, hi = 0, 100 * rounds
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        s_mid = sine(carry(PI * mid, 200 * rounds, 0)[0])
        if 4 * teeth * s_mid * s_mid <= spring * SCALE * SCALE:
            lo = mid
        else:
            hi = mid
    whole, tenth = carry(carry(lo + 5, 10, 0)[0], 10, 0)
    return f"{whole}.{tenth}"


def sum00(s):
    return sum(int(x) for x in s.a[slot00])


# (a) and (b)
for notch in (False, True):
    lay = layout(True, notch)
    s = pinned()
    rest_sum = carry(J * 10**22, 2 * F9, 0)[0]  # where the notch's pull on the sum balances the source's push
    marks, most, least, changes, last = [], None, None, 0, -rest_sum
    for t in range(1, 4001):
        s = step.tick(lay, s)
        total = sum00(s)
        most = total if most is None else max(most, total)
        least = total if least is None else min(least, total)
        now = total - rest_sum
        changes += int(now * last < 0)
        last = now if now else last
        if t in (500, 1000, 2000, 4000):
            marks.append(f"round {t}: the sum {total}, its least {min(int(x) for x in s.a[slot00])}")
    if not notch:
        print(f"(a) a source J = {J} x 10^22 pinned at one Node-clock of {sites}, no notch: " + "; ".join(marks))
    else:
        print(f"(b) the same with the notch, 2 f9 = {2 * F9} (W div {carry(REST, 2 * F9, 0)[0]}): the sum over 4,000 rounds"
              f" from {least} to {most}, about the rest {rest_sum}; sign changes about it {changes}, against"
              f" {beats_expected(2 * F9, REST)} from the notch's beat")

# (c) which slots the notch holds
lay = layout(False, True)
rows_c = (("the 00 slot", {slot00: 10**9}), ("the ii trace", {slot_xx: 10**9, slot_xx + 1: 10**9, slot_xx + 2: 10**9}),
          ("the E part, xx - yy", {slot_xx: 10**9, slot_xx + 1: -(10**9)}), ("the T2 part, yz", {slot_yz: 10**9}))
out = []
for name, rows in rows_c:
    s = laid(rows)
    row = next(iter(rows))
    changes, last, moved = 0, int(s.a[row, 0]), False
    for _ in range(4000):
        s = step.tick(lay, s)
        now = int(s.a[row, 0])
        moved = moved or now != 10**9 * (1 if rows[row] > 0 else -1)
        changes += int(now * last < 0)
        last = now if now else last
    out.append(f"{name}: {changes} sign changes, moved {moved}")
print(f"(c) laid uniform at 10^9, no source, 4,000 rounds (the notch's beat gives {beats_expected(2 * F9, REST)} at the"
      f" rest teeth): " + "; ".join(out))

# (d) the run back
lay = layout(True, True)
s0 = pinned()
s = s0
for _ in range(2000):
    s = step.tick(lay, s)
for _ in range(2000):
    s = step.untick(lay, s)
home = all(np.array_equal(x, y) for x, y in zip(s, s0, strict=True))
print(f"(d) 2,000 rounds out and 2,000 back with the notch and the source: the lay returns bit for bit: {home}")
