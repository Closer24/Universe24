# Gravitational light bending: what the six verbs give, what the age word gives, and where the factor 2 comes from (the open-problems physicist, read-only, 2026-09-21)

Problem (1) of the seven the Boss listed on the owner's question of
14:18Z (record 393 of the log of 2026-09-20, on the Boss's branch at the
time of writing), taken up on the owner's word of 14:23Z (record 396,
translated): "Gravitational light bending is important, isn't it? Why
don't we see it? Maybe it is attached only to light and not to the
clock." Read against the law on `main` at 1976d8dd (the clock's word
decided as the age word at 14:01Z, record 394; `clock-age-v1` not yet
built; form B not on `main`; `optical-v1` designed, reviewed BUILDABLE
and given the owner's go, not built). Every number is from
[light_bending_map.py](light_bending_map.py) beside this note (integers,
the flight rule and the unit label transcribed from BEAM_LAW section 3,
no engine import) and its output
[light_bending_map.out](light_bending_map.out); no run, nothing
registered, nothing decided. Notation as the workflow's rule: a scalar
plain, a vector in bold lowercase, every symbol named at its first use;
the grain family of record 369 where the outside reader looks (the
presence a_r, the age moment a_tau, the heading's pace c_h = 64 / 110
Links per interval, c^2 = 1 / 3).

## 0. The verdicts, stated at the top

