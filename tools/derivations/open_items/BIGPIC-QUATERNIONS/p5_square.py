"""p5: the half-speed hand's square, a whole-speed handed hand the per-gear carry can carry (Big Pic, 2026-10-30).

psi = (psi1, psi2) with Gaussian whole parts; its square v = (psi1^2 - psi2^2, i (psi1^2 + psi2^2), -2 psi1 psi2) in C^3,
v = re + i im. A lead, not a derivation: whether the act keeps a square a square, and where Pauli's sign is kept if the
board holds squares alone, are open. Run: python3 .../p5_square.py (seconds; output p5_square.txt).
"""

import itertools

from qlib import ONE, TWO, Stream, det, report, units

lines = []
st = Stream(2026103005)


def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ca(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cs(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cj(a):
    return (a[0], -a[1])


def sq(psi):
    p1, p2 = psi
    return (
        cs(cm(p1, p1), cm(p2, p2)),
        cm((0, ONE), ca(cm(p1, p1), cm(p2, p2))),
        cm((-TWO, 0), cm(p1, p2)),
    )


def spin(psi):  # s = psi^dagger sigma psi
    p1, p2 = psi
    z = cm(cj(p1), p2)
    return (TWO * z[0], TWO * z[1], p1[0] * p1[0] + p1[1] * p1[1] - p2[0] * p2[0] - p2[1] * p2[1])


def rnd_psi(lo, hi):
    return tuple((st.between(lo, hi), st.between(lo, hi)) for _ in range(TWO))


# 1. the square is isotropic, its parts at right angles and of equal size |psi|^2; psi and -psi give one square
ok_iso = ok_size = ok_sign = True
spins = set()
for _ in range(3000):
    psi = rnd_psi(-9, 9)
    n = sum(x * x for p in psi for x in p)
    if n == 0:
        continue
    v = sq(psi)
    re, im = tuple(x[0] for x in v), tuple(x[1] for x in v)
    vv = (0, 0)
    for x in v:
        vv = ca(vv, cm(x, x))
    ok_iso &= vv == (0, 0)
    ok_size &= sum(a * b for a, b in zip(re, im, strict=True)) == 0 and sum(
        a * a for a in re
    ) == n * n == sum(b * b for b in im)
    ok_sign &= sq(tuple((-p[0], -p[1]) for p in psi)) == v
    cr = (re[1] * im[2] - re[2] * im[1], re[2] * im[0] - re[0] * im[2], re[0] * im[1] - re[1] * im[0])
    s = spin(psi)
    spins.update(sg for sg in (ONE, -ONE) if all(c == sg * n * t for c, t in zip(cr, s, strict=True)))
report(
    lines, "1. v . v = 0, re . im = 0 and |re| = |im| = |psi|^2 on 3,000 whole hands", ok_iso and ok_size
)
report(lines, "   psi and -psi give one square: the sign is what the square does not hold", ok_sign)
report(
    lines,
    "2. re x im = |psi|^2 s, s = psi^dagger sigma psi the root's spin, with one fixed sign on every hand",
    spins == {ONE},
    str(sorted(spins)),
)

# 3. the pair hand from the squares: v(psi) . v(chi) = -2 (psi1 chi2 - psi2 chi1)^2
ok = True
for a in itertools.product(range(-2, 3), repeat=4):
    for b in [(1, -2, 0, 3), (2, 1, -1, 1), (0, 0, 1, -1)]:
        psi, chi = ((a[0], a[1]), (a[2], a[3])), ((b[0], b[1]), (b[2], b[3]))
        dot = (0, 0)
        for x, y in zip(sq(psi), sq(chi), strict=True):
            dot = ca(dot, cm(x, y))
        e = cs(cm(psi[0], chi[1]), cm(psi[1], chi[0]))
        ok &= dot == cm((-TWO, 0), cm(e, e))
report(
    lines,
    "3. v(psi) . v(chi) = -2 (psi1 chi2 - psi2 chi1)^2 on 1,875 whole pairs: the pair hand is read from the squares",
    ok,
)


# 4. every gear turns the square by a whole signed permutation of determinant 1
def u_of(u):  # the gear a + b i + c j + d k as a 2 x 2 Gaussian matrix
    a, b, c, d = u
    return (((a, d), (c, b)), ((-c, b), (a, -d)))


def apply_u(U, psi):
    return (ca(cm(U[0][0], psi[0]), cm(U[0][1], psi[1])), ca(cm(U[1][0], psi[0]), cm(U[1][1], psi[1])))


signed = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product((ONE, -ONE), repeat=3):
        signed.append(tuple(tuple(sg[r] if c == p[r] else 0 for c in range(3)) for r in range(3)))
tests = [rnd_psi(-5, 5) for _ in range(12)]
found = []
for u, s, _ in units():
    U = u_of(u)
    hits = []
    for R in signed:
        good = True
        for psi in tests:
            v, w = sq(psi), sq(apply_u(U, psi))
            rv = tuple(
                ca(ca(cm((R[r][0], 0), v[0]), cm((R[r][1], 0), v[1])), cm((R[r][2], 0), v[2]))
                for r in range(3)
            )
            if any(cm((s, 0), x) != y for x, y in zip(rv, w, strict=True)):
                good = False
                break
        if good:
            hits.append(R)
    found.append(hits)
report(
    lines,
    "4. for each of the 48 gears, exactly one signed permutation R has v(g psi) = R v(psi) on every test hand, "
    "and its determinant is 1: every gear turns the square in whole numbers",
    all(len(h) == ONE and det(h[0]) == ONE for h in found),
)
report(lines, "   the 48 gears give 24 such turns, two gears to each", len({h[0] for h in found}) == 24)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
