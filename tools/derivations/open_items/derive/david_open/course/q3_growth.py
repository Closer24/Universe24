"""The growth as a count: how many composite clocks a board of N Node-clocks can hold, and how its record grows per bang.

usage: python3 -I q3_growth.py
Read from the law's numbers alone (no act is run):
  - the cap (DAVID-TENSOR24-THE-CAP.md, section 1): a Node-clock holds at most m quanta of one matter train, m = 4 for the
    field beside its phase-reversed field (2 for one twin pair); the force carriers stack;
  - a composite clock holds at least two quanta, so the board holds at most N SUM m / 2 of them at once;
  - a whole click is one hand's carry, so a tick writes at most one click per hand: a swing of P = 2 pi sqrt(Gamma / 2)
    ticks writes at most N SUM m P clicks;
  - a hand crosses at most the cone, 1 / sqrt 6 Mesh a tick, so in one swing it meets only the hands within
    2 pi sqrt(Gamma / 12) Meshes, 2 pi times the count's reach;
  - the head's measured clicks per bang (the plan, section 8, item 5: 64, 96, 256 and 1,152, four bangs in a row);
  - K2 (a finite board's per-bang counts are eventually periodic) and K4 (the record grows at every bang that clicks).
"""
import math

GAMMA = 1000
P = 2 * math.pi * math.sqrt(GAMMA / 2)
reach = math.sqrt(GAMMA / 12)
print(f"Gamma {GAMMA:,}: the swing P = 2 pi sqrt(Gamma / 2) = {P:.1f} ticks; the reach sqrt(Gamma / 12) = {reach:.2f} Meshes;"
      f" a hand's way in one swing at most P / sqrt 6 = {P / math.sqrt(6):.1f} Meshes (2 pi times the reach,"
      f" {2 * math.pi * reach:.1f})")
print()
print("the room: composite clocks at once, at most N SUM m / 2 (m = 4 per matter train)")
print("  side    Node-clocks N     one train      two trains (one of each)")
for side in (32, 100, 1_000, 6_300, 7_937, 10_000):
    n = side**3
    print(f"  {side:>6,}  {n:>16,}  {n * 4 // 2:>16,}  {n * 4:>16,}")
need1 = 10**12 * 2 / 4
need2 = 10**12 / 4
print(f"  a trillion at once: N >= {need1:.1e} (side {need1 ** (1 / 3):,.0f}) with one train; N >= {need2:.1e}"
      f" (side {need2 ** (1 / 3):,.0f}) with two, one quantum of each per composite")
print()
print("the record: clicks per swing, at most N SUM m P (every hand clicking at every tick)")
for side in (32, 100, 1_000):
    n = side**3
    print(f"  side {side:>5,}: at most {n * 4 * P:,.0f} clicks a swing with one train; a trillion in the record after at"
          f" least {10**12 / (n * 4 * P):,.0f} swings")
print()
clicks = [64, 96, 256, 1152]
ratios = [b / a for a, b in zip(clicks, clicks[1:])]
gm = math.prod(ratios) ** (1 / len(ratios))
print(f"the head's clicks per bang {clicks}: the ratios {[round(r, 2) for r in ratios]}, their geometric mean {gm:.2f}")
for rho, label in ((ratios[-1], "the last ratio"), (gm, "the geometric mean"), (2.0, "a doubling")):
    j = math.ceil(math.log(10**12 / clicks[-1]) / math.log(rho))
    total = sum(clicks) + sum(clicks[-1] * rho**k for k in range(1, j + 1))
    print(f"  at {label} ({rho:.2f}): a bang of a trillion clicks at bang {4 + j}, the record then {total:.2e}")
print("  on a finite board K2 stops the growth at the room: the per-bang count turns periodic at most N SUM m P a swing,"
      " and the record grows by K4 alone, linearly")
print()
print("in nature's units, the swing is 2 pi times light's crossing of the reach:")
year_ly = 1.0
for reach_ly, label in ((1e8, "a hundred million light-years (lensing's bound)"), (1.4e10, "the Hubble radius")):
    print(f"  a reach of {label}: the swing {2 * math.pi * reach_ly / year_ly:.1e} years")
