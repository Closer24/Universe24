"""Draft D's M2e share recomputed two ways with the verifier's code: the draft's ratio of sums over every (n, setting,
answer), probability-0 answers included, and the same weighted by the first answer's Born odds. Integers only."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/D_verify")
from verify_linearity import Ring, CHI, LIGHT, set_bob, leave_remainder, reading  # noqa: E402
SETS = {"a": ((1, 0), (0, 0)), "a'": ((1, 0), (1, 0))}
PERPS = {"a": ((0, 0), (1, 0)), "a'": ((-1, 0), (1, 0))}
K, L = 4096, 6
for shape in ((14, 1, 1), (14, 3, 3)):
    acc = {}
    for n, chi in CHI.items():
        for x in ("a", "a'"):
            r1, m1 = reading([SETS[x][0][0], SETS[x][0][1], SETS[x][1][0], SETS[x][1][1]])
            psi = tuple(tuple(K * v for v in z) for z in chi)
            rc, sc = reading([psi[0][0], psi[0][1], psi[1][0], psi[1][1]])
            for ans in (1, -1):
                w = rc * r1 + ans * sum(p * q for p, q in zip(sc, m1))  # 2 rho rho_d P(ans): Born's odds of the answer
                lat = Ring(shape, *LIGHT)
                ia, ib = lat.ix[(0, 0, 0)], lat.ix[(L, 0, 0)]
                set_bob(lat, ia, psi)
                leave_remainder(lat, ia, PERPS[x] if ans == 1 else SETS[x])
                for t in range(1, 37):
                    lat.step()
                    if t in (6, 8, 12, 20, 36):
                        rb = reading(lat.a[ib])[0]
                        c = acc.setdefault(t, [0, 0, 0, 0])
                        c[0] += rb; c[1] += rc; c[2] += w * rb; c[3] += w * rc
    print(f"shape {shape}: rho at B over a fitted hand's x10^4 -- draft's way (every answer) / weighted by the answer's odds")
    for t, c in sorted(acc.items()):
        print(f"    Delta {t:2d}: {c[0] * 10000 // c[1]:5d} / {c[2] * 10000 // c[3]:5d}")
