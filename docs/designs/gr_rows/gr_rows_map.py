"""The rows reading the crowd, the arithmetic (read-only, the mathematician, 2026-09-21;
docs/designs/gr_rows/DESIGN.md): the pins of the three general-relativity formulas
(the bending of light, the Shapiro delay, the second-order redshift) and what the
designed rule's integers give for each, on series K's worlds (examples/events/lensing)
and on the Sun; the cost of the map at one Node against K. No run; no fit.

Run from the repository root:

    python docs/designs/gr_rows/gr_rows_map.py > docs/designs/gr_rows/gr_rows_map.out
"""

from __future__ import annotations

import math

Q, T_D = 64, 110  # the pace's grain and the heading's wall: c = Q / T_D Links per interval
C0 = Q / T_D
DWELL = T_D / Q  # intervals per Link on a heading, 1.72

# Series K's worlds (the lensing README): the lamp at x = 2, the mass at x = 28, the screen at x = 54;
# the age moment per Node at the beam's impact distance b at the pair [1, 1] (the README's table).
WORLDS = [
    ("mass", 2**12, 6, 11.4),
    ("heavy", 2**13, 6, 22.7),
    ("near", 2**12, 3, 22.7),
]
X_LAMP, X_MASS, X_SCREEN = 2, 28, 54

# Nature, one source each (DESIGN.md section 1).
GM_SUN = 1.32712e20  # m^3 s^-2, the Sun's gravitational parameter (IAU 2015 nominal)
R_SUN = 6.957e8  # m, the Sun's radius (IAU 2015 nominal)
C_SI = 299_792_458.0
AU = 1.495978707e11

print(
    "1. THE PINS ON THE SUN (nature's numbers): k = G M / (r c^2) at the limb, the deflection 4 k, the Shapiro delay's coefficient 2 G M / c^3"
)
k_limb = GM_SUN / (R_SUN * C_SI**2)
arcsec = 180 / math.pi * 3600
print(
    f"   k at the limb = {k_limb:.3e}; Newton's deflection 2 k = {2 * k_limb * arcsec:.3f} arcsec; Einstein's 4 k = {4 * k_limb * arcsec:.3f} arcsec (Dyson, Eddington and Davidson 1920: 1.98 +- 0.16 and 1.61 +- 0.40; VLBI: gamma = 0.99992 +- 0.00012, Lambert and Le Poncin-Lafitte 2011)"
)
r1, r2, b = (
    AU,
    8.43 * AU,
    1.6 * R_SUN,
)  # the Cassini geometry, roughly: the Earth, Saturn, the ray 1.6 solar radii from the limb
shapiro = 2 * GM_SUN / C_SI**3 * math.log(4 * r1 * r2 / b**2)
print(
    f"   the Shapiro delay at Cassini's geometry (Earth at 1 au, Saturn at 8.43 au, the ray at {b / R_SUN:.1f} solar radii): (2 G M / c^3) ln(4 r_1 r_2 / b^2) = {shapiro * 1e6:.0f} microseconds; Cassini's gamma - 1 = (2.1 +- 2.3) x 10^-5 (Bertotti, Iess and Tortora 2003)"
)
print(
    "   the second-order redshift: nature's 1 + z = 1 / sqrt(1 - 2 k) = 1 + k + (3 / 2) k^2 + (5 / 2) k^3 ...; the law today 1 + z = 1 + k exactly (the clock at 1 / (1 + k), 5.2)"
)
print()

print(
    "2. THE RULE'S INTEGERS ON SERIES K'S WORLDS: the rows' pair is the clock's suspension pair [n_s, d_s]; series K registers suspension 0 (the rows blind, 0.000 kept); the pin world at [1, 256]"
)
N_S, D_S = 1, 256
print(
    f"   [n_s, d_s] = [{N_S}, {D_S}]: k(b) = (n_s / d_s) x (the age moment at b); the wall of the flight 2 T_D (d_s + 2 n_s A) / d_s; the deflection 4 k(b); the delay (2 k(b) b / c) ln(4 r_1 r_2 / b^2)"
)
print(
    "   world | M | b | k(b) | the deflection 4 k(b), radians | the centroid's shift on the screen, pixels (26 Links past the mass) | the delay, intervals | the mean age (89.40 registered) | the lamp's own clock at r = 26, its rate | the phase rate read (8 registered)"
)
for name, m_content, b_links, a_moment in WORLDS:
    k_b = N_S / D_S * a_moment
    deflection = 4 * k_b
    shift = deflection * (X_SCREEN - X_MASS)
    delay = 2 * k_b * b_links / C0 * math.log(4 * (X_MASS - X_LAMP) * (X_SCREEN - X_MASS) / b_links**2)
    k_lamp = k_b * b_links / (X_MASS - X_LAMP)
    rate_lamp = 1 / (1 + k_lamp)
    print(
        f"   {name:5s} | 2^{int(math.log2(m_content))} | {b_links} | {k_b:.4f} | {deflection:.4f} | -{shift:.2f} | {delay:.2f} | {89.40 + delay:.2f} | {rate_lamp:.4f} | {8 * rate_lamp:.3f}"
    )