| Candidate | What it is | Verdict |
| --- | --- | --- |
| (i) the age word for light only, the clock keeping the presence | a row's flight reads the age moment at its Node; a body's clock counts the presence | **NOT ADMISSIBLE**: the clock rows fail under the presence word (NATURE row 12, series T), and one constant of nature (G M / c^3 in Shapiro's delay and in the redshift) becomes two words with two forms (M / r for light, M / r^2 for clocks) |
| (ii) the age word for the clock only (record 394, the law's default) | a body's clock counts the age moment; a row reads nothing | **the law as it stands; it gives no bending and no delay**: series K's 0.000 pixel and 0.00 interval stand, a FAIL row of NATURE stated so that it fails; not an answer to the problem |
| (iii) one word for the clock and the row, f = 1 | the clock's count and the flight's wall read the same age moment at the same pair; the heading turns by the flow's transverse part at the clock's constant | **ADMISSIBLE WITH CORRECTIONS**: Newton's half, 2 G M / (b c^2) (0.876 arcsec at the Sun's limb), Shapiro's logarithm at half its coefficient; passes the three tests as `optical-v1` at `optical: 1`; the corrections are section 6's |
| (iv) `optical-v1` as designed, f = 2 declared | (iii) with the world's integer f = 2 in the wall and in the turn | **ADMISSIBLE WITH CORRECTIONS**: nature's 4 G M / (b c^2) (1.751 arcsec) and Shapiro's coefficient; the 2 is an input of the world, a row of the inputs ledger, not a number of the six verbs; the same corrections |

The one number that decides between (iii) and (iv) is nature's, not the
lattice's: the post-Newtonian parameter gamma (the space part of the
deflection over its time part), gamma = f - 1; the six verbs with one
word give gamma = 0, nature reads gamma = 0.99992 +- 0.00012 (VLBI,
Lambert and Le Poncin-Lafitte 2011, to verify against the source). The
answer to the owner's "why don't we see it": the law's flight reads
nothing of the crowd (BEAM_LAW note 47, the walk's row: "nothing"); the
crowd enters the clock, the push and, under the key `meeting`, the row's
direction with a grain constant; no rule ties a row's pace or turn to the
number a clock reads. And to "maybe it is attached only to light": the
deflection is light's, but its constant is the clock's; light needs the
word in addition to the clock, with the same pair, and beyond that a 2
the clock cannot give.

## 1. The pins, before any number

- **The bending.** Nature: `theta = 4 G M / (b c^2)` toward the mass, G
  Newton's constant, M the mass, b the impact parameter, c the speed of
  light: 1.751 arcsec at the Sun's limb (k = G M / (R c^2) = 2.12 x
  10^-6, the map's section E); Dyson, Eddington and Davidson 1920 read
  1.98 +- 0.16 and 1.61 +- 0.40 arcsec; VLBI reads gamma = 0.99992 +-
  0.00012. Newton's value for a particle at c (Soldner 1801) is half,
  `2 G M / (b c^2)` = 0.876 arcsec. The form is `M / b`; the ratio of
  the two is the factor 2, the time part and the space part of the weak
  metric one each.
- **The delay.** Nature: Shapiro's `Delta t = (2 G M / c^3) ln(4 r_1
  r_2 / b^2)`, the potential `M / r` integrated along the path; Cassini
  reads the coefficient's factor as 2 to 2 x 10^-5 (Bertotti, Iess and
  Tortora 2003).
- **The register.** Series K on `main`: the deflection 0.000 pixel and
  the delay 0.00 interval in every world, at a crowd where nature would
  capture the beam ([the lensing README](../../../../examples/events/lensing/README.md),
  [EXPERIMENTS K](../../../EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20)).
  Series K under `meeting-v1`: the centroid toward the mass by -1.79,
  -4.36 and -2.30 pixels at (M, b) = (2^12, 6), (2^13, 6), (2^12, 3),
  the form `M / b` with a grain constant, no delay in time
  ([EXPERIMENTS K under the meeting](../../../EXPERIMENTS.md#k-under-the-meeting-2026-09-20)).
  Series T: the age clock reads the distance, the presence clock does
  not ([EXPERIMENTS T](../../../EXPERIMENTS.md#t-the-clocks-word-2026-09-21)).
- **What must not move.** Series E's pair (`k_s r^2 = 41.5`, `k_a r =
  36.1` at [1, 2]); series K's registered worlds byte for byte (they
  declare `suspension` 0, so k = 0 under every candidate: section 5).

## 2. The GameBoard: one line of the fan, one row of light at b

**The pieces.** The mass is a measured event at the origin releasing one
unit per interval on each of the 290 primitive directions **D** = (a, b,
c) with `0 < |a| + |b| + |c| <= 6` (series E's and K's fan). Each unit is
a row flying the digital line of **D** at the pace `Q |D| / T_D` Links
per interval (Q = 64 the label's scale, `T_D = isqrt(3 |D|^2 Q^2)` the
direction's resolution), carrying its age tau (intervals since birth),
its amount (1) and its label **u**_d (the integer vector nearest `Q D /
|D|`). The row of light is a row of another number on the heading
(1, 0, 0), passing the mass at the Node (0, b, 0) on its way from (-26,
b, 0) to (26, b, 0) (series K: the lamp at x = 2, the mass at 28, the
screen at 54), dwelling `T_D / Q` = 1.72 intervals per Node on average
(1 or 2, the flight's accumulator).

**What the row's Node holds** (the one reading set of BEAM_LAW note 47,
the rows of the other number present there). At the Node (dx, b, 0) on
the row's line (the map's sections B and C):

| Reading | Its verb-level kind | What it is at the Node | The continuum's field (one source, the fan of every direction) |
| --- | --- | --- | --- |
| the presence P (a_r) | a scalar: the zeroth moment, the count of dwelling rows | the sum over the fan lines through the Node of their dwell (1 or 2) | `q / (4 pi r^2 c)`: `M / r^2` |
| the age moment A (a_tau) | a scalar: the first moment in the age | the sum over those lines of the ages at that Link (at b = 6, dx = 0: the line (0, 1, 0) at its Link 6, the ages 10 and 11, A = 21) | `3 q / (4 pi r)`: `M / r`, the retarded potential (DERIVATIONS 5.1) |
| the flow **V** | a vector: the first moment in the label | the sum of **u**_d over the lines' arrivals (one per line per interval) | `q Q / (4 pi r^2)` **r_hat**: `M / r^2` along the ray |
| the transverse gradient of A | a vector: a difference across the six Ports | `(A(dx, b + 1, 0) - A(dx, b - 1, 0)) / 2`: at this fan not a field (section 4) | `-(3 / Q)` **V**_perp exactly: `V = -(Q / 3) grad A` (5.1 with `c^2 = 1 / 3`) |

**Under the presence word** the row reads P (a scalar) and, as the
meeting reads it, **V** (a vector). **Under the age word** the row reads
A (a scalar) and the same **V**, which in the continuum IS the gradient
of A: the age moment's gradient across the row's line is not a second
reading but the flow the push already reads, at one Node, with no
neighbour. This is the identity that makes "the age word for light"
buildable at one Node (DERIVATIONS 5.1; the design's verb 2).

**Whether the heading turns, and by which verb.** A row's heading is its
direction label, an integer index into the world's table (`int16` in the
store). Of the six verbs, one moves it: the permutation (the arc
permutation `pi_t` of the direction table toward a target, BEAM_LAW
note 35 (ii)), fired by the evaluation (a comparison) of an accumulator
against a wall. The accumulator must carry a SIGN of direction, so it is
a translation of a vector (three integers on the row's record) at a rate
linear in **V**_perp; a scalar reading cannot fire it. So:

- A scalar (P or A) can enter only the translation's wall: the flight's
  accumulator (rate `2 S_1 Q d`, wall `2 T_D (d + f n A)`, S_1 the
  Manhattan length, [n, d] the suspension pair): the row's pace falls to
  `c / (1 + f k)` with `k = (n / d) x` the scalar. That is a delay, never
  a turn. One row on one digital line with a variable pace stays on its
  line.
- The heading turns only on the vector: `w -= f n T_D G (Q^2 V - (V . u)
  u)` per interval (G the angle's grain at load, **u** the row's own
  label), the comparison `w . t(D, D') >= d Q^5 THETA_G(D, D') (W - u) /
  W` per fan neighbour D', the permutation to D' on success with the
  remainder kept (the design's verb 2; the meeting's count on the phase
  per N units is the same permutation with a grain constant in place of
  the clock's `f n / d`).
- The deflection as a wave needs no turn verb: a fan of rows whose walls
  read A gains a phase per path that is the delay, and the click's
  exact phase (BEAM_LAW note 45) picks the stationary-phase direction,
  which is the ray equation's (the design's 5b, Fermat). Series K's
  beam of five directions within 5 degrees cannot show it (its rays
  land on fixed pixels); a wide-fan lamp beside a mass could. The ray
  form (the turn) and the wave form (the wall and the click) are one
  deflection when the turn's constant is the wall's gradient, which the
  design ensures; they are not to be added.

## 3. The deflection per Link, closed, and its sum against nature

Let `k(x) = (n / d) x` the count at the Node (the clock's own k), the
index `n_opt = 1 + f k`, the row along x at the transverse distance b.
The ray equation `d theta / dl = grad_perp n_opt` gives, per Link (the
map's section D):

| Light's word | k(r) | the turn per Link | the sum over the path (-L to L, L = 26) | the limit L -> infinity | the delay beyond the flight's |
| --- | --- | --- | --- | --- | --- |
| the age word, `k_a = (n / d) A` | `M / r` | `f k_a(b) b / (b^2 + x^2)^(3 / 2)` | `2 f k_a(b) L / sqrt(L^2 + b^2)` (0.974 of the limit at b = 6) | `2 f k_a(b)`: the form `M / b`; f = 1 Newton's half, f = 2 Einstein's | `(f k_a(b) b / c) 2 asinh(L / b)` = `(f k_a(b) b / c) ln(4 L^2 / b^2)` to `O(b^2 / L^2)`: Shapiro's logarithm |
| the presence word, `k_s = (n / d) P` | `M / r^2` | `2 f k_s(b) b^2 / (b^2 + x^2)^2` | | `pi f k_s(b)`: the form `M / b^2`, not nature's | `pi f k_s(b) b / c`: the form `M / b`, not Shapiro's |
| the flow (the meeting), **V**_perp | `M / r^2` along the ray, `b / r` of it transverse | `q Q b / (4 pi r^3)` = `-(Q / 3) dA / dy`: the age word's integrand | as the age word's, a grain constant in place of `f n / d` | none (the flight table is one speed) |

So the form of the bending, `M / b`, needs the index to be `M / r`, the
age moment, and its constant to be the clock's; the presence word as an
index gives `M / b^2` and a `1 / b` delay, both refuted by nature in
form; the meeting has the right integrand with the wrong constant. The
owner's intuition that the coupling is "attached to light" is right in
this sense: the bending is a rule on the rows, and the age word is the
word it needs. What it cannot give is the 2.

**Where the factor 2 comes from, and where it does not.** In nature's
weak field the index is `1 + 2 k`: the time part (`g_00`, a clock at the
Node runs slow by `1 - k`, and a wave whose local period is set by that
clock has the coordinate pace `c (1 - k)`) and the space part (`g_ij`, a
ruler at the Node is longer by `1 + k`, the wave crosses more coordinate
distance per period), first order in k each. On the GameBoard the clock's
word supplies the time part: one count, `sum amount x age` of the other
numbers' rows at the Node, entering the clock's owed accumulator and,
under one word, the row's wall at the same pair; that is f = 1, the
parameter-free case, Newton's half. The space part has no source in the
six verbs: the Link is the ruler, and nothing in the law lengthens a
path (the bent line's extra Links are second order in the angle, the
register's +0.50, +1.24, +0.31 intervals). It is an input: the world's
integer f = 2 in `optical-v1`, or a mechanism not yet named. One
correction to the derivation map ([21.4](../../../DERIVATIONS_BEAM.md#214-the-einstein-map-every-result-of-the-special-and-the-general-theory-its-status-today-what-the-six-give-what-must-be-added-the-pin),
row E13): the space half is FIRST order in k (the post-Newtonian gamma),
so the field's self-source (E16, second order in k, the post-Newtonian
beta) cannot supply it; "the space half needs the second-order field" is
to be replaced by "the space half is the world's f, an input; no rule of
the six verbs reads a ruler".

## 4. What the lattice does that the continuum does not: the beam's plane is the fan's comb

The map's finding, not in the design ([gr_rows/DESIGN.md](../../gr_rows/DESIGN.md)
section 4 took A(b) from the README's shell-mean formula, 11.4 and 22.7).

- **The shell means are the register's**: over r = 4 .. 14 the map's
  lines give `P r^2 = 39.6` and `A r = 68.7` (series E: 41.5 and 72.2,
  the ratio `A / (P r)` 1.72 to 1.75 against `sqrt 3`); the lines are
  the engine's (section A). But beyond r = 6 most Nodes of a shell lie
  on no line (63 % at r = 6, 17 % at r = 14): the field is a comb, the
  shell mean its average.
- **The beam of series K lies in the mass's plane** (the lamp, the mass
  and the screen at z = 20). Of the 290 directions 48 lie in that plane
  and never leave it; a line with `c != 0` visits the plane only in its
  first Links. Each in-plane line crosses the row's line once whatever
  b. So along the path the row reads (section D, per unit of `f n / d`,
  the crowd of one unit per direction per interval):

| b | crossings | A(0, b, 0) lattice / continuum | the turn via the flow, `sum 3 V_y / Q` | the closed form `2 k_a(b) L / sqrt(L^2 + b^2)` | the ratio | the delay `sum A / c_h` | the closed form | the ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 47 | 21 / 11.5 | 78.3 rad | 22.5 | 3.5 | 2834 intervals | 521 | 5.4 |
| 3 | 63 | 29 / 23.1 | 98.9 rad | 45.9 | 2.2 | 2202 intervals | 685 | 3.2 |

  From b = 6 to 3 the lattice's deflection grows by 1.26 where the
  continuum's `1 / b` doubles. The register under the meeting already
  shows it: -2.30 pixel at b = 3 against -1.79 at b = 6 (DETECTOR), the
  offline flight's -2.6 against -3.0. One Node off the plane the row
  reads a tenth of it (at (y, z) = (6, 1): 4 crossings, the transverse
  label sum 252 against the plane's 1670 and the isotropic 473; section
  E's table).
- **The gradient of A across the six Ports is not a field at this fan**:
  the neighbour difference along the row's line runs -42, -17, 0, +8, -2
  (b = 6) with sign changes from Node to Node, its sum 331 against the
  flow route's 78; the ratio `(-3 V_y / Q) / (dA / dy)` averages -0.34
  where the continuum gives 1. The identity `V = -(Q / 3) grad A` is a
  shell-mean identity, exact in the dense limit `P >> r` of
  [DERIVATIONS 3.2](../../../DERIVATIONS_BEAM.md#32-the-far-field-a-beam-does-not-dilute-a-shell-does),
  and the row's one-Node reading of the gradient is the flow, not a
  Port difference. (The same holds for any reading of `grad A` across
  the six Ports by a body, covariant-readings-v1's reading (ii): a
  shell-mean statement at this fan; named here for that program, not
  changed.)
- **The lesson of series T again**: a single clock or row on a line reads
  the lines, not the shell mean (the clock note's section 6, "the price
  of the word, named"); a pin for a row beside a mass is computed from
  the lattice's own lines, as this map does, or the run refutes the
  shell-mean number by a factor of 2 to 5 without refuting the rule.

## 5. Series K re-read under each candidate (the map, section E; no run)

**The registered worlds** declare `suspension` 0: `k = 0` under every
candidate, and the register's 0.000 pixel and 0.00 interval stand byte
for byte under (i) to (iv). The bending is not seen in series K because
the law has no rule on the rows AND because the world declares no pair;
under `optical-v1` the key is refused with `suspension` 0 (the design's
refusals), so the run that sees it is a new world.

**The pin world** of the design (must-fix 7: the mass x 16, the pair [1,
4096], the lamp's entry reading `age`, which record 394 makes the
default) re-read on the lattice's lines, the turn read from the flow at
every interval the row dwells (the design's verb 2), the delay from A at
every such interval (verb 1):

| Pair | World | M | b | `k_a(b)` lattice (the design's shell-mean) | the deflection, rad: f = 1 / f = 2 | the centroid's shift, pixels, DETECTOR if run (the bracket 0.5): f = 1 / f = 2 | the delay, intervals, DETECTOR if run (the bracket 1): f = 1 / f = 2 | the lamp's clock rate under the age word, GAMEBOARD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 4096] | `mass` | 2^16 | 6 | 0.0820 (0.0445) | 0.297 / 0.594 | -7.7 / -15.4 (the design: -4.63 at f = 2) | 10.7 / 21.5 (the design: 3.97) | 0.738 |
| [1, 4096] | `heavy` | 2^17 | 6 | 0.164 (0.0887) | 0.594 / 1.19 | -15.4 / -30.9 | 21.5 / 42.9 | 0.585 |
| [1, 4096] | `near` | 2^16 | 3 | 0.113 (0.0887) | 0.372 / 0.743 | -9.7 / -19.3 | 8.7 / 17.4 | 1.000 (the lamp's Node at (-26, 3, 0) lies on no line) |
| [1, 16384] | `mass` | 2^16 | 6 | 0.0205 | 0.0742 / 0.148 | -1.93 / -3.86 | 2.68 / 5.36 | 0.918 |
| [1, 16384] | `heavy` | 2^17 | 6 | 0.0410 | 0.148 / 0.297 | -3.86 / -7.72 | 5.36 / 10.7 | 0.849 |
| [1, 16384] | `near` | 2^16 | 3 | 0.0283 | 0.0929 / 0.186 | -2.42 / -4.83 | 2.17 / 4.34 | 1.000 |

At [1, 4096] the turn is 0.3 to 1.2 radian, dozens of whole fan steps of
2.4 degrees, outside the small-angle form and, for `heavy`, beyond the
box's faces (the register's meeting worlds lost 210 rays to the faces at
a smaller angle). The pair [1, 16384] keeps every shift above the
0.5-pixel bracket and every delay above the 1-interval bracket at angles
below 0.3 radian: the pin this note recommends, with the numbers above
as the pins, f = 1 and f = 2 two worlds each, the difference between them
the factor the run reads (the ratio of the two shifts 2.00 +- the
bracket). What the run cannot read at this fan: the `1 / b` form (the
plane's comb, section 4); a fan of P = 12 (about 8 times the rows, the
host cost to measure) or a beam one Node off the plane at a denser fan
would read it, a second pin, not needed for the factor.

**The Sun** (section E): f = 1 gives 0.876 arcsec, f = 2 gives 1.751;
nature's gamma reads f = 2.000 +- 0.0002.

## 6. The design under its own identity: `optical-v1`, with the corrections

The admissible candidate is the rule already designed, reviewed
BUILDABLE (gr_rows/REVIEW_ROUND2.md) and given the owner's go (record
303): a row's wall reads the age moment and its heading turns by the
flow's transverse part at the clock's constant, the factor f a declared
integer, the key `optical: f`. A second identity for the same rule would
be two names for one thing; none is proposed. What this note adds to the
design, for its writer (the physicist) as one bounded order, and for the
Boss:

1. **The one-word case named.** `optical: 1` is not a control but the
   six verbs' own number: the clock's word applied to the flight's wall
   with nothing added, Newton's half, PPN gamma = 0. `optical: 2` is the
   world's input, PPN gamma = 1. The paper's row states both and which
   nature reads; the inputs ledger (DERIVATIONS 24.1) gains the row
   "the factor f of the optical index, INPUT, 2 by nature's gamma" if
   the owner takes (iv).
2. **The pins from the lattice's lines**, not the shell mean: section
   5's table replaces the design's section 4 table (its 0.0445 becomes
   0.0820 at b = 6, the shifts and delays with it); the pair [1, 16384]
   in place of [1, 4096]; the lamp's rate in `near` 1.000, on no line.
3. **The plane named.** The beam of series K lies in the mass's plane,
   the fan's densest plane; the design's `1 / b` claim is a continuum
   claim the pin world cannot test; the register under the meeting
   (-2.30 against -1.79) is the evidence, not a defect.
4. **The gradient of A across the Ports** is not to be cited as a lattice
   reading at this fan; the flow is the reading, the identity `V = -(Q /
   3) grad A` its continuum warrant.
5. **Under record 394** the lamp's entry needs no `reads: age`
   declaration (the default), and the design's statement that the count
   ratio moves "by the pin world's own declaration" becomes "by the
   law's default word".
6. **The three tests** as the reviews found them stand: generic (one
   primitive, two moments of the one reading set, the world's f, [n, d],
   `THETA_G` and **t** at load, no family name); vector (a translation
   with a state-read wall, a translation of a vector accumulator at a
   bilinear rate, a comparison, a permutation on the fan, the remainder
   kept, no root, no float at run time); local (its own record and the
   moments of its own Node, fixed work per row for fixed K). Nothing here
   changes them.

## 7. The owner's question on the conditional derivations, for this problem

"Do we need to derive them, or is what we have enough?" For the bending:

- **What a derivation of the time part takes**: nothing beyond one word.
  The clock's owed count and the row's wall are one primitive (a count of
  the other numbers' rows at the Node entering an accumulator's wall at
  the pair [n, d]); stated once for everything that counts at a Node, the
  redshift, Shapiro's logarithm at half its coefficient and Newton's
  deflection follow (section 3's closed forms), the last as Fermat's ray
  equation from the wall alone (a wave statement, needing the fan and
  the exact phase) or as the turn verb tied to the same constant. This
  derivation exists in form (the design's 5b, DERIVATIONS 5.1); its run
  is the pin world of section 5.
- **What a derivation of the space part takes**: a verb the law does not
  have, one that lengthens a path or a ruler in a crowd. None of the six
  does; the self-source is the wrong order. So the space part is not
  derivable as the law is declared; it is an input, and the paper says
  so.
- **Can the paper stand with the conditional statement?** Yes, and more
  honestly than with a derivation claimed: "the law's flight is blind to
  the crowd (series K, registered); under `optical-v1`, the clock's word
  applied to the rows, the bending is `2 f G M / (b c^2)` with f the
  world's integer; the six verbs give f = 1 (Newton's 0.876 arcsec); f = 2
  is declared to meet the measured 1.751; the parameter that decides is
  PPN gamma = f - 1". A referee accepts a conditional theorem labelled
  so; what the referee will not accept is the 2 presented as reached.

## 8. Proposed lines for the documents I do not write

- **NATURE.md**, a row 13, the bending (the physicist): "13, the bending of
  light. Series K registers 0.000 pixel at every M and b (DETECTOR): FAIL
  against 1.751 arcsec (VLBI gamma = 0.99992 +- 0.00012). Under
  `optical-v1` at `optical: 1` the six verbs' own word gives Newton's
  0.876 arcsec, FAIL by the factor 2; at `optical: 2` the form and the
  factor of nature by the world's declared integer, the pin world's
  shifts -1.93 / -3.86 pixel at [1, 16384] not yet run."
- **DERIVATIONS_BEAM.md 21.4 row E13** (the derivation mathematician):
  the space half is first order in k (PPN gamma), not the second-order
  field; "to add" reads "the world's factor f under `optical-v1`, an
  input; the time half from one word (f = 1)"; the pin at [1, 16384] from
  the lattice's lines.
- **BEAM_LAW note 47** (the architect): the walk's row keeps "nothing";
  a note that under `optical-v1` it would read A and **V** of the one
  reading set, the one place after the meeting where the crowd enters
  the linear block.
- **The paper** (the coordinator): the confrontation table's bending row
  as NATURE's row 13 above; the open problems' item (2) restated: "no
  local mechanism" becomes "the mechanism is the clock's word on the
  rows, designed; the factor 2 is an input".
- **HIGHLIGHTS 5.4**: nothing; no decision here.

## 9. Questions for the owner, through the Boss

1. **The factor.** Does the paper carry (iv), f = 2 as a declared input of
   `optical-v1` (PPN gamma = 1 by declaration, an honest ledger row), or
   (iii), f = 1 as the law's own word with the bending row a FAIL by the
   factor 2? The physics does not decide; nature does, against (iii).
2. **The run.** The pin world of section 5 at [1, 16384], four worlds
   (`mass` and `near` at f = 1 and f = 2; `heavy` optional), is a build
   plus a run of series K's size (seconds each) once form B and
   `optical-v1` land; the run is not needed for this note's verdicts and
   is needed for the register's row. Ordered or not.

## 10. Links

[BEAM_LAW section 3](../../../BEAM_LAW.md#3-the-nodes-interval-nature_beam)
(the flight rule, the readings, the meeting, the self-creations) and its
[implementation notes](../../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
25, 35, 45, 47;
[DERIVATIONS_BEAM 5](../../../DERIVATIONS_BEAM.md#5-general-relativity-the-equation-of-the-delay-field)
(5.1 the two fields, 5.4 light) and
[21.4](../../../DERIVATIONS_BEAM.md#214-the-einstein-map-every-result-of-the-special-and-the-general-theory-its-status-today-what-the-six-give-what-must-be-added-the-pin);
[the optical-v1 design](../../gr_rows/DESIGN.md) and its
[second review](../../gr_rows/REVIEW_ROUND2.md);
[the clock's word](../../clock_age/NOTE.md);
the orbit's inward legs (docs/designs/orbit_read/NOTE.md on the branch claude/orbit-read at the time of writing, PR #597: the Manhattan factor of a fan, the same lesson);
[NATURE](../../../NATURE.md); [the lensing README](../../../../examples/events/lensing/README.md);
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).
