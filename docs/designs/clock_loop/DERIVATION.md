# Lorentz from the board, stage 1: a drifting loop's clock under two words, the resident count and the Gram form of its steps (the owner's word, 2026-09-22: "go for stage 1, the mathematician derives")

Derived by the derivation mathematician as DERIVATIONS_BEAM section 28 in
commit 1c0b514c0eb68ca1b9df86136e299d7d77860677 (branch
claude/derivations-beam, reverted there on the owner's split, revert
8b64c9c4); checked independently by the Loop Mathematician on 2026-09-22
(every identity re-derived by hand and confirmed in exact rational
arithmetic off the tree; the five items of the Boss's check AGREED, the
corrections folded into the text below and listed in section 6); landed
here on the Boss's order as the design note of stage 1
([record 674](../../LOG_2026-09-20.md#674-the-owner-go-for-stage-1-the-mathematician-derives-lorentz-from-the-board-the-order-2026-09-22-0255z-recorded-by-the-boss-at-0258z-the-owners-four-questions-and-the-bosss-answers-in-order-1-what-would-derive-lorentz-generically-from-the-board-alone-seen-through-a-detector-without-pins-the-bodys-clock-must-be-a-thing-on-the-board-a-loop-of-events-each-moving-one-link-per-interval-binding-as-a-loop-feature-14-read-by-the-lamp-the-drift-lengthens-the-loops-period-by-itself-the-light-clock-no-pin-the-obstacle-is-that-on-the-six-port-lattice-the-geometry-is-manhattan-a-resident-count-or-a-single-arm-gives-1---v-first-order-as-a14-writes-and-lorentz-is-even-in-the-speed-pythagoras-the-one-square-on-the-board-is-the-bilinear-verb-the-gram-form-since-second-moments-add-over-orthogonal-axes-and-counts-do-not-so-the-candidate-is-the-clock-as-a-second-moment-of-the-loops-events-over-the-six-ports-what-decides-is-a14s-run-the-pins-only-where-the-curve-meets-the-muon-the-bosss-conjecture-not-a-derivation-2-so-there-will-be-a-clock-row-at-a-node-that-is-actually-read-we-have-such-a-thing-no-yes-twice-the-lamp-newton-d3s-probe-carries-a-two-row-lamp-and-its-period-is-read-from-the-clicks-alone-and-the-clock-word-the-age-moment-a_tau-record-394-an-assumption-p9-in-the-paper-nothing-new-to-add-on-the-detectors-side-what-is-between-the-lamp-and-lorentz-is-what-drives-the-lamps-rate-an-accumulator-per-interval-today-no-slowing-route-a-or-the-bodys-own-loop-hypothesis-15-3-summarise-what-is-needed-what-it-gives-how-we-conclude-stage-1-a-derivation-on-paper-the-loops-rate-at-drift-v-for-two-clock-words-the-resident-count-and-the-gram-form-the-curve-for-each-stage-2-a-build-only-if-a-word-gives-an-even-curve-feature-14-under-a-key-off-by-default-the-gate-set-byte-identical-stage-3-a14-as-written-rest-and-v--12-13-14-18-axis-and-diagonal-64-intervals-the-clicks-counted-the-pins-from-the-derived-curve-and-its-competitor-before-the-run-the-conclusion-by-a-table-both-words-first-order-lorentz-does-not-come-out-and-the-identity-stays-beside-the-law-sqrt1---v2-in-one-word-that-word-goes-to-the-build-with-its-pins-the-clicks-on-the-curve-within-1t_d-on-axis-and-diagonal-lorentz-derived-at-rung-1-on-the-detector-and-the-muon-row-turns-from-fail-to-a-confirmation-axis-and-diagonal-apart-a-gameboard-anisotropy-reported-as-such-another-curve-back-to-paper-4-the-owners-word-go-for-stage-1-the-mathematician-derives-the-order-the-derivation-mathematician-session_01qeuzedtmbvpjjqn1enddpv-trig_01ts6qbxwsxxifcdggganzea-fired-0258z-after-the-proof-of-c-c-first-each-reported-separately-one-new-section-of-derivations_beam-about-two-hours-no-code-no-run-the-loops-clock-rate-at-drift-v-for-the-resident-count-and-for-the-gram-form-over-the-six-ports-the-matrix-stated-the-exact-lattice-expression-the-small-v-expansion-evenness-axis-against-diagonal-which-curve-where-the-square-comes-from-on-a-manhattan-lattice-the-additivity-of-second-moments-the-bosss-conjecture-confirmed-or-refuted-the-verdict-one-of-a-both-first-order-b-sqrt1---v2-in-one-word-with-a14s-pins-before-any-run-c-another-even-curve-with-what-distinguishes-it-at-the-muons-043-c-and-086-c-the-boss-opens-the-pr-the-physics-rule-reviewer-reads-it-stage-2-only-on-the-owners-word-after-the-verdict)).
A derivation on paper: no code, no run, no world file, nothing pinned from
a reading. Every number below is a closed form off the board, neither a
DETECTOR nor a GAMEBOARD reading; a root appears only in a closed form
off the board, never in a rule on it.

## 1. The object and the drift model (the assumption of this note)

In the loop picture of binding ([EXPERIMENTS A14](../../EXPERIMENTS.md#a14-kinematic-time-dilation-of-a-moving-bound-group),
feature 14; [HYPOTHESES 15](../../HYPOTHESES.md#15-time-dilation-from-transit-a-moving-bound-groups-clock-runs-at-1--v))
a bound body is a closed loop of events, each event stepping one Link per
interval along one of the six Ports, the loop's clock the period of its
loop, its tick the binding rule firing at the corners while the events
are resident. Units of this note: the Link and the interval, an event's
pace one Link per interval (the loop picture's c = 1; the Beam Law's
c = 1 / sqrt 3 enters only where the matrix diag(1, 3, 3, 3) is named).

The loop drifts at the velocity **v** (a vector, Links per interval):
its corners shift one Link every k intervals along the drift's
direction, v = 1 / k on an axis (v the speed, a scalar); on a diagonal
the DDA line shifts one Link on each of the diagonal's axes per k
intervals (two shift steps per k on a face diagonal, three on a body
diagonal). Over T intervals (T the run's length, a count) an event makes
T steps: R resident steps around the loop and S shift steps along the
drift, R + S = T, with S = abs(**v**)_1 T (abs(**v**)_1 the Manhattan speed,
1 / k on an axis, 2 / k on a face diagonal, 3 / k on a body diagonal; the
Euclidean speed abs(**v**)_2 is 1 / k, sqrt 2 / k, sqrt 3 / k). The loop's
geometry splits the resident steps over the axes in fixed fractions
**a** = (a_x, a_y, a_z), a_x + a_y + a_z = 1 (a unit square in the xy
plane, E5's ring: **a** = (1/2, 1/2, 0); a cube loop (1/3, 1/3, 1/3)).
The shift steps are the vector **S** = (S_x, S_y, S_z), S_x + S_y + S_z = S,
and **s** = **S** / T is the unsigned Manhattan velocity, its components
non-negative counts per interval.

**The drift model** (a shift interval per Manhattan Link of drift, every
event shifting together, no corner meeting in a shift interval) is A14's
"corners shifting", stated here as the assumption of this note; every
count below is exact under it (rung 1). **The convention for a diagonal
speed**, named because A14's numbers depend on it: A14 writes "v = 1/2,
1/3, 1/4, 1/8 Links per interval along an axis and along a diagonal"; this
note reads the diagonal's v = 1 / k as one Link on each of the diagonal's
axes per k intervals (the DDA line's own step), whose Euclidean speed is
sqrt 2 / k on a face diagonal; A14's entry should say which speed it
means, since both words' face-diagonal numbers (sections 2 and 3) change
with the reading.

## 2. Word (i), the resident count

The tick fires once per resident interval, so the clock's count over T
intervals is R and the rate relative to rest is

    rate_i = R / T = 1 - abs(v)_1,

exact over every whole number of periods k; over a run of T intervals
that is not a multiple of k the count is T - floor(T / k) or
T - ceil(T / k) by the DDA line's phase, exact within one tick (A14's 64
intervals at k = 3: 43 or 42 against 64 x 2 / 3 = 42.67, the 1 / T_D
bracket of record 674's criterion). On an axis 1 - v (1/2, 2/3, 3/4, 7/8
at v = 1/2, 1/3, 1/4, 1/8); on a face diagonal 1 - 2 / k = 1 - sqrt 2
abs(**v**)_2 (0, 1/3, 1/2, 3/4); on a body diagonal 1 - 3 / k = 1 - sqrt 3
abs(**v**)_2 (saturating at k = 3). First order in abs(v), with a cusp at
v = 0: the curve is unchanged under **v** -> -**v** (it reads the absolute
value) but it is not a function of v^2, which is what "even" means in
this note; and it is anisotropic by the Manhattan-to-Euclidean ratio,
sqrt 2 on a face diagonal and sqrt 3 on a body diagonal at the same
Euclidean speed. The curve is 1 - v, HYPOTHESES 15's, and it is not
sqrt(1 - v^2) (0.866, 0.943, 0.968, 0.992) at any v. Rung 1. (A14's "to
first order" is the count's own first order; under this drift model the
count is exactly linear.)

## 3. Word (ii), the Gram form of the steps over the six Ports

The second moment of the events' steps is the matrix **G** = the sum over
steps of **u** **u**^T, **u** the step's unit vector. For steps along the
axes **u** = +-**e**_i (**e**_i the unit vector of axis i), so
**u** **u**^T = **e**_i **e**_i^T and **G** = diag(g_x, g_y, g_z) with g_i
the number of steps along +-i regardless of sense: the second moment of
unit axis steps is the unsigned Manhattan count per axis, u_i^2 =
abs(u_i). This is the fact the note turns on: a sum of squares of unit
axis steps is linear in the steps; no square of a length arises from it.
Under the drift, exactly, with **g** = (g_x, g_y, g_z),

    g = R a + S = (T - S) a + S,      trace G = T.

Every bilinear form of the state **g** with a declared symmetric matrix
**M**, B(**g**) = **g**^T **M** **g**, is then a quadratic in T with
coefficients in the Manhattan velocity **s**. Writing alpha =
**a**^T **M** **a** (the rest value, B_rest = alpha T^2),

    B / T^2 = (1 - abs(s)_1)^2 alpha + 2 (1 - abs(s)_1) a^T M s + s^T M s.

The clock word: the n-th tick when n^2 P^2 alpha <= B (P the rest period;
a comparison of two bilinear forms, verbs 1, 2 and 6, no root on the
board; its counters grow with the run as 17.7 (2)'s do), so off the board
the rate is sqrt(B / (alpha T^2)).

- The first-order term in **s** is 2 (**a**^T **M** **s** - alpha abs(**s**)_1)
  = 2 (**M** **a** - alpha **1**)^T **s** (**1** the all-ones vector; abs(**s**)_1
  = **1**^T **s** since **s** is non-negative); it vanishes for every drift
  if and only if **M** **a** = alpha **1**, the condition for an even
  curve. The trace's form, **M** = **1** **1**^T, satisfies it and gives
  B = T^2: no dilation at all. Every even form is **M** = alpha **1** **1**^T
  + **M'** with **M'** **a** = 0, and then B / T^2 = alpha + **s**^T **M'** **s**
  exactly: even, second order, and it reads only the part of **s** that
  **M'** sees.
- For the square loop, **a** = (1/2, 1/2, 0), the symmetric matrices
  with **M'** **a** = 0 form a three-parameter family,

      M' = [[mu, -mu, nu], [-mu, mu, -nu], [nu, -nu, c]],   mu, nu, c declared

  (the symmetric forms on the plane orthogonal to (1, 1, 0), spanned by
  (1, -1, 0) and (0, 0, 1); the cross term nu couples the loop's plane to
  the third axis), so every even Gram clock of the square loop is

      rate_ii = sqrt(1 - lambda (s_x - s_y)^2 - c' s_z^2 - 2 nu' (s_x - s_y) s_z),

  lambda, c', nu' declared (the signs of mu, c, nu over alpha). On an
  axis (**s** = (v, 0, 0)) with lambda = 1: rate_ii = sqrt(1 - v^2)
  EXACTLY, Lorentz's curve (0.866, 0.943, 0.968, 0.992 at v = 1/2, 1/3,
  1/4, 1/8); it is the product form 4 g_x g_y = (T + S)(T - S) = T^2 -
  S^2, the light clock's Pythagoras written as a difference of squares:
  the x-count grows by the shift, the y-count shrinks by it, and their
  product is T^2 - S^2. The same on the y axis, and on the z axis with
  c' = 1. On the face diagonal of the loop's own plane (s_x = s_y, s_z =
  0): **g** = (T/2, T/2, 0), the same as at rest, so rate_ii = 1 for every
  k and every choice of lambda, c', nu': the drift is INVISIBLE to the
  steps' second moment (the resident steps lost on x are replaced one
  for one by shift steps on x, likewise on y). On a face diagonal out of
  the loop's plane (**s** = (v', 0, v'), v' = 1 / k) with lambda = c' = 1
  and nu' = 0: rate_ii = sqrt(1 - 2 v'^2) = sqrt(1 - abs(**v**)_2^2),
  Lorentz in the Euclidean speed (0.707, 0.882, 0.935, 0.984 at k = 2, 3,
  4, 8); the cross term nu' moves this reading and no axis or in-plane
  reading. On the body diagonal (**s** = (v', v', v')) with c' = 1:
  rate_ii = sqrt(1 - v'^2) = sqrt(1 - abs(**v**)_2^2 / 3) (0.943, 0.968,
  0.992 at k = 3, 4, 8 against Lorentz's 0.816, 0.901, 0.976 at the same
  Euclidean speed), short by the factor 3 in the square. So the even Gram
  clock with lambda = c' = 1 is Lorentz on the three axes and on the two
  face diagonals out of the loop's plane, blind on the loop's own face
  diagonal, and off by a factor in the square on the body diagonal: an
  anisotropy of the whole effect (sqrt(1 - v^2) against 1), not one
  within a tolerance; it is not a clock of the board, and the axis
  agreement is the coincidence (T + S)(T - S), the one place a square of
  the drift appears in a product of two linear counts.
- The same holds for any loop: **g** is invariant under a drift along the
  loop's own symmetric direction (**s** proportional to **a**, a
  realizable DDA direction for every non-negative **a**), since then
  **g** = (T - S) **a** + S **a** = T **a**; so no function of **g**,
  bilinear or not, detects that drift, and an isotropic even curve from
  the steps' second moment does not exist. Rung 1 (exact algebra on
  exact counts).

## 4. Where the square comes from, and the conjecture

The conjecture (the additivity of second moments over orthogonal axes)
is CONFIRMED for the form and REFUTED as the source: X^2 + Y^2 + Z^2 is
additive over the axes, as every diagonal quadratic form is, and so is
the Manhattan count abs(X) + abs(Y) + abs(Z); additivity does not choose
the square. What Lorentz needs is a square of the NET displacement,
abs(**X**)_2^2 = (the sum of the steps)^2, which is not a sum over steps
of anything: the board's accumulators sum steps, and a sum of unit axis
steps' squares is the step count. A square of the net displacement can
be formed on the board only from the accumulated first moments (T, X, Y,
Z) of the loop with a declared matrix: by verb 2 on them, Q = T^2 - (X^2
+ Y^2 + Z^2) in the loop's units, T^2 - 3 (X^2 + Y^2 + Z^2) in the Beam
Law's (the matrix diag(1, -3, -3, -3) on (T, X, Y, Z)); or, the same
thing as an accumulator, by verb 1 with a rate bilinear in the state
(Q raised by 2 T + 1 per interval and lowered by 3 (2 X + 1) per step on
x, 17.7 (4)'s construction), which needs the same declared matrix. The
owner's diag(1, 3, 3, 3) of 17.6 M3 is the momentum-space form of the
same declared 3 = 1 / c^2: positive definite, it gives E^2 = m^2 + 3
**p** . **p** (E the energy, m the mass in label units, **p** the
momentum), whose inverse reading m^2 = E^2 - 3 **p** . **p** is the
(+, -, -, -) form. A clock ticking when n^2 P^2 <= Q (no root on the
board, 17.7's construction) reads sqrt(1 - abs(**v**)_2^2 / c^2): even,
isotropic, Lorentz exactly (0.9028 and 0.5103 at the muon's 0.43 c and
0.86 c); but the square and its coefficient are the declared matrix's,
an input, and the rule is the covariant identity's proper-time gate in
the loop's letters, not a count the loop's geometry produces. The
lattice supplies the first moments exactly (X, Y, Z, T are counts); the
signature (+, -, -, -) and the 3 are declared.

## 5. The verdict: (A)

Both words of the board are first order in v or blind: the resident
count gives 1 - abs(**v**)_1, first order in abs(v), anisotropic by sqrt 2
and sqrt 3; the Gram form of the steps gives either the trace (rate 1),
the transverse count (1 - abs(**v**)_1 again) or an even form that is
Lorentz on the axes (sqrt(1 - v^2), the product of the two in-plane
counts) and 1 on the loop's own face diagonal, invisible to the drift
there. Lorentz does not come out of the board by itself; the only
isotropic even curve is the declared Minkowski form on the net
displacement, the covariant identity, which stays beside the law.

For the reviewer and A14, the closed forms the two board words would
carry, before any run (rates relative to rest at v = 1/2, 1/3, 1/4, 1/8
in the convention of section 1; no reading is pinned here, these are the
words' closed forms):

| Word | on an axis | on the loop's own face diagonal | on a face diagonal out of the loop's plane | on the body diagonal (k = 3, 4, 8) |
| --- | --- | --- | --- | --- |
| (i) the resident count | 1/2, 2/3, 3/4, 7/8 | 0, 1/3, 1/2, 3/4 | 0, 1/3, 1/2, 3/4 | 0, 1/4, 5/8 |
| (ii) the even Gram clock, lambda = c' = 1, nu' = 0 | 0.866, 0.943, 0.968, 0.992 (Lorentz's own numbers) | 1, 1, 1, 1 | 0.707, 0.882, 0.935, 0.984 (Lorentz in the Euclidean speed) | 0.943, 0.968, 0.992 |
| Lorentz, sqrt(1 - abs(**v**)_2^2), for comparison | 0.866, 0.943, 0.968, 0.992 | 0.707, 0.882, 0.935, 0.984 | 0.707, 0.882, 0.935, 0.984 | 0.816, 0.901, 0.976 |

What would distinguish the even Gram word from Lorentz at the muon's
0.43 c and 0.86 c: nothing on an axis (0.90 and 0.51 both), everything on
the loop's own diagonal (1.00 against 0.90 and 0.51): the direction
dependence is the test, and a rate that depends on the drift's direction
at the scale of the effect is a GameBoard anisotropy, reported as such
(A14's criterion). A14's run design must therefore name its diagonal
relative to the loop's plane. No root on the board anywhere above; the
roots are the closed forms' off the board.

**The three tests, for the even Gram clock read as a rule** (stated so
that stage 2, if ordered, starts from the verdicts): generic, PASS (one
primitive, the bilinear form of the record's own step counts with a
declared matrix, every loop alike through **a**, no family name); vector,
PASS as a comparison of two bilinear forms (verbs 1, 2 and 6, no root,
the same admission 17.7 (4) asks for its products); local, PASS (the
record's own counts, nothing kept at a Node). It fails nature, not the
tests: the curve is anisotropic at the scale of the effect.

## 6. The independent check (the Loop Mathematician, 2026-09-22)

The five items of the Boss's check against the text of 1c0b514c, each
re-derived by hand and confirmed in exact rational arithmetic on random
symmetric matrices, drift vectors and loop fractions (a scratch script,
not in the tree):

1. Word (i), rate 1 - abs(**v**)_1 with the closed forms of the axis and
   the face diagonal: AGREED. Folded: "odd" replaced by "first order in
   abs(v), a cusp at 0, not a function of v^2"; "exactly for every k"
   qualified to whole periods, within one tick otherwise (section 2).
2. Word (ii): AGREED on every identity (u_i^2 = abs(u_i); **g** = (T - S)
   **a** + **S**; the expansion of B / T^2; the first-order term and the
   condition **M** **a** = alpha **1**; the even form alpha + **s**^T **M'** **s**;
   4 g_x g_y = (T + S)(T - S) on an axis; rate 1 on the loop's own
   diagonal). Folded: the family of **M'** is three-parameter, the cross
   term nu between the loop's plane and the third axis was missing; it
   vanishes on every axis and on the loop's own diagonal, so the
   verdict's readings stand, and the face diagonals out of the loop's
   plane and the body diagonal are now stated (section 3, the table of
   section 5).
3. No isotropic even curve from the steps for any loop: AGREED (the
   invariance **g** = T **a** under **s** proportional to **a**, for every
   non-negative **a**).
4. The square of the net displacement only from the first moments with
   a declared matrix: AGREED in substance. Folded: the accumulator form
   (verb 1 with a bilinear rate) named beside verb 2; the sentence on
   diag(1, 3, 3, 3) reworded (the shared thing is the declared 3, not the
   signature).
5. The drift model an assumption, nothing pinned: AGREED. Folded: the
   convention for a diagonal speed named against A14's wording (section 1).

One view on the verdict: (A) closes stage 1 for the object as defined, a
loop of unit-Link steps through the six Ports under the drift model; item
3 is a proof over every loop shape. The one object outside this note is
a loop whose legs are the Beam Law's own rows on the fan's digital lines
at the Euclidean pace c through the flight's wall T_D = isqrt(3 abs(**D**)^2
Q^2) (**D** a direction of the table, Q the label's scale): there a light
clock's Pythagoras is supplied by T_D, but T_D is the root declared at
load (the same admission record 647 names for optical-v1), and the bound
pair in motion under the law is registered off Lorentz already
(DERIVATIONS_BEAM 12b.2: 1.31 to 1.43 against gamma, the Lorentz factor);
so it is a different object for the physicist, not a gap in this
derivation, and it does not reopen stage 1.

## 7. Links

[DERIVATIONS_BEAM section 17](../../DERIVATIONS_BEAM.md#17-the-law-above-newton-and-einstein-the-theorem-of-covariant-readings-built-on-newton-and-tried-on-lorentz)
(the covariant identity; 17.6 M3 the exact square; 17.7 the root-free
gate); [EXPERIMENTS A14](../../EXPERIMENTS.md#a14-kinematic-time-dilation-of-a-moving-bound-group);
[HYPOTHESES 15](../../HYPOTHESES.md#15-time-dilation-from-transit-a-moving-bound-groups-clock-runs-at-1--v);
[Highlights 5.4](../../HIGHLIGHTS.md), the lines "Speed
is a clock slowing", "Lorentz, A and B", "Lorentz, B replaced", "The
clock's word is the age word" and "Stage 1 of Lorentz from the board";
[the clock's word](../clock_age/NOTE.md) (the form of a design note);
[the three tests](../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).
