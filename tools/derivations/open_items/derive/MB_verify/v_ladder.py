"""Verifier's probe (MB_verify): the 24's ladder rebuilt from the 48 elements of 2O, exactly.

Independent of Animate's kinds_ladder.py: no character table is typed. The group is built as its 48 unit
quaternions with coordinates in Q(sqrt 2) (pairs of Fractions a + b sqrt 2); the classes, the squares and the
powers are computed by quaternion products; the characters are built from
  E1/2(q) = 2 w (the trace of q in SU(2)),
  T1(q)   = 4 w^2 - 1 (the trace of the rotation v -> q v q^-1),
  A2(q)   = the sign of q's permutation of the cube's 4 body diagonals,
and products: T2 = T1 A2, E = Sym^2 T1 - A1 - T2, E5/2 = E1/2 A2, G3/2 = E1/2 E.
Every multiplicity is (1/48) SUM over the 48 elements, checked to be an integer (no float anywhere).

Reads:
 1. orthonormality of the eight characters, the class sizes, the Frobenius-Schur signs;
 2. the product table K1 x K2 (all 36 pairs) and the symmetric and antisymmetric squares;
 3. the ladder from {A1} and from {A1, E1/2} with every pair of kinds fused (Animate's premise);
 4. the ladder under David's rule (#2187 6469872764): equal quanta of a spinor kind fuse only into Alt^2, of the
    24's kinds only into Sym^2; different kinds fuse fully; three readings of which quanta are equal;
 5. n twin hands: the full tensor power E1/2^n (n = 1..8) and, under the rule, the antisymmetric power Lambda^n;
 6. mutants that must fail: a wrong table (E1/2 with the sqrt 2 sign swapped on one class), David's rule off.
"""

from fractions import Fraction as F
from itertools import combinations_with_replacement, product as iproduct


# ---- Q(sqrt 2) as pairs (a, b) = a + b sqrt 2 ----
def qa(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qm(x, y):
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def qn(x):
    return (-x[0], -x[1])


ZERO, ONE = (F(0), F(0)), (F(1), F(0))
HALF = (F(1, 2), F(0))
ISQ2 = (F(0), F(1, 2))  # 1 / sqrt 2 = sqrt 2 / 2


def qs(n):
    return (F(n), F(0))


# ---- quaternions (w, x, y, z), each coordinate in Q(sqrt 2) ----
def hmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    w = qa(qa(qm(a1, a2), qn(qm(b1, b2))), qn(qa(qm(c1, c2), qm(d1, d2))))
    x = qa(qa(qm(a1, b2), qm(b1, a2)), qa(qm(c1, d2), qn(qm(d1, c2))))
    y = qa(qa(qm(a1, c2), qn(qm(b1, d2))), qa(qm(c1, a2), qm(d1, b2)))
    z = qa(qa(qm(a1, d2), qm(b1, c2)), qa(qn(qm(c1, b2)), qm(d1, a2)))
    return (w, x, y, z)


def hconj(q):
    return (q[0], qn(q[1]), qn(q[2]), qn(q[3]))


def build_2O():
    els = set()
    for i in range(4):
        for s in (1, -1):
            v = [ZERO] * 4
            v[i] = qs(s)
            els.add(tuple(v))
    for signs in iproduct((1, -1), repeat=4):
        els.add(tuple(qm(qs(s), HALF) for s in signs))
    for i in range(4):
        for j in range(i + 1, 4):
            for si, sj in iproduct((1, -1), repeat=2):
                v = [ZERO] * 4
                v[i], v[j] = qm(qs(si), ISQ2), qm(qs(sj), ISQ2)
                els.add(tuple(v))
    els = sorted(els)
    assert len(els) == 48
    S = set(els)
    assert all(hmul(a, b) in S for a in els for b in els), "not closed"
    return els


G = build_2O()
IDX = {g: n for n, g in enumerate(G)}
ID = (ONE, ZERO, ZERO, ZERO)


def power(g, k):
    r = ID
    for _ in range(k):
        r = hmul(r, g)
    return r


# conjugacy classes
classes, seen = [], set()
for g in G:
    if g in seen:
        continue
    cl = {hmul(hmul(h, g), hconj(h)) for h in G}
    seen |= cl
    classes.append(sorted(cl))


def w_of(q):
    return q[0]


def rot_apply(q, v):
    """v -> q v q^-1 for a pure quaternion v = (0, v)."""
    p = (ZERO, *v)
    r = hmul(hmul(q, p), hconj(q))
    return r[1:]


DIAGS = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]


