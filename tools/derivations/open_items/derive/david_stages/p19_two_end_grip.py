"""David's p19: the Boss's two-end grip (6488223224 item 2) against the law's per-end gearing, beside p13.

usage: python3 -I p19_two_end_grip.py
Four forms of light's step at a Node-clock i, each a coefficient on (phi_j - phi_i) / h^2 per Mesh to a neighbour j,
counted per round of the great clock (a beat at N_i of the rounds enters squared, as N_i^2):
  the law's: every beat at the full rate, the gears' W reading the ruler at i's own count, N_i^4 (p13's per-end form);
  (c) split: the beat at N_i and W reading Y_i^2, N_i^2 x N_i^2;
  the Boss's two-end grip: the beat at N_i and the grip g0 p_i p_j / Gamma^2, N_i^2 x N_i N_j;
  (c) with the vacuum's grip: the beat at N_i alone, N_i^2.
Each is set against general relativity's wave operator on the law's metric N A = 1, phi_tt = N^4 phi'', at h = 2 pi / n
for n from 64 to 1,024 (a form that is the operator misses by h^2), and its coordinate speed is read in a uniform N.
Floats: a continuum statement read on its lattice, as p13; no engine is run.
"""
import math


def lapse(x):
    return 1 + 0.3 * math.sin(x)


FORMS = {
    "the law's, the gears reading the ruler, N_i^4": lambda ni, nj: ni**4,
    "(c) split, the beat and W at Y^2, N_i^2 N_i^2": lambda ni, nj: ni**2 * ni**2,
    "the Boss's two-end grip, N_i^2 N_i N_j": lambda ni, nj: ni**2 * ni * nj,
    "(c) with the vacuum's grip, N_i^2": lambda ni, nj: ni**2,
}
for name, form in FORMS.items():
    errors = []
    for n in (64, 256, 1024):
        h = 2 * math.pi / n
        worst = 0.0
        for i in range(n):
            x = i * h
            ni = lapse(x)
            lattice = sum(form(ni, lapse(x + s * h)) * (math.cos(2 * (x + s * h)) - math.cos(2 * x)) for s in (1, -1)) / h**2
            target = ni**4 * (-4 * math.cos(2 * x))
            worst = max(worst, abs(lattice - target))
        errors.append(worst)
    speeds = [math.sqrt(form(n_, n_)) for n_ in (0.9, 0.99)]
    print(f"{name}: largest error {errors[0]:.2e} at n = 64, {errors[1]:.2e} at 256, {errors[2]:.2e} at 1,024; "
          f"speed in a uniform N 0.9 and 0.99: {speeds[0]:.4f}, {speeds[1]:.4f} (N^2: 0.8100, 0.9801)")
print("so in a uniform slab the two-end grip reads light at N^2 as the law's form does, and in a gradient of N it")
print("misses general relativity's operator by order 1 (its extra 2 N^3 N' phi'), where the law's form misses by h^2")
