"""H-Quartet-Carriage-1's one-Node test of the carriage algebra on the quartet's matrices (read through gram of the flagged copy, a reader's import): (a) G Gamma_a symmetric, J Gamma_a = Gamma_a J, J^T G J = G; (b) the two eigenspaces of Gamma_a are G-orthogonal, so the axial of any vector x is e (|P+ x|_G^2 - |P- x|_G^2) with P+- = (I +- Gamma_a) div 2 (checked on x = 2 P x so the halves are integers); (c) the one-Node step with the own coefficient S = 0 and no neighbours sends (now, before) = (A v, B J v) to (-B J v, A v): the axial's sign on the born axis kept exactly, the magnitude B^2 against A^2; (d) the leaver bound: for a per-line error e with every entry at most 1 in absolute value the G-norm is at most the largest row sum of |G| times 8, so the sign on the axis is kept while the kept part's G-norm exceeds it. Integers only.
Usage: python one_node_test.py <src of the flagged copy> <out.json>"""
import json
import sys

sys.path.insert(0, sys.argv[1])
from event_universe import gram  # noqa: E402

Q = 8
G, J = gram.gram(Q), gram.rotation(Q)
GAM = gram.axes(Q)
I = gram.identity(Q)


def T(m):
    return [list(r) for r in zip(*m)]


def mv(m, x):
    return gram.matvec(m, x)


def form(m, x, y):
    return gram.form(m, x, y)


out = {"G Gamma_a symmetric": [gram.matmul(G, g) == T(gram.matmul(G, g)) for g in GAM],
       "J Gamma_a = Gamma_a J": [gram.matmul(J, g) == gram.matmul(g, J) for g in GAM],
       "J^T G J = G": gram.matmul(T(J), gram.matmul(G, J)) == G,
       "Gamma_a^2 = I": [gram.matmul(g, g) == I for g in GAM],
       "Gamma_a Gamma_b + Gamma_b Gamma_a = 0 (a != b)": [gram.matmul(GAM[a], GAM[b]) == [[-x for x in r] for r in gram.matmul(GAM[b], GAM[a])] for a in range(3) for b in range(3) if a != b]}
# (b) a lattice of test vectors: every digit vector in {-1, 0, 1}^8 with at most three nonzero digits, doubled
import itertools
vectors = []
for picks in itertools.combinations(range(Q), 3):
    for signs in itertools.product((-1, 1), repeat=3):
        x = [0] * Q
        for p, s in zip(picks, signs):
            x[p] = 2 * s
        vectors.append(x)
held = 0
for a, g in enumerate(GAM):
    gg = gram.matmul(G, g)
    for x in vectors:
        gx = mv(g, x)
        plus = [(xi + gi) // 2 for xi, gi in zip(x, gx)]
        minus = [(xi - gi) // 2 for xi, gi in zip(x, gx)]
        assert form(G, plus, minus) == 0, "the eigenspaces are not G-orthogonal"
        held += form(gg, x, x) == form(G, plus, plus) - form(G, minus, minus)
out["axial = |P+ x|_G^2 - |P- x|_G^2 on the digit vectors"] = [held, 3 * len(vectors)]
# (c) the one-Node step at S = 0 with no neighbours: now' = -before, before' = now
A, B = 125, 144
kept = 0
for a, g in enumerate(GAM):
    gg = gram.matmul(G, g)
    v = gram.spin_vector(Q, a, 1) if hasattr(gram, "spin_vector") else None
    if v is None:
        break
    now, before = [A * x for x in v], [B * x for x in mv(J, v)]
    s0 = form(gg, now, now)
    now2 = [-x for x in before]
    s1 = form(gg, now2, now2)
    kept += (s0 > 0) == (s1 > 0)
    out["axial at the lay and after one step, axis %d" % a] = [s0, s1, "v.G.v", form(G, v, v)]
out["sign kept after the one-Node step"] = [kept, len(GAM)]
# (d) the leaver's bound
row_sum = max(sum(abs(x) for x in r) for r in G)
ones = [1] * Q
out["largest |G| row sum"] = row_sum
out["G-norm of the all-ones error"] = form(G, ones, ones)
out["bound 8 x row sum"] = 8 * row_sum
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps(out))