def a2_sign(q):
    """Sign of the permutation of the 4 body-diagonal lines under q's rotation."""
    perm = []
    for d in DIAGS:
        img = rot_apply(q, tuple(qs(c) for c in d))
        key = tuple(c[0] for c in img)  # images are integer vectors (rational, no sqrt2 part)
        assert all(c[1] == 0 for c in img)
        for n, e in enumerate(DIAGS):
            if key == e or key == tuple(-c for c in e):
                perm.append(n)
                break
    assert sorted(perm) == [0, 1, 2, 3]
    sign, p = 1, list(perm)
    for i in range(4):
        while p[i] != i:
            j = p[i]
            p[i], p[j] = p[j], p[i]
            sign = -sign
    return qs(sign)


# characters as lists over the 48 elements (values in Q(sqrt 2))
chiA1 = [ONE for g in G]
chiE12 = [qm(qs(2), w_of(g)) for g in G]
chiT1 = [qa(qm(qs(4), qm(w_of(g), w_of(g))), qs(-1)) for g in G]
chiA2 = [a2_sign(g) for g in G]


def cmul(a, b):
    return [qm(x, y) for x, y in zip(a, b)]


def cadd(a, b, s=1):
    return [qa(x, qm(qs(s), y)) for x, y in zip(a, b)]


def at_power(chi, k):
    return [chi[IDX[power(g, k)]] for g in G]


def sym2(chi):
    return [qm((F(1, 2), F(0)), qa(qm(x, x), y)) for x, y in zip(chi, at_power(chi, 2))]


def alt2(chi):
    return [qm((F(1, 2), F(0)), qa(qm(x, x), qn(y))) for x, y in zip(chi, at_power(chi, 2))]


chiT2 = cmul(chiT1, chiA2)
chiE = cadd(cadd(sym2(chiT1), chiA1, -1), chiT2, -1)
chiE52 = cmul(chiE12, chiA2)
chiG32 = cmul(chiE12, chiE)
KINDS = {"A1": chiA1, "A2": chiA2, "E": chiE, "T1": chiT1, "T2": chiT2, "E1/2": chiE12, "E5/2": chiE52, "G3/2": chiG32}
ORDER = list(KINDS)
SPINOR = {"E1/2", "E5/2", "G3/2"}


def inner(a, b):
    t = ZERO
    for x, y in zip(a, b):
        t = qa(t, qm(x, y))
    t = (t[0] / 48, t[1] / 48)
    if t[1] != 0 or t[0].denominator != 1:
        raise ValueError(f"not an integer multiplicity: {t}")
    return int(t[0])


def parts(chi, table=None):
    table = table or KINDS
    return {k: m for k, v in table.items() if (m := inner(chi, v))}


def show(d):
    return " + ".join((f"{m} " if m > 1 else "") + k for k, m in sorted(d.items(), key=lambda kv: ORDER.index(kv[0]))) or "0"


def fs(chi):
    t = ZERO
    for y in at_power(chi, 2):
        t = qa(t, y)
    assert t[1] == 0 and t[0] % 48 == 0
    return int(t[0] / 48)


def fuse(kinds, rule, table=None):
    """One bang: every pair of kinds present fused (each with itself too), the parts kept; `rule` names which
    square a pair of one kind may enter: 'full' (Animate), or David's rule with the set of kinds whose two
    quanta are unequal (those fuse fully), the others into Sym^2 (the 24's kinds) or Alt^2 (spinor kinds)."""
    table = table or KINDS
    found = set(kinds)
    for k1, k2 in combinations_with_replacement(sorted(kinds, key=ORDER.index), 2):
        if k1 != k2 or rule == "full" or k1 in rule:
            chi = cmul(table[k1], table[k2])
        else:
            chi = alt2(table[k1]) if k1 in SPINOR else sym2(table[k1])
        found |= set(parts(chi, table))
    return found


def ladder(start, rule, bangs=7, table=None):
    rungs, present = [], set(start)
    for _ in range(bangs):
        rungs.append(sorted(present, key=ORDER.index))
        present = fuse(present, rule, table)
    return rungs


def first_full(rungs):
    return next((n for n, r in enumerate(rungs, start=1) if len(r) == 8), None)


def lambda_powers(chi, nmax):
    """Antisymmetric powers by Newton's identity: k L_k = SUM_{i=1..k} (-1)^(i-1) chi(g^i) L_{k-i}."""
    L = [[ONE for _ in G]]
    pw = {i: at_power(chi, i) for i in range(1, nmax + 1)}
    for k in range(1, nmax + 1):
        acc = [ZERO for _ in G]
        for i in range(1, k + 1):
            term = cmul(pw[i], L[k - i])
            acc = cadd(acc, term, 1 if i % 2 == 1 else -1)
        L.append([(x[0] / k, x[1] / k) for x in acc])
    return L


