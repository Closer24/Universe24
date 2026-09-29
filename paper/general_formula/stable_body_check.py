"""The stable body theorem in closed form (COMPUTED): the first-order functional on a Gaussian body of width R in three dimensions,
F(R) = a / R^2 - b / R^3 - c / R (the band's pressure, the binding hollow beyond its reach, gravity), its two critical points
R_-+ = (a -+ sqrt(a^2 - 3 b c)) / c, the minimum at R_+ and the saddle at R_-, the largest mass with a minimum M_max, and the
lattice check of the two kernels' constants on a box of 128^3 Nodes."""

import numpy as np

NUM, DEN = 4000, 6000
NB, DB = 5760, 6000
GAMMA = 6000
G = (DEN - NUM) / DEN
KAPPA = np.arccosh(3 * DB / NB - 2)
CONTACT = (
    3 * DB / (6 * (DB - NB))
)  # the binding kernel's weight per unit source, summed over the GameBoard
A = NUM / (
    2 * DEN
)  # the pressure per quantum of a Gaussian of width R in three dimensions, times 1 / R^2
B_UNIT = (
    (2 * G / GAMMA) * CONTACT / (2 * np.pi) ** 1.5
)  # times M / E_b: the contact well, 1 / R^3; the gain of 2 cos omega is 4 g Phi / Gamma, halved for the self-source
C_UNIT = (2 * G / GAMMA) * (3 / (4 * np.pi)) * np.sqrt(2 / np.pi)  # times M / E_g: Poisson's well, 1 / R
print(
    f"kappa {KAPPA:.3f} (reach {1 / KAPPA:.2f} Links), a = {A:.4f}, b = {B_UNIT:.3e} M / E_b, c = {C_UNIT:.3e} M / E_g"
)
print(f"M_max = a / sqrt(3 b c) x sqrt(E_b E_g) = {A / np.sqrt(3 * B_UNIT * C_UNIT):,.0f} sqrt(E_b E_g)")

# the GameBoard check of the constants: s_b -> 3 and s_g -> 1 with the constants above, on 128^3 at widths 3 to 6
N, D = 128, 3
ks = [2 * np.pi * np.fft.fftfreq(N) for _ in range(D)]
grid = np.meshgrid(*ks, indexing="ij")
lap = 2 * (D - sum(np.cos(k) for k in grid))
kb = 3 * DB / (NB * lap + 6 * (DB - NB))
with np.errstate(divide="ignore"):
    kg = np.where(lap > 0, 3.0 / np.where(lap > 0, lap, 1), 0.0)
coords = np.meshgrid(*[np.arange(N) - N // 2 for _ in range(D)], indexing="ij")
r2 = sum(c.astype(float) ** 2 for c in coords)
print(
    "GameBoard 128^3: width, pressure x R^2 / a, contact well x R^3 / b, Poisson well x R / c (each 1 in the continuum)"
)
for R in (3.0, 4.0, 6.0):
    phi = np.exp(-r2 / (2 * R * R))
    phi /= np.sqrt((phi**2).sum())
    rho = phi**2
    fr = np.fft.fftn(rho)
    K = sum(float(np.sum((phi - np.roll(phi, 1, ax)) ** 2)) for ax in range(D)) * NUM / (3 * DEN)
    Wb = (2 * G / GAMMA) * float(np.sum(rho * np.real(np.fft.ifftn(kb * fr))))
    Wg = (2 * G / GAMMA) * float(np.sum(rho * np.real(np.fft.ifftn(kg * fr))))
    print(f"   R {R:3.0f}: {K * R**2 / A:6.3f}  {Wb * R**3 / B_UNIT:6.3f}  {Wg * R / C_UNIT:6.3f}")

print(
    "the two critical points (Links) and the kind, per divisors and mass; '-' where a^2 < 3 b c (no minimum: the collapse)"
)
for E_b, E_g in ((2, 10), (10, 10), (20, 10), (50, 10), (200, 10), (None, 10), (2, None)):
    print(
        f"=== binding at {E_b}, gravity at {E_g}: M_max {A / np.sqrt(3 * B_UNIT * C_UNIT) * np.sqrt(E_b * E_g):,.0f} ==="
        if E_b and E_g
        else f"=== binding at {E_b}, gravity at {E_g} ==="
    )
    for M in (10000, 20000, 30000, 40000, 60000, 100000, 200000):
        b = B_UNIT * M / E_b if E_b else 0.0
        c = C_UNIT * M / E_g if E_g else 0.0
        if c == 0:
            print(
                f"   M {M:>7}: one critical point at R = 3 b / (2 a) = {3 * b / (2 * A):6.2f} Links, a saddle (a maximum along the dilation)"
            )
            continue
        disc = A * A - 3 * b * c
        if disc < 0:
            print(f"   M {M:>7}: - (a^2 - 3 b c = {disc:+.3f}; the collapse)")
            continue
        Rp = (A + np.sqrt(disc)) / c
        Rm = (A - np.sqrt(disc)) / c
        print(
            f"   M {M:>7}: minimum at {Rp:6.2f} Links"
            + (f", the saddle (the barrier) at {Rm:5.2f} Links" if b else "")
            + f"; W_g / (3 W_b) at the minimum {(c * Rp**2 / (3 * b)) if b else float('inf'):6.2f}"
        )
