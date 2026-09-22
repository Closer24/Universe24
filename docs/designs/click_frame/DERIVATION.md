# Lorentz from the clicks: Bondi's two factors on the GameBoard, the one line that makes them one, and what the register has read (the owner's order, 2026-09-22, records 723, 725 and 728)

The derivation mathematician, 2026-09-22, on the Boss's order of about
04:30Z; a derivation on paper, no run, no code; every number a closed
form or a registered reading labelled by its kind (DETECTOR or
GAMEBOARD); the run, if any, is the owner's word.

**The verdict in one line: LORENTZ FROM THE CLICKS GIVEN the line
`k_AB = k_BA` (the two directions alike, the relativity principle),
which is `r^2 = 1 - v^2` for the moving record's own count; NOT WITHOUT
IT.** And for part (4), the board's own cost of a hop with no square as an
input (section 5): LORENTZ FROM THE BOARD'S OWN COST OF A HOP: NO; every
wall of the law is linear in the Manhattan momentum, the cost gives `r =
1 - beta` or 1, and the square that would give YES is the Minkowski norm
declared into the wall. And for part (5), the hop as an amplitude
(section 6): CLICKS BEHAVE LIKE LORENTZ IN OUR SPACE: NO; the law's hop
is a whole-record pattern (`by_drive` with `at_most` 1), not a split of
amount and phase between staying and hopping, so no interference in
flight makes the square root. Under the law as it stands the two factors differ (`k_BA / k_AB =
1 - v^2`), under the loop's resident count they differ the other way
(`(1 + v) / (1 - v)`), and under covariant-readings-v1 they are equal
by that identity's declared rate. The measurable that decides is the
ratio of the two one-way Doppler factors, read at the ground through
records; its pins are in section 3.

## 1. The frame, and the names

