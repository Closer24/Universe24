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
    over 4,000 rounds, its sign changes about that rest against the count of the sum's own linear recurrence on the
    spring 2 f9 at the teeth W (the expected counts, below), a period near 565 rounds;
(c) which slots the notch holds: each of the 00 slot, the ii trace, the E part and the T2 part laid uniform at 10^9
    on the whole board, no source, sign changes over 4,000 rounds: the 00 slot and the trace swing at the notch's one
    beat; the E and T2 parts, with no notch and no gradient, stand still (no rest beat);
(d) the run back with the notch and the source: 2,000 rounds out and 2,000 unticks back, bit for bit, on this lay,
    where the moving 00 row's teeth read no row and every row that reads the 00 slot stands still, while the 00 slot
    itself swings (the same lay as (b));
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
(e) the waves of period 64 on a ring of 64 along x: light, the E part, the T2 part, the 00 slot and the ii trace, each
    laid alone on the triangle wave 10^9 (32 - 2 min(x, 64 - x)), whole at every site and largest at x = 0, the notch
    on: sign changes at x = 0 over 4,000 rounds against the count of the same lay's exact linear run on the whole ring,
    in the same rounds and in tenths over ten times the rounds;
(f) the order and the reach on this notch (the fifth text): the three ii slots laid uniform at rest at c0, no source;
    over the expanding half (the grip falling) the sign of G2's scale factor's second difference, A ~ grip^(-1/2), read
    exactly by squares with no root, and the grips' largest over their least, the reach's stated whole part tested by
    squares; at c0 = 10^9, 9/10, 999975/10^6 and 999999/10^6 of GRIP / 2.

The expected counts of (b), (c) and (e) are no closed form and no search: each runs an exact linear recurrence from its
section's own lay at rest (x- = x) taken 10^40 times larger, each division by Rule3's carry with its fine tooth kept,
and counts its sign changes over ten times the act's rounds, the count in tenths by one more carry. (b) and (c) lay one
mode each and run x+ = 2 x - x- - s x div W, s the notch's 2 f9. (e)'s triangle is no one mode (its odd harmonics fall
about as 1 over n^2), so (e) runs every site of the ring at once, each with its own fine tooth, x+ = 2 x - x- - (s x -
F x) div W: F is the act's own pull on the slot's row (mesh.pull on the ring's layout) with the grips' read left out,
which lands 0 at rest and so enters the pull at second order only; on this board F x is the slot's grip times x's two
neighbours along x less twice x, the y and z Spokes reaching the site itself; s is the spring, 0 or the notch's 2 f9;
W is REST, the teeth of every slot (e) counts, the 00 slot at 0 in every lay but its own and the 00 row reading no row.
No circular function enters the file, in a lay or in a count (law line 102, on scribe-5).

Usage: python3 -I term9_notch.py <src of main at 0df0e8385>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.mesh import pull  # noqa: E402
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


SCALE = 10**40  # the expected counts' recurrences run at SCALE times the act's lay


def beats_expected(spring, teeth, lay, rounds=4000):
    """The sign changes of one mode's exact linear recurrence, x+ = 2 x - x- - spring x div teeth, from the act's lay at
    rest (x = x- = lay) taken SCALE times larger, each division by Rule3's carry with its fine tooth kept, counted over
    ten times the rounds and read in tenths of the rounds' count by one more carry: no closed form and no search."""
    x, before, kept, changes = lay * SCALE, lay * SCALE, 0, 0
    last = x
    for _ in range(10 * rounds):
        fall, kept = carry(spring * x, teeth, kept)
        x, before = 2 * x - before - fall, x
        changes += int(x * last < 0)
        last = x if x else last
    whole, tenth = carry(changes, 10, 0)
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
        beat_b = beats_expected(2 * F9, REST, -rest_sum)  # the board's sum laid at 0, rest_sum below its rest
        print(f"(b) the same with the notch, 2 f9 = {2 * F9} (W div {carry(REST, 2 * F9, 0)[0]}): the sum over 4,000"
              " rounds"
              f" from {least} to {most}, about the rest {rest_sum}; sign changes about it {changes}, against"
              f" {beat_b} from the notch's beat")

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
beat_c = beats_expected(2 * F9, REST, 10**9)  # the uniform mode on the notch's spring, from (c)'s own lay at 10^9
print(f"(c) laid uniform at 10^9, no source, 4,000 rounds (the notch's beat gives {beat_c} at the"
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

# (e) the waves of period 64 on a ring of 64 on the x axis: each slot laid alone on the triangle wave
# 10^9 (32 - 2 min(x, 64 - x)), whole at every site and largest at x = 0, sign changes at x = 0 over 4,000 rounds,
# against the same lay's exact linear run on the whole ring (ring_beats_expected), the spring 0 or the notch's 2 f9
nb64 = board((64, 1, 1))
sites64 = nb64.shape[1]
spokes64, meshes64 = geometry(nb64, 3)
grips64 = np.full((ROWS, 3 * sites64), GRIP, dtype=object)
grips64[matter_row, :] = 0
triangle = [10**9 * (32 - 2 * min(x, 64 - x)) for x in range(64)]  # the ring's site x is its index x
no_read = Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))  # lands 0


