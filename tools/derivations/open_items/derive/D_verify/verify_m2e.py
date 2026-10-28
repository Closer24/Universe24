"""Verifier's recomputation of draft D's M2e (part 4.4) with the verifier's own lattice code (verify_linearity.Ring):
no bob at B, A's remainder left at tick 0; per case (n, pair, answer) the alignment of B's axis with -a m1 and B's rho
against the fitted hand's. Integers only; ratios printed x 10^4 by integer division. Run: python3 -I -B verify_m2e.py"""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/D_verify")
from verify_linearity import Ring, CHI, LIGHT, set_bob, leave_remainder, reading  # noqa: E402

SETS = {"a": ((1, 0), (0, 0)), "a'": ((1, 0), (1, 0))}
PERPS = {"a": ((0, 0), (1, 0)), "a'": ((-1, 0), (1, 0))}
K, L = 4096, 6
for shape in ((14, 1, 1), (14, 3, 3)):
    rows = {}
    for n, chi in CHI.items():
        for x in ("a", "a'"):
            r1, m1 = reading([SETS[x][0][0], SETS[x][0][1], SETS[x][1][0], SETS[x][1][1]])
            for ans in (1, -1):
                lat = Ring(shape, *LIGHT)
                ia, ib = lat.ix[(0, 0, 0)], lat.ix[(L, 0, 0)]
                set_bob(lat, ia, tuple(tuple(K * v for v in z) for z in chi))
                rho_child = reading(lat.a[ia])[0]
                leave_remainder(lat, ia, PERPS[x] if ans == 1 else SETS[x])
                rho_rem = reading(lat.a[ia])[0]
                for t in range(1, 37):
                    lat.step()
                    if t in (6, 8, 12, 20, 36):
                        rb, sb = reading(lat.a[ib])
                        tgt = tuple(-ans * v for v in m1)
                        al = (rb * r1 + sum(p * q for p, q in zip(sb, tgt)), 2 * rb * r1)
                        rows.setdefault(t, []).append((al, rb, rho_child, rho_rem))
    print(f"[M2e, own code] light train, shape {shape}: per case (24 settings x n x answers = 24 cases with something written)")
    for t, cases in sorted(rows.items()):
        live = [c for c in cases if c[1] > 0]
        wnum = sum(c[0][0] for c in live); wden = sum(c[0][1] for c in live)
        worst = min(live, key=lambda c: c[0][0] * 10**8 // c[0][1]) if live else None
        share_max = max((c[1] * 10000 // c[2]) for c in cases)
        share_of_rem = max((c[1] * 10000 // c[3]) for c in cases if c[3])
        print(f"    Delta {t:2d}: weighted alignment x10^4 {wnum * 10000 // wden if wden else '-'}; worst case {worst[0][0] * 10000 // worst[0][1] if worst else '-'} (rho_B {worst[1] if worst else '-'}); "
              f"max rho_B / fitted hand x10^4 {share_max}; max rho_B / remainder x10^4 {share_of_rem}; empty B in {len(cases) - len(live)} of {len(cases)}")