print(
    "   the bracket of series K is 0.5 pixel and 1 interval: every shift and every delay above is outside it, toward the mass and later, and the two grow together with k(b) as one number"
)
print(
    "   the factor 2 is the rule's one new integer: at [n_s, d_s] with the factor 1 (Newton's) the shifts and the delays are half of the above; Cassini's bound reads the factor as 2 to 2 x 10^-5"
)
print()

print(
    "3. THE TURN ON THE FAN: the step at the light's directions (2.4 degrees between (1, 0, 0) and (24, +-1, 0)), the mean turn as a fraction of one step, the rows that turn one step under the wheel's dither"
)
step = math.atan(1 / 24)
for name, _m_content, _b_links, a_moment in WORLDS:
    k_b = N_S / D_S * a_moment
    fraction = 4 * k_b / step
    print(
        f"   {name:5s}: the mean turn {4 * k_b:.4f} rad = {fraction:.2f} steps of {step:.4f} rad; of 122 rays about {min(122, round(122 * (fraction - math.floor(fraction))))} turn one more step than the rest; the centroid's mean exact, the per-ray turn whole"
    )
print()

print(
    "4. THE SECOND-ORDER REDSHIFT: not the rows' rule (a static crowd stretches no stream); the clock's owed rate with one bilinear term, w = k' + (3 / 2) k'^2 in integers (2 k n d + 3 k^2 n^2) / (2 d^2)"
)
for k_prime in (1 / 16, 1 / 64, 1 / 1000, 2.1e-6):
    law_today = 1 + k_prime
    quadratic = 1 + k_prime + 1.5 * k_prime**2
    gr = 1 / math.sqrt(1 - 2 * k_prime)
    print(
        f"   k' = {k_prime:.2e}: 1 + z today {law_today:.7f}, with the quadratic term {quadratic:.7f}, nature's {gr:.7f}; the residual {quadratic - gr:+.1e} (the third order, (5 / 2) k'^3 = {2.5 * k_prime**3:.1e})"
    )
print(
    "   the pin: a lamp at k' = 1 / 16 read by a clock at k' = 0: 1 + z = 1.0625 today, 1.0684 with the term, nature's 1.0690; the rate at most bilinear in the state (k x k), no root"
)
print()

print(
    "5. THE MAP AT ONE NODE, THE COST AGAINST K (the operations per row per interval; 13.1's counts for the walk 16 and the reading 26 per row read)"
)
rows = [
    (
        "the Node's moments of the other numbers' rows (the presence, the flow V, the age moment A)",
        "26 per row read, once per Node per interval; today only at Nodes with a body, under the rule at every Node with a row",
    ),
    ("the wall of the flight: 2 T_D (d_s + 2 n_s A), one multiply and one add", "2"),
    ("the walk against the wall (the carry, the deficits)", "16 (today's)"),
    (
        "the turn accumulators per transverse axis: w_a += 2 n_s T_D V_a, two multiplies and two adds",
        "4",
    ),
    (
        "the step of the direction label when |w_a| crosses the wall d_s Q^2 x step (a comparison per axis, the fan's neighbour by the table)",
        "2 + the table's lookup",
    ),
    ("the wheel's dither of the accumulator at birth: one multiply and one division", "2, once per row"),
]
for what, cost in rows:
    print(f"   {what:120s} | {cost}")
print(
    "   the store per row: two integers (the turn accumulators); nothing at the Node (the moments are readings of the rows present, recomputed per interval)"
)
print()
print(
    "6. THE VERDICT: REACHABLE IN FORM for the bending and the delay (one identity, optical-v1: the flight's wall and the turn read the crowd's age moment and flow at the row's Node with the clock's pair and the factor 2), the pin series K at [1, 256]; the second-order redshift a companion term on the clock's rate, not the rows'; the run waits on the owner's go and the physics-rule review"
)
