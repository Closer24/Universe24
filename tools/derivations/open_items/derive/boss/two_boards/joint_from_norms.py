"""Are David's joint sizes (two_boards.py, toys-5 f3661f524) the Gaussian norms of one shared hand in two frames?

usage: python3 -I joint_from_norms.py

The twins' shared hand: psi = e1 x e2 - e2 x e1 (total zero), whole numbers. Each detector's frame is a Gaussian
integer u = x + iy: outcome + along (x, y), outcome - along (-y, x). The joint size of (s_A, s_B) is the square of the
overlap <a_s x b_t | psi> = a_s[0] b_t[1] - a_s[1] b_t[0], a whole number. Nothing typed but the four frames.
"""

from fractions import Fraction

FRAMES_A = {0: (1, 0), 1: (1, 1)}  # a = 1, a' = 1 + i
FRAMES_B = {0: (5, 2), 1: (5, -2)}  # b = 5 + 2i, b' = 5 - 2i
COS = {(0, 0): 21, (0, 1): 21, (1, 0): 20, (1, 1): -20}  # David's table, cosines over 29


def outcomes(u):
    x, y = u
    return {1: (x, y), -1: (-y, x)}


def david(x, y):
    k = COS[(x, y)]
    return [29 - k, 29 + k, 29 + k, 29 - k]


ok = True
for x in (0, 1):
    for y in (0, 1):
        a, b = outcomes(FRAMES_A[x]), outcomes(FRAMES_B[y])
        sizes = [
            (a[s][0] * b[t][1] - a[s][1] * b[t][0]) ** 2 for s, t in ((1, 1), (1, -1), (-1, 1), (-1, -1))
        ]
        mine = [Fraction(v, sum(sizes)) for v in sizes]
        his = [Fraction(v, 116) for v in david(x, y)]
        same = mine == his
        ok &= same
        e = sum(st * p for st, p in zip((1, -1, -1, 1), mine, strict=True))
        print(
            f"settings {x}{y}: norms {sizes} (sum {sum(sizes)}), David's {david(x, y)} over 116: equal {same}; E = {e}"
        )
s = sum(
    sg * sum(st * Fraction(v) for st, v in zip((1, -1, -1, 1), david(*k), strict=True)) / 116
    for k, sg in (((0, 0), 1), ((0, 1), 1), ((1, 0), 1), ((1, 1), -1))
)
print(f"all four equal: {ok}; S = {s}")
# The same frames with the twins' hands NOT shared (each twin its own hand, a product state): the largest |S| over a
# small set of hands, an illustration of Bell's bound of 2 and no proof of it.
best = Fraction(0)
for ha in ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)):
    for hb in ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)):
        tot = Fraction(0)
        for (x, y), sg in (((0, 0), 1), ((0, 1), 1), ((1, 0), 1), ((1, 1), -1)):
            a, b = outcomes(FRAMES_A[x]), outcomes(FRAMES_B[y])
            pa = {s: (a[s][0] * ha[0] + a[s][1] * ha[1]) ** 2 for s in (1, -1)}
            pb = {t: (b[t][0] * hb[0] + b[t][1] * hb[1]) ** 2 for t in (1, -1)}
            ea = Fraction(pa[1] - pa[-1], pa[1] + pa[-1])
            eb = Fraction(pb[1] - pb[-1], pb[1] + pb[-1])
            tot += sg * ea * eb
        best = max(best, abs(tot))
print(
    f"twins with separate hands (a product state), the largest |S| over 36 pairs of hands: {best} = {float(best):.4f}"
)
