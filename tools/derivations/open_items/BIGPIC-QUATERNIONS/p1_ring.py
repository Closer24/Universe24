"""p1: the 48 gears and the cube's 24 turns, in whole numbers (Big Pic, 2026-10-30; README.md beside it).

Run: python3 tools/derivations/open_items/BIGPIC-QUATERNIONS/p1_ring.py   (seconds; output p1_ring.txt)
"""

import itertools

from qlib import (
    ONE,
    TWO,
    apply3,
    det,
    mm3,
    mul,
    perm_sign,
    report,
    sigma,
    turn_matrix,
    units,
    units_y,
    ymul,
)

lines = []
U = units()
I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

# 1. two gears to a turn
turns = {}
for u, s, kind in U:
    turns.setdefault(turn_matrix(u, s), []).append((u, s, kind))
report(
    lines,
    "1. the 48 gears give 24 turns, two gears to each (g and -g)",
    len(U) == 48 and len(turns) == 24 and all(len(v) == TWO for v in turns.values()),
)
report(
    lines,
    "   every turn is a signed permutation of the axes with determinant 1",
    all(sum(abs(x) for x in row) == ONE for m in turns for row in m)
    and all(det(m) == ONE for m in turns),
)

# 2. Hurwitz's 24 make the 12 even turns, the root-2 gears the 12 odd turns
even = {m for m, v in turns.items() if all(k != "root2" for _, _, k in v)}
odd = {m for m, v in turns.items() if all(k == "root2" for _, _, k in v)}
report(
    lines,
    "2. Hurwitz's 24 units (whole and all halves) make 12 turns, all even axis permutations",
    len(even) == 12 and all(perm_sign(m) == ONE for m in even),
)
report(
    lines,
    "   the 24 gears with a root of 2 make the other 12, all odd axis permutations",
    len(odd) == 12 and all(perm_sign(m) == -ONE for m in odd),
)

# 3. the hand turns twice the gear's angle: trace = 1 + 2 cos(theta), Re(g) = cos(theta / 2), so s trace = 4 u0^2 - s
report(
    lines,
    "3. on all 48, s * trace(turn) = 4 u0^2 - s: the hand turns by twice the gear's angle",
    all(s * sum(turn_matrix(u, s)[i][i] for i in range(3)) == 4 * u[0] * u[0] - s for u, s, _ in U),
)


# 4. which gear makes which turn
def kind_of(u, s):
    m = turn_matrix(u, s)
    t = sum(m[i][i] for i in range(3))
    if t == 3:
        return "none"
    if t == 0:
        return "corner third turn"
    if t == ONE:
        return "face quarter turn"
    axis = [v for v in itertools.product((-1, 0, 1), repeat=3) if any(v) and apply3(m, v) == v][0]
    return "face half turn" if sum(map(abs, axis)) == ONE else "edge half turn"


table = {}
for u, s, k in U:
    key = (kind_of(u, s), k)
    table[key] = table.get(key, 0) + 1
lines.append("   the gears by turn and by number: " + str(sorted(table.items())))
report(
    lines,
    "4. +-1 no turn; +-i, +-j, +-k the face half turns; the 16 all-halves the corner turns; "
    "root 2 with a real part the face quarter turns; pure root 2 the edge half turns",
    table
    == {
        ("none", "whole"): 2,
        ("face half turn", "whole"): 6,
        ("corner third turn", "halves"): 16,
        ("face quarter turn", "root2"): 12,
        ("edge half turn", "root2"): 12,
    },
)

# 5. the quarter turn's gear (1 + k) / root 2: g^2 = k, g^4 = -1, g^8 = 1; the hand is back after four
u = (1, 0, 0, 1)
u2 = mul(u, u)
u4 = mul(u2, u2)
u8 = mul(u4, u4)
m = turn_matrix(u, TWO)
report(
    lines,
    "5. (1 + k)^2 = 2 k, (1 + k)^4 = -4, (1 + k)^8 = 16: g^2 = k, g^4 = -1, g^8 = 1",
    u2 == (0, 0, 0, 2) and u4 == (-4, 0, 0, 0) and u8 == (16, 0, 0, 0),
)
report(
    lines,
    "   the whole-speed hand is back after four quarter turns, the half-speed one after eight",
    mm3(mm3(m, m), mm3(m, m)) == I3 and mm3(m, m) != I3,
)

# 6. A2 is the field's second sign: sigma(g) = +g on the even turns' gears, -g on the odd turns'; multiplicative
Y = units_y()
negy = lambda y: tuple(-v for v in y)  # noqa: E731
signs = []
for y in Y:
    signs.append(ONE if sigma(y) == y else (-ONE if sigma(y) == negy(y) else 0))
report(
    lines,
    "6. sigma(g) = A2(turn) g on all 48: the A2 kind is the Galois sign of root 2",
    all(sg == perm_sign(turn_matrix(u, s)) for (u, s, _), sg in zip(U, signs, strict=True)),
)
mult = all(
    (ONE if sigma(ymul(a, b)) == ymul(a, b) else -ONE) == sa * sb
    for (a, sa), (b, sb) in itertools.product(zip(Y, signs, strict=True), repeat=2)
)
report(lines, "   sigma(g)/g is multiplicative over all 48 x 48 products: a character", mult)

# 7. the six Spokes are the six pure units, permuted by every turn
spokes = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
report(
    lines,
    "7. every turn permutes the six Spokes +-i, +-j, +-k",
    all(sorted(apply3(m, v) for v in spokes) == sorted(spokes) for m in turns),
)

# 8. the mirror is the bar: v -> g v-bar g-bar = -(g v g-bar) on pure v gives the 24 mirrors; the cube's 48 in all
neg = lambda m: tuple(tuple(-x for x in row) for row in m)  # noqa: E731
mirrors = {neg(m) for m in turns}
all_signed = set()
for p in itertools.permutations(range(3)):
    for sg in itertools.product((ONE, -ONE), repeat=3):
        all_signed.add(tuple(tuple(sg[r] if c == p[r] else 0 for c in range(3)) for r in range(3)))
report(
    lines,
    "8. the 24 turns and their 24 mirrors (the bar on pure v) are all 48 signed permutations: the cube's 48",
    len(mirrors) == 24 and set(turns) | mirrors == all_signed and len(all_signed) == 48,
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
