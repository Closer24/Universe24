"""I_verify v3: independent recount of draft I's R2 (no charge-keeping quotient on primitive momenta) and R3
(no quadratic invariant of the integer step) with the verifier's own code and other parameters. Integers and Fractions only."""
import random
from fractions import Fraction as Fr
from math import gcd

# R2 recount: every quotient v whose remainders lie strictly inside the teeth, enumerated from scratch
prim = prim_keep = nonprim = nonprim_keep = 0
for w in range(2, 13):
    for p3 in range(-60, 61):
        for p12 in range(-60, 61):
            if max(abs(p3), abs(p12)) < w:
                continue
            c3 = [v for v in range(-61, 62) if abs(p3 - w * v) < w]
            c12 = [v for v in range(-61, 62) if abs(p12 - w * v) < w]
            keep = any(v3 * p12 - v12 * p3 == 0 for v3 in c3 for v12 in c12)
            if gcd(abs(p3), abs(p12)) == 1:
                prim += 1
                prim_keep += keep
            else:
                nonprim += 1
                nonprim_keep += keep
print(f"R2 recount: {prim} primitive momenta with max |P'_k| >= w' (w' = 2..12, |P'_k| <= 60), a charge-keeping quotient at {prim_keep};"
      f" {nonprim} non-primitive, a keeping quotient at {nonprim_keep}")

# the theorem's edge: w' = 1 is excluded by the teeth >= 2; check the bound (w' - 1)|P| >= w' for w' >= 2, |P| >= w'
bad = sum(1 for w in range(2, 200) for p in range(w, 400) if (w - 1) * p < w)
print(f"R2 bound (w' - 1) |P'_k| >= w' for w' >= 2, |P'_k| >= w': {bad} failures")

def mid(w):
    return w // 2

def carry(total, teeth, fine):
    c = total + fine
    q = c // teeth
    return q, c - teeth * q

def null_dim(rows, n):
    M = [list(r) for r in rows]
    rank = 0
    for col in range(n):
        piv = next((i for i in range(rank, len(M)) if M[i][col] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][col]
        M[rank] = [x / pv for x in M[rank]]
        for i in range(len(M)):
            if i != rank and M[i][col] != 0:
                f = M[i][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[rank])]
        rank += 1
    return n - rank

def monos(s):
    out = [Fr(1)] + [Fr(v) for v in s]
    for i in range(len(s)):
        for j in range(i, len(s)):
            out.append(Fr(s[i]) * Fr(s[j]))
    return out

rng = random.Random(777)
for (w, X, c) in ((1000, 5, 11), (999, 2, 23), (64, 1, 3)):
    def step(s):
        a3, a12, b3, b12, r3, r12 = s
        P = [w * (a3 - b3) + r3 - mid(w), w * (a12 - b12) + r12 - mid(w)]
        P1 = [P[0] - X * c * a3, P[1] - X * c * a12]
        v3, n3 = carry(P1[0], w, mid(w))
        v12, n12 = carry(P1[1], w, mid(w))
        return (a3 + v3, a12 + v12, a3, a12, n3, n12)
    rows = []
    for _ in range(300):
        a3, a12 = rng.randint(-5000, 5000), rng.randint(-5000, 5000)
        s = (a3, a12, a3 + rng.randint(-60, 60), a12 + rng.randint(-60, 60), rng.randrange(w), rng.randrange(w))
        t = step(s)
        rows.append([x - y for x, y in zip(monos(t), monos(s))])
    print(f"R3 recount (w={w}, X={X}, c={c}): null space dimension {null_dim(rows, 28)} over the 28 monomials of degree <= 2")
