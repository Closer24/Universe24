# The ring mean and the orbit's mean over one turn: the proof and the bound (the Ring Mean Mathematician, 2026-09-22)

The order (the Boss, 2026-09-22, about 10:15Z, on the model owner's referee
point 5 of the paper, "pass to the Boss for handling", record 883 of the log
as the Boss numbered it in the order; the log on `origin/main` at the base
commit below ends at record 877, so the record is cited by the number the
order gave it): the paper's Section 4 says that the mean push over one
closed turn of an orbit equals the ring mean (the orientation average of the
push at the orbit's radius) "only where the body's dwell is uniform in angle,
a sampling the paper does not prove". Prove the equality or give the bound,
in the law's integers where it can be and in the continuum limit where it
must be, apply it to the registered case (series D3), and give the paper its
one sentence.

Base commit: `4028b020b95512e796485d8b3e98522d39f82093` (`origin/main`,
"Merge pull request #830"). This file changes no rule, no world, no pin and
no code, and nothing here was run on the engine: every number below is
**GAMEBOARD by formula**, the arithmetic of the declared integers and of
the register's own recorded numbers, never a measurement; a number the
register holds from a detector is quoted with its kind, **DETECTOR**, and
its source line. Sources: [DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md)
sections 3.2 and 3.3 (the push and its shell mean), section 5.1 (the dwell
along a line) and entry 58 of section 21.5 (Kepler's laws under the six
points); `docs/designs/light_bending/STEP_ALGEBRA.md` section 9 on
branch `light-bending-algebra` (PR #821, head `23ef9ce9`, not yet on main, so
cited by path and not linked; the ring of starts and its mean); record 872 of [the log](../../LOG_2026-09-20.md) (where the
L1 incidence factor comes from); record 817 (Newton's and Kepler's forms on
the comparison side only); the paper's Section 4 ground paragraph in
`paper/general_formula/main.tex` on branch `claude/paper-owner-review-five`
(PR #802, head `735ee8c8`, line 469); the series D3 register
([examples/events/orbit_lamp/README.md](../../../examples/events/orbit_lamp/README.md),
[docs/EXPERIMENTS.md](../../EXPERIMENTS.md) "D3") and its paper row
(`paper/general_formula/NUMBERS.md` line 172).

## 0. The verdict, at the top

**PROVED in the continuum, BOUNDED on the lattice, and the equality the
paper doubted is not the true statement.** The mean push over one closed
turn equals the ring mean at one radius of the loop, exactly in the
continuum limit and for every closed turn, circular or not: the radius is
`r_* = <r^2>_theta / <r>_theta` on the plane (the `1 / r` push) and
`r_* = sqrt(<r^2>_theta)`, the equal-area radius, in space (the `1 / r^2`
push), where `<.>_theta` is the mean uniform in angle over the turn
(Theorem B, section 4). The proof needs only the area rule of a radial push,
which follows from the push being along the crowd's radial lines; Kepler's
second law is the comparison, not an input. What the paper wrote is a
different comparison, the orbit's mean against the ring mean at the loop's
angle-mean radius `r_bar = <r>_theta`, and there the sampling matters
exactly as the paper feared, with the sign and the size now known: the
orbit's mean is the smaller of the two by the factor
`r_bar^2 / <r^2>_theta`, which lies between `1 - e^2` and `1` for a loop
whose radius over the turn runs from `r_min` to `r_max`,
`e = (r_max - r_min) / (r_max + r_min)`, and equals `1` only where the
radius is constant in angle, the circle (Theorem B, step B6). On the
lattice the equality holds up to four named grain terms (Theorem A, section
3): the ring's Node count against `2 pi r` (Gauss's circle problem; on the
plane `68 / 75.40 = 0.902` at `r = 12` and `144 / 150.80 = 0.955` at
`r = 24`), the ring's incidence against the fan's L1 factor (the sums `144`
and `160` over the 120 lines against `154.5`), the drive's anisotropy at
the registered pace (`6.9` per cent, `0` as `v / c -> 0`) and one Node's
dwell per crossing of a line. The L1 incidence factor `F_L1` of record 872
multiplies both means alike and cancels from their ratio (section 1.3).
For series D3 the turn's extreme radii are not on record; the run's
whole-record extremes give `e <= 0.96` at `r = 12` and `e <= 0.70` at
`r = 24`, floors `0.07` and `0.51` on the factor, GAMEBOARD by formula,
which decide nothing, as the register's own word already says (section 5).
The paper's sentence, in its two forms, is in section 6.

## 1. The push as a body reads it on the GameBoard

### 1.1 The integers (DERIVATIONS_BEAM 3.2 and 3.3, lines 838 to 855 and 876 to 892)

The source B, a body of content `M_B` (the content, a count of units), sits
at the origin and holds a free family. The fan is a set of `K` primitive
integer directions; one direction is the vector **d** (the integer vector
the tree writes `D`), with `S_1(d) = abs(d_x) + abs(d_y) + abs(d_z)` its
Manhattan length and `abs(d)` its Euclidean length. Along each direction
runs one digital line `L_d`, the Manhattan walk of DERIVATIONS_BEAM line
321 (at step `j` the axis maximising `abs(d_i) (j + 1) - S_1 abs(x_i)`, the
lowest axis on a tie), one Node per Manhattan step, so that `L_d` has
`S_1(d) / abs(d)` Nodes per Euclidean Link and every Node of it lies within
one Link, in each coordinate, of the Euclidean line through the origin
along **d**. At each self-creation the source releases
`by_clock(age, M_B n, d)` units on every direction of the fan
(`nature_beam.py:3546-3566`), the same count per direction; a released row
walks its line one Link per step and is never split, so in the steady state
the amount arriving per interval is the same at every Node of the line
(DERIVATIONS_BEAM line 876: "the field along a beam is `1 / r^0`"). Call
that amount the line's flux `phi_d`; the fan's flux is `q = sum_d phi_d`
(`K M_B n / d` per interval, line 842).

A body A of content `M_A` at the Node **x** reads the label flow (DERIVATIONS
line 844; the tree's `V`, here **v** as the notation rule writes a vector)

    v(x) = sum over the lines L_d through x of phi_d u_d,

with **u**_d the direction table's unit vector along **d**, of length `Q`
within `1.35` per cent on every direction (line 845). The flow is a comb:
it is `phi_d u_d` on a Node of one line, the sum on a Node where lines
meet, and `0` on every Node off the fan's lines. The push per interval is
the gravity column of the coupling (line 846),

    f(x) = - M_A v(x)      (label units per interval; the momentum p_A += f),

and the drive steps the body one Link per `D / abs(p)` self-creations,
`D = Q S M_A + abs(p)` (line 850). The body reads only its own Node: the
push is LOCALITY-1's (its own record and the six neighbouring Nodes; the
arrivals are at the Node), the integers are bounded, and no Node keeps
anything. On the Node **x** of the line `L_d` the push is along **u**_d,
that is along **d**, and **x** lies along **d** within one Link, so the push
is radial to the angle `1 / r` at the distance `r = abs(x)`; write `f(x)`
plain for the push's magnitude toward the source, `M_A phi_d Q` on a Node of
`L_d`, and carry the tangential remainder, at most `f(x) / r`, as a grain
term (section 3, term (iv)).

### 1.2 The chain in the continuum (DERIVATIONS_BEAM 3.2)

The ring at the distance `r`, `abs(dist - r) < 1 / 2`, holds `N(r)` Nodes
and the fan's `K` lines cross it; DERIVATIONS_BEAM line 883 counts one
Node per line and writes the shell mean of the flow as `q Q / N(r)`,
`q Q / (2 pi r)` on the plane and `q Q / (4 pi r^2)` in space as
`N(r) -> 2 pi r` and `4 pi r^2`, with the lattice's count of Nodes on a
shell, Gauss's circle problem `N(r) = 2 pi r + O(r^theta)`,
`theta <= 131 / 208`, as the ripple (line 888). Newton's form
`a = - G M_B / r^2` with `G = K (n / d) / (4 pi S)` follows in that mean
(line 942) and is the comparison, never an input (record 817).

### 1.3 The L1 incidence factor `F_L1`, and whether it enters

Record 872 and STEP_ALGEBRA section 9 correct the count of section 1.2: a
line crosses a ring of width one Link not at one Node but at
`S_1(d) / abs(d)` Nodes on the mean over the ring's width, because the
arrival flow counts one arrival per Node per interval on each line and a
digital line has `S_1 / abs(d)` Nodes per Euclidean Link. The flow's shell
mean therefore carries the fan's mean of `S_1 / abs(d)`, the factor `F_L1`:
`1.436` over the 290 directions of series K's fan and `1.421` weighted by
the shells (record 872, GAMEBOARD by formula), `3 / 2` in the isotropic
limit in space (the mean of `abs(x) + abs(y) + abs(z)` over the unit
sphere), and on the plane `4 / pi = 1.2732` in the isotropic limit (the
mean of `abs(cos t) + abs(sin t)` over the circle, computed here) and
`1.2871` on series D3's fan of 120 in-plane primitive directions with
`0 < a^2 + b^2 <= 64` (computed here, section 5). So the ring mean of the
push a body reads is `F_L1 q Q M_A / (2 pi r)` on the plane and
`F_L1 q Q M_A / (4 pi r^2)` in space, not the continuum's `q Q M_A / (2 pi
r)`; the clock's presence per Node, the dwell `sqrt 3 abs(d) / S_1`,
cancels the incidence and the age moment's shell mean is the continuum's
(record 872); which of the two constants the law's gravity stands on is the
owner's open question (record 872) and is not touched here.

**Whether it enters this statement, and how.** `F_L1` is a property of the
fan's lines, the same at every Node of a line and the same for every way of
sampling the lines; it multiplies the ring mean and the orbit's mean by the
same factor (section 2: both means are sums of `phi_d` times a count of
Nodes on `L_d`, and the count carries `S_1 / abs(d)` in both). It therefore
cancels from the ratio of the two means, and every statement of sections 3
and 4 holds with it and without it. It enters only where a mean is set
against the continuum's `q / (2 pi r)` (section 1.2), which is record 872's
question and not this file's. What does enter is the ring's incidence at one
radius, the integer count `m_d(r_0)` of section 2.1, whose sum over the fan
at one `r_0` is not exactly `F_L1 K`: that is grain term (ii) of Theorem A.

## 2. The two means, exactly

### 2.1 The ring mean at the radius `r_0` (as STEP_ALGEBRA section 9 constructs it)

The ring `R(r_0)` is the set of Nodes **x** with `abs(abs(x) - r_0) <=
1 / 2` (the ring of section 9's starts and of DERIVATIONS_BEAM 3.2, width
one Link), `N(r_0)` its count of Nodes, and for each line `m_d(r_0)` the
integer count of Nodes of `L_d` inside the ring (`1` or `2` on series D3's
fan at `r_0 = 12` and `24`, computed here). The ring mean is the uniform
average over the ring's Nodes of the push toward the source, one Node one
vote:

    f_ring(r_0) = (1 / N(r_0)) sum over x in R(r_0) of f(x)
                = (M_A Q / N(r_0)) sum_d phi_d m_d(r_0).                    (2.1)

The second line is exact in the integers: the comb is `0` off the lines,
`M_A phi_d Q` on a Node of `L_d`, and a Node where two lines meet counts
each. With `sum_d phi_d m_d(r_0) = q F(r_0)`, `F(r_0)` the ring's own
incidence factor (whose mean over many radii is `F_L1`), and `N(r_0) =
2 pi r_0 (1 + rho(r_0))`, `rho` the ring count's ripple,

    f_ring(r_0) = F(r_0) q Q M_A / (2 pi r_0 (1 + rho(r_0)))   (the plane).  (2.2)

### 2.2 The orbit's mean over one closed turn, as the body samples it

The turn is the closed loop `C` of Nodes `x_1, ..., x_L` the body visits
from one crossing of the reference column to the next crossing in the same
sense (the recurrence series D3 reads: README.md lines 126 to 129, "the
mean spacing of successive crossings of the centre column in one
direction"), the angle about the source advancing by `2 pi`; `tau_j` is the
dwell at `x_j`, the integer number of intervals the body sits there (the
drive: `D / abs(p)` self-creations per Link, the momentum's direction and
the per-axis rows deciding the Link); `T = sum_j tau_j` is the period. The
orbit's mean is the dwell-weighted mean of what the body read, which is
what the time mean of the push is:

    f_orbit = (1 / T) sum_j tau_j f(x_j)
            = (M_A Q / T) sum_d phi_d tau_d(C),                             (2.3)
    tau_d(C) = sum over the j with x_j on L_d of tau_j,

`tau_d(C)` the body's whole dwell on the line `L_d` during the turn. The
second line is again exact in the integers, for the same reason as (2.1).
The dwell is not uniform in angle: on a non-circular loop the body moves
faster near the source and slower far from it, and on any loop the dwell
per Node is quantised (a whole number of self-creations per Link) and, under
the registered per-axis drive, depends on the local direction of the step
(section 3, term (iii)). Both means are radial magnitudes; the tangential
components are grain term (iv).

**Lemma 1 (every line is crossed; the plane).** If the loop `C` is a simple
closed 4-connected lattice path around the source (the body steps one Link
along an axis per step, so its path is 4-connected), then every line `L_d`
of the fan shares at least one Node with `C`, hence `tau_d(C) >= 1` for
every **d**. Proof: a simple closed 4-curve separates its complement into two
8-connected components (the digital Jordan theorem, Rosenfeld 1979), and
`L_d`, a 4-connected path from the origin (inside) to the GameBoard's edge
(outside), is in particular 8-connected, so it meets `C`. In space a line
generally misses a curve; there the loop's plane carries the statement,
both means restricted to the lines in that plane (the registered world is
the plane, `121 x 121 x 1`, with a fan of 120 in-plane directions).

**Lemma 2 (the crossing's dwell; the continuum of the lattice geometry).**
Let the body cross `L_d` with the Euclidean speed `v` in the local step
direction **e** (the loop's own integer direction, `S_1(e) / abs(e)` Nodes
per Euclidean Link), the angle between **e** and **d** being `chi`, so the
speed across the line is `v sin chi = v_t`, the body's tangential speed
about the source (the line is radial). The loop's Nodes near the crossing
form a band of Euclidean width `w = S_1(e) / abs(e)` across **e** (one Node
per unit area of the band, `S_1(e) / abs(e)` of them per Link along it);
the line's Nodes inside the band number `(S_1(d) / abs(d)) w / sin chi` on
the mean over the crossing's phase (the position of the crossing along the
line's Bresenham pattern), and the dwell per Node is `abs(e) / (S_1(e) v)`
(the body passes `v S_1(e) / abs(e)` Nodes per interval: `v` Euclidean
Links per interval at `S_1(e) / abs(e)` Nodes per Euclidean Link). The
product is the body's dwell on the line per crossing,

    tau_d = (S_1(d) / abs(d)) / v_t x (1 + g_d),                            (2.4)

the loop's own Manhattan factor `S_1(e) / abs(e)` cancelling and the
line's `S_1(d) / abs(d)` staying (this is why the incidence factor is the
fan's and not the loop's, section 1.3). The grain `g_d`: the count of a
line's Nodes inside a band differs from the band's length times the line's
density by less than one Node at each edge of the band, so the crossing's
dwell departs from its mean by at most two Nodes' dwell,
`abs(g_d) <= 2 tau_node / tau_d = 2 (abs(e) abs(d) v_t) / (S_1(e) S_1(d) v)
<= 2`. The bound is exact per crossing; the mean over the fan's crossings is
smaller when the crossings' phases are spread over the lines' patterns,
which is expected of a loop not aligned with the fan and is not proved here.

## 3. Theorem A: the circle of the lattice's kind

**Theorem A.** Let the loop `C` be a circle of the lattice's kind: every
Node of it within the ring `R(r_0)`'s half-Link of `r_0` (so at every
crossing `r = r_0` to the ring's width) and the time per unit angle constant
up to the grain, `r theta_dot = r_0 omega (1 + a_d)` at the crossing of
`L_d` with `abs(a_d) <= delta_a` (`theta_dot` the angular rate about the
source, `omega` its mean over the turn). Then

    f_orbit / f_ring(r_0) = [N(r_0) / (2 pi r_0)] x [sum_d phi_d S_1(d) / abs(d)
                             / sum_d phi_d m_d(r_0)] x (1 + eta),         (3.1)
    abs(eta) <= 2 delta_a + max_d abs(g_d) + 1 / r_0     (to first order),

and in the limit `r_0 -> infinity` at fixed fan, `v / c -> 0` and the
crossings' phases spread, every factor tends to `1`: the orbit's mean equals
the ring mean at `r_0`, up to the grain term named in (3.1).

**Proof, in the integers where it can be.**

A1 (exact). By (2.3) and Lemma 1, `f_orbit = (M_A Q / T) sum_d phi_d
tau_d(C)`, every line contributing.

A2 (the continuum of the crossing). By Lemma 2 at `v_t = r_0 omega
(1 + a_d)`: `tau_d(C) = (S_1(d) / abs(d)) (1 + g_d) / (r_0 omega
(1 + a_d))`, one crossing per line on a circle (a radial line meets a
star-shaped loop once).

A3 (the period). `T = integral of dtheta / theta_dot over the turn =
(2 pi / omega) (1 + a_bar)` with `abs(a_bar) <= delta_a`.

A4 (substitute). `f_orbit = (M_A Q / (2 pi r_0)) sum_d phi_d (S_1(d) /
abs(d)) (1 + g_d) / ((1 + a_d) (1 + a_bar))`, so `f_orbit = (M_A Q /
(2 pi r_0)) sum_d phi_d S_1(d) / abs(d) x (1 + eta')` with `abs(eta') <=
2 delta_a + max abs(g_d)` to first order.

A5 (divide by (2.1)). `f_ring(r_0) = (M_A Q / N(r_0)) sum_d phi_d
m_d(r_0)`; the quotient is (3.1), the term `1 / r_0` of `eta` being the
tangential remainder of section 1.1 (term (iv)). QED.

**The four grain terms, named.** (i) The ring's count against `2 pi r_0`:
`N(r_0) / (2 pi r_0) = 1 + rho(r_0)`, Gauss's circle problem, `rho =
O(r_0^(theta - 1))`; exact by formula on the plane: `N(12) = 68` against
`75.40` (`0.902`), `N(24) = 144` against `150.80` (`0.955`). (ii) The
ring's incidence at one radius against the fan's L1 factor: `sum_d phi_d
m_d(r_0)` against `sum_d phi_d S_1(d) / abs(d)`; on series D3's fan of
120 lines with equal flux per line, `144` at `r_0 = 12` and `160` at
`r_0 = 24` against `154.5 = 120 x 1.2871` (`1.073` and `0.966`), so that
the product of (i) and (ii), the ratio `f_orbit / f_ring(r_0)` of (3.1)
before `eta`, is `0.968` at `r_0 = 12` and `0.922` at `r_0 = 24`: on the
plane at these radii a perfect circle's orbit mean is below the lattice
ring mean by three and eight per cent (the ring holds fewer Nodes than
`2 pi r_0`, so its mean per Node is the larger), before (iii) and (iv). (iii) The dwell's non-uniformity in angle, `delta_a`: on a
lattice circle under the registered per-axis drive the Euclidean pace is
`9 / 41 = 0.2195` along an axis and `0.2346` on the diagonal (the drive's
per-axis form `v_i = p_i / (Q S M_A + abs(p_i))` at `abs(p) / (Q S M_A) =
9 / 32`, computed here; the register's `pace` and its "6.9 percent faster at
45 degrees", README.md lines 289 to 301), so `delta_a = 0.069` at the
registered pace and `0` as `v / c -> 0`; and one Node's dwell per crossing
of a line, `abs(g_d) <= 2 tau_node / tau_d`, on the plane at the registered
pace `tau_node = 4.556` intervals along an axis against the mean crossing
dwell `F_L1 / v_t = 5.86` intervals: a bound of order one per crossing,
smaller in the mean over 120 crossings if their phases are spread (not
proved). (iv) The tangential remainder, at most `1 / r_0`: `0.083` at
`r_0 = 12`, `0.042` at `24`, and `0` in the mean over the fan's 48 signed
axis permutations on a loop with the same symmetry (section 9's tangential
mean `0.00000` at every ring).

**What would break it.** A loop that is not 4-connected (a body stepping
diagonally: not in the law), a line crossing the loop where the body's step
runs along the line (then `sin chi -> 0`, `tau_d` grows and Lemma 2's bound
is on the count, not the dwell), or a fan whose lines meet at Nodes of the
ring (then a Node counts twice in both means alike, and nothing breaks).

## 4. Theorem B: a general closed turn, in the continuum

**The setting (the continuum limit, as DERIVATIONS_BEAM entry 58 takes
it).** Many lines per turn (`K -> infinity` with the fan's 48 symmetry, so
its density in angle is uniform to the fan's grain); the Link to zero
(`r -> infinity` in Links); small momentum (`v / c -> 0`, so the drive is
`v = p / (Q S M_A)`, isotropic, and the per-axis cap's anisotropy is gone).
The body's motion is then the central-push problem

    p' = - f(r) r_hat,   v = p / (Q S M_A),   f(r) = f_ring(r) = k / r^n,

`n = 1` on the plane (`k = F_L1 q Q M_A / (2 pi)`), `n = 2` in space
(`k = F_L1 q Q M_A / (4 pi)`), the push a body reads being the ring mean at
its radius once the lines are dense (Theorem A at every radius, the loop
crossing the lines at the rate `(K / 2 pi) theta_dot`, each crossing giving
the impulse `phi_d Q M_A (S_1 / abs(d)) / (r theta_dot)` by (2.4), the sum
per interval `F_L1 q Q M_A / (2 pi r)`).

**Theorem B.** For every closed turn of the central-push problem, with
`<.>_theta` the mean uniform in the angle `theta` over the turn (the
orientation average, which is what the ring mean is),

    f_orbit = <f(r) r^2>_theta / <r^2>_theta = k <r^(2 - n)>_theta / <r^2>_theta,   (4.1)

so that (a) `f_orbit = f_ring(r_*)` exactly, at the one radius
`r_*^n = <r^2>_theta / <r^(2 - n)>_theta`: `r_* = <r^2>_theta / <r>_theta`
on the plane, `r_* = sqrt(<r^2>_theta) = sqrt(A / pi)` in space, `A` the
area the loop encloses; (b) against the ring mean at the loop's angle-mean
radius `r_bar = <r>_theta`, for both powers,

    f_orbit / f_ring(r_bar) = r_bar^2 / <r^2>_theta = 1 / (1 + var_theta(r) / r_bar^2) <= 1,   (4.2)

with equality if and only if `r` is constant in angle (the circle): the
orbit's mean is the smaller; and (c) if the radius over the turn runs from
`r_min` to `r_max`, with `e = (r_max - r_min) / (r_max + r_min)` (the
eccentricity when the loop is an ellipse about the source),

    1 - e^2 <= f_orbit / f_ring(r_bar) <= 1.                                (4.3)

**Proof, each step labelled.**

B1 (the area rule, derived). The push is along `r_hat`, so the angular
momentum `l = Q S M_A r^2 theta_dot` about the source is constant along the
motion: `r^2 theta_dot = h`, a constant of the turn, and `dt = r^2 dtheta /
h`. This is the area rule of a radial push; Kepler's second law is the
comparison side of it (record 817), and no form of Kepler's or Newton's is
put in.

B2 (the time mean as an angle mean). `f_orbit = (1 / T) integral of f(r(t))
dt over the turn = (1 / (h T)) integral of f(r(theta)) r(theta)^2 dtheta
from 0 to 2 pi`.

B3 (the period the same way). `T = integral dt = (1 / h) integral of r^2
dtheta`. Dividing, `h` cancels: `f_orbit = integral f r^2 dtheta / integral
r^2 dtheta = <f(r) r^2>_theta / <r^2>_theta`, the first equality of (4.1);
with `f = k / r^n` the second. Every weight is now uniform in angle: the
dwell `dt` has been traded for `r^2 dtheta` by B1, which is the whole
content of the "sampling" the paper doubted.

B4 (statement (a)). `f_ring(r_*) = k / r_*^n` equals (4.1) at `r_*^n =
<r^2>_theta / <r^(2 - n)>_theta`; on the plane `r_* = <r^2>_theta /
<r>_theta`, in space `r_*^2 = <r^2>_theta = (1 / 2 pi) integral r^2 dtheta =
A / pi`.

B5 (statement (b)). On the plane `f_orbit / f_ring(r_bar) = r_bar <r>_theta
/ <r^2>_theta = r_bar^2 / <r^2>_theta`; in space `r_bar^2 / <r^2>_theta`
directly; and `<r^2>_theta = r_bar^2 + var_theta(r)` with `var_theta(r) >=
0`, zero if and only if `r` is constant in angle.

B6 (statement (c)). For `r` in `[r_min, r_max]`, `var(r) <= (r_max -
r_bar) (r_bar - r_min)` (Bhatia and Davis, 2000), and `(r_max - r_bar)
(r_bar - r_min) / r_bar^2` is largest at `r_bar = 2 r_min r_max / (r_min +
r_max)`, where it is `(r_max - r_min)^2 / (4 r_min r_max) = e^2 / (1 -
e^2)`; so `r_bar^2 / <r^2>_theta >= 1 / (1 + e^2 / (1 - e^2)) = 1 - e^2`.
QED.

**The check against the ellipse (the comparison side).** For a loop that
is an ellipse about the source with the semi-axes `a` and `b = a sqrt(1 -
e^2)`: `<r>_theta = b` and `<r^2>_theta = a b` (the integrals of `p / (1 +
e cos theta)` and its square over a turn, `p = a (1 - e^2)`), so in space
`f_orbit = k / (a b)`, the ring mean at `sqrt(a b)`, and `f_orbit /
f_ring(b) = b / a = sqrt(1 - e^2)`, inside (4.3); and against the ring mean
at the semi-major axis `a`, which is neither `r_*` nor `r_bar`, the orbit's
mean is the larger by `1 / sqrt(1 - e^2)`: the sign of the difference
depends on which radius of the loop the ring is drawn at, which is why the
theorem names `r_*` and `r_bar` and the paper's sentence must too. Under the
`1 / r` push the loop is not an ellipse (the apsidal angle `pi / sqrt 2`,
DERIVATIONS_BEAM entry 58), and (4.1) to (4.3) hold for it as for any
closed turn. Both forms of (4.1) were checked by quadrature of the
central-push problem at three eccentricities per power (GAMEBOARD by
formula, agreement to five digits; the arithmetic is not in the tree).

**Theorem B on the lattice (the grain it carries there).** B1 holds on the
lattice up to the line's offset: at a crossing Node the push is along
**u**_d while the Node sits within one Link of the Euclidean line, so the
torque per interval is at most the push times one Link, and over the turn
`abs(delta l) <= T f_orbit x 1 Link`; on a near circle `T f_orbit` is the
momentum's whole turning, `2 pi abs(p)`, and `l = abs(p) r`, so the area
rule holds per turn to `2 pi / r` in the worst case (every crossing's torque
of one sign): `0.26` at `r = 24.2` and `0.19` at `r = 33.7` (series D3's
mean radii on record), a ceiling the fan's 48 symmetry lowers on a loop
with the same symmetry. B2 and B3 carry Theorem A's terms (i) to (iv) at
each crossing. The drive's cap at the registered pace (`v = 0.22` Links per
interval against `c = 0.577`) adds the per-axis anisotropy `delta_a =
0.069` to B1 (the velocity is not parallel to the momentum off the axes),
`0` as `v / c -> 0`.

## 5. The registered case: series D3, by formula

The register (examples/events/orbit_lamp/README.md; EXPERIMENTS.md "D3";
NUMBERS.md line 172): the plane `121 x 121 x 1`, the source of content
`2^32` at the centre on a fan of 120 in-plane primitive directions (every
`(a, b, 0)` with `0 < a^2 + b^2 <= 64`), the probe of held content `2^20`
started at `r = 12` and `r = 24` on `+x` with the momentum `606 339 072`
along `+y` (the world files `r12.json`, `r24.json`), the period read as one
recurrence of the clicks' `x` per radius: `T(12) = 407.3` and `T(24) =
813.3` intervals, `T(24) / T(12) = 1.997` inside its bracket `1.82 .. 2.18`
(DETECTOR, README.md lines 254 to 260), the register's own word "consistent
with the `1 / r` form and not decisive" on "loops that are not similar
figures", "one recurrence per radius" (README.md lines 274 to 283;
EXPERIMENTS.md lines 7637 to 7640). Nothing below is pinned and nothing
was run; every number is GAMEBOARD by formula from the declarations and the
register's recorded numbers.

| Quantity | Formula | `r = 12` loop | `r = 24` loop | Kind |
| --- | --- | --- | --- | --- |
| The fan's L1 factor `F_L1` | mean of `(abs(a) + abs(b)) / sqrt(a^2 + b^2)` over the 120 directions | `1.2871` | `1.2871` | GAMEBOARD by formula (the plane's isotropic limit `4 / pi = 1.2732`) |
| The ring's count `N(r_0)` and term (i) | Nodes with `abs(sqrt(x^2 + y^2) - r_0) <= 1 / 2`; `N / (2 pi r_0)` | `68`; `0.902` | `144`; `0.955` | GAMEBOARD by formula |
| The ring's incidence and term (ii) | `sum_d m_d(r_0)` over the 120 lines; against `120 x 1.2871 = 154.5` | `144` (`m_d` = 1 or 2); `1.073` | `160`; `0.966` | GAMEBOARD by formula |
| The product (i) x (ii) | a perfect circle's orbit mean against the lattice ring mean at `r_0`, the ratio of (3.1) before `eta` | `0.968` | `0.922` | GAMEBOARD by formula |
| The drive's anisotropy, term (iii) | `0.2346 / 0.2195 - 1` at the registered pace `9 / 41` | `0.069` | `0.069` | GAMEBOARD by formula (the register's "6.9 percent") |
| The tangential ceiling, term (iv) | `1 / r_0` | `0.083` | `0.042` | GAMEBOARD by formula |
| The area rule's ceiling per turn | `2 pi / r` at the loop's mean radius on record (`24.2`, `33.7`) | `0.26` | `0.19` | GAMEBOARD by formula |
| The turn's extreme radii | needed for `e` of Theorem B (c) | not on record | not on record | the register records the least, greatest and mean radius at the lamp's births over the WHOLE run (README.md lines 146 to 149: `1.4 .. 73.2`, mean `24.2`; `11.0 .. 62.3`, mean `33.7`), not the one turn's; no eccentricity is on record as a number |
| The bound on `e` from the run's extremes | `e_turn <= e_run = (r_max - r_min) / (r_max + r_min)` (a turn's extremes lie inside the run's) | `<= 0.9625` | `<= 0.6999` | GAMEBOARD by formula from DETECTOR extremes |
| The floor on the factor of (4.3) | `1 - e_run^2` | `>= 0.074` | `>= 0.510` | GAMEBOARD by formula |

**The bound as a function, since the eccentricity is not on record.** For
each loop, with `e` the turn's own `(r_max - r_min) / (r_max + r_min)`,

    (1 - e^2) f_ring(r_bar) <= f_orbit <= f_ring(r_bar),   r_bar = <r>_theta of the turn,

and `f_orbit = f_ring(<r^2>_theta / <r>_theta)` exactly in the continuum;
on the lattice the factors of the table multiply in, `0.968` and `0.922`
for (i) and (ii), `+- 0.069` for (iii), `+- 0.083` and `+- 0.042` as
ceilings for (iv). The register's mean radii `24.2` and `33.7` are means
over births every 8 intervals, that is dwell-weighted means, `<r>_t`, not
the angle-mean `r_bar = <r>_theta` the theorem names (on an eccentric loop
`<r>_t > <r>_theta`: the body dwells far out); neither turn's `r_bar` is on
record. The floors `0.074` and `0.510` are what the run's whole-record
extremes allow and decide nothing: the register's own word, "consistent,
not decisive", stands, and this file gives it its reason: the ratio
`T(24) / T(12)` rests on the `1 / r` push's scale symmetry, which Theorem B
neither uses nor tests, and the register's periods are one recurrence each
on loops whose per-turn shape was not recorded. A turn's `r_min`, `r_max`
and `<r>_theta` are readable from the register's own click list (the
radius at every birth, `tools/orbit_lamp_readings.py` lines 167 to 174)
restricted to one recurrence, a host reading of a DETECTOR record, if the
owner wants the number; no new run is needed for it.

## 6. The one sentence the paper takes (two forms; the writer pastes it on this file's SHA)

**Form "proved" (the continuum, with the grain term):** "The mean push over
one closed turn equals the ring mean at one radius of the loop,
`<r^2>_theta / <r>_theta` on the plane and the equal-area radius
`sqrt(<r^2>_theta)` in space, exactly in the continuum limit for every
closed turn by the area rule of a radial push (docs/designs/ring_mean/PROOF.md,
Theorem B; Kepler's second law the comparison, not an input); against the
ring mean at the loop's angle-mean radius the orbit's mean is the smaller by
the factor `r_bar^2 / <r^2>_theta`, between `1 - e^2` and `1`, and equal to
it only where the radius is constant in angle; on the lattice the equality
holds up to the ring's count against `2 pi r` (`0.90` at `r = 12`, `0.95`
at `r = 24` on the plane), the ring's incidence against the fan's L1 factor
(`1.07` and `0.97`), the drive's anisotropy at the registered pace (`0.069`)
and one Node's dwell per crossing of a line, GAMEBOARD by formula."

**Form "bounded by" (the registered case):** "On series D3's loops the
mean push over the read turn lies between `1 - e^2` and `1` times the ring
mean at the turn's angle-mean radius, `e` the turn's `(r_max - r_min) /
(r_max + r_min)`, which is not on record; the run's whole-record extremes
bound it by `0.96` at `r = 12` and `0.70` at `r = 24` (floors `0.07` and
`0.51` on the factor, GAMEBOARD by formula), which decides nothing, and the
ratio `T(24) / T(12) = 1.997` rests on the `1 / r` push's scale symmetry,
not on this equality (docs/designs/ring_mean/PROOF.md, section 5)."

The paper's present clause, "which equals the ring mean only where the
body's dwell is uniform in angle, a sampling the paper does not prove", is
replaced by the first form; the second form is for the D3 sentence of the
same paragraph if the writer wants the bound beside the reading. Both are
statements of the law's push matching a form, never of how nature is
(record 762).

## 7. What this is not

- **No new rule.** Nothing is added to the law: the push, the drive, the
  fan and the ring are as the tree declares them; the two means are
  definitions, the theorems are arithmetic and the continuum limit of what
  is declared. **The three tests of every rule (generic, vector, local) do
  not apply**, because no rule is proposed; the push whose means are taken
  passed them where it entered the law (DERIVATIONS_BEAM 3.2, BEAM_LAW).
- **No physical claim beyond the law's push.** Newton's inverse square and
  Kepler's three laws appear only on the comparison side: the area rule of
  step B1 is derived from the push's radial direction, Kepler's second law
  is what it is compared with, and the ellipse of section 4 is a check of
  the formula against a known figure, never an input (record 817). The
  file does not say which of the law's two constants of gravity (the
  clock's or the push's, record 872) the coefficient stands on.
- **Not a run, not a pin.** No engine was imported or run; no number here
  is a measurement; the numbers of section 5 are the arithmetic of the
  declared fan, the ring's definition, the drive's per-axis form at the
  registered pace and the register's recorded extremes, each so labelled.
  The quadrature check of Theorem B is arithmetic of the continuum
  equations and is not kept in the tree (the order: one file).
- **One note for the derivation mathematician (not changed here).**
  DERIVATIONS_BEAM 3.2 line 883 counts the fan's `K` lines as crossing a
  shell at `K` Nodes; the exact count is `sum_d m_d(r)`, whose mean over
  the radii carries the L1 incidence factor of record 872 (section 1.3);
  the shell mean there is `F_L1 q Q / N(r)`, not `q Q / N(r)`. That line is
  the derivation mathematician's to amend.

## 8. Links

- [DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md): section 1.2 (the walk;
  the Manhattan line, line 321), 3.2 (the shell mean, lines 874 to 892),
  3.3 (Newton's form, line 938), 5.1 (the dwell along a line, lines 1168 to
  1198), section 21.5 entry 58 (Kepler's laws under the six points, lines
  6422 to 6510).
- `docs/designs/light_bending/STEP_ALGEBRA.md` section 9 (the ring
  of starts: the construction of the ring mean, `F_L1`, the tangential mean
  `0.00000`, the grain `0.085` to `0.107`), on branch
  `light-bending-algebra` at `23ef9ce93721963098c45e0add3f846a7154a1fb`
  (PR #821).
- [The log](../../LOG_2026-09-20.md): records 762 (whatever can be computed
  algebraically is computed algebraically; matching nature, never how
  nature is), 817 (Einstein's, Lorentz's and Newton's forms on the
  comparison side only), 872 (where `F_L1` comes from; the law's two
  constants of gravity), 883 (the order, as numbered by the Boss).
- The series D3 register:
  [examples/events/orbit_lamp/README.md](../../../examples/events/orbit_lamp/README.md),
  [docs/EXPERIMENTS.md](../../EXPERIMENTS.md) ("D3"), `paper/general_formula/NUMBERS.md`
  line 172, `tools/orbit_lamp_readings.py` lines 167 to 174.
- The paper: `paper/general_formula/main.tex` line 469 on branch
  `claude/paper-owner-review-five` at `735ee8c81b8615a5a73de45f82cd4724ccf4657c`
  (PR #802), the ground paragraph of Section 4.
- The notation and the kinds: [skills/workflow.md](../../../skills/workflow.md),
  "Notation" and "The main course" (7).
