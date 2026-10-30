"""p3: every kind on a signed-permutation train, and which trains carry spin 1/2 (Big Pic, 2026-10-30).

The 48 gears as y = 2q over Z[sqrt 2]. Characters are pairs (x, y) = x + y root 2. Every subgroup of the 48 that holds
-1 is closed from two gears; a sign character (values +-1) sends -1 to -1 iff -1 is not in the subgroup made of the
squares and commutators; the train Ind_H(lam) is a signed permutation of 48 / |H| gears, and holds a kind K exactly
<lam, Res_H K> times (Frobenius). Run: python3 .../p3_trains.py (about a minute; output p3_trains.txt).
"""

from qlib import ONE, TWO, carry, exact, perm_sign, report, turn_matrix, units, units_y, ymul

lines = []
Y = units_y()
UU = units()
idx = {y: n for n, y in enumerate(Y)}
one = next(y for y in Y if y[0] == TWO and not any(y[1:]))
neg = lambda y: tuple(-v for v in y)  # noqa: E731
minus = neg(one)
inv = {y: next(z for z in Y if ymul(y, z) == one) for y in Y}
turn = {y: turn_matrix(u, s) for y, (u, s, _) in zip(Y, UU, strict=True)}


def chi_e12(y):
    return (y[0], y[1])  # 2 Re(g), the trace of g on C^2


def chi_e52(y):
    return (y[0], -y[1])  # its Galois twin


def chi_e(y):
    p = turn[y]
    fixed = sum(1 for r in range(3) if p[r][r] != 0)
    return {3: TWO, 0: -ONE, 1: 0}[fixed] if perm_sign(p) == ONE else 0


def chi_g32(y):
    a = chi_e12(y)
    e = chi_e(y)
    return (a[0] * e, a[1] * e)


def inner(chi_a, chi_b):
    """<chi_a, chi_b> over the 48 for real characters, as a pair; each part divided by 48 exactly."""
    s0 = s1 = 0
    for y in Y:
        a, b = chi_a(y), chi_b(y)
        s0 += a[0] * b[0] + TWO * a[1] * b[1]
        s1 += a[0] * b[1] + a[1] * b[0]
    return exact(s0, 48), exact(s1, 48)


KINDS = (("E1/2", chi_e12), ("E5/2", chi_e52), ("G3/2", chi_g32))

# 1. the units' own train of 24 gears: one tooth per pair +-g, the board turning by left multiplication
reps = []
for y in Y:
    if y not in reps and neg(y) not in reps:
        reps.append(y)


def train24(g):
    out = {}
    for n, h in enumerate(reps):
        gh = ymul(g, h)
        out[n] = (reps.index(gh), ONE) if gh in reps else (reps.index(neg(gh)), -ONE)
    return out


T = {g: train24(g) for g in Y}
hom = all(
    all(T[ymul(g, h)][n] == (T[g][T[h][n][0]][0], T[g][T[h][n][0]][1] * T[h][n][1]) for n in range(24))
    for g in Y
    for h in Y
)
report(
    lines,
    "1. the 24-gear train of the units is a signed permutation for every gear, a homomorphism on all "
    "48 x 48, and -1 sends every tooth to minus itself",
    len(reps) == 24 and hom and all(v == (n, -ONE) for n, v in T[minus].items()),
)


def chi24(y):
    return (sum(sg for n, (m, sg) in T[y].items() if m == n), 0)


mult = {name: inner(ch, chi24) for name, ch in KINDS}
lines.append("   it holds, by characters (complex count): " + str(mult))
report(
    lines,
    "   E1/2 twice, E5/2 twice, G3/2 four times",
    mult == {"E1/2": (2, 0), "E5/2": (2, 0), "G3/2": (4, 0)},
)


# 2. every subgroup holding -1, and those with a sign character sending -1 to -1
def closure(gens):
    S, frontier = {one}, [one]
    while frontier:
        new = []
        for s in frontier:
            for g in gens:
                t = ymul(s, g)
                if t not in S:
                    S.add(t)
                    new.append(t)
        frontier = new
    return frozenset(S)


subs = {closure([g, h]) for g in Y for h in Y}
hold = [H for H in subs if minus in H]
lines.append("   the subgroups holding -1, by order: " + str(sorted(len(H) for H in hold)))


def has_sign_char(H):
    made = [ymul(x, x) for x in H] + [ymul(ymul(x, z), ymul(inv[x], inv[z])) for x in H for z in H]
    return minus not in closure(list(set(made)))


good = sorted(len(H) for H in hold if has_sign_char(H))
report(
    lines,
    "2. of the " + str(len(hold)) + " subgroups holding -1, only {+-1} and the four sixfold C6 carry a "
    "sign character sending -1 to -1",
    len(hold) == 30 and good == [2, 6, 6, 6, 6],
    str(good),
)

# 3. the trains Ind_H(lam) for those, and which half-speed kinds each holds
found = []
for H in (H for H in hold if has_sign_char(H)):
    gen = next(g for g in H if closure([g]) == H)
    lam, x = {}, one
    for k in range(len(H)):
        _, odd = carry(k, TWO, 0)
        lam[x] = ONE - TWO * odd
        x = ymul(x, gen)
    if lam[minus] != -ONE:
        continue

    def chi_ind(y, H=H, lam=lam):
        tot = sum(lam[c] for c in (ymul(ymul(inv[z], y), z) for z in Y) if c in H)
        return (exact(tot, len(H)), 0)

    found.append((exact(48, len(H)), {name: inner(ch, chi_ind)[0] for name, ch in KINDS}))
lines.append("   the trains and what they hold: " + str(found))
report(
    lines,
    "3. the train from {+-1} has 24 gears and holds 2 E1/2 + 2 E5/2 + 4 G3/2; each C6 gives 8 gears "
    "holding 2 G3/2 alone; so spin 1/2 rides no signed-permutation train of fewer than 24 gears, and never alone",
    sorted(found, key=lambda f: f[0])
    == [(8, {"E1/2": 0, "E5/2": 0, "G3/2": 2})] * 4 + [(24, {"E1/2": 2, "E5/2": 2, "G3/2": 4})],
)

# 4. the subgroups without -1 (odd orders 1 and 3: their only sign character is trivial) give plain permutation trains
plain = []
for H in sorted({H for H in subs if minus not in H}, key=len):

    def chi_ind1(y, H=H):
        return (exact(sum(1 for z in Y if ymul(ymul(inv[z], y), z) in H), len(H)), 0)

    plain.append((len(H), exact(48, len(H)), inner(chi_e12, chi_ind1)[0]))
lines.append("   the subgroups without -1 (order, gears, E1/2 held): " + str(sorted(set(plain))))
report(
    lines,
    "4. without -1 only orders 1 and 3 occur; order 3 gives 16 gears holding no E1/2, order 1 the 48 of the "
    "regular train: so the 24-gear train is the least that holds spin 1/2",
    sorted(set(plain)) == [(1, 48, 2), (3, 16, 0)],
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