def main():
    out = []
    p = out.append
    sizes = sorted(len(c) for c in classes)
    p(f"1. 2O built: {len(G)} elements, {len(classes)} classes of sizes {sizes}")
    bad = [(a, b) for a in ORDER for b in ORDER if inner(KINDS[a], KINDS[b]) != (a == b)]
    p(f"   orthonormality fails at {len(bad)} of 64 pairs; dimensions " + ", ".join(f"{k} {int(v[IDX[ID]][0])}" for k, v in KINDS.items()))
    p("   Frobenius-Schur sign (the A1 pairing's exchange sign): " + ", ".join(f"{k} {fs(v):+d}" for k, v in KINDS.items()))
    p("2. the product table K1 x K2")
    for k1, k2 in combinations_with_replacement(ORDER, 2):
        p(f"   {k1} x {k2} = {show(parts(cmul(KINDS[k1], KINDS[k2])))}")
    p("   symmetric and antisymmetric squares")
    for k in ORDER:
        p(f"   {k}: Sym^2 = {show(parts(sym2(KINDS[k])))};  Alt^2 = {show(parts(alt2(KINDS[k])))}")
    p("3. Animate's premise: every pair of kinds present fused, both quanta of a pair unequal")
    for start in ({"A1"}, {"A1", "E1/2"}):
        rungs = ladder(start, "full")
        p(f"   from {sorted(start, key=ORDER.index)}: all eight at bang {first_full(rungs)}")
        for n, r in enumerate(rungs[:5], start=1):
            p(f"     bang {n}: {len(r)} {r}")
    p("4. David's rule: equal quanta of a spinor kind into Alt^2 only, of the 24's kinds into Sym^2 only")
    cases = [
        ("one family, no antiquanta: every pair of one kind equal", frozenset()),
        ("the twin hands unequal (quantum and antiquantum, or two families); composites equal", frozenset({"E1/2"})),
        ("every kind with unequal quanta (rule inert)", frozenset(ORDER)),
    ]
    for label, unequal in cases:
        rungs = ladder({"A1", "E1/2"}, unequal)
        p(f"   {label}: all eight at bang {first_full(rungs)}")
        for n, r in enumerate(rungs[:5], start=1):
            p(f"     bang {n}: {len(r)} {r}")
    p("5. n twin hands: full tensor power (distinct quanta) against Lambda^n (equal quanta, David's rule)")
    pw = list(chiA1)
    L = lambda_powers(chiE12, 8)
    for n in range(1, 9):
        pw = cmul(pw, chiE12)
        p(f"   n = {n}: E1/2^{n} = {show(parts(pw))}  (dim {int(pw[IDX[ID]][0])});  Lambda^{n} = {show(parts(L[n])) if any(x != ZERO for x in L[n]) else '0'}")
    p("6. mutants that must fail")
    wrong = dict(KINDS)
    cls8 = next(c for c in classes if len(c) == 6 and chiE12[IDX[c[0]]][1] != 0)
    wrong["E1/2"] = [qn(x) if g in cls8 else x for g, x in zip(G, chiE12)]
    try:
        bad = [(a, b) for a in ORDER for b in ORDER if inner(wrong[a], wrong[b]) != (a == b)]
        p(f"   (a) E1/2 with sqrt 2 negated on one order-8 class: orthonormality fails at {len(bad)} pairs -> {'FAILS' if bad else 'PASSES (bad)'}")
    except ValueError as err:
        p(f"   (a) E1/2 with sqrt 2 negated on one order-8 class: a multiplicity is not an integer ({err}) -> FAILS")
    r_rule = ladder({"A1", "E1/2"}, frozenset())
    r_off = ladder({"A1", "E1/2"}, "full")
    p(f"   (b) David's rule switched off: the one-family ladder reaches eight at bang {first_full(r_off)}, against {first_full(r_rule)} with the rule -> the assertion 'one family stays at 2 kinds' {'FAILS' if len(r_off[-1]) != 2 else 'holds'}")
    # assertions of the probe
    assert not [(a, b) for a in ORDER for b in ORDER if inner(KINDS[a], KINDS[b]) != (a == b)]
    assert all(len(r) == 2 for r in r_rule)
    print("\n".join(out))


if __name__ == "__main__":
    main()
