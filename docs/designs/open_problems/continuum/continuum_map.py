"""The continuum limit: the map of problem (7) of the seven (the open-problems physicist,
read-only, 2026-09-21; docs/designs/open_problems/continuum/NOTE.md).

Integers of the flight rule transcribed from BEAM_LAW section 3 (no engine import), no run.
A scaling theory names its grains and the rate at which each formula's error falls with
them; this map measures the rates the law already has.

(A) The grain Q (the label's scale): the pace per direction Q |D| / T_D against 1 / sqrt 3
    over every primitive direction within Manhattan 6, the largest departure at Q = 64, 256,
    1024, 4096, 65536: the isotropy of c converges as 1 / (sqrt 3 Q) (NATURE 5a).
(B) The grain N (the circle): Born's rung error 1 / (2 N) and the CHSH deficit 8 / N at N =
    64 to 65536 (DERIVATIONS 6.2, the paper's theorem).
(C) The grain P (the fan's bound): the fraction of a shell's Nodes on some line of the fan
    of every primitive direction within Manhattan P, at r = 4 .. 20, for P = 4, 6, 8, 12:
    when the crowd is a field and when a comb (the dense-fan condition of DERIVATIONS 3.2).
(D) The shell means' ripple: P r^2 and A r over the shells at each P against the continuum's
    q sqrt 3 / (4 pi) and 3 q / (4 pi): the 1 / r^2 and 1 / r forms as limits in P.

Run from the repository root:

    python docs/designs/open_problems/continuum/continuum_map.py > docs/designs/open_problems/continuum/continuum_map.out
"""

from __future__ import annotations

import math
from collections import defaultdict

C_CONT = 1 / math.sqrt(3)


def primitive_fan(bound: int):
    found = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                if (a or b or c) and abs(a) + abs(b) + abs(c) <= bound:
                    if math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                        found.append((a, b, c))
    return sorted(found)


print(
    "A. THE GRAIN Q: the pace Q |D| / T_D per direction against 1 / sqrt 3, T_D = isqrt(3 |D|^2 Q^2), over the 290 primitive directions within Manhattan 6"
)
print("   Q | the largest relative departure | the smallest | the bound 1 / (sqrt 3 Q - 1)")
fan6 = primitive_fan(6)
for q in (64, 256, 1024, 4096, 65536):
    devs = []
    for d in fan6:
        n2 = sum(c * c for d_ in [d] for c in d_)
        t = math.isqrt(3 * n2 * q * q)
        pace = q * math.sqrt(n2) / t
        devs.append(pace / C_CONT - 1)
    print(f"   {q:6d} | {max(devs):.3e} | {min(devs):.3e} | {1 / (math.sqrt(3) * q - 1):.3e}")
print(
    "   the anisotropy of c falls as 1 / Q, never below 1 / sqrt 3 (isqrt rounds down): the limit Q -> infinity is isotropic at the rate of the grain"
)
print()

print("B. THE GRAIN N: Born's rung error and the CHSH deficit")
print("   N | the rung's error bound 1 / (2 N) | the CHSH bound 8 / N | the registered S | 2 sqrt 2 - S")
registered = {64: 176 / 64, 256: 720 / 256, 1024: 2896 / 1024, 4096: 11584 / 4096}
for n in (64, 256, 1024, 4096, 65536):
    s = registered.get(n)
    s_text = f"{s:.6f}" if s else "11585 / 4096 = 2.828369 (the closed form)"
    deficit = f"{2 * math.sqrt(2) - s:.2e}" if s else "5.8e-05"
    print(f"   {n:5d} | {1 / (2 * n):.2e} | {8 / n:.2e} | {s_text} | {deficit}")
print(
    "   Born and Tsirelson are limits in N at the rate 1 / N; the tables' 1 / 256 stays as a floor (2.1e-6 in S with the tables fixed)"
)
print()


def bresenham(vector):
    s1 = sum(abs(c) for c in vector)
    line = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


