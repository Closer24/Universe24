"""The rows reading the crowd, the arithmetic (read-only, the mathematician, 2026-09-21;
docs/designs/gr_rows/DESIGN.md, amended per the physics-rule review of record 312): the
pins of the general-relativity formulas (the bending of light, the Shapiro delay, Snell's
law, the second-order redshift) and what the designed rule's integers give for each, on
series K's worlds (examples/events/lensing) re-scaled to the pin world of must-fix 7 (the
mass sixteen times the registered, the pair [1, 4096]) and on the Sun; the back-reaction
of the beam's own age moment on the crowd; the count ratio under the lamp's reading; the
rays the mass may take; the cost of the map at one Node against K. No run; no fit.

Run from the repository root:

    python docs/designs/gr_rows/gr_rows_map.py > docs/designs/gr_rows/gr_rows_map.out
"""

from __future__ import annotations

import math

Q, T_D = 64, 110  # the pace's grain and the heading's wall: c = Q / T_D Links per interval
C0 = Q / T_D
DWELL = T_D / Q  # intervals per Link on a heading, 1.72
F = 2  # the world's declared factor (the key optical: 2); the Newton world declares 1
G_GRAIN = 2**16  # the grain of THETA_G, a constant of the law at load
W = 4096  # the birth wheel

# The registered series K worlds (the lensing README): the lamp at x = 2, the mass at x = 28, the
# screen at x = 54; the age moment per Node at the beam's impact distance b at the pair [1, 1].
REGISTERED = [
    ("mass", 2**12, 6, 11.4),
    ("heavy", 2**13, 6, 22.7),
    ("near", 2**12, 3, 22.7),
]
X_LAMP, X_MASS, X_SCREEN = 2, 28, 54
SCALE = 16  # the pin world: sixteen rays per direction per interval (M x 16), the pair [1, 4096]
N_S, D_S = 1, 4096
BEAM_A_LOW, BEAM_A_HIGH = (
    45.0,
    77.0,
)  # the beam's own age moment per Node (the README's GameBoard readings, must-fix 7)

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
r1, r2, b_ray = AU, 8.43 * AU, 1.6 * R_SUN
shapiro = 2 * GM_SUN / C_SI**3 * math.log(4 * r1 * r2 / b_ray**2)
print(
    f"   the Shapiro delay at Cassini's geometry (Earth at 1 au, Saturn at 8.43 au, the ray at {b_ray / R_SUN:.1f} solar radii): (2 G M / c^3) ln(4 r_1 r_2 / b^2) = {shapiro * 1e6:.0f} microseconds; Cassini's gamma - 1 = (2.1 +- 2.3) x 10^-5 (Bertotti, Iess and Tortora 2003)"
)
print(
    "   the second-order redshift: nature's 1 + z = 1 / sqrt(1 - 2 k) = 1 + k + (3 / 2) k^2 + (5 / 2) k^3 ...; the law today 1 + z = 1 + k exactly (the clock at 1 / (1 + k), 5.2)"
)
print()

print(
    f"2. THE RULE'S INTEGERS ON THE PIN WORLD (must-fix 7): series K's worlds with the mass x {SCALE} ({SCALE} rays per direction per interval), the pair [n_s, d_s] = [{N_S}, {D_S}], the key optical: {F}"
)
print(
    "   the age moment at b scales with the mass: A = 16 x the README's; k_a(b) = n_s A / d_s; the wall 2 T_D (d_s + f n_s A); the deflection 2 f k_a(b); the delay (f k_a(b) b / c) ln(4 r_1 r_2 / b^2)"
)
print(
    "   the beam's own age moment A_beam = 45 to 77 per Node (a GameBoard reading of the README): the crowd's rows inside the beam read it, k_beam = A_beam / d_s, their pace 1 / (1 + f k_beam), their presence and age moment there up by the inverse: the back-reaction on what the beam reads"
)
k_beam_low, k_beam_high = BEAM_A_LOW / D_S, BEAM_A_HIGH / D_S
back_low, back_high = 1 + F * k_beam_low, 1 + F * k_beam_high
print(
    f"   k_beam = {k_beam_low:.4f} to {k_beam_high:.4f}; the crowd's pace inside the beam {1 / back_low:.3f} to {1 / back_high:.3f}; the back-reaction factor on A read by the beam {back_low:.3f} to {back_high:.3f}"
)
print()
print(
    "   world | M | b | k_a(b) (derived) | the deflection 2 f k_a(b), radians (derived) | the centroid's shift, pixels, DETECTOR (the bracket 0.5) | the same with the back-reaction | the delay, intervals (derived) | the mean age, DETECTOR (89.40 registered; the bracket 1) | with the back-reaction | the lamp's clock rate at r = sqrt(26^2 + b^2), GAMEBOARD | the count ratio, DETECTOR (the bracket 1 percent) | the phase rate, DETECTOR (8 registered)"
)
PIN_ROWS = []
for name, m_content, b_links, a_registered in REGISTERED:
    m_pin = m_content * SCALE
    a_moment = a_registered * SCALE
    k_b = N_S / D_S * a_moment
    deflection = 2 * F * k_b
    shift = deflection * (X_SCREEN - X_MASS)
    delay = F * k_b * b_links / C0 * math.log(4 * (X_MASS - X_LAMP) * (X_SCREEN - X_MASS) / b_links**2)
    r_lamp = math.sqrt(
        (X_MASS - X_LAMP) ** 2 + b_links**2
    )  # the lamp at [2, 20 + b, 20], the mass at [28, 20, 20]: 26.7 and 26.2 Links
    k_lamp = k_b * b_links / r_lamp  # A falls as 1 / r
    rate_lamp = 1 / (1 + k_lamp)
    PIN_ROWS.append((name, m_pin, b_links, k_b, deflection, shift, delay, rate_lamp))
    print(
        f"   {name:5s} | 2^{int(math.log2(m_pin))} | {b_links} | {k_b:.4f} | {deflection:.4f} | -{shift:.2f} | -{shift * back_low:.2f} to -{shift * back_high:.2f} | {delay:.2f} | {89.40 + delay:.2f} | {89.40 + delay * back_low:.2f} to {89.40 + delay * back_high:.2f} | {rate_lamp:.4f} | {rate_lamp:.3f} | {8 * rate_lamp:.3f}"
    )
