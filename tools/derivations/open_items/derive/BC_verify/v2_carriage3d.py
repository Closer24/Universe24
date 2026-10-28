"""BC verifier, part 2: can the one formula's own light carry the detectors' frames to the two ends of the
fitting's Mesh, each frame at its own end (crux (i))?

Light per the law's dispersion (ALGEBRA.md line 33: cos w = (cos kx + cos ky + cos kz) / 3) on the cubic lattice:
    u(t+1) + u(t-1) = (1/3) * (sum of the six neighbours of u(t)).
Integers: v(t) = 3^t u(t) obeys v(t+1) = (sum of six v(t)) - 9 v(t-1).  The propagator is real and spin-blind, so a
frame phi launched at a detector arrives as G * phi.  Geometry on the x axis: the fitting's Mesh has its B end at
(0,0,0) and its A end at (1,0,0); detector A at (1+d,0,0), detector B at (-d,0,0).  So the A end holds
G(d) phi_A + G(d+1) phi_B and the B end G(d+1) phi_A + G(d) phi_B.
Two launches: an impulse (the frame shown once at tick 0) and a held frame (shown at every tick from 0: a setting
fixed before the fitting).  At each tick the fitting splits against what stands at its two ends (Animate's act),
the children carry their senses, and the far detectors click against their own frames (law 6, local).
Run: python3 -I -B v2_carriage3d.py
"""
import numpy as np
from fractions import Fraction as Fr
import importlib.util, sys, os, math

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("v1", os.path.join(here, "v1_algebra.py"))
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)

def propagate(T):
    R = T + 3
    n = 2 * R + 1
    prev = np.zeros((n, n, n), dtype=np.int64)
    cur = np.zeros((n, n, n), dtype=np.int64)
    cur[R, R, R] = 1                       # v(0) = delta, v(-1) = 0
    hist = [cur.copy()]
    for t in range(T):
        # no int64 wrap: bound the step's result before forming it
        assert 6 * int(np.abs(cur).max()) + 9 * int(np.abs(prev).max()) < 2 ** 63
        s = np.zeros_like(cur)
        s[1:, :, :] += cur[:-1, :, :]; s[:-1, :, :] += cur[1:, :, :]
        s[:, 1:, :] += cur[:, :-1, :]; s[:, :-1, :] += cur[:, 1:, :]
        s[:, :, 1:] += cur[:, :, :-1]; s[:, :, :-1] += cur[:, :, 1:]
        nxt = s - 9 * prev
        prev, cur = cur, nxt
        hist.append(cur.copy())
        assert np.abs(cur).max() < 2 ** 62
    return hist, R

def S_mixed(al, be):
    """S of Animate's act when the A end reads al phi_x + be phi_y and the B end be phi_x + al phi_y (integers)."""
    Es = []
    for x, y in v1.PAIRS:
        px, py = v1.REAL[x], v1.REAL[y]
        fA = v1.lin((al, 0), px, (be, 0), py)
        fB = v1.lin((be, 0), px, (al, 0), py)
        if v1.rho(fA) == 0 or v1.rho(fB) == 0:
            return None
        Es.append(v1.run(fA, fB, px, py)[0])
    return v1.chsh(Es)

