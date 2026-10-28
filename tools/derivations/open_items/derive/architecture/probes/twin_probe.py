# Probe for RULING 8 (iv): 2T's only 4-row signed-permutation action with centre -1 (induced from Z6)
# against the twin hands' E1/2 on four real rows (left multiplication on the quaternions). Exact, in halves.
from fractions import Fraction as Fr
import itertools
def qm(p, q):
    a1, b1, c1, d1 = p; a2, b2, c2, d2 = q
    return (a1*a2-b1*b2-c1*c2-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2, a1*c2-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2-c1*b2+d1*a2)
h = Fr(1, 2)
G = [tuple(Fr(s) if k == i else Fr(0) for k in range(4)) for i in range(4) for s in (1, -1)]
G += [tuple(h*s for s in sg) for sg in itertools.product((1, -1), repeat=4)]
assert len(G) == 24
inv = lambda q: (q[0], -q[1], -q[2], -q[3])
gen = (h, h, h, h); H = [(Fr(1), Fr(0), Fr(0), Fr(0))]
for _ in range(5): H.append(qm(H[-1], gen))
chi = {H[k]: (-1) ** k for k in range(6)}
assert qm(H[-1], gen) == H[0] and len(set(H)) == 6
ind = lambda g: Fr(sum(chi.get(qm(qm(x, g), inv(x)), 0) for x in G), 6)
W = lambda g: 4 * g[0]                      # trace of left multiplication: the twin hand's E1/2 on 4 rows
diff = [(g, ind(g), W(g)) for g in G if ind(g) != W(g)]
print('centre acts as -1 in Ind:', ind((Fr(-1), Fr(0), Fr(0), Fr(0))) == -4)
print('elements where the induced (signed-permutation) character differs from E1/2 on four rows:', len(diff))
print('example:', [(tuple(str(c) for c in g), str(i), str(w)) for g, i, w in diff[:2]])