The frame is the decided one (records 281, 562, 678, 709, 713 to 723):
the tick is GAMEBOARD and never read; a detector at rest at a Node has
its own count of intervals, stretched by the crowd at its Node
(`age_wall`, the age moment `a_tau`); information leaves the board only
through clicks (the Node, the detector's own count, what arrived); a
moving detector is a record with momentum that hops at most one Node per
interval (`c = 1` Node per interval in this section's units; on the
Beam Law's lattice the flight's pace `N_l abs(D)_2 / T_D`, isotropic
within `1 / T_D`, plays c and every count below scales with it) and
re-emits (transponds) what it receives, its own count read at the
ground only through the records it emits; two detectors compare counts
only through rows between them, never in zero time; a velocity is Nodes
apart over the difference of two counts.

Names. A: the detector at rest at Node 0, in no crowd, its own count
per interval 1. B: the moving record on an axis, `v = 1 / k` Nodes per
interval (k a whole number of intervals per hop, the hop pattern
`x_B(t) = floor(t / k)`), its own count per interval r, a rational
`n_r / d_r` kept by an accumulator with its remainder (r is B's clock
rate against the tick, to be found or measured, never assumed). T: the
number of a detector's own counts between two records it emits. `k_AB`:
B's own count between two arrivals of A's records, over T. `k_BA`: A's
own count between two arrivals of B's records, over T. Every k is a
ratio of two counts of one detector, hence a DETECTOR reading; every
tick below is GAMEBOARD arithmetic that the reader never sees.

## 2. The theorem of the clicks

**(a) The two factors, exact in the mean.** A emits its n-th record at
the tick `n T` from Node 0; it hops one Node per interval and reaches B
at the first tick `a_n` with `a_n - n T >= floor(a_n / k)` (the record
has hopped to B's Node). Writing `a_n = n T / (1 - v) + e_n` with `v = 1
/ k`, the floor's remainder `e_n` is bounded (below one hop of B, k
intervals, and periodic in n with the period of the rational slope), so
over m records `a_m - a_0 = m T k / (k - 1)` exactly in the mean, the
remainder never accumulating (the accumulator's carry, 1.2 (T)). B's own
count over those intervals is `r (a_m - a_0)` with r's remainder kept.
So

    k_AB = r / (1 - v)   exactly in the mean (rung 1 on the counts, the remainder below one hop and one count).

B emits its n-th record at its own count `n T`, i.e. at the tick `t_n =
n T / r` (with r's accumulator, exact in the mean) from the Node `x_B(t_n)
= floor(t_n / k)`; the record hops back one Node per interval and
reaches A at `t_n + x_B(t_n) = t_n (1 + v) + e'_n`, `e'_n` bounded as
before. So

    k_BA = (1 + v) / r   exactly in the mean.

On the Beam Law's lattice the same two forms hold with v the Euclidean
speed over the flight's isotropic pace, within `1 / T_D`; on a face
diagonal in the hop frame of this section (a Manhattan light), v is
replaced by the Manhattan speed `abs(v)_1 = 2 / k` (three Nodes per k on
a body diagonal), the record needing `abs(v)_1 t` hops to reach B: the
anisotropy of stage 1 reappears exactly there, and which speed a run
reads is the fan's grain, not this section's.

**(b) The line.** The two directions are alike, `k_AB = k_BA`, if and
only if

    r / (1 - v) = (1 + v) / r,   i.e.   r^2 = (1 - v)(1 + v) = 1 - v^2,

by one multiplication. Under it the common factor is Bondi's, `k =
sqrt((1 + v) / (1 - v))`, and the rest is linear algebra with no further
physics: A assigns an event the radar coordinates `(t, x)` from its
emission count `t - x` and its reception count `t + x` (c = 1); B's
counts of the same two records are `k (t - x)` and `(t + x) / k` (the
first record went A to B, the second B to A, each stretched by the one
k), so B's radar coordinates `(t', x')` satisfy `t' - x' = k (t - x)`
and `t' + x' = (t + x) / k`, which is the Lorentz boost with `v = (k^2 -
1) / (k^2 + 1)` and `gamma = (k + 1 / k) / 2`; and the boost's own
clock rate is `1 / gamma = sqrt(1 - v^2) = r`. So: the clicks and `c`
give the two factors `r / (1 - v)` and `(1 + v) / r` and nothing more;
Lorentz is equivalent to their equality; the one line the owner's claim
needs is `k_AB = k_BA`, the relativity principle for the two directions,
and it fixes the moving record's own count at `r = sqrt(1 - v^2)`. Rung
1 for the equivalence (exact algebra on the two counts); the boost's
form is the standard k-calculus, no limit taken.

**(c) The three tests for the transponding detector**, the rule the
frame needs (a record with momentum that re-emits at each arrival).
Generic: one primitive, a body's lamp keyed to arrivals instead of to a
turn, the same for every family, no name read. Vector: the release verb
at the arrival (a translation of the lamp's accumulator by the arrival's
amount), no root, no float. Local: the record's own Node and the rows
that arrive there; nothing kept at a Node; fixed work per arrival.

## 3. The board's r, and the numbers

Three values of r are on the tree, none of them a measurement of a
moving body's own count (section 4):

- the law on `main`: `r = 1` at every speed (DERIVATIONS_BEAM 4.3, the
  counter at the rest rate; NATURE row 4a's FAIL against gamma);
- the loop's resident count (stage 1, docs/designs/clock_loop, verdict A):
  `r = 1 - abs(v)_1`, first order, anisotropic, `1 - v` on an axis;
- covariant-readings-v1 (17.6 M1): `r = E_0 / E = 1 / gamma = sqrt(1 -
  v^2)` by the identity's declared square, the whole root of `m^2 + 3`
  **p** `.` **p** (17.7: the root's rounding the only price).

The two factors and the deciding ratio `k_BA / k_AB`, exact fractions
on an axis (Lorentz's k as a closed form off the board):

| v | k | `r = 1` (the law): k_AB, k_BA, ratio | `r = 1 - v` (the loop): k_AB, k_BA, ratio | `r = sqrt(1 - v^2)` (the identity): k_AB = k_BA, ratio |
| --- | --- | --- | --- | --- |
| 1/2 | 2 | 2, 3/2, 3/4 | 1, 3, 3 | sqrt 3 = 1.7321, 1 |
| 1/4 | 4 | 4/3, 5/4, 15/16 | 1, 5/3, 5/3 | sqrt(5/3) = 1.2910, 1 |
| 1/8 | 8 | 8/7, 9/8, 63/64 | 1, 9/7, 9/7 | sqrt(9/7) = 1.1339, 1 |
| 1/16 | 16 | 16/15, 17/16, 255/256 | 1, 17/15, 17/15 | sqrt(17/15) = 1.0646, 1 |

In general: `r = 1` gives `k_AB = k / (k - 1)`, `k_BA = (k + 1) / k`, the
ratio `1 - v^2 = (k^2 - 1) / k^2`; `r = 1 - v` gives `k_AB = 1` (the
moving detector counts A's records at its own rate, the resident loss
cancelling the stretch exactly) and `k_BA = (k + 1) / (k - 1)`, the ratio
`(1 + v) / (1 - v)`; `r = sqrt(1 - v^2)` gives both `sqrt((k + 1) / (k -
1))`, the ratio 1. On a face diagonal in the hop frame, replace v by
`abs(v)_1 = 2 / k` (k = 4, 8, 16: the ratios `3/4, 15/16, 63/64` under
the law as at v = 1/2, 1/4, 1/8 on an axis; `3, 5/3, 9/7` under the
loop) and on a body diagonal by `3 / k`; on the Beam Law's lattice with
its isotropic flight the axis table stands for every direction within
`1 / T_D`.

What a run should show under the law as it stands: the two factors
`k / (k - 1)` and `(k + 1) / k`, their ratio `1 - v^2` (3/4 at v = 1/2),
not 1; this is a prediction to be proved by a run, not a result, and
the run is the owner's word.

## 4. The register: which factor is already read, and the missing direction

- **`k_BA`, a moving lamp counted at rest: READ, under both r's.** NATURE
  row 4b: series G2's star `s_mz2` at beta = 0.2674 gives `z = 0.2636`
  (DETECTOR, the pointer's reading at the fixed detector's window), i.e.
  `1 + z = 1 + v` to the count's grain, the law's `k_BA = (1 + v) / r` at
  `r = 1` (nature: `gamma (1 + beta) = 0.315`, FAIL); under
  covariant-readings-v1 the same world read `z = 0.3674` for the pin
  `0.369 +- 0.003` (DETECTOR, series S), `k_BA = gamma (1 + v)` with the
  identity's `r = 1 / gamma` AND the identity's own v: under the key the
  drive's pace is `p / E'`, so the star's beta is 0.3040 (gamma 1.04967),
  not 4b's 0.2674 at the law's pace `p / (Q S M + p)`; `1.04967 x 1.3040
  = 1.3688` reproduces the pin, while gamma (1 + 0.2674) would give
  1.315. So the B-to-A factor exists in the register in both forms, and
  it is the identity's r and its pace, not a measured r, that move it.
- **r itself, the moving body's own count: NOT READ AS A MEASUREMENT.**
  Series J4 PINS the muon's `become` at tick 64 at every speed
  (HYPOTHESES 21's pin; NATURE 4a: no world file, not run; the one run
  reading of 64 is at rest, series S's `j4_muon_rest` under the key, the
  `become` line at 64, GAMEBOARD) and series S reads the 64th
  self-creation at 70 and 124
  (GAMEBOARD) with the beta clicks at 392, 369, 345 (DETECTOR, the
  products' face clicks): both are the gate's own count read against the
  tick or through the decay's products, r by declaration (1 on the law,
  `1 / gamma` under the identity), never r read at the ground through
  the spacing of the body's own records.
- **The clock series (series T, clock-age-v1; NATURE row 12): a different
  factor.** The lamp on a body at rest read at a fixed detector gives the
  crowd's stretch of the count, the ratio 1.907 against the pin `1.909
  +- 0.05` (the map's, the register's), the continuum's 2.00 outside the
  pin, at the distances 6 and 3 (DETECTOR; the potential's form): the age
  moment's
  factor at v = 0, no Doppler direction; it fixes nothing of r(v).
- **`k_AB`, a lamp at rest counted by a moving transponding body: NOT
  READ, and it is the missing direction.** The world it needs: a lamp at
  rest emitting one record every T of its count on an open bar; a body
  with momentum on the bar's axis carrying the transponding rule of 2
  (c): at each arrival it re-emits one record toward the ground detector
  at the bar's far end; the ground detector's own count between the
  re-emitted records, over T, is `k_AB x k_BA` (the round trip's two
  factors in series: `(1 + v) / (1 - v)` under every r, the k-calculus's
  round trip, so the round trip alone reads nothing of r under any r,
  and the second lamp on the body is therefore the whole of the new
  information); the body's own count of the arrivals, read through that
  second lamp emitting every T of its own count, gives `k_AB` against
  the ground's `k_BA`, and their ratio decides. The pins, from the formulas, before
  any run, each within `1 / T` of the count (the accumulators' remainder)
  and, on the Beam Law's lattice, within `1 / T_D` of the pace: `k_AB`
  and `k_BA` at v = 1/2, 1/4, 1/8, 1/16 as the table of section 3 has
  them under the law (`2, 4/3, 8/7, 16/15` and `3/2, 5/4, 9/8, 17/16`, the
  ratio `3/4, 15/16, 63/64, 255/256`), under the identity (`1.7321,
  1.2910, 1.1339, 1.0646` both, the ratio 1), and the round trip `3, 5/3,
  9/7, 17/15` under both. A ratio of 1 within `1 / T` is Lorentz from the
  clicks; a ratio of `1 - v^2` is the law's counter at the rest rate;
  `(1 + v) / (1 - v)` the resident loop's. No reading is pinned here
  from a run; these are the closed forms, and the run is the owner's.

## 5. Part (4), corrected (the owner's word, record 732: "make sure Lorentz is not already in the formula"): the board's own cost of a hop, with no square as an input

**Certification of the inputs.** This section uses only: (1) the six
verbs (skills/workflow.md, record 202); (2) the law's drive on `main`,
the pace `v = p / (Q S M + p)` Links per interval (DERIVATIONS_BEAM 3.3
and 4.4; the paper's P9, `abs(p_a) / (N_l N_w M + abs(p_a))` per axis),
linear in p on both sides; (3) form B's directional drive
(docs/designs/light_speed/FORM.md section 3.1; the path
docs/designs/drive_b/DESIGN.md named in the order does not exist on
`main`): the rate `abs(p)_1 Q` against the wall `Q^2 S M + abs(p)_1 T_h`,
`T_h = isqrt(3 Q^2) = 110`, linear in the Manhattan momentum `abs(p)_1`;
(4) the age wall's crowd, `a_tau`, entering every wall linearly
(`core.integer.age_wall`); (5) stage 1's resident count, `r = 1 -
abs(v)_1` (docs/designs/clock_loop/DERIVATION.md). None of these
carries a square of the momentum or of a length: (2) and (3) are linear
in `abs(p)_1`, (4) is linear in `a_tau`, (5) is linear in `abs(v)_1`.
The identity's square `W = E_0^2 + 3` **p** `.` **p** and its root `E'`
appear below only as the thing the result is compared with, never as an
input; the previous draft of this section, which took r = E_0 / E' from
W, derived Lorentz from Lorentz and is withdrawn (its conclusion "only by
declaration" stands, restated at the end as what the declaration is).

**(i) The energy the law charges for a hop.** On `main` the law charges
no energy for a body's motion: the push adds momentum for free (`p +=
push`, 3.3), the content M is unchanged, and the law has no energy of
motion (E5 not reached, 4.5). What the pace costs is momentum: at `v = 1
/ k` on an axis, `v = p / (Q S M + p)` gives `p = Q S M v / (1 - v) = E_0
/ (k - 1)` in label units, `E_0 = Q S M`; linear in v at small v (`p =
E_0 v (1 + v + ...)`). Under form B the body's wall carries the motion:
`Q^2 S M + abs(p)_1 T_h = Q (E_0 + u)` with `u = abs(p)_1 T_h / Q` the
motion's share in the units of `E_0`, and the pace in units of the
rows' `c_h = Q / T_h` is `beta = u / (E_0 + u)`, so `u = E_0 beta / (1 -
beta)` and the wall is

    E_B(beta) = E_0 + u = E_0 / (1 - beta):   linear in beta at first order (E_0 beta), not E_0 beta^2 / 2, and not E_0 / sqrt(1 - beta^2).

So the board's cost of a hop is LINEAR in `abs(p)_1` (both walls), first
order in beta, and no quadratic cost is present in any wall of the law:
the one square the verbs hold is verb 2, the bilinear form with a
declared matrix, and the law applies it at the click alone (the Gram
form of the phase-count vector, 6.5), never to a body's momentum. Rung
1 (the walls as declared).

**(ii) The r it gives.** Two readings of the moving record's own count
from these inputs, and no third: (a) the law as it stands, `r = 1` at
every speed, the counter stretched by the crowd's `a_tau` alone (the age
wall's one member), a hop costing the clock nothing (4.3; NATURE 4a's
FAIL); (b) the rest share of the LINEAR wall, `r = E_0 / E_B = 1 - beta`,
which is stage 1's resident count on an axis, `1 - abs(v)_1`, reached
now from form B's wall instead of the loop's steps: the same first-order
law by two roads, both Manhattan (the wall reads `abs(p)_1`, the loop
counts hops), anisotropic by `sqrt 2` and `sqrt 3` on the diagonals. No
input of this section gives `sqrt(1 - beta^2)`, since none holds a
square.

**(iii) The two Doppler factors under that r.** With section 2's forms,
`k_AB = r / (1 - beta)` and `k_BA = (1 + beta) / r`: under (a), `k_AB = 1
/ (1 - beta)` and `k_BA = 1 + beta`, the ratio `k_BA / k_AB = 1 - beta^2`
(3/4, 15/16, 63/64, 255/256 at v = 1/2, 1/4, 1/8, 1/16); under (b),
`k_AB = 1` exactly (the resident loss cancels the stretch) and `k_BA = (1
+ beta) / (1 - beta)`, the ratio `(1 + beta) / (1 - beta)` (3, 5/3, 9/7,
17/15). Neither agrees; the relativity line `k_AB = k_BA` fails under
both.

**(iv) Approximate Lorentz at small v, and the order.** Expand in beta.
Lorentz: `k = sqrt((1 + beta) / (1 - beta)) = 1 + beta + beta^2 / 2 +
O(beta^3)`, `r = 1 - beta^2 / 2 - beta^4 / 8`. Under (a): `k_AB = 1 +
beta + beta^2 + ...`, `k_BA = 1 + beta`: the two agree with each other
and with Lorentz to FIRST order and part at second (`beta^2` against
`beta^2 / 2` and 0): Lorentz to order 1, by charging the clock nothing.
Under (b): `k_AB = 1`, `k_BA = 1 + 2 beta + ...`: they part at FIRST
order; a linear cost breaks the symmetry at the order it enters. A
quadratic cost, `r = 1 - beta^2 / 2`, would give `k_AB = 1 + beta +
beta^2 / 2 + ...` and `k_BA = 1 + beta + beta^2 / 2 + ...`, agreement to
second order and Lorentz to order 2 (exact only with the full root,
whose expansion adds `- beta^4 / 8`, the identity's W): that is the
form no input of this section has. The lattice's anisotropy enters
where the Manhattan length does: under (b) at first order (`abs(v)_1`
against `abs(v)_2`, `sqrt 2` on a face diagonal); under (a) not through
r (which is 1 in every direction) but only through the light's own
grain, at `1 / T_D` on the Beam Law's isotropic flight or at first order
in `abs(v)_1` in the hop frame's Manhattan light (section 2 (a)).

**(v) The verdict for (4): LORENTZ FROM THE BOARD'S OWN COST OF A HOP:
NO.** The one line that decides: every wall of the law is linear in
`abs(p)_1` (`Q S M + p` on `main`, `Q^2 S M + abs(p)_1 T_h` under form
B), so the record's own rate from the board's cost is `1 - beta` (first
order, the two factors parting at first order) or 1 (no cost, the
factors agreeing to first order only), and no square of the momentum is
formed anywhere but at the click. What a cost would have to be for YES,
as a question for the owner and not as a rule: the wall the drive reads
would have to satisfy `E(p)^2 - E_0^2 = 3` **p** `.` **p** in the
identity's units, i.e. be verb 2's quadratic form on (E_0, **p**) with
the matrix `diag(1, 3, 3, 3)`; the verbs allow it (a bilinear form with
a declared matrix, the three tests as 17.6 M3 and 17.7 pass them), the
law chose the linear wall, and the quadratic choice is the Minkowski
norm itself, so Lorentz would then be declared by that choice, not
derived: does the owner want the drive's wall to be that square? The
three tests apply to any such cost, and nothing is kept at a Node beyond
the events there under either wall. The earlier "only by declaration"
is this: the declaration is the square in the wall.

## 6. Part (5): does a click carry its information from Node to Node the way an amplitude does? The hop as a pattern or as a split with phase (the owner's word, record 737)

**(1) The known mathematics, as the comparison and not as our law.** An
amplitude on a line that at each interval either hops one Node (at c =
1 Node per interval) or stays, the two with a phase between them and in
superposition, is the discrete-time Dirac walk (the Dirac cellular
automaton: Bialynicki-Birula 1994, Meyer 1996, Strauch 2006). In one
dimension, with `m` the staying share as an angle (the mass) and `k` the
wave number, its dispersion is `cos w = cos m cos k`, `w` the frequency
per interval; its group velocity is `v = dw / dk = cos m sin k / sin w`;
and at small m and k, `w^2 = m^2 + k^2 + O(4)`, so `v = k / w + O(3)` and
the rest share of the frequency is

    r = m / w = sqrt(1 - v^2) + O(k^4, m^2 k^2):

the clocks of such an amplitude, read as Bondi's two factors, agree to
SECOND order, with the lattice's own corrections beyond (in three
dimensions the walk's dispersion is anisotropic from the fourth order on,
the lattice's `k^4` terms). The square root is the interference of the
staying amplitude with the hopping one (`cos w = cos m cos k` is a
product of two cosines, and `w^2 = m^2 + k^2` the square it gives at
small angles); it is not a fraction of resident intervals and cannot be
made from one. Rung: mathematics, cited, not the law's.

**(2) The law's row, read from the tree.** The law's hop is a
deterministic schedule of the whole record, never a split of its amount
between staying and hopping. The body (`engine.step_axis`, the
docstring): "the step fires exactly when `floor(n |p| / D)` increments
over the self-creations n ... never two in one self-creation ... The
count primitive is `core.integer.by_drive` ... with `at_most` 1: the
step's own rule of one Link per interval, the residual of a larger
momentum kept in the drive"; and `engine._move`: "its centre moves one
Link and its set with it", "at most one per interval", the phase turning
at the Link "by the difference of two floors". The row (`nature_beam.py`,
`walk_step`): "the residue gains the rate over the wall
(`by_drive_rows`)", the digital line of its direction, the whole amount
on one Node at every interval (the flight table indexed by (D, tau),
rem:nodispersion). The massive rows (`massive_rows`, `amplitude.py`):
"the record's waiting state ... per Node the units, the content and the
labels of the rows that ended there and were NOT placed at their
arrival", "resolved at the completion: the chosen end's quantum placed,
the rest cancelled": a rule of the click's placement over rows that have
ENDED, not a split of a row in flight. So: at every interval a record's
whole amount is at one Node, and either it hops or it stays by a
Bresenham-like accumulator; no amplitude stays behind while another
hops; the law has amplitudes only at the click, over ended rows (the
phase-count vector, 6.5). Rung 1 (the definitions).

**(3) Which the law is today, and what follows.** Deterministic. Under a
deterministic pattern a clock that counts resident intervals gives `r =
1 - abs(v)_1` (stage 1; section 5's linear wall by the second road) and
the clock as built gives `r = 1`; the two Doppler factors part at first
order under the first and agree to first order only under the second
(section 5 (iv)); there is no staying amplitude to interfere with a
hopping one, so no `sqrt(1 - v^2)` can arise in flight: the clicks of
the law do not behave like Lorentz in our space. A split with phase
would give the walk's dispersion, `r = sqrt(1 - v^2)` to second order and
the anisotropy from the fourth: the clicks would behave like Lorentz in
the long-wave limit. The law is the first.

**(4) The smallest change, as a question for the owner and not a rule.**
Make the hop at every Node of free space a split: each interval a row of
amount a at a Node becomes two rows, one hopping one Link along its
direction and one staying, their amounts and phases by a declared table
over the circle of N (the splitter's own tables `C'`, `S'`, th:isometry's
verb), the staying row turned by the family's rest turn (the pair `[n,
d]`, the family's E_0 = h n / d: the mass angle of (1) IS the family's
declared phase rate) and the hopping row by the flight's phase per Link;
rows of equal (Node, direction, phase) merged by the group ring's
addition. The verbs: the split (verb 2, a bilinear form with a declared
table) and the merge (verb 3), no root, no float, the tables' rounding
the declared one (record 328). The integers: the family's `[n, d]` and
the split table, nothing new. The three tests: generic, one split table
per interval for every family, no name read; vector, verbs 2 and 3 with
rates at most bilinear; local, the row's own Node and its six
neighbours, the storage per Node bounded by 6 N rows (one per direction
and phase after the merge), fixed work per row, nothing kept beyond the
rows present. What it would cost the registered pins: everything the
flight's exactness pinned moves, since every beam spreads: series Q's
face clicks (290 of 290 at the derived interval), L7's cone (the age 29
on both rows), series C's "no dilution", L2's fringes (the fan's
geometry replaced by the walk's own diffraction), the massive rows'
bands of 23.3 (36.5, 60, 83.5, the turn `abs(p) N / h` replaced by the
walk's group velocity), and the covariant identity's gate (its r would be
the walk's, not a declared square); the two-slit and Bell clicks would
keep their form (the click's evaluation is unchanged) with new numbers.
It would be a hypothesis under its own identity beside the law, the
pins rewritten before any run; not built here. The question: does the
owner want the flight to be a split with phase at every Node?

**(5) The verdict for part (5): CLICKS BEHAVE LIKE LORENTZ IN OUR SPACE:
NO.** The hop is a pattern and the resident count is linear. The one
line that decides: every hop of the law is `by_drive` with `at_most` 1
on the whole record (`step_axis`, `walk_step`), the amount never splits
between staying and hopping, so no staying amplitude interferes with a
hopping one in flight, and the only square the law forms is at the
click over rows that have ended.

## 7. Links

[DERIVATIONS_BEAM 4.3](../../DERIVATIONS_BEAM.md#43-a-moving-clock-the-rate-is-one-at-every-speed),
[17.6](../../DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes),
[17.7](../../DERIVATIONS_BEAM.md#177-the-proper-time-gate-without-a-root-two-counters-compared-against-the-whole-root-the-owners-word-2026-09-22-records-642-and-647);
[the clock loop, stage 1](../clock_loop/DERIVATION.md); [NATURE rows 4a, 4b
and 12](../../NATURE.md); [the covariant worlds](../../../examples/events/covariant/README.md);
[HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector).
