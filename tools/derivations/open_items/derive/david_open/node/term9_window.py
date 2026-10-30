"""Term 9's window: the notch's rest is a uniform background, the slot form's clicks read it in gamma, no strength
serves.

Whole numbers alone, every division Rule3's carry (tensor24.algebra.carry.carry), no root: a bound on a length is read
as a bound on its square.

(a) the readings in a tied background, in exact ratios: a uniform depth u_c on the 00 slot with each ii slot tied to it
    (v_c = -(gamma over 2) u_c, condition (i), which the notch laid as (f9 over 3) tr^2 keeps), and a small well du on
    top. The clocks read N^2 = 1 over (1 + u) and the spatial metric A^2 = 1 over (1 - gamma u) (G2's readings, tied
    at every order); against the far clocks and rods of the background, the well reads 1 - N^2 = 2 U and A^2 - 1 =
    2 gamma_obs U. The probe gives gamma_obs = (A^2 - 1) over (1 - N^2) at du = u_c over 10^9, against
    gamma (1 + u_c) over (1 - gamma u_c), for gamma 1 and 2;
(a2) the case (a) must tell apart: a background that is a change of coordinates (term 13's law above), the well's
    depth scaled with the clocks and rods, where the clicks read gamma_obs = gamma at every u_c;
(b) the notch's rest in the universe: u_c = 3 Omega_m (lambda H0 over c)^2 for a range lambda (the screened rest of a
    uniform density, 8 pi G rho lambda^2 over c^2), at Planck 2018's H0 = 67.4 km/s/Mpc and Omega_m = 0.315, for the
    range of a period of the universe's age (673 Mpc) and the least range the growth of structure allows (445 Mpc),
    and the gamma the clicks would read there at gamma = 1;
(c) Cassini's bound |gamma - 1| <= 2.3 x 10^-5 read as a bound on lambda^2, and the whole lambda in Mpc on each side;
(d) the gamma that a chosen value would need to cancel the rest at 673 Mpc, against Postulate 6's gamma = 1.

Usage: python3 -I term9_window.py <src of main at 0df0e8385>
"""

import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402


def places(num, den, digits):
    """num over den to the given places, rounded half up, num at least 0 and den above 0."""
    scale = 10**digits
    q = carry(2 * num * scale + den, 2 * den, 0)[0]
    whole, frac = carry(q, scale, 0)
    return f"{whole}." + str(frac).rjust(digits, "0")


# (a) gamma_obs in a tied background, exact ratios with du = u_c div 10^9 (u_c as p over q)
lines_a = []
for gamma in (1, 2):
    for p, q in ((0, 1), (1, 1000), (1, 50), (1, 10)):
        # u_c = p / q; du = 1 / (q 10^9) when p = 0, else p / (q 10^9); work in units of 1 / (q 10^9)
        unit = q * 10**9
        uc = p * 10**9  # u_c in those units
        du = p if p else 1
        # 1 - N^2 against the background's clocks: N^2 = (1 + u_c) / (1 + u_c + du)  ->  1 - N^2 = du / (1 + u_c + du)
        one_n_num, one_n_den = du, unit + uc + du
        # A^2 - 1 against the background's rods: A^2 = (1 - g u_c) / (1 - g u_c - g du)  ->  g du / (1 - g u_c - g du)
        a_num, a_den = gamma * du, unit - gamma * uc - gamma * du
        obs_num, obs_den = a_num * one_n_den, a_den * one_n_num
        form_num, form_den = gamma * (unit + uc), unit - gamma * uc
        lines_a.append(f"gamma {gamma}, u_c = {p}/{q}: gamma_obs {places(obs_num, obs_den, 6)}, the form"
                       f" gamma (1 + u_c) over (1 - gamma u_c) {places(form_num, form_den, 6)}")
print("(a) a well du = u_c over 10^9 on a tied background u_c (du = 10^-9 at u_c = 0): " + "; ".join(lines_a))

# (a2) the case the probe must tell apart: a background that is a change of coordinates (term 13's law above), where
# the well's depth and the clocks and rods scale together; there the clicks read gamma_obs = gamma at every u_c
lines_a2 = []
for gamma in (1, 2):
    for p, q in ((1, 1000), (1, 50), (1, 10)):
        unit = q * 10**9
        uc = p * 10**9
        du = p
        # the well's depth scaled with the background as the clocks are: du (1 + u_c) on the 00 slot, and on the rods
        # -gamma du (1 - gamma u_c) / (1 + u_c) times (1 + u_c): read against the background's clocks and rods the
        # well is du and gamma du, so the ratio is gamma
        one_n_num, one_n_den = du * (unit + uc), (unit + uc) * unit + du * (unit + uc)
        a_num, a_den = gamma * du * (unit - gamma * uc), (unit - gamma * uc) * unit - gamma * du * (unit - gamma * uc)
        obs_num, obs_den = a_num * one_n_den, a_den * one_n_num
        lines_a2.append(f"gamma {gamma}, u_c = {p}/{q}: gamma_obs {places(obs_num, obs_den, 6)}")
