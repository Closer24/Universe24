"""Two small checks: the 00 slot's own wave against light's in a well (P5 measured at rest only), and the drive's
quotient under the flipped tooth (the proof sketch's step 3). Whole numbers only.

Clock: the clock-rate wave's speed where the clock is deep; the drive run back.
Algebra: the engine's act; Rule3's carry.
Board: a ring of 6.
Clicks: n/a.

Run: <t24b>/.venv/bin/python -I probe_small.py; the output is probe_small.txt.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "g2" / "n2_second"))

import numpy as np  # noqa: E402
from n2b_lib import A1ROWS, ROWS, S00, T1ROWS, State, carry, engine_plan, layout, spring, step, table, terms  # noqa: E402

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line, flush=True)
    OUT.append(line)


REST, GRIP, G = 3000, 500, 210
LIGHT = T1ROWS[0]
SPRING = terms(spring(G, [(A1ROWS, table("A1"))]))


def mode6(n, amplitude):
    seq = [2 * amplitude, amplitude]
    while len(seq) < n:
        seq.append(seq[-1] - seq[-2])
    return np.array(seq[:n], dtype=object)


def crossings_about(L_, s_, row, site, centre, wanted):
    """Rounds for a[row, site] - centre to change sign `wanted` times."""
    rounds, count, sign = 0, 0, None
    while count < wanted:
        s_ = step.tick(L_, s_)
        rounds += 1
        v = int(s_.a[row, site]) - centre
        if v != 0:
            new = 1 if v > 0 else -1
            if sign is not None and new != sign:
                count += 1
            sign = new
        if rounds > 100000:
            return None
    return rounds


say("== 1. the 00 slot's own standing wave against light's, at rest and in a well (the 00 row's teeth at rest, every other row's W = rest + c00)")
L6 = layout((1, 1, 6), REST, REST, GRIP, 1, 1, clock="others")._replace(plan=engine_plan(SPRING))
n = 6
for c00 in (0, REST, 3 * REST):
    a = np.zeros((ROWS, n), dtype=object)
    a[S00] = c00 + mode6(6, 10**3)
    s00 = State(a, a.copy(), 0 * a, 0 * a)
    t00 = crossings_about(L6, s00, S00, 0, c00, 40)
    a = np.zeros((ROWS, n), dtype=object)
    a[S00] = c00
    a[LIGHT] = mode6(6, 10**6)
    sl = State(a, a.copy(), 0 * a, 0 * a)
    tl = crossings_about(L6, sl, LIGHT, 0, 0, 40)
    say(f"  c00 = {c00} (W = {1 + c00 // REST} rest for light): the 00 wave's 40 sign changes in {t00} rounds, light's in {tl}: the 00 wave's speed over light's, squared, {carry(1000 * tl * tl, t00 * t00, 0)[0]} permille")
say("  P5's 'runs at light's speed' holds at rest alone: in a well the 00 wave keeps c^2 = grip / rest while light slows to grip / W")

say("\n== 2. the drive under the flipped tooth: carry(J, T_d, T_d - 1 - r_d+) against the forward quotient (an even row), and carry(-J, T_d, r_d+) (an odd row)")
same_q, neg_q, flipped_r, same_r = 0, 0, 0, 0
total = 0
for T in (1, 2, 3, 7, 100):
    for J in range(-300, 301, 7):
        for rd in range(T):
            q, rd1 = carry(J, T, rd)
            qe, re_ = carry(J, T, T - 1 - rd1)
            qo, ro = carry(-J, T, rd1)
            total += 1
            same_q += qe == q
            flipped_r += re_ == T - 1 - rd
            neg_q += qo == -q
            same_r += ro == rd
say(f"  of {total} cases: even row (J kept, tooth flipped): the quotient the same {same_q}, the remainder T_d - 1 - r_d {flipped_r}; odd row (J negated, tooth kept): the quotient negated {neg_q}, the remainder r_d {same_r}")
say("  so the proof sketch's step 3, 'the drive's flipped tooth gives the quotient's negative', is the odd row's case with the tooth unflipped; on an even row the quotient is the same and the gear's flipped dividend does the negating")

Path(HERE / "probe_small.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8")
