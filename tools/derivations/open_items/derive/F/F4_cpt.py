"""F4: C from the kinds' conjugation, the rewind with the kinds' signs, the mirror, and the CPT check
(draft F; root II item 26; the one-hand coupling of section 24, item 5).

Exact integers only, no float. Run: python3 -I F4_cpt.py [MUTANT]
MUTANT: none (default), lead_now (the lead read at the now slot alone), kramers (the twin conjugation
without its minus sign), a0 (the rewind without the time gear's sign on the offset). Each mutant must
make at least one check FAIL.

The state on the torus of side 3: a hand z (now, before), a twin pair psi = (psi1, psi2) (now, before),
the offset's time gear A0 at each Node-clock and its three odd gears A_a read on the forward Mesh
x -> x + e_a (now, before). The engine's three exact operations:
  R  the rewind's involution: now and before exchanged on every gear, the offset's time gear negated
     (the four-vector's time part, OL-S1's mend);
  P  the inversion x -> -x of the 48: site gears moved, the link gear A_a(x) -> -A_a(-x - e_a);
  C  the kinds' conjugation: z -> conj z, psi -> (-conj psi2, conj psi1) (the intertwiner of E1/2 with its
     conjugate, C C = -1), the offset negated.
Each reading is computed on the moved state and compared, at the moved place, with the reading of the
state: its parity is +1, -1, or none. CPT = C P (C R) acts on every bilinear as P R.
Also: the Frobenius-Schur indicators of the kinds of O and of 2O (from the 24's integer matrices), and the
twin pairs fixed by C (none but 0).
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


L = 3
SITES = list(itertools.product(range(L), repeat=3))
E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def add(x, d, k=1):
    return tuple((x[i] + k * d[i]) % L for i in range(3))


def neg(x):
    return tuple((-v) % L for v in x)


# Gaussian integers as pairs
def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gconj(a):
    return (a[0], -a[1])


def gsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def gadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def im_cx(a, b):
    """Im(conj(a) b)."""
    return a[0] * b[1] - a[1] * b[0]


def re_cx(a, b):
    """Re(conj(a) b)."""
    return a[0] * b[0] + a[1] * b[1]


def rnd_state(rng):
    G = lambda: (rng.randint(-9, 9), rng.randint(-9, 9))  # noqa: E731
    s = {"zn": {}, "zb": {}, "pn": {}, "pb": {}, "A0n": {}, "A0b": {}, "An": {}, "Ab": {}}
    for x in SITES:
        s["zn"][x], s["zb"][x] = G(), G()
        s["pn"][x], s["pb"][x] = (G(), G()), (G(), G())
        s["A0n"][x], s["A0b"][x] = rng.randint(-9, 9), rng.randint(-9, 9)
        for a in range(3):
            s["An"][(x, a)], s["Ab"][(x, a)] = rng.randint(-9, 9), rng.randint(-9, 9)
    return s


# ---------------------------------------------------------------- the three operations
def op_R(s):
    sign = 1 if MUT == "a0" else -1
    return {"zn": dict(s["zb"]), "zb": dict(s["zn"]), "pn": dict(s["pb"]), "pb": dict(s["pn"]),
            "A0n": {x: sign * v for x, v in s["A0b"].items()}, "A0b": {x: sign * v for x, v in s["A0n"].items()},
            "An": dict(s["Ab"]), "Ab": dict(s["An"])}


def op_P(s):
    out = {k: {} for k in s}
    for x in SITES:
        for k in ("zn", "zb", "pn", "pb", "A0n", "A0b"):
            out[k][x] = s[k][neg(x)]
        for a in range(3):
            src = add(neg(x), E[a], -1)  # -x - e_a
            out["An"][(x, a)] = -s["An"][(src, a)]
            out["Ab"][(x, a)] = -s["Ab"][(src, a)]
    return out


def kramers(p):
    if MUT == "kramers":
        return (gconj(p[1]), gconj(p[0]))
    return ((-p[1][0], p[1][1]), gconj(p[0]))  # (-conj psi2, conj psi1)


def op_C(s):
    return {"zn": {x: gconj(v) for x, v in s["zn"].items()}, "zb": {x: gconj(v) for x, v in s["zb"].items()},
            "pn": {x: kramers(v) for x, v in s["pn"].items()}, "pb": {x: kramers(v) for x, v in s["pb"].items()},
            "A0n": {x: -v for x, v in s["A0n"].items()}, "A0b": {x: -v for x, v in s["A0b"].items()},
            "An": {k: -v for k, v in s["An"].items()}, "Ab": {k: -v for k, v in s["Ab"].items()}}


# ---------------------------------------------------------------- the readings
def lead(z, x, a):
    return im_cx(z[x], z[add(x, E[a])])


def r_Q(s):  # the sweep, the charge: Im(conj(z-) z)
    return {x: im_cx(s["zb"][x], s["zn"][x]) for x in SITES}


def r_J(s):  # the lead on the Mesh x -> x + e_a, both slots
    out = {}
    for x in SITES:
        for a in range(3):
            v = lead(s["zn"], x, a)
            if MUT != "lead_now":
                v += lead(s["zb"], x, a)
            out[(x, a)] = v
    return out


def site_vec_from_links(lk):
    return {x: tuple(lk[(x, a)] + lk[(add(x, E[a], -1), a)] for a in range(3)) for x in SITES}


def spin(p):
    c = gmul(gconj(p[0]), p[1])
    return (2 * c[0], 2 * c[1], p[0][0] ** 2 + p[0][1] ** 2 - p[1][0] ** 2 - p[1][1] ** 2)


def r_S(s):  # the twin pair's spin, both slots: the middle slot's T1 of the twin bilinear
    return {x: tuple(u + v for u, v in zip(spin(s["pn"][x]), spin(s["pb"][x]))) for x in SITES}


def two_time(s, x):
    n, b = s["pn"][x], s["pb"][x]
    D = {}
    for i in range(2):
        for k in range(2):
            X = gsub(gmul(gconj(b[i]), n[k]), gmul(gconj(n[i]), b[k]))
            D[(i, k)] = (-X[1], X[0])  # i X
    return D


def r_W(s):  # the twin pair's two-time density D_uu + D_dd (draft D's two-time reading)
    out = {}
    for x in SITES:
        D = two_time(s, x)
        out[x] = D[(0, 0)][0] + D[(1, 1)][0]
    return out


def sw_of(D, ysign=1):
    """The two-time spin (2 Re D_ud, ysign 2 Im D_ud, D_uu - D_dd): ysign +1 turns as the twin spin S does under
    the 24 (checked below); draft D's -1 is the conjugate basis."""
    return (2 * D[(0, 1)][0], ysign * 2 * D[(0, 1)][1], D[(0, 0)][0] - D[(1, 1)][0])