print("(a2) the mutant the probe must catch, a background read as a change of coordinates (the depth scaled with the"
      " clocks and rods): " + "; ".join(lines_a2))

# (b) the notch's rest in the universe: c over H0 in Mpc, u_c = 3 Omega_m (lambda over (c / H0))^2
C_KM = 299792458  # c in m/s; H0 = 67.4 km/s/Mpc, so c / H0 = 299792.458 / 67.4 Mpc = 299792458 / 67400 Mpc
H0_TENTHS = 674  # H0 in tenths of km/s/Mpc
# c / H0 in Mpc = C_KM / (1000 H0) = C_KM / (100 H0_TENTHS)
HUBBLE_NUM, HUBBLE_DEN = C_KM, 100 * H0_TENTHS
OMEGA_NUM, OMEGA_DEN = 315, 1000
print(f"(b) c over H0 = {places(HUBBLE_NUM, HUBBLE_DEN, 2)} Mpc at H0 = 67.4 km/s/Mpc, Omega_m = 0.315 (Planck 2018);"
      " ", end="")
lines_b = []
for lam in (673, 445):
    # u_c = 3 Omega (lam H0 / c)^2 = 3 OMEGA_NUM lam^2 HUBBLE_DEN^2 / (OMEGA_DEN HUBBLE_NUM^2)
    uc_num = 3 * OMEGA_NUM * lam * lam * HUBBLE_DEN * HUBBLE_DEN
    uc_den = OMEGA_DEN * HUBBLE_NUM * HUBBLE_NUM
    # gamma_obs - 1 at gamma = 1: (1 + u_c) / (1 - u_c) - 1 = 2 u_c / (1 - u_c)
    shift_num, shift_den = 2 * uc_num, uc_den - uc_num
    lines_b.append(f"lambda = {lam} Mpc: u_c = {places(uc_num, uc_den, 5)}, the clicks' gamma - 1 ="
                   f" {places(shift_num, shift_den, 5)},"
                   f" {places(shift_num * 100000, shift_den * 23, 0)} times Cassini's"
                   " 2.3 x 10^-5")
print("; ".join(lines_b))

# (c) Cassini: 2 u_c / (1 - u_c) <= 23 / 10^6, so u_c <= 23 / (2 10^6 + 23); lambda^2 <= (c / H0)^2 u_c / (3 Omega)
bound_num = 23 * OMEGA_DEN * HUBBLE_NUM * HUBBLE_NUM
bound_den = (2 * 10**6 + 23) * 3 * OMEGA_NUM * HUBBLE_DEN * HUBBLE_DEN
passes = [(lam, lam * lam * bound_den <= bound_num) for lam in (15, 16, 445)]
print(f"(c) Cassini's |gamma - 1| <= 2.3 x 10^-5 at gamma = 1 reads u_c <= 23 over (2 x 10^6 + 23) and lambda^2 <="
      f" {places(bound_num, bound_den, 2)} Mpc^2, no root taken: lambda = 15 Mpc (225 Mpc^2) passes: {passes[0][1]};"
      f" 16 Mpc (256 Mpc^2) passes: {passes[1][1]}; the structure's least, 445 Mpc (198025 Mpc^2), passes:"
      f" {passes[2][1]}: the window is empty: {not passes[2][1]}")

# (d) the gamma that would cancel the rest at 673 Mpc: gamma (1 + u_c) = 1 - gamma u_c, so gamma = 1 / (1 + 2 u_c)
uc_num = 3 * OMEGA_NUM * 673 * 673 * HUBBLE_DEN * HUBBLE_DEN
uc_den = OMEGA_DEN * HUBBLE_NUM * HUBBLE_NUM
print("(d) to cancel the rest at 673 Mpc a chosen gamma = 1 over (1 + 2 u_c) ="
      f" {places(uc_den, uc_den + 2 * uc_num, 5)}"
      " at that place and time alone, against Postulate 6's gamma = 1 (G2), and the rest swings with the notch")
