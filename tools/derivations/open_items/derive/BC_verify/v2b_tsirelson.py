"""BC verifier, part 2b: does the one formula's own carriage of held frames ever pass Tsirelson's bound?
Exact: S^2 > 8 tested as num^2 > 8 den^2.  Scans every tick to 34 for d = 4..12, and a direct scan of the mixing
weights (A end alpha phi_x + beta phi_y, B end beta phi_x + alpha phi_y) over beta/alpha = j/64, j = 0..128.
Run: python3 -I -B v2b_tsirelson.py
"""
import importlib.util, os, math
from fractions import Fraction as Fr
here = os.path.dirname(os.path.abspath(__file__))
def load(n, f):
    s = importlib.util.spec_from_file_location(n, os.path.join(here, f)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
v2 = load("v2", "v2_carriage3d.py")
T = 34
hist, R = v2.propagate(T)
def ints(a, b):
    den = a.denominator * b.denominator // math.gcd(a.denominator, b.denominator)
    return int(a * den), int(b * den)
over = []; best = (Fr(0), None)
for d in range(4, 13):
    ha = hb = Fr(0)
    for t in range(T + 1):
        ha += Fr(int(hist[t][R + d, R, R]), 3 ** t); hb += Fr(int(hist[t][R + d + 1, R, R]), 3 ** t)
        if ha == 0 and hb == 0:
            continue
        A, B = ints(ha, hb)
        s = v2.S_mixed(A, B)
        if s is None:
            continue
        if s.numerator ** 2 > 8 * s.denominator ** 2:
            over.append((d, t, float(s), float(hb / ha)))
        if abs(s) > best[0]:
            best = (abs(s), (d, t, float(hb / ha)))
print(f"held frames, d = 4..12, ticks 0..{T}: S^2 > 8 at {len(over)} (d, tick) cells; largest |S| = {float(best[0]):.5f} at (d, tick, ratio) {best[1]}")
for row in over[:12]:
    print("   past Tsirelson:", row)
rows = []
for j in range(0, 129):
    s = v2.S_mixed(64, j)
    rows.append((j, s))
past = [j for j, s in rows if s is not None and s.numerator ** 2 > 8 * s.denominator ** 2]
mx = max(rows, key=lambda r: abs(r[1]) if r[1] is not None else 0)
print(f"mixing scan beta/alpha = j/64: S^2 > 8 for j in {past[:3]}..{past[-3:] if past else []} ({len(past)} of 129); "
      f"max |S| = {float(abs(mx[1])):.5f} at j = {mx[0]}; |S| > 2 for {sum(1 for j, s in rows if s is not None and abs(s) > 2)} of 129")
