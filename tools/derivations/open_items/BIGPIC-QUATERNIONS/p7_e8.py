"""p7: the eight-part whole hand under its natural metric is the E8 lattice (Big Pic, 2026-10-30).

The order Z[root 2] 2O, eight whole rows (y = 2x). Its reduced norm N(x) = N0 + N1 root 2; the form Q = 2 (N0 + N1),
the trace of ((2 + root 2) / 2) N, is whole and even on the order, of determinant 1, and positive: even unimodular of
rank 8, which is E8 alone. The families mathematician found it first (boss-derive 78b82057b, fam_math item 9); this is
the check on my own basis. Run: python3 .../p7_e8.py (seconds; output p7_e8.txt).
"""

from qlib import TWO, det, exact, order_basis, report

lines = []
B, D, _ = order_basis()


def q_form(y):
    """Q(x) = 2 (N0 + N1) for x = y / 2, 2 x_t = a_t + b_t root 2: N0 = SUM (a^2 + 2 b^2) / 4, N1 = SUM a b / 2."""
    a, b = y[0::2], y[1::2]
    four_n0 = sum(u * u + TWO * v * v for u, v in zip(a, b, strict=True))
    two_n1 = sum(u * v for u, v in zip(a, b, strict=True))
    return exact(four_n0 + TWO * two_n1, TWO)


def add(u, v):
    return [p + q for p, q in zip(u, v, strict=True)]


G = [
    [exact(q_form(add(B[i], B[j])) - q_form(B[i]) - q_form(B[j]), TWO) for j in range(8)]
    for i in range(8)
]
diag = [G[i][i] for i in range(8)]
minors = [det([row[:k] for row in G[:k]]) for k in range(1, 9)]
lines.append("   the Gram matrix's diagonal: " + str(diag) + "; leading minors: " + str(minors))
report(
    lines,
    "1. the Gram matrix of the order's whole basis under Q is whole: each entry is an exact carry, and a "
    "remainder would have stopped the run",
    len(G) == 8,
)
report(lines, "2. its diagonal is even", all(exact(x, TWO) * TWO == x for x in diag))
report(lines, "3. its determinant is 1", det(G) == 1, str(det(G)))
report(lines, "4. its leading minors are all positive: the form is positive", all(m > 0 for m in minors))
lines.append("   so the eight-part whole hand under Q is an even unimodular lattice of rank 8: E8")

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
