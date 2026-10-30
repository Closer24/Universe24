"""Term 13, the frozen clock, on the slot form: where the strong field takes the clocks and the grips, in whole numbers.

Whole numbers alone, every division Rule3's carry, on the act (engine/mesh.py and engine/step.py at main 0df0e8385),
with the reads laid by hand as in g2_static.py: every row's teeth W = rest + the metric family's 00 slot (term 2),
every Spoke's grip = the grip + its axis's ii slot at both ends of its Mesh (term 3).

(a) the strong field's pull on the act: on a board of 6 by 6 by 6 the 00 slot laid at K U and every ii slot at
    -gamma G0 U, the grip g, U a whole field strong enough that some Meshes' grips reach 0 and pass it: the 00 row's
    pull is exactly K times the Laplacian of g U - gamma G0 U^2 at every Node-clock, no order dropped, for gamma 1
    and 2; so with u = U / S and g = 2 S G0, the field's law is the Laplacian of w = u - (gamma / 2) u^2;
(b) light where a grip vanishes and where it turns negative: a ring of 8 Node-clocks on one axis, light laid on four
    of them; with the Meshes at the ring's two ends of those four held at a grip of 0, the other four never move;
    with those Meshes at a small grip, light crosses; with one Mesh at a negative grip, the ring runs away;
(c) the static exterior in exact ratios (r in G M / c^2, M = 1):
    (c1) the slot form's own (the ii slots tied to the 00 slot, or pulled through grips that read them: at gamma = 1
         the two agree): w = u - u^2 / 2 = 2 / r, so u = 1 - x and the grip over g is x at r = 4 / (1 - x^2), the
         clocks reading N^2 = 1 / (2 - x) and light's coordinate speed squared N^2 x; at gamma 1 and 2 the grips
         vanish at r = 4 gamma, where u = 1 / gamma and N^2 = gamma / (1 + gamma);
    (c2) general relativity's static field in isotropic radius: the slot form's flux r^2 (grip / g) du / dr with
         u = N^-2 - 1 and grip / g = A^-2, against general relativity's own lapse equation's flux r^2 A dN / dr;
    (c3) general relativity's horizon read in the act's terms: N = 0 with A = 4, the grip g / 16, at r = 1/2;
    (c4) what a uniform shift of the 00 slot does to the clocks' reading of one depth: N_A^2 / N_B^2 - 1 across a
         depth of rest / 50, at a background of 0 and of plus and minus rest / 10;
    (c5) the slot form's spheres: the areal radius R = A r with A^4 = 1 / (1 - 4 / r) at gamma = 1, so R^4 =
         r^5 / (r - 4); its least over r = 401/100 to 20, and the most compact body it can hold, G M / (c^2 R), against
         the compactness of two neutron stars read by NICER under general relativity's metric.

Usage: python3 -I term13_frozen.py <src of main at 0df0e8385>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import mesh, step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

GRIP = 15162856759112389 * 1000 * 1000
REST = 6 * GRIP
matter_row, light_row, slot00, slot_xx = 0, 1, 2, 6  # rows as in g2_static.py: matter, light, the 00 slot, xx (yy, zz)
ROWS = 12
no_plan = Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
no_read = Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
reads_ii = Read(np.array([slot_xx, slot_xx, slot_xx + 1, slot_xx + 1, slot_xx + 2, slot_xx + 2], dtype=np.intp),
                np.ones(6, dtype=object), np.arange(6, dtype=np.intp))


def fraction(num, den):
    """A ratio in lowest terms, by Euclid's steps in carries, as num/den with den above 0."""
    if den < 0:
        num, den = -num, -den
    a, b = abs(num), den
    while b:
        a, b = b, carry(a, b, 0)[1]
    return f"{carry(num, a, 0)[0]}/{carry(den, a, 0)[0]}" if a else "0/1"


# (a) the strong field's pull on the act
nb6 = board((6, 6, 6))
sites6 = nb6.shape[1]
spokes6, meshes6 = geometry(nb6, 3)
S, G0, K = 1000, 7, 12
g = 2 * S * G0
seq = 20261030
U = []
for _ in range(sites6):
    _, seq = carry(1103515245 * seq + 12345, 2147483648, 0)
    U.append(carry(seq, 2 * S + 1, 0)[1])  # 0 to 2 S: u = U / S from 0 to 2, the grips 1 - (u_i + u_j) / 2 to -1
lay6 = Layout(nb6, spokes6, meshes6, np.full((1, 3 * sites6), g, dtype=object),
              Gearing(*(np.ones((ROWS, 1), dtype=object),) * 4), no_plan, no_read, reads_ii)