def main():
    T = 34
    hist, R = propagate(T)
    for d in (4, 6, 10):
        print(f"== d = {d} (each end is d Meshes from its own detector, d+1 from the other) ==")
        G = lambda r, t: int(hist[t][R + r, R, R])          # G(r, t) = this / 3^t
        held_a = held_b = Fr(0)
        rows = []
        for t in range(T + 1):
            ga, gb = Fr(G(d, t), 3 ** t), Fr(G(d + 1, t), 3 ** t)
            held_a += ga; held_b += gb
            rows.append((t, ga, gb, held_a, held_b))
        print("  tick | impulse: G(d), G(d+1)  -> S |  held: sum G(d), sum G(d+1), ratio  -> S")
        for t, ga, gb, ha, hb in rows:
            if t < d or (t > d + 3 and t % 4 and t != T):
                continue
            def s_of(a, b):
                den = (a.denominator * b.denominator) // math.gcd(a.denominator, b.denominator)
                A, B = int(a * den), int(b * den)
                if A == 0 and B == 0:
                    return "nothing"
                s = S_mixed(A, B)
                return "nothing" if s is None else f"{float(s):+.4f}"
            ratio = "-" if ha == 0 else f"{float(hb / ha):+.4f}"
            print(f"  {t:4d} | {float(ga):+.3e} {float(gb):+.3e} -> {s_of(ga, gb):>8s} | "
                  f"{float(ha):+.4e} {float(hb):+.4e} {ratio:>8s} -> {s_of(ha, hb):>8s}")
    # bare-word front: G(d, d) = 3^-d exactly, and G(d+1, d) = 0
    print("== the front ==")
    for d in (4, 6, 10):
        print(f"  d = {d}: G(d, d) = {hist[d][R + d, R, R]} / 3^{d}; G(d+1, d) = {hist[d][R + d + 1, R, R]}")
    # parity: G(r, t) = 0 unless r = t mod 2
    bad = sum(int(hist[t][R + r, R, R] != 0) for t in range(T + 1) for r in range(0, T + 1) if (r - t) % 2)
    print(f"  parity: G(r, t) nonzero with r - t odd in {bad} cases (r, t <= {T})")
    # the frames fully mixed (equal weights at both ends): still setting-dependent
    print(f"== both ends read the same mixture phi_x + phi_y: S = {S_mixed(1, 1)} ({float(S_mixed(1, 1)):+.4f})")
    # dilution: a field g that does not depend on the settings also stands at the fitting (the source's own light,
    # the room's light); weight w relative to the held frames' alpha at d = 10, tick T
    d = 10
    ha = sum(Fr(int(hist[t][R + d, R, R]), 3 ** t) for t in range(T + 1))
    hb = sum(Fr(int(hist[t][R + d + 1, R, R]), 3 ** t) for t in range(T + 1))
    den = (ha.denominator * hb.denominator) // math.gcd(ha.denominator, hb.denominator)
    A, B = int(ha * den), int(hb * den)
    print(f"== dilution at d = {d}, tick {T}: held weights {float(ha):.4e} (own end), {float(hb):.4e} (other end) of a frame")
    for gname, g in (("z", ((1, 0), (0, 0))), ("x", ((1, 0), (1, 0))), ("y", ((1, 0), (0, 1))), ("(2+i, -1+3i)", ((2, 1), (-1, 3)))):
        def S_w(wn, wd):
            Es = []
            for x, y in v1.PAIRS:
                px, py = v1.REAL[x], v1.REAL[y]
                fA = v1.lin((A * wd, 0), px, (B * wd, 0), py)
                fB = v1.lin((B * wd, 0), px, (A * wd, 0), py)
                gg = v1.sc((A * wn, 0), g)          # w = (wn / wd) alpha, in units of the own-end weight
                fA = (v1.ga(fA[0], gg[0]), v1.ga(fA[1], gg[1])); fB = (v1.ga(fB[0], gg[0]), v1.ga(fB[1], gg[1]))
                Es.append(v1.run(fA, fB, px, py)[0])
            return v1.chsh(Es)
        lo, hi = Fr(0), Fr(64)
        if abs(S_w(64, 1)) > 2:
            print(f"  g = {gname}: |S| > 2 even at w = 64 alpha"); continue
        for _ in range(24):
            mid = (lo + hi) / 2
            if abs(S_w(mid.numerator, mid.denominator)) > 2:
                lo = mid
            else:
                hi = mid
        print(f"  g = {gname}: S(w=0) = {float(S_w(0, 1)):+.4f}, S(w=alpha) = {float(S_w(1, 1)):+.4f}; "
              f"|S| <= 2 once w > {float(lo):.3f} alpha = {float(lo * ha):.2e} of a frame")

if __name__ == "__main__":
    main()