def ring_beats_expected(row, spring, lay, rounds=4000):
    """The sign changes at x = 0 of the lay's exact linear run on the whole ring: at every site x+ = 2 x - x- -
    (spring x - F x) div REST, F the act's own pull on the slot's row (mesh.pull) with the grips' read left out, which
    lands 0 at rest and so enters the pull at second order only. From the lay at rest (x- = x) taken SCALE times
    larger, each division by Rule3's carry with each site's fine tooth kept; counted over the rounds, and over ten
    times the rounds read in tenths by one more carry, as beats_expected reads its own."""
    linear = Layout(nb64, spokes64, meshes64, grips64[[row]], gearing, plan_of(False, False), clock, no_read)
    x = np.array([v * SCALE for v in lay], dtype=object)
    before, kept, changes, last, in_rounds = x.copy(), np.zeros(sites64, dtype=object), 0, int(x[0]), None
    for t in range(1, 10 * rounds + 1):
        fall, kept = carry(spring * x - pull(linear, x[None, :])[0], REST, kept)
        x, before = 2 * x - before - fall, x
        now = int(x[0])
        changes += int(now * last < 0)
        last = now if now else last
        if t == rounds:
            in_rounds = changes
    whole, tenth = carry(changes, 10, 0)
    return f"{in_rounds}, {whole}.{tenth}"


lay64 = Layout(nb64, spokes64, meshes64, grips64, gearing, plan_of(False, True), clock, stretch)
rows_e = (("light", {light_row: 1}, 0), ("the E part, yy - zz", {slot_xx + 1: 1, slot_xx + 2: -1}, 0),
          ("the T2 part, yz", {slot_yz: 1}, 0), ("the 00 slot", {slot00: 1}, 2 * F9),
          ("the ii trace", {slot_xx: 1, slot_xx + 1: 1, slot_xx + 2: 1}, 2 * F9))
lines_e = []
for name, rows, spring in rows_e:
    a = np.zeros((ROWS, sites64), dtype=object)
    for row, sign in rows.items():
        a[row, :] = [sign * v for v in triangle]
    s = State(a, a.copy(), np.full((ROWS, sites64), carry(REST, 2, 0)[0], dtype=object),
              np.zeros((ROWS, sites64), dtype=object))
    row = next(iter(rows))
    expected = ring_beats_expected(row, spring, a[row])  # the counted slot's own lay; in the linear run the trace's
    # three slots move as one, each on 2 f9, and the E part's trace stays 0, so it meets no spring
    changes, last = 0, int(s.a[row, 0])
    for _ in range(4000):
        s = step.tick(lay64, s)
        now = int(s.a[row, 0])
        changes += int(now * last < 0)
        last = now if now else last
    lines_e.append(f"{name}: {changes} (expected {expected})")