print(
    "   the sign: the turn accumulator w takes -V (the flux points away from the source, 5.1), so the step is toward the mass, negative in y on the screen (the README's convention)"
)
print(
    "   the factor: with optical: 1 (Newton's index) every shift and every delay above is halved; Cassini reads the factor as 2 to 2 x 10^-5"
)
print(
    "   the count ratio: the lamp's entry declares reads: age for the mass's family, so its self-creations are slowed by 1 / (1 + k_lamp) and its births with them (series E's reading): outside series K's 1 percent bracket in heavy, by the pin world's own declaration and not by the rows' rule"
)
print()

print(
    "3. THE TURN ON THE FAN: the step at the light's directions (2.4 degrees between (1, 0, 0) and (24, +-1, 0)), THETA_G = round(G x angle), the mean turn in steps, the wheel's share"
)
step = math.atan(1 / 24)
theta_g = round(G_GRAIN * step)
print(
    f"   G = 2^16, THETA_G(2.4 degrees) = {theta_g}; the wall per row (W - u) d_s Q^5 THETA_G / W is whole because Q^5 = 2^30 is a multiple of W = 2^12 (no remainder discarded at birth)"
)
for name, _m, _b, _k_b, deflection, _s, _d, _r in PIN_ROWS:
    fraction = deflection / step
    print(
        f"   {name:5s}: the mean turn {deflection:.4f} rad = {fraction:.2f} steps of {step:.4f} rad; of 122 rays about {min(122, round(122 * (fraction - math.floor(fraction))))} turn one more step than the rest; the centroid's mean exact over records, the per-ray turn whole"
    )
print(
    "   the bound of the rate: f n_s T_D G Q^2 |V| within 2^62 - 1 asks |V| <= 2^62 / (f n_s T_D G Q^2) = "
    f"{2**62 // (F * N_S * T_D * G_GRAIN * Q * Q):.2e} label units at [1, 4096]'s n_s = 1, tested by division before the product as the meeting's (iv); the pin world's |V| at b is of order 10^3"
)
print()

print(
    "4. THE RAYS THE MASS MAY TAKE (should-fix 10): the turn before x = 28 lowers a ray by about theta b / 2; the beam's lowest ray at the mass's plane sits b - 26 / 12 Links from the mass's row of Nodes (the (12, -1, 0) direction)"
)
for name, _m, b_links, _k, deflection, _s, _d, _r in PIN_ROWS:
    lowest = b_links - 26 / 12
    drop = deflection * b_links / 2
    print(
        f"   {name:5s}: the lowest ray at {lowest:.1f} Links, lowered by {drop:.2f}: clears the mass's Node by {lowest - drop:.1f} Links"
        + (
            ""
            if lowest - drop > 1
            else "; the (12, -1, 0) share, one fifth of the rays, may enter the mass's Node: the centroid's bracket must allow it"
        )
    )
print()