Q = 64


def stationary(fan, links):
    """Per Node: the presence (the dwell count) and the age moment of one source releasing one
    unit per direction per interval (the flight rule's ages at every Link)."""
    presence = defaultdict(int)
    age_moment = defaultdict(int)
    for v in fan:
        s1 = sum(abs(c) for c in v)
        t_d = math.isqrt(3 * sum(c * c for c in v) * Q * Q)
        steps = bresenham(v)
        rate, wall, start = 2 * s1 * Q, 2 * t_d, t_d

        def age_of(made, rate=rate, wall=wall, start=start):
            return max(0, -(-(made * wall - start) // rate))

        x = y = z = 0
        for made in range(1, links + 1):
            sx, sy, sz = steps[(made - 1) % s1]
            x, y, z = x + sx, y + sy, z + sz
            ages = range(age_of(made), age_of(made + 1))
            presence[(x, y, z)] += len(ages)
            age_moment[(x, y, z)] += sum(ages)
    return presence, age_moment


SHELLS = defaultdict(list)
for x in range(-21, 22):
    for y in range(-21, 22):
        for z in range(-21, 22):
            rr = math.sqrt(x * x + y * y + z * z)
            r = round(rr)
            if 4 <= r <= 20 and abs(rr - r) < 0.5:
                SHELLS[r].append((x, y, z))

print(
    "C. THE GRAIN P: the fraction of a shell's Nodes on some line of the fan within Manhattan P (the field against the comb)"
)
print("   r | " + " | ".join(f"P = {p}" for p in (4, 6, 8, 12)))
results = {}
for p in (4, 6, 8, 12):
    fan = primitive_fan(p)
    presence, age_moment = stationary(fan, 40)
    results[p] = (len(fan), presence, age_moment)
for r in (4, 6, 8, 10, 12, 16, 20):
    row = []
    for p in (4, 6, 8, 12):
        _n, presence, _a = results[p]
        nodes = SHELLS[r]
        hit = sum(1 for n in nodes if presence.get(n, 0))
        row.append(f"{100 * hit / len(nodes):5.1f} %")
    print(f"   {r:2d} | " + " | ".join(row))
print("   the fans: " + ", ".join(f"P = {p}: {results[p][0]} directions" for p in (4, 6, 8, 12)))
print(
    "   a shell is covered while r is below about P / 2 and becomes a comb beyond it: the crowd is a field only where P >> r (DERIVATIONS 3.2's limit); the registered fans (P = 6 in space, 7 on the plane) are combs beyond r = 4"
)
print()

print("D. THE SHELL MEANS' RIPPLE AGAINST THE CONTINUUM'S 1 / r^2 AND 1 / r, per P (q = the fan's size)")
print(
    "   P | q | P r^2 over r = 4 .. 14: the mean, the least, the largest, over q sqrt 3 / (4 pi) | A r likewise over 3 q / (4 pi)"
)
for p in (4, 6, 8, 12):
    n_fan, presence, age_moment = results[p]
    pr2, ar = [], []
    for r in range(4, 15):
        nodes = SHELLS[r]
        mp = sum(presence.get(n, 0) for n in nodes) / len(nodes)
        ma = sum(age_moment.get(n, 0) for n in nodes) / len(nodes)
        pr2.append(mp * r * r / (n_fan * math.sqrt(3) / (4 * math.pi)))
        ar.append(ma * r / (3 * n_fan / (4 * math.pi)))
    print(
        f"   {p:2d} | {n_fan:5d} | {sum(pr2) / len(pr2):.3f}, {min(pr2):.3f}, {max(pr2):.3f} | {sum(ar) / len(ar):.3f}, {min(ar):.3f}, {max(ar):.3f}"
    )
print(
    "   the shell means carry the 1 / r^2 and 1 / r forms at every P within the ripple; the ripple is the comb's, and a single Node reads a line or nothing where the shell is not covered"
)