def r_SW(s):  # the twin pair's two-time spin, in the basis that turns with S
    return {x: sw_of(two_time(s, x)) for x in SITES}


def r_Pm(s):  # the hand's momentum, centred in space, the two slots' difference in time
    out = {}
    for x in SITES:
        dz = gsub(s["zn"][x], s["zb"][x])
        comp = []
        for a in range(3):
            g = gadd(gsub(s["zn"][add(x, E[a])], s["zn"][add(x, E[a], -1)]),
                     gsub(s["zb"][add(x, E[a])], s["zb"][add(x, E[a], -1)]))
            comp.append(-re_cx(dz, g))
        out[x] = tuple(comp)
    return out


def r_E(s):  # the electric field on the Mesh: -(A - A-) - grad of the time gear (both slots)
    out = {}
    for x in SITES:
        for a in range(3):
            y = add(x, E[a])
            a0 = lambda q: s["A0n"][q] + s["A0b"][q]  # noqa: E731
            out[(x, a)] = -(s["An"][(x, a)] - s["Ab"][(x, a)]) - (a0(y) - a0(x))
    return out


def plaq(A, x, a, b):
    return A[(add(x, E[a]), b)] - A[(x, b)] - A[(add(x, E[b]), a)] + A[(x, a)]


def r_B(s):  # the curl of the odd gears on the forward plaquettes (both slots); face (x, c) with (a, b, c) cyclic
    out = {}
    for x in SITES:
        for c in range(3):
            a, b = (c + 1) % 3, (c + 2) % 3
            out[(x, c)] = plaq(s["An"], x, a, b) + plaq(s["Ab"], x, a, b)
    return out


def site_B(bf):
    out = {}
    for x in SITES:
        comp = []
        for c in range(3):
            a, b = (c + 1) % 3, (c + 2) % 3
            comp.append(bf[(x, c)] + bf[(add(x, E[a], -1), c)] + bf[(add(x, E[b], -1), c)]
                        + bf[(add(add(x, E[a], -1), E[b], -1), c)])
        out[x] = tuple(comp)
    return out


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


