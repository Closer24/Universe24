"""The grain form of doppler-v1 and the oblique weight, on the G2 star
worlds' numbers (the mathematician, 2026-09-20, read-only; standalone
integers, the flight table's pace from the engine's `flight_table`, the
one import). Output beside this file: `grain_map.out`.

The star of `examples/events/hubble_stars/gravity_none.json` on
`claude/series-g2-stars` (5322dc4): a lamp family's body of amount 4096
holding 4 194 304 of `mass` (the content M = 4 198 400 = K), width
S = 2^20, `release` [1, 65536] (64 units of mass per direction per
interval), momenta from 9 715 512 228 193 to 114 460 878 438 400 label
units on one axis; the reader of a mass row is another star of the same
content (its `read` entry on `mass`, the gravity column, E n = M x 1).
"""

from __future__ import annotations

import math
from fractions import Fraction

from event_universe.events.nature_beam import flight_table

Q = 64
S = 2**20
M = 4096 + 4194304
K = 4198400
CEILING = 2**62 - 1
G = 2**12  # the grain of the speed, 1 / 4096 Links per interval (the choice of section 1)
MOMENTA = (9715512228193, 13104644400819, 16573520859859, 108365328699077, 114460878438400)
T_HEADING = math.isqrt(3 * Q * Q)  # 110; the heading's pace (N, T) = (32, 55)


def bits(x: int) -> float:
    return math.log2(x) if x > 0 else float("-inf")


def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


section("1. The exact pair against the grain form, one mass row (amount 64) read by a star")
V = 64 * Q  # the label flow of one row of amount 64 on a heading
E_n = M  # the gravity column: the reader's content times the value 1
print(
    f"Q S M = {Q * S * M} = 2^{bits(Q * S * M):.1f}; |V| = {V}; |E n| = {E_n} = 2^{bits(E_n):.2f}; |V E n| = 2^{bits(V * E_n):.2f}"
)
print(
    f"{'p':>16s} {'D_a':>18s} {'v = p/D':>9s} {'exact pair product bits':>24s} {'w = G p // D':>12s} {'grain weight':>26s} {'flow product bits':>18s} {'bias of v':>10s}"
)
for p in MOMENTA:
    D = Q * S * M + p
    v = Fraction(p, D)
    exact_num = 32 * D - 55 * p  # receding along +x from a row on +x: s p > 0
    exact_product = V * E_n * abs(exact_num)
    w = (G * p) // D
    grain_num = G * 32 - 55 * w  # the pair (|G N_d - T_d s w|, G N_d) on a heading, receding
    flow_product = V * abs(grain_num)
    print(
        f"{p:16d} {D:18d} {float(v):9.5f} {bits(exact_product):24.1f} {w:12d} {grain_num:>8d}/{G * 32:<8d}={float(Fraction(grain_num, G * 32)):.5f} {bits(flow_product):18.1f} {float(v - Fraction(w, G)):10.2e}"
    )
print(
    f"the register's ceiling 2^62; the exact pair's product refuses every star (2^{bits(V * E_n * 32 * (Q * S * M)):.0f}); the grain form's flow product is 2^30 and then today's push 2^{bits(V * E_n):.0f}."
)
print(
    f"the bias of the quantised speed is below 1 / G = {1 / G:.2e} Links per interval, downward in |v|; the weight's bias below T / (G N) = 55 / {G * 32} = {55 / (G * 32):.2e} of the rate on a heading."
)

