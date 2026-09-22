# Lorentz from the clicks: Bondi's two factors on the GameBoard, the one line that makes them one, and what the register has read (the owner's order, 2026-09-22, records 723, 725 and 728)

The derivation mathematician, 2026-09-22, on the Boss's order of about
04:30Z; a derivation on paper, no run, no code; every number a closed
form or a registered reading labelled by its kind (DETECTOR or
GAMEBOARD); the run, if any, is the owner's word.

**The verdict in one line: LORENTZ FROM THE CLICKS GIVEN the line
`k_AB = k_BA` (the two directions alike, the relativity principle),
which is `r^2 = 1 - v^2` for the moving record's own count; NOT WITHOUT
IT.** Under the law as it stands the two factors differ (`k_BA / k_AB =
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
  identity's `r = 1 / gamma`. So the B-to-A factor exists in the
  register in both forms, and it is the identity's r, not a measured
  one, that moves it.
- **r itself, the moving body's own count: NOT READ AS A MEASUREMENT.**
  Series J4 reads the muon's `become` at tick 64 at every speed
  (GAMEBOARD, the self-creation count against the tick; NATURE 4a's
  register line) and series S reads the 64th self-creation at 70 and 124
  (GAMEBOARD) with the beta clicks at 392, 369, 345 (DETECTOR, the
  products' face clicks): both are the gate's own count read against the
  tick or through the decay's products, r by declaration (1 on the law,
  `1 / gamma` under the identity), never r read at the ground through
  the spacing of the body's own records.
- **The clock series (series T, clock-age-v1; NATURE row 12): a different
  factor.** The lamp on a body at rest read at a fixed detector gives the
  crowd's stretch of the count, the ratio 1.907 for the pin 2.00 at the
  distances 6 and 3 (DETECTOR; the potential's form): the age moment's
  factor at v = 0, no Doppler direction; it fixes nothing of r(v).
- **`k_AB`, a lamp at rest counted by a moving transponding body: NOT
  READ, and it is the missing direction.** The world it needs: a lamp at
  rest emitting one record every T of its count on an open bar; a body
  with momentum on the bar's axis carrying the transponding rule of 2
  (c): at each arrival it re-emits one record toward the ground detector
  at the bar's far end; the ground detector's own count between the
  re-emitted records, over T, is `k_AB x k_BA` (the round trip's two
  factors in series: `(1 + v) / (1 - v)` under every r, the k-calculus's
  round trip, so the round trip alone reads nothing of r); the body's
  own count of the arrivals, read through a second lamp on the body
  emitting every T of its own count, gives `k_AB` against the ground's
  `k_BA`, and their ratio decides. The pins, from the formulas, before
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

## 5. Links

[DERIVATIONS_BEAM 4.3](../../DERIVATIONS_BEAM.md#43-a-moving-clock-the-rate-is-one-at-every-speed),
[17.6](../../DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes),
[17.7](../../DERIVATIONS_BEAM.md#177-the-proper-time-gate-without-a-root-two-counters-compared-against-the-whole-root-the-owners-word-2026-09-22-records-642-and-647);
[the clock loop, stage 1](../clock_loop/DERIVATION.md); [NATURE rows 4a, 4b
and 12](../../NATURE.md); [the covariant worlds](../../../examples/events/covariant/README.md);
[HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector).
