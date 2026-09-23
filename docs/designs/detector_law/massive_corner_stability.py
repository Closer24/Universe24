"""COMPUTATION on the algebra (a 6^3 periodic box in the rational form, floats;
not an engine run): the checkerboard mode under the two massive forms
(MASSIVE_RECORD.md section 3: form (A) grows at the corner, form (B) is bounded).

    PYTHONPATH=src python docs/designs/detector_law/massive_corner_stability.py

  (S) form (A), the self term on the w = 1/3 rule (the second draft's section 1):
      3 q (a_next + a_before) = q SUM6 - 3 p a_now
  (W) form (B), the pair on the six-neighbour term alone (DESIGN.md 4.1's uncompensated pair):
      3 den (a_next + a_before) = num SUM6,   den > num

Characters: (S) 2 cos omega = (2/3) SUM cos k_i - p/q, the corner 2 cos omega = -2 - p/q < -2 (grows);
            (W) 2 cos omega = (2 num / 3 den) SUM cos k_i, within [-2, 2] for every num < den (stable).
"""

import numpy as np


def sum6(a):
    return sum(np.roll(a, s, ax) for ax in range(3) for s in (1, -1))


def run(form, p, q, steps, seed_amp=1.0, smooth_amp=2**20):
    n = 6
    x, y, z = np.meshgrid(*[np.arange(n)] * 3, indexing="ij")
    checker = ((x + y + z) % 2 * 2 - 1).astype(float)
    smooth = smooth_amp * np.cos(2 * np.pi * x / n)
    a_before = smooth.copy() + seed_amp * checker
    a_now = smooth * np.cos(0.3) + seed_amp * checker * (-1)
    peak = []
    for _t in range(steps):
        if form == "S":
            a_next = sum6(a_now) / 3 - (p / q) * a_now - a_before
        else:  # W with num = 2 q, den = 2 q + p (the same gap to first order)
            num, den = 2 * q, 2 * q + p
            a_next = num * sum6(a_now) / (3 * den) - a_before
        a_before, a_now = a_now, a_next
        peak.append(np.abs(a_now).max())
    return np.array(peak)


for p, q in ((1, 64), (1, 8)):
    ps = run("S", p, q, 200)
    pw = run("W", p, q, 200)
    rate = np.arccosh(1 + p / (2 * q))
    print(f"[p,q]=[{p},{q}] (the seed 1 unit of checkerboard on a smooth 2^20 record):")
    print(
        f"  (S) self-term form: peak |a| at t=50,100,200 = {ps[49]:.3e}, {ps[99]:.3e}, {ps[199]:.3e};"
        f" the characters' growth acosh(1 + p/2q) = {rate:.4f} per interval, e^(200 rate) = {np.exp(200 * rate):.2e}"
    )
    print(
        f"  (W) six-term pair [2q, 2q+p]: peak |a| at t=50,100,200 = {pw[49]:.3e}, {pw[99]:.3e}, {pw[199]:.3e} (bounded)"
    )

# the pace of the massive kind near k = 0 under (W): c_m^2 = c^2 num/den = c^2 cos omega0
c2 = 1 / 3
for num, den in ((128, 129), (32, 33), (16, 17), (8, 9), (2, 3)):
    om0 = np.arccos(num / den)
    print(
        f"(W) [num,den]=[{num},{den}]: omega0 = {om0:.4f} (N_0 = {2 * np.pi / om0:.1f}), c_m/c = sqrt(num/den) = {np.sqrt(num / den):.4f}"
        f" = 1 - {(1 - np.sqrt(num / den)) * 100:.2f} % ; the same c in the limit num/den -> 1"
    )