print(
    "5. THE SECOND-ORDER REDSHIFT AS A DETECTOR PIN (must-fix 8, should-fix 9): two lamps at k'_1 and k'_2 read at one screen, 1 + z = (1 + w_1) / (1 + w_2) with w = k' + (3 / 2) k'^2 in integers (2 k n d + 3 k^2 n^2) / (2 d^2)"
)
for k1, k2 in ((1 / 16, 1 / 256), (1 / 64, 1 / 1024), (1 / 1000, 1 / 16000)):
    w1, w2 = k1 + 1.5 * k1**2, k2 + 1.5 * k2**2
    today = (1 + k1) / (1 + k2)
    quadratic = (1 + w1) / (1 + w2)
    gr = math.sqrt((1 - 2 * k2) / (1 - 2 * k1))
    print(
        f"   k'_1 = {k1:.2e}, k'_2 = {k2:.2e}: the phase-rate ratio today {today:.7f}, with the term {quadratic:.7f}, nature's {gr:.7f}; the residual {quadratic - gr:+.1e} (the third order, (5 / 2) k'_1^3 = {2.5 * k1**3:.1e})"
    )
print(
    "   the bound of 3 k^2 n_s^2: k the age moment at a dense Node (the nucleon's 57 rows at ages of hundreds, k of order 10^4) times n_s, within 2^62 tested at the frame; the term under the same key optical, so series E (k = 2 to 9 at [1, 1], the added wait 6 to 121) is unchanged without it"
)
print()

print(
    "6. THE MAP AT ONE NODE, THE COST AGAINST K (the operations per row per interval; 13.1's counts for the walk 16 and the reading 26 per row read)"
)
rows = [
    (
        "the Node's moments of the other numbers' rows: A (the age moment, two columns) and V (the flow, three): five of the table's thirteen columns",
        "about 12 per row read when computed alone (26 where a body at the Node reads the whole table), once per Node per interval, at every Node with a row",
    ),
    ("the wall of the flight: 2 T_D (d_s + f n_s A), one multiply and one add", "2"),
    (
        "the walk against the wall (the carry, the deficits), the position accumulator now a field of the row",
        "16 (today's)",
    ),
    (
        "the turn accumulator w += -f n_s T_D G (Q^2 V - (V . u) u): a dot product, a scale, three multiplies, three adds",
        "10",
    ),
    (
        "the projections on the fan's neighbours of D: p = w . t(D, D') against (W - u) d_s Q^5 THETA_G / W, one per neighbour",
        "2 per neighbour, 4 to 6 neighbours",
    ),
    ("the step to D' and the remainder kept: w -= t(D, D') d_s Q^3 THETA_G", "3, at a step"),
]
for what, cost in rows:
    print(f"   {what:140s} | {cost}")
print(
    "   the store per row: four integers (the position accumulator with its residue, the three of w); nothing at the Node (the moments are readings of the rows present, recomputed per interval); the host's segmented sums reported apart (the meeting's 4.6 ms per interval on mass, note 35 (vii), the reference)"
)
print()

print(
    "7. SNELL'S LAW AT A BOUNDARY OF TWO CROWDS: n = 1 + f k_a the pace ratio; the rule's turn across the boundary is Delta theta = -(n_2 - n_1) tan theta_1 (Fermat's ray equation at n near 1); Snell's n_1 sin theta_1 = n_2 sin theta_2"
)
print(
    "   the pin before the numbers: the rule gives Snell to first order in n_2 - n_1 = f (k_2 - k_1), the residual of order (n_2 - n_1)^2; the sign toward the denser crowd; no world yet makes a slab of crowd (a crowd of M / r has no sharp boundary): the pin is the ray equation's, Snell in the limit of a thin transition"
)
for k2 in (1 / 256, 1 / 64, 1 / 16):
    n2 = 1 + F * k2
    for theta1_deg in (30.0, 60.0):
        theta1 = math.radians(theta1_deg)
        theta2_snell = math.asin(math.sin(theta1) / n2)
        theta2_rule = theta1 - (n2 - 1) * math.tan(theta1)
        print(
            f"   k_2 = 1/{round(1 / k2):d} (n_2 = {n2:.5f}), theta_1 = {theta1_deg:.0f} deg: Snell's theta_2 = {math.degrees(theta2_snell):.3f} deg, the rule's {math.degrees(theta2_rule):.3f} deg, the difference {math.degrees(theta2_rule - theta2_snell):+.3f} deg (order (n_2 - 1)^2 = {(n2 - 1) ** 2:.1e})"
        )
print(
    "   Fermat's least time: the rule is the ray equation d theta / dl = grad_perp(f k_a), Fermat's Euler-Lagrange form at n near 1; the fan's choice of direction (the Huygens fan of TWO_SLITS section 7) gives the least-time path as the click's stationary phase only if the row's phase advances per interval (a clock, the slits' declaration), not per Link"
)
print()
print(
    "8. THE VERDICT: REACHABLE IN FORM for the bending and the delay (one identity, optical-v1, keyed by the world's optical: f; the flight's wall and the turn read the crowd's age moment and flow at the row's own Node with the clock's pair), the pin the re-scaled series K at [1, 4096]; Snell to first order; the second-order redshift a bilinear term on the clock's rate under the same key; the build waits on the owner's go (record 303), form B on main, and the reviewer's re-read"
)
