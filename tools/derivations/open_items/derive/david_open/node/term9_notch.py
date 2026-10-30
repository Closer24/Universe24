"""Term 9, the volume's notch: a spring on the metric family's scalar slots, and what it does on the act.

Whole numbers alone, on the act (engine/step.py, mesh.py and contract.py at main 0df0e8385), the reads laid by hand as
in g2_static.py: the rows matter, light and the metric family in the square's basis (00; 0x 0y 0z; xx yy zz; yz zx xy).
Every row but the 00 row reads its teeth from the 00 slot (W = rest + c00, term 2); the 00 row stands at the rest
teeth, so no row's teeth read its own count. Every Spoke's grip reads its axis's ii slot at both ends (term 3). The
board: 4 by 4 by 4, wrapped on every axis. The notch is laid as plan monomials (the vertex law, contract.pushes):
f9 c00 c00 on the 00 slot, and (f9 / 3) on the ii trace squared, so each Node-clock's 00 slot stands on a spring 2 f9
of its own and the trace of its ii slots on 2 f9 per slot as well, one range for both (the first text's (f9 / 2) gave
the trace 3 f9, a range whose square is 2/3 of the 00 slot's); the E part (xx - yy, yy - zz) and the T2 part (yz, zx,
xy) get none.

(a) a source pinned at one Node-clock (matter held still there, pushing its 00 slot by J times its count each round),
    no notch: the 00 slot's sum over the board and its least at rounds 500, 1,000, 2,000 and 4,000: the board's mean
    runs off;
(b) the same with the notch: the 00 slot's sum swings about J's total over 2 f9 and returns: its largest and least
    over 4,000 rounds, its sign changes about that rest against 4,000 omega / pi from 4 sin^2 (omega / 2) = 2 f9 / W
    (computed in whole numbers), a period near 565 rounds;
(c) which slots the notch holds: each of the 00 slot, the ii trace, the E part and the T2 part laid uniform at 10^9
    on the whole board, no source, sign changes over 4,000 rounds: the 00 slot and the trace swing at the notch's one
    beat; the E and T2 parts, with no notch and no gradient, stand still (no rest beat);
(d) the run back with the notch and the source: 2,000 rounds out and 2,000 unticks back, bit for bit, on this lay,
    where the 00 slot stands at rest and so every clock that reads it stands still;
(d2) the run back where the teeth move: the 00 slot laid at REST div 3 with the source, the xx slot at 10^9, under the
    loader's reads (every row reads the 00 slot, the 00 row its own) and under this probe's, with and without the
    notch: the first round where untick(tick(s)) is not s;
(d3) (d2)'s moving lay on the first-order form (N2's second text, the Boss's branch boss-derive b271ddfb8): each gear
    carries its rate p = W (a - b) + r whole, the tick p+ = p + push and a+ = a + p+ div W, the mirror the drift undone
    and an even row's rate flipped in the now slot's teeth; 2,000 rounds out and back, on this probe's reads and on the
    loader's, with how many site-rounds light's teeth rose and fell;
(b2) a source on the ii slots too, at G2's ratio (the 00 push 12, each ii push -1, per 10^22 of matter): the xx slot's
    sum over the board at rounds 1,000, 2,000 and 4,000, with and without the notch, and with it the sum's range and
    sign changes about its rest -J_xx over 2 f9;
(b3) a source large against Rule3's floor, 3 x 10^30: the sum's range over 4,000 rounds against the equation's swing,
    from 0 to J_total over f9;
(e) the waves at the wave number 2 pi over 64, on a ring of 64 along x: light, the E part, the T2 part, the 00 slot
    and the ii trace, each laid alone on cos(2 pi x over 64) at 10^9, the notch on: sign changes at x = 0 over 4,000
    rounds against 4 sin^2 (omega / 2) = (grip 4 sin^2 (k / 2) + spring) / W, the spring 0 or the notch's 2 f9.

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
F9 = 6 * carry(REST, 97200, 0)[0]  # the notch's monomial factor, a multiple of 6: the spring 2 f9 near W div 8100,
# a period of about 565 rounds
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
                          np.array([UNIT], dtype=np.intp), np.array([J], dtype=object),
                          np.array([slot00], dtype=np.intp)))
    if notch:
        factors, legs = [F9], [(slot00, slot00)]
        third, _ = carry(F9, 3, 0)  # (f9 / 3) tr^2: f9 / 3 on each c_ii c_ii, 2 f9 / 3 on each c_ii c_jj, i < j
        for i in range(3):
            factors.append(third)
            legs.append((slot_xx + i, slot_xx + i))
            for j in range(i + 1, 3):
                factors.append(2 * third)
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


def signed_sine(x):
    """The sine at any sign of x: the series floors each term, so it is summed at |x| and the sign put back."""
    return -sine(-x) if x < 0 else sine(x)


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
        print(f"(b) the same with the notch, 2 f9 = {2 * F9} (W div {carry(REST, 2 * F9, 0)[0]}): the sum over 4,000"
              " rounds"
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

# (d2) the run back where the teeth move: the loader's reads (every row, the 00 row included, reads the 00 slot) and
# the probe's reads, the 00 slot laid at REST div 3 with the source and the notch: the first round t where
# untick(tick(s_t)) is not s_t
clock_all = Read(np.full(ROWS, slot00, dtype=np.intp), np.ones(ROWS, dtype=object), np.arange(ROWS, dtype=np.intp))


def first_miss(lay_out, s, rounds=2000):
    for t in range(rounds):
        s_next = step.tick(lay_out, s)
        back = step.untick(lay_out, s_next)
        if not all(np.array_equal(x, y) for x, y in zip(back, s, strict=True)):
            return t
        s = s_next
    return None


lines_d2 = []
for name, read in (("the loader's reads, the 00 row reading its own slot", clock_all), ("this probe's reads", clock)):
    for notch in (False, True):
        lay_out = Layout(nb, spokes, meshes, grips, gearing, plan_of(True, notch), read, stretch)
        s = pinned()
        s.a[slot00, :] = carry(REST, 3, 0)[0]
        s.b[slot00, :] = carry(REST, 3, 0)[0]
        s.a[slot_xx, :] = 10**9  # the trace moving, as the mathematician's R2 lays it
        miss = first_miss(lay_out, s)
        lines_d2.append(f"{name}, {'with' if notch else 'without'} the notch: "
                        + (f"the run back misses from round {miss}" if miss is not None
                           else "the run back holds every round of 2,000"))
print("(d2) the 00 slot laid at REST div 3, the source pinned, the xx slot at 10^9, round by round: "
      + "; ".join(lines_d2))

# (d3) the same moving lay on the first-order form (N2's second text, boss-derive b271ddfb8, n2b_lib.py): each gear
# carries its rate p = W (a - b) + r whole; the tick p+ = p + push, a+ = a + p+ div W at the now slot's teeth; the
# mirror R undoes the drift (the rows that read no row first) and flips an even row's rate in the now slot's teeth,
# an odd row's count negated; the run back is R, the tick, R
EVEN = np.array([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1], dtype=object).reshape(-1, 1)  # the 0i slots are odd


def tick_first(lay_out, s):
    a, p, z, rd = s
    w = step.weight(lay_out.gearing, lay_out.clock, a)
    force, j = step.sources(lay_out, a)
    qd, rd1 = step.drive(j, lay_out.gearing.drive, rd)
    p1 = p + step.driven(lay_out.gearing, force, qd)
    return State(a + carry(p1, w, 0)[0], p1, z, rd1)


def mirror_first(lay_out, s):
    a1, p, z, rd = s
    a = a1
    for _ in range(2):  # the drift undone in two carries: the 00 row reads no row, every other row reads the 00 row
        a = a1 - carry(p, step.weight(lay_out.gearing, lay_out.clock, a), 0)[0]
    w = step.weight(lay_out.gearing, lay_out.clock, a)
    tau = EVEN + EVEN - 1
    return State(tau * a, p + EVEN * (w - 1 - p - p), z, rd + EVEN * (lay_out.gearing.drive - 1 - rd - rd))


def back_first(lay_out, s, rounds=2000):
    """The first round back that departs on the first-order form, or None; and how many site-rounds the light row's
    teeth rose and fell on the way out."""
    states, rose, fell = [s], 0, 0
    for _ in range(rounds):
        w0 = step.weight(lay_out.gearing, lay_out.clock, states[-1].a)[light_row]
        states.append(tick_first(lay_out, states[-1]))
        w1 = step.weight(lay_out.gearing, lay_out.clock, states[-1].a)[light_row]
        rose += sum(int(x > y) for x, y in zip(w1, w0, strict=True))
        fell += sum(int(x < y) for x, y in zip(w1, w0, strict=True))
    t = states[-1]
    for k in range(rounds):
        t = mirror_first(lay_out, tick_first(lay_out, mirror_first(lay_out, t)))
        if not all(np.array_equal(x, y) for x, y in zip(t, states[rounds - 1 - k], strict=True)):
            return k + 1, rose, fell
    return None, rose, fell


lines_d3 = []
for name, read in (("this probe's reads, no row reading its own count", clock),
                   ("the loader's reads, the 00 row reading its own slot", clock_all)):
    lay_out = Layout(nb, spokes, meshes, grips, gearing, plan_of(True, True), read, stretch)
    s = pinned()
    s.a[slot00, :] = carry(REST, 3, 0)[0]
    s.b[slot00, :] = carry(REST, 3, 0)[0]
    s.a[slot_xx, :] = 10**9
    w = step.weight(lay_out.gearing, lay_out.clock, s.a)
    s = State(s.a, w * (s.a - s.b) + s.r, s.r, s.rd)  # p = W (a - b) + r
    miss, rose, fell = back_first(lay_out, s)
    lines_d3.append(f"{name}: " + (f"the run back departs at round back {miss}" if miss is not None
                                   else "the run back holds every round of 2,000")
                    + f" (light's teeth rose at {rose} and fell at {fell} site-rounds on the way out)")
print("(d3) (d2)'s moving lay on the first-order form, the notch and the source on: " + "; ".join(lines_d3))

# (b2) a source on the ii slots too, at G2's ratio -1 / 12 of its 00 push (the 00 push 12, each ii push -1, times the
# matter count 10^22): the xx slot's sum over the board and the x grip next to the source, with and without the notch
src_ii = Plan(np.array([matter_row] * 4, dtype=np.intp), np.array([UNIT] * 4, dtype=np.intp),
              np.array([UNIT] * 4, dtype=np.intp), np.array([12, -1, -1, -1], dtype=object),
              np.array([slot00, slot_xx, slot_xx + 1, slot_xx + 2], dtype=np.intp))
lines_b2 = []
for notch in (False, True):
    parts = [src_ii] + ([plan_of(False, True)] if notch else [])
    plan = Plan(*(np.concatenate([p[k] for p in parts]) for k in range(5)))
    lay_out = Layout(nb, spokes, meshes, grips, gearing, plan, clock, stretch)
    s = pinned()
    marks, least, most, changes, last = [], None, None, 0, None
    rest_xx = -carry(10**22, 2 * F9, 0)[0]  # the xx sum's rest: -J_xx / (2 f9), the trace's spring 2 f9 a slot
    for t in range(1, 4001):
        s = step.tick(lay_out, s)
        total = sum(int(x) for x in s.a[slot_xx])
        least = total if least is None else min(least, total)
        most = total if most is None else max(most, total)
        now = total - rest_xx
        if last is not None:
            changes += int(now * last < 0)
        last = now if now else last
        if t in (1000, 2000, 4000):
            marks.append(f"round {t}: {total}")
    lines_b2.append(f"{'with' if notch else 'without'} the notch: the xx sum " + ", ".join(marks)
                    + (f"; from {least} to {most} about its rest {rest_xx}, {changes} sign changes about it"
                       if notch else ""))
print("(b2) the source pushing the 00 slot by 12 and each ii slot by -1 per 10^22 of matter: " + "; ".join(lines_b2))

# (b3) a source large against Rule3's floor: matter 10^30 at J = 3; the sum against the equation's swing, 0 to
# J_total / f9
lay_out = layout(True, True)
s = laid({})
s.a[matter_row, 0] = 10**30
s.b[matter_row, 0] = 10**30
least, most = None, None
for t in range(1, 4001):
    s = step.tick(lay_out, s)
    total = sum00(s)
    least = total if least is None else min(least, total)
    most = total if most is None else max(most, total)
print(f"(b3) a source of 3 x 10^30, 4,000 rounds: the sum from {least} to {most}, against the equation's swing from 0"
      f" to J_total / f9 = {carry(3 * 10**30, F9, 0)[0]}")

# (e) the waves at a wave number k = 2 pi / 64, on a ring of 64 on the x axis: each slot laid alone on the mode
# cos(2 pi x / 64) at 10^9, sign changes at x = 0 over 4,000 rounds, against 4 sin^2 (omega / 2) =
# (grip 4 sin^2 (k / 2) + spring) / W, the spring 0 or the notch's 2 f9
nb64 = board((64, 1, 1))
sites64 = nb64.shape[1]
spokes64, meshes64 = geometry(nb64, 3)
grips64 = np.full((ROWS, 3 * sites64), GRIP, dtype=object)
grips64[matter_row, :] = 0
cosines = [signed_sine(carry(PI, 2, 0)[0] - carry(2 * PI * x, 64, 0)[0]) for x in range(64)]  # cos(2 pi x / 64)
mode = [carry(10**9 * c, SCALE, 0)[0] for c in cosines]
half_k = sine(carry(PI, 64, 0)[0])  # sin(k / 2), SCALE
grip_k = carry(4 * GRIP * half_k * half_k, SCALE * SCALE, 0)[0]  # grip 4 sin^2 (k / 2), whole
lay64 = Layout(nb64, spokes64, meshes64, grips64, gearing, plan_of(False, True), clock, stretch)
rows_e = (("light", {light_row: 1}, 0), ("the E part, yy - zz", {slot_xx + 1: 1, slot_xx + 2: -1}, 0),
          ("the T2 part, yz", {slot_yz: 1}, 0), ("the 00 slot", {slot00: 1}, 2 * F9),
          ("the ii trace", {slot_xx: 1, slot_xx + 1: 1, slot_xx + 2: 1}, 2 * F9))
lines_e = []
for name, rows, spring in rows_e:
    a = np.zeros((ROWS, sites64), dtype=object)
    for row, sign in rows.items():
        a[row, :] = [sign * v for v in mode]
    s = State(a, a.copy(), np.full((ROWS, sites64), carry(REST, 2, 0)[0], dtype=object),
              np.zeros((ROWS, sites64), dtype=object))
    row = next(iter(rows))
    changes, last = 0, int(s.a[row, 0])
    for _ in range(4000):
        s = step.tick(lay64, s)
        now = int(s.a[row, 0])
        changes += int(now * last < 0)
        last = now if now else last
    lines_e.append(f"{name}: {changes} (expected {beats_expected(grip_k + spring, REST)})")
print("(e) at k = 2 pi / 64 on a ring of 64, each slot laid alone on cos(2 pi x / 64) at 10^9, the notch on, sign"
      " changes at x = 0 in 4,000 rounds: " + "; ".join(lines_e))