lines_a = []
for gamma in (1, 2):
    a_f = np.zeros((ROWS, sites6), dtype=object)
    a_f[slot00, :] = [K * x for x in U]
    for d in range(3):
        a_f[slot_xx + d, :] = [-gamma * G0 * x for x in U]
    f00 = mesh.pull(lay6, a_f)[slot00]
    w = [g * x - gamma * G0 * x * x for x in U]
    exact = all(int(f00[i]) == K * sum(w[int(nb6[k, i])] - w[i] for k in range(6)) for i in range(sites6))
    grips = [g - gamma * G0 * (U[i] + U[int(nb6[k, i])]) for i in range(sites6) for k in range(0, 6, 2)]
    lines_a.append(f"gamma {gamma}: the pull equals K Lap(g U - gamma G0 U^2) at all {sites6} Node-clocks: {exact};"
                   f" of the {len(grips)} Meshes, {sum(int(x > 0) for x in grips)} with a grip above 0,"
                   f" {sum(int(x == 0) for x in grips)} at 0 and {sum(int(x < 0) for x in grips)} below it")
print(f"(a) the 00 slot laid at {K} U and each ii slot at -gamma {G0} U, the grip g = 2 S G0 = {g}, U from 0 to 2 S"
      f" (S = {S}): " + "; ".join(lines_a))

# (b) light where a grip vanishes and where it turns negative: a ring of 8 on the x axis
nb8 = board((8, 1, 1))
sites8 = nb8.shape[1]
spokes8, meshes8 = geometry(nb8, 3)
ones = np.ones((ROWS, 1), dtype=object)
clock = Read(np.full(ROWS, slot00, dtype=np.intp), np.ones(ROWS, dtype=object), np.arange(ROWS, dtype=np.intp))


def ring(cut_grip, negative=None):
    """The ring's grips: GRIP on every +x Mesh but those from site 3 and site 7 (to sites 4 and 0), which carry
    cut_grip; with negative, the +x Mesh from site 1 carries that grip instead of GRIP."""
    grips = np.full((1, 3 * sites8), GRIP, dtype=object)
    grips[0, 3], grips[0, 7] = cut_grip, cut_grip
    if negative is not None:
        grips[0, 1] = negative
    return Layout(nb8, spokes8, meshes8, grips, Gearing(REST * ones, ones, ones.copy(), ones.copy()), no_plan, clock,
                  no_read)


def light_lay():
    a = np.zeros((ROWS, sites8), dtype=object)
    a[light_row, :4] = [10**6, -(10**6), 10**6, -(10**6)]
    return State(a, a.copy(), np.full((ROWS, sites8), carry(REST, 2, 0)[0], dtype=object),
                 np.zeros((ROWS, sites8), dtype=object))


def far_side(lay, rounds=4000):
    """The largest |light| on sites 4 to 7 over the rounds, and the round light first passes 10^60 (or 0)."""
    s, top, gone = light_lay(), 0, 0
    for t in range(1, rounds + 1):
        s = step.tick(lay, s)
        top = max(top, max(abs(int(v)) for v in s.a[light_row, 4:]))
        if max(abs(int(v)) for v in s.a[light_row]) > 10**60:
            gone = t
            break
    return top, gone


top0, gone0 = far_side(ring(0))
top_small, gone_small = far_side(ring(carry(GRIP, 100, 0)[0]))
top_neg, gone_neg = far_side(ring(GRIP, negative=-carry(GRIP, 2, 0)[0]))
print(f"(b) a ring of 8, light laid on sites 0 to 3 at 10^6 (alternating), 4,000 rounds: with the Meshes 3-4 and 7-0 at a"
      f" grip of 0, the largest |light| on sites 4 to 7 is {top0} (runs away: {bool(gone0)}); at a grip of g / 100,"
      f" {top_small} (runs away: {bool(gone_small)}); with every grip g but the Mesh 1-2 at -g / 2, light passes 10^60 at"
      f" round {gone_neg}")

# (c1) the slot form's own exterior, gamma = 1: x = p / q, r = 4 q^2 / (q^2 - p^2), u = 1 - x
rows_c1 = []
for p, q in ((1, 2), (1, 10), (1, 100), (1, 1000)):
    r_num, r_den = 4 * q * q, q * q - p * p
    u_num, u_den = q - p, q
    w_ok = (u_num * 2 * u_den - u_num * u_num) * r_num == 2 * 2 * u_den * u_den * r_den  # u - u^2 / 2 = 2 / r
    n2_num, n2_den = q, 2 * q - p  # N^2 = 1 / (2 - x)
    rows_c1.append(f"x = {fraction(p, q)}: r = {fraction(r_num, r_den)}, u = {fraction(u_num, u_den)}, grip / g ="
                   f" {fraction(p, q)}, N^2 = {fraction(n2_num, n2_den)}, light's speed squared"
                   f" {fraction(n2_num * p, n2_den * q)}; u - u^2 / 2 = 2 / r: {w_ok}")
