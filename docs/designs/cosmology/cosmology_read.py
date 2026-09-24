"""The host arithmetic of COSMOLOGY_READ.md (CLOSER24, 2026-09-24).

Pure integers and fractions from the standard library; a root appears only
as an integer square root at a declared scale, a COMPUTATION on the host and
never a step of the law. Every number printed is a COMPUTATION on DATA or on
the algebra's closed forms, none a reading of any run. Run: python
docs/designs/cosmology/cosmology_read.py > docs/designs/cosmology/cosmology_read.out
"""

from fractions import Fraction as F
from math import isqrt

SCALE = 10**12


def root(x):
    """The square root of a non-negative fraction as a fraction, to 1e-6."""
    return F(isqrt(int(x * SCALE * SCALE)), SCALE)


def show(label, value, digits=4):
    print(f"{label}: {float(value):.{digits}f}")


print("1. The deceleration parameter q_0 = Omega_m / 2 - Omega_DE (1 + 3 w_0) / 2 from DATA")
rows = [
    ("Planck 2018 flat LCDM, Omega_m 0.3153 +- 0.0073", F(3153, 10000), F(6847, 10000), F(-1)),
    ("Pantheon+ flat LCDM, Omega_m 0.334 +- 0.018", F(334, 1000), 1 - F(334, 1000), F(-1)),
    (
        "DESI 2024 + CMB + Pantheon+, w_0 = -0.827 at Omega_m 0.31 (Omega_m RECALLED)",
        F(31, 100),
        F(69, 100),
        F(-827, 1000),
    ),
]
for label, om, ode, w0 in rows:
    q0 = om / 2 + ode * (1 + 3 * w0) / 2
    g1 = -q0 / (2 + q0)
    show(f"  {label}: q_0", q0)
    show("    the clocks' stretch gradient nature's q_0 would need, g_1 = -q_0 / (2 + q_0)", g1)
show("  the uncertainty of Planck's q_0 at fixed flatness, 3/2 x 0.0073", F(3, 2) * F(73, 10000))
show("  the uncertainty of Pantheon+'s q_0, 3/2 x 0.018", F(3, 2) * F(18, 1000))

print("2. The Hubble tension, DATA: 73.04 +- 1.04 (SH0ES 2022) against 67.36 +- 0.54 (Planck 2018)")
d = F(7304, 100) - F(6736, 100)
s2 = F(104, 100) ** 2 + F(54, 100) ** 2
show("  the difference", d)
show("  the difference over the combined error, squared", d * d / s2)
show("  the difference over the combined error", root(d * d / s2))
show("  the ratio 73.04 / 67.36", F(7304, 6736))
show(
    "  the crowd stretch difference k_B - k_B' the detector's own rate would need, H_d = r_B H",
    F(7304, 6736) - 1,
)

print("3. The baryon fraction from Planck's densities, Omega_b h^2 / (Omega_b h^2 + Omega_c h^2)")
show("  0.0224 / (0.0224 + 0.120)", F(224, 10000) / (F(224, 10000) + F(120, 1000)), 3)

print("4. The kinematic numbers at K = 3 on the lattice, beta_c = 1 / sqrt 3 (COMPUTATION)")
beta = root(F(1, 3))
show("  beta_c", beta, 5)
show(
    "  the law's one-way factor behind a receding emitter, (1 - beta) / (1 + beta) = 2 - sqrt 3",
    2 - root(F(3)),
    5,
)
show(
    "  its square, 7 - 4 sqrt 3 (the wave's energy share behind over ahead on a chain)",
    7 - 4 * root(F(3)),
    5,
)
show(
    "  the free emitter's product (1 + z_behind)(1 + z_ahead) = gamma_m^2 (1 - beta_c^2) at gamma_m 1.22606",
    F(122606, 100000) ** 2 * F(2, 3),
    5,
)
show(
    "  the bound emitter's product on row 4b's world, (1 - beta_c^2) / (f / f_0)^2 at f / f_0 = 0.7931",
    F(2, 3) / F(7931, 10000) ** 2,
    5,
)
show(
    "  the same product light's gamma would give, gamma(c)^2 (1 - beta_c^2) = 1 exactly",
    F(3, 2) * F(2, 3),
    5,
)

print(
    "5. Tolman's exponent: the surface brightness ratio times (1 + z), the law's 1 against nature's (1 + z)^-3"
)
for label, z1 in (
    ("row 4b's pin 1 + z = 1.9889", F(19889, 10000)),
    ("the ray law's 1 + beta_c", 1 + beta),
):
    show(f"  {label}: nature's (1 + z)^-3", 1 / z1**3)

print("6. The neutrino bounds over the electron's mass 0.511 MeV (DATA over DATA)")
show("  KATRIN 2025 0.45 eV / 0.511 MeV", F(45, 100) / F(511000), 9)
show("  DESI 2024 + CMB, the sum 0.072 eV over three, over 0.511 MeV", F(72, 1000) / 3 / F(511000), 9)

print(
    "7. Seeliger's history, the law's own crowd (DARK_ENERGY.md section 3 (b)): q_eff = 2 k_0 (3 - k_0) / (1 - k_0)^2"
)
for k0 in (F(1, 100), F(1, 10)):
    show(f"  at k_0 = {k0}", 2 * k0 * (3 - k0) / (1 - k0) ** 2)