READINGS = {
    "Q the sweep (charge)": ("site", r_Q),
    "J the lead (current), on the Mesh": ("link", r_J),
    "Pm the momentum": ("site", r_Pm),
    "S the twin spin (middle slot)": ("site", r_S),
    "W the twin two-time density": ("site", r_W),
    "SW the twin two-time spin": ("site", r_SW),
    "E the electric field, on the Mesh": ("link", r_E),
    "B the curl, on the plaquette": ("face", r_B),
    "Q A0 (the charge's coupling)": ("site", lambda s: {x: r_Q(s)[x] * (s["A0n"][x] + s["A0b"][x]) for x in SITES}),
    "J A (the current's coupling), on the Mesh": ("link", lambda s: {k: v * (s["An"][k] + s["Ab"][k]) for k, v in r_J(s).items()}),
    "S . B (the spin term)": ("site", lambda s: {x: dot(r_S(s)[x], site_B(r_B(s))[x]) for x in SITES}),
    "S . J (the plan's one-hand coupling)": ("site", lambda s: {x: dot(r_S(s)[x], site_vec_from_links(r_J(s))[x]) for x in SITES}),
    "SW . J (two-time spin with the current)": ("site", lambda s: {x: dot(r_SW(s)[x], site_vec_from_links(r_J(s))[x]) for x in SITES}),
    "S . Pm (spin with momentum)": ("site", lambda s: {x: dot(r_S(s)[x], r_Pm(s)[x]) for x in SITES}),
    "S . E (spin with the electric field)": ("site", lambda s: {x: dot(r_S(s)[x], site_vec_from_links(r_E(s))[x]) for x in SITES}),
}


def place(kind, key, moved_by_P):
    """Where the reading at `key` of the moved state is compared in the original."""
    if not moved_by_P:
        return key
    if kind == "site":
        return neg(key)
    x, a = key
    if kind == "link":
        return (add(neg(x), E[a], -1), a)
    b1, b2 = (a + 1) % 3, (a + 2) % 3  # face (x, c=a): its plaquette spans the two other axes
    return (add(add(neg(x), E[b1], -1), E[b2], -1), a)


def parity(kind, fn, op, moved_by_P, states):
    sign = None
    for s in states:
        orig, moved = fn(s), fn(op(s))
        for key, val in moved.items():
            ref = orig[place(kind, key, moved_by_P)]
            for v, w in (zip(val, ref) if isinstance(val, tuple) else [(val, ref)]):
                if w == 0 and v == 0:
                    continue
                here = 1 if v == w else (-1 if v == -w else 0)
                if here == 0 or (sign is not None and here != sign):
                    return 0
                sign = here
    return sign if sign is not None else 0


OPS = {
    "R": (op_R, False),
    "P": (op_P, True),
    "C": (op_C, False),
    "CP": (lambda s: op_C(op_P(s)), True),
    "T=CR": (lambda s: op_C(op_R(s)), False),
    "CPT=C P (C R)": (lambda s: op_C(op_P(op_C(op_R(s)))), True),
    "PR": (lambda s: op_P(op_R(s)), True),
}
rng = random.Random(24)
states = [rnd_state(rng) for _ in range(6)]
table = {}
print("   parity     " + "  ".join(f"{k:>14}" for k in OPS))
for name, (kind, fn) in READINGS.items():
    row = {op: parity(kind, fn, f, mp, states) for op, (f, mp) in OPS.items()}
    table[name] = row
    print(f"   {name[:44]:44}" + "  ".join(f"{'+' if v == 1 else ('-' if v == -1 else 'none'):>14}" for v in row.values()))


def row(name):
    return tuple(table[name][k] for k in ("R", "P", "C"))


check("T1 CPT = C P (C R) acts on every reading as P R (C C = -1 drops out of the bilinears)",
      all(table[n]["CPT=C P (C R)"] == table[n]["PR"] for n in table))
check("T2 the charge Q and the current J: (R, P, C) = (-, +, -) and (+, -, -), so both CPT-odd as a four-vector's parts",
      row("Q the sweep (charge)") == (-1, 1, -1) and row("J the lead (current), on the Mesh") == (1, -1, -1))
check("T3 E and B: (-, -, -) and (+, +, -), both CPT-even as a rank-2 tensor's parts",
      row("E the electric field, on the Mesh") == (-1, -1, -1) and row("B the curl, on the plaquette") == (1, 1, -1))
check("T4 the electromagnetic couplings Q A0, J A and the spin term S . B are even under R, P and C separately",
      all(row(n) == (1, 1, 1) for n in ("Q A0 (the charge's coupling)", "J A (the current's coupling), on the Mesh", "S . B (the spin term)")))
check("T5 the middle-slot spin S is (+, +, -): the classical twin bilinear is C-odd (nature's spin density is C-even)",
      row("S the twin spin (middle slot)") == (1, 1, -1))
check("T6 the two-time spin SW is R-odd: the axial current's T-parity class",
      table["SW the twin two-time spin"]["R"] == -1, str(row("SW the twin two-time spin")))
sj = table["S . J (the plan's one-hand coupling)"]
check("T7 the plan's coupling S . J breaks the mirror (P-odd) and is CPT-ODD on the engine", sj["P"] == -1 and sj["PR"] == -1,
      str({k: sj[k] for k in ("R", "P", "C", "PR")}))
