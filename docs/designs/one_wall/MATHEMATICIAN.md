# One-wall-v1 (issue #605): the wall's 2 and the push's 2 are one term; the verdict on "4 with no declared 2"

The derivation mathematician, 2026-09-21, read-only, on the Boss's order
of 15:45Z. Nothing here is built or decided; the law on `main`
(ba775d2f) is unchanged. The manner is [DERIVATIONS_BEAM](../../DERIVATIONS_BEAM.md)'s
(the rule, the limit, the order of the expansion, the error term, the pin
before the run), the numbers of the lattice are the light-bending map's
([NOTE.md](../open_problems/light_bending/NOTE.md) sections 3 to 5 and
`light_bending_map.out`), and the arithmetic of the closed forms is in
one_wall_check.py (`docs/designs/one_wall/one_wall_check.py`, deleted 2026-09-26) (its output [one_wall_check.out](one_wall_check.out)).
Every symbol is named at its first use.

**The verdict in one line: REFUTED.** The claim of issue #605, "the wall
alone gives `2 G M / (b c^2)`, the push on the row's energy gives
`2 G M / (b c^2)`, the sum is Einstein's `4 G M / (b c^2)` with no
declared 2", counts one term twice: both are the time part of the weak
field (g_00, the potential in the clock), the first in the wave language
(Fermat's index) and the second in the ray language (the geodesic's
`Gamma^i_00`). No reading of a detector adds them (section 3). What
one-wall-v1 reaches, taken whole, is Newton's half, `2 G M / (b c^2)`,
with the Shapiro delay at half of nature's coefficient, consistently
(the post-Newtonian gamma = 0). The 4 needs the space part (a rule that
lengthens a ruler, first order in the potential), which no verb of the
six and no term of #605 supplies; declaring it is optical-v1's f = 2
(record 303), the declared 2 the issue set out to avoid.

## 1. The rule, as the issue states it, in the law's letters