print("(e) on a ring of 64 along x, each slot laid alone on the triangle wave 10^9 (32 - 2 min(x, 64 - x)), the notch"
      " on, sign changes at x = 0 in 4,000 rounds, against the same lay's exact linear run on the ring at 10^40 times"
      " its size (its count in the same rounds, then in tenths over 40,000): " + "; ".join(lines_e))


# (f) the order and the reach on this page's notch: the three ii slots laid uniform and at rest at c0, so the grip
# GRIP + 2 c (both ends of each Mesh) starts at its largest and G2's scale factor A ~ grip^(-1/2) at its least; over the
# expanding half (the grip falling) the sign of A's second difference A+ - 2 A + A- read exactly with no root: for
# x = grip+, y = grip-, z = grip its sign is that of 2 z (x y)^(1/2) - (4 x y - z (x + y)): + where 4 x y - z (x + y)
# is below 0, else the sign of 4 z^2 x y - (4 x y - z (x + y))^2; the reach, A's largest over its least, is the grips'
# ratio's square root, its stated whole part tested by squares
def a_second(x, y, z):
    lhs = 4 * x * y - z * (x + y)
    if lhs < 0:
        return 1
    d = 4 * z * z * x * y - lhs * lhs
    return int(d > 0) - int(d < 0)


def expanding_half(c0, rounds=2000):
    s = laid({slot_xx: c0, slot_xx + 1: c0, slot_xx + 2: c0})
    grip = [GRIP + 2 * c0]
    for t in range(1, rounds + 1):
        s = step.tick(lay_f, s)
        g = GRIP + int(s.a[slot_xx, 0]) + int(s.a[slot_xx, nb[0, 0]])
        if g <= 0:
            return None, None, None, grip, t
        if g >= grip[-1] and t > 1:
            break
        grip.append(g)
    signs = [a_second(grip[t + 1], grip[t - 1], grip[t]) for t in range(1, len(grip) - 1)]
    return len(grip) - 1, signs.count(1), signs.count(-1), grip, None


lay_f = layout(False, True)
lines_f = []
for label, c0, bracket in (("the probe's own lay, c0 = 10^9", 10**9, None),
                           ("c0 = 9/10 of GRIP / 2", carry(9 * GRIP, 20, 0)[0], None),
                           ("c0 = 999975/10^6 of GRIP / 2", carry(999975 * GRIP, 2 * 10**6, 0)[0], 389),
                           ("c0 = 999999/10^6 of GRIP / 2", carry(999999 * GRIP, 2 * 10**6, 0)[0], None)):
    falling, plus, minus, grip, zero_at = expanding_half(c0)
    if zero_at is not None:
        lines_f.append(f"{label}: the grips pass 0 at round {zero_at}")
        continue
    most, least = max(grip), min(grip)
    ratio_whole, ratio_rest = carry(10 * most, least, 0)
    text = (f"{label}: {falling} rounds falling; A's second difference + for {plus} rounds, - for {minus}; the grips'"
            f" largest over least {carry(ratio_whole, 10, 0)[0]}.{carry(ratio_whole, 10, 0)[1]}")
    if bracket is not None:
        text += (f"; {bracket}^2 <= that ratio < {bracket + 1}^2: "
                 f"{bracket * bracket * least <= most < (bracket + 1) * (bracket + 1) * least}")
    lines_f.append(text)
print(f"(f) the order and the reach on this notch, (f9 / 3) tr^2 (the trace's spring 2 f9 = W div"
      f" {carry(REST, 2 * F9, 0)[0]}), the three ii slots laid uniform at rest, no source: " + "; ".join(lines_f))