section("2. Bit-identity at rest and the bounds of the grain form")
print(
    "at p = 0: w = 0, the pair is (G N_d, G N_d) = 1 exactly, by_clock(age, |V| x G N_d, G N_d) = |V|: bit-identical to today's flow, so to today's push, for every fixed body and every free body at rest."
)
worst_num = G * (4096 + 12288)  # N_d <= a Q <= 64 Q = 4096; T_d <= isqrt(3 x 3 x 64^2 x Q^2) = 12288
print(
    f"the numerator bound on any direction of the table: G (N_d + T_d) <= {worst_num} = 2^{bits(worst_num):.1f}; a flow of amount A on one direction: |V_d| x num <= A x Q x 2^{bits(worst_num):.1f} = A x 2^{bits(Q * worst_num):.1f}: fits for A up to 2^{62 - bits(Q * worst_num):.0f} per direction per interval."
)
print(
    "the load-time bound: none new beyond today's (the weighted flow is at most (1 + T_d / N_d) x the flow, at most 4.75 x on the heading and 3 x |D|^2 / a^2 ... on a fan direction; the static budget of the columns takes the flow's largest value times that factor)."
)

section("3. The oblique weight: per axis against the flux, a body moving on x")
headings = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
fan = ((1, 1, 0), (1, 1, 1), (2, 1, 0), (3, 1, 0), (5, 1, 0), (1, 2, 0), (0, 1, 1), (1, 3, 2))
table = flight_table(((0, 0, 0), (0, 0, 0)) + headings + fan)
v_test = Fraction(1, 3)  # the review's test speed on the fan diagonal (0.1875 against 0.594)
v_star = Fraction(114460878438400, Q * S * M + 114460878438400)
print(
    "for a direction D = (a, b, c) with T_d = isqrt(3 |D|^2 Q^2): the message's velocity is (Q / T_d) D per axis (Links per interval),"
)
print(
    "  the per-axis form (as built): 1 - v_x / c_{d,x} = 1 - v_x T_d / (Q a);  the flux form: 1 - (v . c) / |c|^2 = 1 - v_x T_d a / (Q |D|^2)"
)
print(
    f"{'direction':>12s} {'T_d':>5s} {'c_x':>8s} {'per-axis @1/3':>14s} {'flux @1/3':>10s} {'per-axis @star':>15s} {'flux @star':>11s} {'ratio of the v-terms':>21s}"
)
for index in range(2, 2 + len(headings) + len(fan)):
    D = tuple(int(x) for x in table.vectors[index])
    if D[0] <= 0:
        continue
    t_d = int(table.resolution[index])
    n2 = sum(x * x for x in D)
    c_x = Fraction(Q * D[0], t_d)

    def per_axis(v: Fraction, t_d: int = t_d, a: int = D[0]) -> Fraction:
        return 1 - v * t_d / (Q * a)

    def flux(v: Fraction, t_d: int = t_d, a: int = D[0], n2: int = n2) -> Fraction:
        return 1 - v * t_d * a / (Q * n2)

    print(
        f"{str(D):>12s} {t_d:5d} {float(c_x):8.4f} {float(per_axis(v_test)):14.4f} {float(flux(v_test)):10.4f}"
        f" {float(per_axis(v_star)):15.4f} {float(flux(v_star)):11.4f} {Fraction(n2, D[0] * D[0])!s:>21s}"
    )
print(
    "the per-axis form equals the flux form on a heading (|D|^2 = a^2) and overstates the Doppler term by |D|^2 / a^2 on every other direction:"
)
print(
    "  x 2 on a face diagonal, x 3 on a cube diagonal, x 26 on (5, 1, 0) read by a body moving on y ... (the term with the small component)."
)
print(
    "the flux form in the grain's integers, one scalar per (row direction, body), applied to the row's whole label vector:"
)
print(
    "  f_d = (G Q |D|^2 - T_d sum_a s_a w_a D_a) / (G Q |D|^2), w_a = G |p_a| // D_a per axis, s_a = sign(p_a);"
)
worst = G * (Q * 3 * 64 * 64 + 12288 * 192)
print(
    f"  the numerator bound G (Q |D|^2 + T_d S_1) <= {worst} = 2^{bits(worst):.1f}; a flow of amount A: A x Q x 2^{bits(worst):.1f}: fits for A up to 2^{62 - bits(Q * worst):.0f}."
)