The names. G is Newton's constant, M the mass (the content of the
source), b the impact parameter, c the speed of light (`1 / sqrt 3`
Links per interval in the limit, `c_h = 32 / 55` on a heading), r the
distance from the source, x the coordinate along the row's line, L the
half length of the line (26 Links in series K), k the dimensionless
potential `k = G M / (r c^2)`, A the age moment at a Node (5.1: `A = q /
(4 pi c^2 r)` in the continuum, q the source's rows per interval), **V**
the arrival flow at a Node (5.1: **V** `= -(Q c^2 / 1) grad A` with the
dwell `1 / c`, Q the label's scale), `[n, d]_susp` the world's
suspension pair (the clock's owed count), `[n, d]_rel` the release pair
(3.3), S the width of the push, K the number of directions of the fan,
E a row's energy (the magnitude of its label), **p** its momentum,
theta the deflection and tau the delay.

1. **The wall.** Every accumulator's wall is stretched by the crowd:
   `by_drive(acc, rate x d, wall x (d + n A))` with `[n, d]` the
   suspension pair, so a row's pace is `c_h / (1 + k_w)` with
   `k_w = (n / d)_susp A`. In the continuum this is a medium of index
   `n_opt = 1 + k_w` (a wave whose local pace is `c (1 - k_w)` at first
   order). The heading is untouched: a scalar enters only the wall.
2. **The push with the energy as the weight.** The row's vector
   accumulator gains `-E` **V** per interval (the body's `-M` **V** with
   E for M); with `E = |`**p**`| c` for a row the heading changes per
   interval by `d theta = E |V_perp| dt / |p| = c |V_perp| dt`, the same
   rule that gives a body `a = -G M / r^2` in 3.3 (`G = K (n / d)_rel /
   (4 pi S)`), so in the continuum `d theta / dl = -grad_perp Phi / c^2`
   with `Phi = -G M / r`, i.e. `d theta / dl = grad_perp k_p`,
   `k_p = G M / (r c^2)`, PROVIDED the row's turn divides by its weight
   as the body's step rule divides by `Q S M` (the design's choice; a
   different divisor changes the constant, never the form).
3. **The turn.** The heading moves to the fan direction nearest the
   accumulated momentum, a permutation on the fan: the ray's turn in the
   grain of the fan.

Two constants appear, `k_w` and `k_p`. From 5.1 and 3.3 exactly (the
check's part 3, in rationals):

    k_w / k_p = (n / d)_susp x S.

They are one constant if and only if the suspension pair is `[1, S]`,
which is also the condition under which the clock's redshift (5.2,
`k_a = G M / (r c^2)`) carries the same G as the orbit (3.3). The pin
worlds of the light-bending note declare `[1, 16384]` at `S = 4096`: there
the wall's constant is a quarter of the push's, a world with two G's; not
a defect of the derivation, an input to be declared once.

## 2. The three identities of the limit

**(i) The push IS Fermat's ray equation of the wall's index.** The
Hamiltonian of a wave in the index `n_opt(x)` is `H = c |p| / n_opt`;
its force is `dp / dt = -grad H = (c |p| / n_opt^2) grad n_opt = E grad
k_w (1 + O(k))`, so `d theta / dl = grad_perp k_w`. Newton's push on a
particle of energy E at the speed c is `dp / dt = -(E / c^2) grad Phi =
E grad k_p`: the same force to first order, the same turn per Link,
`b / (b^2 + x^2)^(3/2)` per unit `G M / c^2` (the check's part 1: the two
sums equal to every printed digit at b = 3 and 6, L = 26 and 1000). Summed
over the line each gives

    theta = 2 (G M / c^2) L / (b sqrt(L^2 + b^2)) = (2 G M / (b c^2)) (1 - b^2 / (2 L^2) + O(b^4 / L^4)),

Newton's half. The 2 is the integral `int b dx / (b^2 + x^2)^(3/2) = 2 /
b^2`, a geometric 2, not a declared one; it is the SAME 2 in both
languages, because the ray equation of an index is the geodesic of the
metric whose time part is that index (`n_opt = 1 + k` is `g_00 = -(1 -
2 k)` for light, `Gamma^i_00 = d_i k`).

**(ii) The wavefront's tilt is the derivative of the Shapiro delay.** Under
the wall alone the delay of a row on the line at b is `tau(b) = (1 / c)
int k_w dl = (G M / c^3) 2 asinh(L / b) = (G M / c^3) ln(4 L^2 / b^2)
(1 + O(b^2 / L^2))`, and the tilt of the surface of equal arrival across
b is

    c |d tau / db| = 2 (G M / c^2) L / (b sqrt(L^2 + b^2)),

the turn's closed form of (i) exactly, at every L (the check's part 2).
So the wall's "deflection" is the derivative of its own delay, and the
push's deflection is the same number: one deflection, two readings.

**(iii) The delay has one source.** The push changes the heading and not
the pace, so it adds no first-order delay; the bent path's extra Links
are `O(theta^2 L)`, second order (the register's +0.50, +1.24, +0.31
intervals under the meeting, 5.4). Under the wall alone, the push alone
and both, the Shapiro coefficient is `G M / c^3`, one way, against
nature's `(1 + gamma) G M / c^3 ln(4 r_1 r_2 / b^2)` (the round trip
twice that): gamma = 0, half of nature's `2 G M / c^3`.

## 3. The four questions of the order

**(a) The deflection.** One row and a bundle on the lattice's lines at
series K's geometry (the lamp at x = 2, the mass at x = 28, the screen at
x = 54; b = 3 and 6; the fan of 290 directions; the beam in the mass's
plane, the fan's densest plane, NOTE section 4):

| Reading | Wall alone | Push alone | Both |
| --- | --- | --- | --- |
| The heading of one row, the continuum (`L -> infinity`) | 0 exactly | `2 G M / (b c^2)` | `2 G M / (b c^2)` |
| The heading at L = 26, the continuum | 0 | `0.974 x 2 G M / (b c^2)` (b = 6), `0.993 x` (b = 3) | the push's |
| The heading on the lattice (the flow summed over the crossings, the map's section C and D, per unit crowd and per unit `n / d`) | 0: the row stays on its line | 78.3 rad (b = 6, 47 crossings), 98.9 rad (b = 3, 63 crossings); at the pin world `[1, 16384]`, M = 2^16: 0.0742 and 0.0929 rad, the centroid -1.93 and -2.42 pixels (DETECTOR if run, the bracket 0.5) | the push's |
| The b exponent, 6 to 3 | none | the lattice 1.26 against the continuum's 2 (the plane's comb; the register under the meeting -2.30 against -1.79) | the push's |
| A bundle's wavefront tilt (the delay's gradient across b, section 2 (ii)) | `2 G M / (b c^2)` in the continuum; on the lattice see (c) | 0 (no pace changes) | the wall's |

At finite P (the fan of 290) and Q (64): the turn is a permutation to the
nearest fan direction, so a single row turns in whole steps of the fan
(2.4 degrees the smallest of K's table) once its accumulator fills one
grain; below the grain the accumulated momentum is the remainder kept,
and a bundle's centroid reads the mean, which is the continuum's turn to
`O(1 / N_theta)` (N_theta the fan's grain) plus the comb of the lines. The
error term of the lattice at this fan is not small: 3.5 (b = 6) and 2.2
(b = 3) against the shell-mean closed form (the map's ratios), because a
row on a line reads the lines and not the shell mean (the lesson of
series T, NOTE section 4).

**(b) The Shapiro delay.** Against nature's one-way `(1 + gamma) (G M /
c^3) ln(4 r_1 r_2 / b^2)`:

| | Wall alone | Push alone | Both |
| --- | --- | --- | --- |
| The continuum, the coefficient of the logarithm | `G M / c^3` (gamma = 0, half of nature's) | 0 (second order, `O(theta^2 L / c)`) | `G M / c^3` |
| The form | `2 asinh(L / b) = ln(4 L^2 / b^2) (1 + O(b^2 / L^2))`: Shapiro's | none | Shapiro's |
| The lattice at series K (the map's D: `sum A / c_h` over the row's line, per unit `n / d` and per unit crowd) | 2834 intervals (b = 6), 2202 (b = 3); the continuum's 521 and 685; at `[1, 16384]`, M = 2^16: 2.68 and 2.17 intervals above the registered mean age 89.40 (the bracket 1) | 0 | the wall's |

The lattice's delay at this fan FALLS from b = 6 to b = 3 (2834 to 2202)
where the logarithm rises (521 to 685): the line at b = 3 crosses more
lines (63 against 47) but reads smaller ages (the sums 1281 against
1649). The form `M / r` integrated to a logarithm is the continuum's; at
series K's fan the comb decides, and the pin must be the lattice's
number, as the note's section 5 already states.

**(c) Does the wall turn a heading at all?** No, in the law's verbs: a
scalar enters only the wall (the flight accumulator's threshold), the
row's direction is a fan index that only the permutation verb changes,
and one row on one digital line at a variable pace stays on its line.
The registered 0.000 pixel of series K stands under the wall alone, byte
for byte in the centroid. What tilts is a bundle's surface of equal
arrival: the rows nearer the mass arrive later, so across the screen the
mean age per pixel has the gradient `d tau / db` of section 2 (ii). The
reading that sees it is a difference of two pixels' mean age (the
record's first moment in time), which is the reading of a two-element
interferometer (the VLBI's reading of the bending is exactly a delay
difference across a baseline); an angle `c |d tau / db| = 2 G M / (b
c^2)` in the continuum. It is NOT in the click's phase: the phase counts
Links and the wall changes no Link count ("the row's phase per Link
follows the flight"), so the fringes of series K stay where they are. At
series K's fan the two-pixel reading between b = 3 and b = 6 has the
comb's sign (the delay smaller at 3 than at 6): the reading needs a
denser fan or two pixels on lines of equal density, one Node apart, and
its pin is the lattice's difference of the sums, not the logarithm's
derivative.

**(d) One term or two, exactly, in the limit.** ONE. Both are the time
part `g_00` of the weak field: the wall is the index `1 + k` (the
coordinate pace of a wave whose period a slowed clock sets), the push is
`Gamma^i_00 = d_i k` (the geodesic's Newtonian term at `v = c`); the ray
equation of the index and the geodesic of the metric with that time part
are the same equation, and their deflections are the same integral (the
check's part 1, the difference 0 exactly, not to a tolerance). The space
part `g_ij = (1 + 2 gamma k) delta_ij` is what makes Einstein's 4 out of
Newton's 2, first order in k (the note's correction of 21.4 row E13 stands:
the post-Newtonian gamma, not the second-order field); it is absent from
the wall (a pace, not a length), from the push (Newton's force, no
`Gamma^i_jk v^j v^k` term) and from the turn (a permutation). Adding the
wall's 2 to the push's 2 is adding the wave form of one term to the ray
form of the same term. Where the two constants differ (`(n / d)_susp !=
1 / S`, section 1) they are still one term with two declared constants,
a world in which the delay's G and the turn's G differ, never a sum.

## 4. The verdict, and what would reach the 4

- **Refuted**: "wall 2 + push 2 = 4 with no declared 2". Each reading of
  a detector gives at most Newton's half: the centroid the push's 2, the
  wavefront's tilt the wall's 2, the Shapiro coefficient the wall's 1;
  none gives 4 (the check's part 4).
- **What is derived** from #605 taken whole, if built at `[n, d]_susp =
  [1, S]`: one consistent time-part metric for rows (gamma = 0): the
  bending `2 G M / (b c^2)` (the Sun: 0.876 arcsec against the measured
  1.751), the Shapiro coefficient `G M / c^3` (half), the redshift of 5.2,
  the rays normal to their wavefronts. Its merit over optical-v1 at f = 1
  is that the turn is the push's own verb with the energy as the weight
  (no second reading of the flow for rows), and that its two constants
  are the law's `[n, d]` and S, nothing new.
- **The hypothesis that reaches 4** must add the space part: a term
  first order in k that lengthens the path or the ruler, entering the
  deflection AND the delay together (`1 + gamma` in both, one gamma).
  On the GameBoard the Link is the ruler and no verb of the six reads
  it; the only way in form is to declare it, as `optical-v1`'s f = 2
  does (the wall stretched by `d + 2 n A`, or the push weighted by 2 E;
  either doubles both the tilt and the delay's coefficient at once, the
  one consistent declaration; doubling the turn alone would give the
  bending's 4 with Shapiro's half, which nature refutes: Cassini's gamma
  = 1.000021 +- 0.000023 is a delay measurement). An input row in 24.1,
  PPN gamma = f - 1, as the light-bending note proposes.

## 5. F08, the state in one line

F08 (the dictionary h against `h N_phi`, 6.4: Planck's constant the
declared quantum times the circle; the two energies one only under
17.6's constraint `h (n / d) = Q S / 3`) is OPEN as a calibration, exactly
as I left it in PR #594: no line of DERIVATIONS_BEAM changed for it, a fix
only on order.

## 6. Links

[Issue #605](https://github.com/Closer24/Universe24/issues/605);
[DERIVATIONS_BEAM 3.3](../../DERIVATIONS_BEAM.md#33-newtons-law-and-gs-place),
[5.1](../../DERIVATIONS_BEAM.md#51-the-two-fields-of-one-stream-and-the-equation-they-obey),
[5.2](../../DERIVATIONS_BEAM.md#52-the-clock-the-gravitational-redshift),
[5.4](../../DERIVATIONS_BEAM.md#54-light-no-optical-metric-on-main-the-meetings-turn-as-a-key)
and [21.4](../../DERIVATIONS_BEAM.md#214-the-einstein-map-every-result-of-the-special-and-the-general-theory-its-status-today-what-the-six-give-what-must-be-added-the-pin)
row E13; [the light-bending note](../open_problems/light_bending/NOTE.md)
and its map; [the optical-v1 design](../gr_rows/DESIGN.md); [HIGHLIGHTS
5.4](../../HIGHLIGHTS.md#54-the-detector), the decisions of 2026-09-21 on
optical-v1 (record 303), the three tests (record 202), the measurement
rule (record 281) and the method (record 300).
