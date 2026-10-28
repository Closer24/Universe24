"""V1: law 10's two sentences on a cycle, and the dial reading (verifier of draft F, section 2.5).

Integers only. Run: python3 -I V1_law10.py [MUTANT]   MUTANT: none, open (the cycle left open: no closing step)
 A. exhaustive: on a cycle of n bangs (n = 1..7) no integer reading 0..4 rises at every step, the closing one
    included; readings that rise at every step but one exist; over any closed cycle the rises total the falls;
 B. the dial reading (law 11): dials of radices (3, 4) stepped one tooth a bang with the carry: every dial
    advances one tooth mod its radix at every bang it moves, the cycle closes after 12 bangs, and the whole
    reading N = d1 + 3 d2 rises by 1 at 11 bangs and falls by 11 at the closing bang (the top dial's carry);
    if the top's carry is kept as a count (Postulate 4: no integer lost), the count rises and the full state
    never returns;
 C. the massless uniform drift on a dial: a+ = 2 a - a- mod M is a bijection of (Z/M)^2, so its orbits close;
    the drift a = a0 + t closes at period M, each closing one carry.
"""

import itertools
import random
import sys

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


# A. exhaustive cycles
rising_all, rising_but_one = 0, 0
for n in range(1, 8):
    for f in itertools.product(range(5), repeat=n):
        steps = [(i, (i + 1) % n) for i in range(n)] if MUT != "open" else [(i, i + 1) for i in range(n - 1)]
        ups = sum(1 for i, j in steps if f[j] > f[i])
        if ups == len(steps) and len(steps) > 0:
            rising_all += 1
        if ups == len(steps) - 1:
            rising_but_one += 1
check("A1 no reading rises at every bang of a closed cycle (n = 1..7, values 0..4, exhaustive)", rising_all == 0, f"{rising_all} found")
check("A2 readings that rise at every bang but one exist (the closing bang falls)", rising_but_one > 0, f"{rising_but_one} found")
rng = random.Random(10)
ok = True
for _ in range(1000):
    n = rng.randint(1, 30)
    f = [rng.randint(-10 ** 6, 10 ** 6) for _ in range(n)]
    d = [f[(i + 1) % n] - f[i] for i in range(n)]
    ok = ok and sum(x for x in d if x > 0) == -sum(x for x in d if x < 0)
check("A3 over a closed cycle the rises total exactly the falls (1000 random integer cycles)", ok)

# B. the dial reading
R1, R2 = 3, 4
d1, d2, kept = 0, 0, 0
states, N, top_carries = [(d1, d2)], [d1 + R1 * d2], []
for bang in range(1, 2 * R1 * R2 + 1):
    d1 += 1
    c1 = d1 // R1
    d1 %= R1
    d2 += c1
    c2 = d2 // R2
    d2 %= R2
    kept += c2
    if c2:
        top_carries.append(bang)
    states.append((d1, d2))
    N.append(d1 + R1 * d2)
period = next(t for t in range(1, len(states)) if states[t] == states[0])
rises = [N[t] - N[t - 1] for t in range(1, period + 1)]
check("B1 the two dials close a cycle of 12 bangs", period == R1 * R2, str(period))
check("B2 the whole reading N rises by 1 at 11 bangs and falls by 11 at the closing bang, the top dial's carry",
      rises.count(1) == period - 1 and rises[-1] == -(period - 1) and top_carries[0] == period, f"steps {rises}")
check("B3 the top's carry kept as a count rises at every closing, so the full state (dials, count) never returns",
      kept == 2 and top_carries == [period, 2 * period], f"count {kept} after {2 * period} bangs")

# C. the uniform drift on a dial
M = 7
ok_bij = len({((2 * a - b) % M, a) for a in range(M) for b in range(M)}) == M * M
a, b, t, closes = 3, 2, 0, []
start = (a, b)
while True:
    a, b = (2 * a - b) % M, a
    t += 1
    if (a, b) == start:
        closes.append(t)
        break
check("C1 a+ = 2 a - a- mod M is a bijection of (Z/M)^2 (M = 7), so every orbit on the dial closes", ok_bij)
check("C2 the drift of one notch a tick closes after M ticks on the dial (one carry per closing)", closes == [M], str(closes))

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