rows_g = []
for gamma in (1, 2):
    # the grips vanish where 1 - gamma u = 0: u = 1 / gamma, w = u - (gamma / 2) u^2 = 1 / (2 gamma) = 2 / r
    rows_g.append(f"gamma {gamma}: the grips vanish at r = {4 * gamma}, u = {fraction(1, gamma)}, N^2 ="
                  f" {fraction(gamma, 1 + gamma)}")
print("(c1) the slot form's exterior at gamma = 1, w = u - u^2 / 2 = 2 / r: " + "; ".join(rows_c1) + "; "
      + "; ".join(rows_g))

# (c2) general relativity in isotropic radius, m = 1 / (2 r): N = (1 - m) / (1 + m), A = (1 + m)^2,
# dN / dr = (1 / r^2) / (1 + m)^2; the slot form's flux r^2 A^-2 d(N^-2) / dr = -2 r^2 A^-2 N^-3 dN / dr
rows_c2 = []
for r_num, r_den in ((1, 1), (2, 1), (4, 1), (10, 1)):
    m_num, m_den = r_den, 2 * r_num  # m = 1 / (2 r)
    one_p, one_m = m_den + m_num, m_den - m_num  # (1 + m) m_den, (1 - m) m_den
    # GR's flux r^2 A dN / dr = r^2 (1 + m)^2 (1 / r^2) / (1 + m)^2 = 1
    gr_num, gr_den = 1, 1
    # the slot form's flux: -2 / ((1 - m^2)^3) = -2 m_den^6 / (one_p one_m)^3
    sf_num, sf_den = -2 * m_den**6, (one_p * one_m) ** 3
    rows_c2.append(f"r = {fraction(r_num, r_den)}: the slot form's flux {fraction(sf_num, sf_den)}, general"
                   f" relativity's {fraction(gr_num, gr_den)}")
print("(c2) general relativity's static field in isotropic radius: the slot form's flux r^2 (grip / g) du / dr"
      " (constant where the slot form's 00 equation holds) against general relativity's r^2 A dN / dr: "
      + "; ".join(rows_c2))

# (c3) the horizon in the act's terms: r = 1/2, m = 1
print("(c3) general relativity's horizon at r = 1/2 (m = 1): N = 0/2, A = 4, the grip g / A^2 = g/16: the clocks'"
      " teeth W = rest / N^2 without bound at a finite grip; the slot form's field reaches u = 1 / gamma, W = (1 + 1 /"
      " gamma) rest, where its grips vanish")

# (c4) the reading of one depth against a uniform background
rows_c4 = []
for c_bar_num, label in ((0, "0"), (1, "+rest / 10"), (-1, "-rest / 10")):
    # W_A = rest + c_bar + rest / 50, W_B = rest + c_bar; N_A^2 / N_B^2 = W_B / W_A; the depth read: W_A / W_B - 1
    wb = 50 * (10 + c_bar_num)  # in units of rest / 500
    wa = wb + 10
    rows_c4.append(f"background {label}: W_A / W_B - 1 = {fraction(wa - wb, wb)}")
print("(c4) one depth of rest / 50 read by two clocks, W_A / W_B - 1 (the square of their rate's ratio, less 1): "
      + "; ".join(rows_c4) + " (a first-order dependence on the uniform part)")

# (c5) the least sphere of the slot form's exterior: R^4 = r^5 / (r - 4), r = k / 100
least = None
for k in range(401, 2001):
    num, den = k**5, 10**8 * (k - 400)  # (k / 100)^5 / (k / 100 - 4) = k^5 / (10^8 (k - 400))
    if least is None or num * least[2] < least[1] * den:
        least = (k, num, den)
k0, r4_num, r4_den = least
# the most compact body: (G M / (c^2 R))^4 = r4_den / r4_num, against NICER's 0.156 and 0.247 (their fourth powers)
nicer = ((156, "PSR J0030+0451, 1.34 solar masses at 12.71 km (Riley and others 2019)"),
         (247, "PSR J0740+6620, 2.072 solar masses at 12.39 km (Riley and others 2021)"))
rows_c5 = [f"{fraction(c, 1000)} for {name}: reachable {c**4 * r4_num <= r4_den * 1000**4}" for c, name in nicer]
print(f"(c5) the slot form's spheres at gamma = 1, R^4 = r^5 / (r - 4): the least over r = 401/100 to 20 at r ="
      f" {fraction(k0, 100)}, R^4 = {fraction(r4_num, r4_den)} (G M / c^2)^4, so no body more compact than"
      f" (G M / (c^2 R))^4 = {fraction(r4_den, r4_num)}, G M / (c^2 R) near 134 thousandths; the compactness G M / (c^2 R) "
      + "; ".join(rows_c5))