check("T8 SW . J, S . Pm and S . E break the mirror and are CPT-even",
      all(table[n]["P"] == -1 and table[n]["PR"] == 1 for n in ("SW . J (two-time spin with the current)", "S . Pm (spin with momentum)", "S . E (spin with the electric field)")))

# ---------------------------------------------------------------- the 24's three-fold turn on the twin readings
from fractions import Fraction as Fr  # noqa: E402

h = Fr(1, 2)
U3 = [[(h, -h), (-h, -h)], [(h, -h), (h, h)]]  # (1 - i (s_x + s_y + s_z)) / 2, the turn about (1, 1, 1)


def turn(p):
    return tuple(gadd(gmul(U3[i][0], p[0]), gmul(U3[i][1], p[1])) for i in range(2))


def cyc(v):  # x -> y -> z -> x
    return (v[2], v[0], v[1])


def two_time_pair(n, b):
    D = {}
    for i in range(2):
        for k in range(2):
            X = gsub(gmul(gconj(b[i]), n[k]), gmul(gconj(n[i]), b[k]))
            D[(i, k)] = (-X[1], X[0])
    return D


ok_S = ok_SW = True
bad_D = False
for _ in range(40):
    n = ((Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))), (Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))))
    b = ((Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))), (Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))))
    ok_S = ok_S and spin(turn(n)) == cyc(spin(n))
    ok_SW = ok_SW and sw_of(two_time_pair(turn(n), turn(b))) == cyc(sw_of(two_time_pair(n, b)))
    bad_D = bad_D or sw_of(two_time_pair(turn(n), turn(b)), -1) != cyc(sw_of(two_time_pair(n, b), -1))
check("R1 under the 24's three-fold turn (the spinor's (1 - i(s_x + s_y + s_z))/2) S turns x -> y -> z", ok_S)
check("R2 the two-time spin with +2 Im D_ud turns the same way, so SW . J is kept by the 24; draft D's -2 Im D_ud does not (the conjugate basis)",
      ok_SW and bad_D)

# ---------------------------------------------------------------- the Frobenius-Schur indicators
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


G24 = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        m = [[0] * 3 for _ in range(3)]
        for i in range(3):
            m[p[i]][i] = sg[i]
        m = tuple(tuple(r) for r in m)
        if det3(m) == 1:
            G24.append(m)


def chi(kind, g):
    tr = g[0][0] + g[1][1] + g[2][2]
    perm = tuple(next(j for j in range(3) if g[j][i] != 0) for i in range(3))
    sgn = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if perm[i] > perm[j]:
                sgn = -sgn
    fixed = sum(1 for i in range(3) if perm[i] == i)
    return {"A1": 1, "A2": sgn, "E": fixed - 1, "T1": tr, "T2": sgn * tr}[kind]


fs_O = {k: sum(chi(k, mul(g, g)) for g in G24) // 24 for k in ("A1", "A2", "E", "T1", "T2")}
# 2O: each g of the 24 has two preimages; the spinor E1/2 has chi(h^2) = 2 cos(phi) = tr(g) - 1 at both,
# phi the rotation angle of g; E5/2 = E1/2 x A2 and G3/2 = E1/2 x E, so chi(h^2) multiplies by chi(g^2)
fs_spin = {}
for name, extra in (("E1/2", "A1"), ("E5/2", "A2"), ("G3/2", "E")):
    tot = sum(2 * ((g[0][0] + g[1][1] + g[2][2]) - 1) * chi(extra, mul(g, g)) for g in G24)
    fs_spin[name] = tot // 48
print("   Frobenius-Schur indicators: O", fs_O, " 2O spinors", fs_spin)
check("F1 every kind of O is real (indicator +1): C on them is the plain conjugation, C C = +1", all(v == 1 for v in fs_O.values()))
check("F2 every spinor kind of 2O is quaternionic (indicator -1): C is eps K, C C = -1; no kind of 2O is complex",
      all(v == -1 for v in fs_spin.values()))
# twin pairs fixed by C: psi = kramers(psi) only at 0
box = range(-3, 4)
fixed = [(a, b, c, d) for a in box for b in box for c in box for d in box
         if kramers(((a, b), (c, d))) == ((a, b), (c, d)) and (a, b, c, d) != (0, 0, 0, 0)]
twice = all(kramers(kramers(((a, b), (c, d)))) == ((-a, -b), (-c, -d)) for a in box for b in box for c in box for d in box)
check("F3 C C = -1 on every twin pair of the box, and no twin pair but 0 is its own conjugate (no Majorana twin train)",
      twice and not fixed, f"{len(fixed)} fixed")

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
