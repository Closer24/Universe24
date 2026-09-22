# Lorentz from the clicks: Bondi's two factors on the GameBoard, the one line that makes them one, and what the register has read (the owner's order, 2026-09-22, records 723, 725 and 728)

The derivation mathematician, 2026-09-22, on the Boss's order of about
04:30Z; a derivation on paper, no run, no code; every number a closed
form or a registered reading labelled by its kind (DETECTOR or
GAMEBOARD); the run, if any, is the owner's word.

## 0. The click theorem (the owner's word, records 745 and 749): the assumptions, the theorem, the proof sketch, the paper's frame

**The stance, first.** Lorentz of the real world is assumed here, not
proved: the theorem explains how a click brings Lorentz to a detector,
which amplitudes are needed to convert the clicks back to Lorentz, and
what the board must not contradict. No wall of the law, no declared
identity and no square of a momentum enters; the language is modern
algebra (groups on integer counts), no code and no run.

**Definitions.** Two worlds. The GameBoard: Nodes on the cubic lattice,
integer rows on them, and the tick, the interval's count, which no
detector ever reads. The real world: detectors and their clicks only. A
detector D at a Node has its own count `n_D`, its count of intervals
stretched by what arrives at it (the age wall's member at coefficient
1, record 709): an internal count that advances every interval and is
slowed by the crowd at its Node; the detector never reads the tick,
only `n_D`. A click is the event of receiving a packet (a record's
arrival at the detector's Node), stamped with `n_D`: a triple (the
Node, `n_D` at the arrival, what arrived); between arrivals `n_D`
advances on its own, which is how A emits every T of its own count
with nothing arriving (section 2). A click family `F_D` is the set of clicks of one detector and
its six neighbours, each with its counts and its contents. A detector's
velocity is a click that passes information to the detector beside it:
the pair (Nodes apart, counts apart) between two clicks of neighbouring
detectors, so a velocity is a ratio of two integers and never a reading
of the tick. Symbols: t and x the counts and Nodes apart along one axis
in the hop frame's units (one Node per interval, c = 1, section 1); u =
t - x and w = t + x the light-cone coordinates; k Bondi's factor; m the
mass angle and `kappa` the wave number of an amplitude; `omega` its
frequency per interval; r a detector's own count per interval against
the tick, a ratio the detector cannot see but two families can compare
through their clicks.

**The conversion, and the two assumptions that define it (the owner's,
records 745, 749, 753).** What is to be shown is a statement about a
CONVERSION: from the lattice and the momentum inside it (an integer
vector **p** on a record) to motion in the real world, the conversion
made by clicks that pass information, with the amplitudes of the
passing packet; the claim is that this conversion is Lorentz. The two
assumptions define the conversion. (A1) A click is the passage of
information from Node to Node, at most one Node per interval: c is the
unit, the same in every family, and nothing passes faster. (A2) A
click's content is an amplitude with a phase that splits each interval
between staying and hopping, the mass the staying share: the packet
that passes is converted by its amplitudes.

**Theorem (the click theorem).** The conversion defined by (A1) and
(A2), from the lattice's momentum to motion read by clicks, is Lorentz
up to a correction of relative order `m^2 v^2 / 6` in the rate, second
order in v at a fixed mass angle m and vanishing as m -> 0 (the spacing
over the reduced Compton wavelength), exact in the continuum limit,
with the lattice's own anisotropy beyond. In the algebra: let G be the set of transformations
between click families that preserve the conversion's structure: they
carry counts to counts and Nodes to Nodes linearly (the counts of a
family add, so a transformation is a Q-linear map on the counts'
ratios in the mean (section 2 (a)) of the pairs (t, x), up to a choice
of origin), and they preserve (A1) (a click that moves
one Node per interval in one family moves one Node per interval in
every family); G is the conversion's symmetry. Then: (i) G is a group,
and with (A1) alone it is the Lorentz group up to scale: in one dimension the maps `(u, w) -> (k u, w / k)` (and the
reflection `u <-> w`), the one-parameter group of boosts with the
invariant `u w = t^2 - x^2`, whose parameter is the one-way factor k of
section 2 and whose axiom is the equality of the two one-way factors
(`k_AB = k_BA`); in three dimensions the Lorentz group SO(1, 3) up to
scale and translation, by the theorem of Alexandrov and Zeeman (the
bijections of Minkowski space preserving the causal order are the
Lorentz maps, dilations and translations; Zeeman 1964). (ii) With (A2)
the group acts on the amplitudes as the covariance of the discrete-time
Dirac walk (section 6): the boost carries the walk's dispersion `cos
omega = cos m cos kappa` to itself to second order (`omega^2 - kappa^2 =
m^2 + O(4)`, the invariant of (i) on the amplitude's frequency and wave
number), so the boost also fixes the detector's own rate at `r = m /
omega = sqrt(1 - v^2) (1 - kappa^2 / 6 + O(4))`, `kappa^2 = m^2 v^2 / (1
- v^2)`, a correction of relative order `m^2 v^2 / 6`, second order in v
at fixed m and vanishing as m -> 0 (the loss of order is in the step
from the invariant to r, since `kappa / omega` is not small where the
angles are); the amplitudes with phase are
exactly what converts the clicks back to Lorentz: a click structure of
(A1) gives the group, and only (A2) gives the group something to act on
whose invariant is the proper time. (iii) The lattice's own symmetries
are the 48 (the 24 rotations of the six Ports with the hand), which
contain no boost; hence (ii) holds up to that correction of order `m^2
v^2`, and in three dimensions the board differs from the world in
direction from the fourth order on (the walk's `kappa^4` anisotropy),
where the two could be told apart.

**Proof sketch, in the algebra.** (a) The group: the composition of two
structure-preserving maps preserves the structure, the identity does,
and the inverse of a Q-linear bijection that carries the unit-speed
clicks onto themselves carries them back; so G is a group. (Over Z it
would not be: the only cone-preserving bijections of the integer pairs
are the reflections, the 48 in three dimensions, which is (iii), and the
inverse of a map such as (2, 1) is not Z-linear; over Q, under the
axiom, G is the boosts with rational k, `v = (k^2 - 1) / (k^2 + 1)`
rational, the hop frame's `1 / k`, dense in SO(1, 1), and the Lorentz
group up to scale is its closure.) (b) One
dimension: a linear map of (t, x) preserving the cone `{t = x} U {t =
-x}` maps the light-cone coordinates to multiples of themselves, `u ->
a u, w -> b w` (or swaps them), and every such map is a boost by `k =
sqrt(a / b)` times a dilation `lambda = sqrt(a b)`. The two one-way
factors of section 2 are `a = k_AB = r / (1 - v)` (A's counts read in
B's family) and `1 / b = k_BA = (1 + v) / r`, so `k = sqrt(k_AB k_BA) =
sqrt((1 + v) / (1 - v))` for EVERY r (the boost, Lorentz's, is r-free:
the round trip `a / b` reads nothing of r) and `lambda = sqrt(a b) =
r / sqrt(1 - v^2)` (the dilation carries r alone). The dilation is
physical here: it is the moving record's own rate r against the tick,
left free by (A1) alone, which is exactly what "up to scale" means; the
relativity of the two families, the two directions alike (`a = 1 / b`,
`k_AB = k_BA`), or (A2), is what fixes it at Lorentz's, `lambda = 1`, `r
= sqrt(1 - v^2)`, and then `u w` is invariant: `t^2 - x^2` is the same in
every family. The law as built fixes it at `r = 1`: `a = 1 / (1 - v)`, `1
/ b = 1 + v`, `lambda = 1 / sqrt(1 - v^2) = gamma = (k + 1 / k) / 2`, a
dilation by gamma away from Lorentz, which is why its round trip (`a /
b = k^2`) is Lorentz's and its one-way factors are not (sections 2 and
6) (the reviewer's "dilation by k" reads the same map with `b = 1 + v`,
the B-to-A factor taken as the multiplier of w rather than its inverse,
giving `lambda = sqrt(a b) = k`; the two readings differ only in the
naming of b, and the round trip `a / b` is r-free in either); `k = sqrt((1 + v) / (1 - v))`, `v =
(k^2 - 1) / (k^2 + 1)`, `gamma = (k + 1 / k) / 2`, the boosts compose by
`k_1 k_2` (a one-parameter abelian group, SO(1, 1)), the k-calculus of
section 2 (b) being the theorem's one-dimensional case. The scale: a
common factor `lambda` on u and w is a dilation, allowed by (A1) and
removed by fixing the count's unit in one family (the "up to scale").
(c) Three dimensions: the light cone is `t^2 = x^2 + y^2 + z^2` and the
group preserving it linearly is O(1, 3) times the dilations
(Alexandrov, Zeeman); the boosts along an axis are (b) with the
transverse Nodes fixed. (d) The amplitudes: under (A2) one interval of a
click's content is the unitary `U = S C` on a two-component amplitude
per Node, S the shift by one Node of the hopping component and C the
coin mixing the staying and the hopping components by the mass angle m;
its plane waves obey `cos omega = cos m cos kappa`; expanding to second
order, `omega^2 = m^2 + kappa^2`, which is the invariant `u w` of (b)
written on `(omega, kappa)` in place of `(t, x)` up to the sign of the
metric, so the boost of (b) carries the walk's small-angle plane waves
to plane waves of the same m: the walk is covariant to that order (its
continuum limit is the Dirac equation, exactly covariant), and its
group velocity `v = d omega / d kappa = cos m sin kappa / sin omega =
(kappa / omega) (1 - m^2 / 3 + O(4))` gives `r = m / omega = sqrt(1 -
v^2) (1 - kappa^2 / 6 + O(4))` with `kappa^2 = m^2 v^2 / (1 - v^2)`,
from `omega^2 = m^2 + kappa^2 - m^2 kappa^2 / 3 + O(6)`: the lattice's
correction to the rate is of relative order `m^2 v^2 / 6`, second order
in v at fixed m and vanishing as m -> 0 (checked here on six pairs of
angles: `r / sqrt(1 - v^2) - 1` over `kappa^2` between -0.1641 and
-0.1667, `v / (kappa / omega) - 1` over `m^2` between -0.3334 and
-0.3451; the section's arithmetic, not a run). Beyond second order in
the angles `cos m cos kappa` is not a function of `omega^2 - kappa^2`
alone, so the covariance fails there, which is (iii). (e) The 48 contain no boost because
they are finite and a boost has infinite order; so no lattice symmetry
implements a boost exactly, and (ii) is the best the lattice affords.

**What the theorem says of the law as it stands**, one sentence, a fact
and not an order: the law meets (A1) (one Node per interval, the flight
blind, section 1) and does not meet (A2), its hop being a whole-record
schedule with no staying amplitude (parts 4 and 5, sections 5 and 6),
so its clicks carry the group of (i) and, read by one clock, Lorentz's
radar (section 6, the sharpening's (b)), and lack the amplitude of (ii)
that would fix `r` at `sqrt(1 - v^2)`.

**The paper's frame, three sentences, marked as such (the owner's shape,
record 753).** To convert the lattice and the momentum inside it into
motion in our real world, one uses clicks that pass information, a
click being the passage of information from Node to Node at most one
Node per interval (A1) and its content an amplitude with a phase that
splits each interval between staying and hopping, the mass the staying
share (A2); Lorentz of the real world is assumed, and what is shown is
that this conversion brings it. The symmetry of the conversion, the
transformations between click families that preserve (A1) and (A2), is
the Lorentz group up to scale, acting on the amplitudes of the passing
packet as the Dirac walk's covariance, so that the passage of clicks is
Lorentz up to corrections of order `m^2 v^2`, exact in the continuum
limit, a detector's own rate `sqrt(1 - v^2) (1 - kappa^2 / 6)` with the
mass angle m the spacing over the reduced Compton wavelength; in three
dimensions the lattice's anisotropy begins at the fourth order. The
conversion is made exactly with the amplitudes, converting the packet
that passes, and it comes out from there; the law as built satisfies
(A1) and not (A2), a fact stated for the owner's word.

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
(docs/designs/light_speed/FORM.md section 3.1; the design
docs/designs/drive_b/DESIGN.md named in the order is on the branch
drive-b, 6e245ddd, not on `main`): the rate `abs(p)_1 Q` against the wall `Q^2 S M + abs(p)_1 T_h`,
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
formed in any wall of the drive on `main`. The exact claim, with its
exceptions named: the law forms one square of a LENGTH at load, the
flight table's resolution `T_D = isqrt(3 abs(D)^2 Q^2)` per direction
(nature_beam.py, the table's construction; the pace's isotropy within
`1 / T_D` that section 1 uses), and beside the law two keyed squares of
the momentum exist: optical-v1's `T(P) = isqrt(3 abs(P)^2 Q^2)` on a
pushed row (`momentum_pair`) and covariant-readings-v1's W; on `main`
the drive's wall is linear and the only square in the law's own
interval is the click's. What a cost would have to be for YES,
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
and at small m and k, `w^2 = m^2 + k^2 - m^2 k^2 / 3 + O(6)`, so `v = (k
/ w) (1 - m^2 / 3 + O(4))` and the rest share of the frequency is

    r = m / w = sqrt(1 - v^2) (1 - k^2 / 6 + O(4)),   k^2 = m^2 v^2 / (1 - v^2):

the clocks of such an amplitude, read as Bondi's two factors, agree
with Lorentz up to a correction of relative order `m^2 v^2 / 6`, second
order in v at fixed m and vanishing as m -> 0 (section 0 (ii); in three
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
would give the walk's dispersion, `r = sqrt(1 - v^2)` up to the
correction of order `m^2 v^2` and the anisotropy from the fourth: the clicks would behave like Lorentz in
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
rows present. What it would cost the registered pins: every pin that
reads a row's position, presence or age at a Node moves, which is the
whole register but the click's form. A beam that spreads changes the
presence and the age moment at every Node, so every clock reading moves
with it (the age wall's crowd at any detector or source: series T's
1.907 and NATURE row 12's PASS; the crowd worlds U, V and X, the shell's
5086 and its fixed point; G2's stars), and so does every tick derived
from the flight table (`Flight.manhattan_steps`: series K's delays,
D3's periods, series S's clicks 392, 369, 345); with them the flight's
own pins (series Q's face clicks, 290 of 290 at the derived interval;
L7's cone at the age 29; series C's "no dilution"; L2's fringes, the
fan's geometry replaced by the walk's own diffraction; the massive rows'
bands of 23.3, 36.5, 60, 83.5, the turn `abs(p) N / h` replaced by the
walk's group velocity; the covariant identity's gate, its r the walk's
and not a declared square). The two-slit and Bell clicks keep their
FORM (the click's evaluation is unchanged) with new numbers, and
nothing else does.
It would be a hypothesis under its own identity beside the law, the
pins rewritten before any run; not built here. The question: does the
owner want the flight to be a split with phase at every Node?

**The owner's sharpening (record 742), answered in five points.**

(a) The correspondence, in the law's letters. At the law's pace `v = p /
(Q S M + p)` the wall of the drive is the sum of two shares: the mass
share `Q S M` and the momentum share p; each interval the drive gains p
and carries one Link when it reaches the wall, so the momentum share is
what hops and the mass share is what stays, the mass slowing the
passage and c the bound as p outgrows `Q S M` (the pace tends to one
Link per interval on `main`, to the rows' `c_h` under form B's wall).
A change of direction costs momentum (the push, and the drive's signed
residual cancelling what was driven the other way, `step_axis`). And
`r = 1` is the declaration that the record's own count is the tick:
the self-creation fires every interval whether the record hopped or
stayed (`_suspend` gates it by the crowd alone). That is the owner's
picture and it is the law as built.

(b) Under `r = 1` every one-clock reading is Lorentzian. The round trip
of section 4, `k_AB k_BA = (1 / (1 - v)) (1 + v) = (1 + v) / (1 - v)`, is
exactly Bondi's `k^2`, so every radar reading (one clock, out and back:
a distance, a relative velocity, a rate read by echo) is the Lorentz
one; what differs is the one-way split alone, `1 / (1 - v)` and `1 + v`
against two equal roots `sqrt((1 + v) / (1 - v))`, a difference of
`1 - v^2` in their ratio (second order). This is the owner's
"demonstrate it in our world": the law's clicks, read by one clock,
already give Lorentz's radar; the one place they part from Lorentz is
the comparison of two clocks' own counts, which needs the second lamp
on the moving body (section 4's missing direction) to be read at all.

(c) The one difference, and the code. In the law the staying share and
the hopping share ADD AS AMOUNTS: the wall is `Q S M + p` (E = m + p,
the Manhattan dispersion, section 5), and a massive row's stay or hop
each interval is a schedule of the whole amount by one accumulator:
`nature_beam.walk_step`, "the residue gains the rate over the wall
(`by_drive_rows`, the one verb; the rate within the wall, so the count
is 0 or 1), and the step is the m-th unit step of the direction's line"
(`moved, _ = by_drive_rows(residue, rate, self.wall[direction])`; the
Link `self.lines[direction, place] * moved`, one whole step or none);
the phase advances at the Link only, `turned`: "the phase steps rows
gain at the Link they cross ... the remainder kept on the row"; and the
body likewise, `step_axis`'s `by_drive(drive, momentum, D, at_most=1)`.
Between the stayed and the hopped part there is no interference in
flight because there are no two parts: the row is one term of the group
ring at one Node with one phase; the merge (`merge_words`, "equal words
are identical rows") sums identical rows and cancels an equal opposite
pair of one record at one Node, a linear addition of terms that happen
to meet, never a split of one row. In the Dirac walk the two shares add
as amplitudes with a phase, linearly at every interval through the coin
(the staying and the hopping components of one amplitude are recombined
by a rotation before the next hop), and the square appears only at the
detection; the quadrature `w^2 = m^2 + k^2` is the composition of those
rotations, not a square taken in flight.

(d) The smallest change, restated exactly. It is not a square in flight
(verb 2's square before the next hop would be a measurement at every
Node and would kill the interference); it is the SPLIT: each interval a
row of amount a and phase f at a Node becomes a hopping row and a
staying row by one declared table over the circle (the splitter's `C'`,
`S'`, the two entries the coin's two shares; the mass angle m the
family's rest pair `[n, d]`, the hop's phase the flight's per Link), and
where the paths of one record meet at a Node the merge adds them as it
already does (verb 3, the cancel included); the square stays at the
click. The integers: the family's `[n, d]`, the split table at the
declared rounding (record 328), the row's amount and phase; the
recombination rule the existing merge. The three tests: generic (one
table per interval for every family, no name); vector (verb 2 for the
split's weights, verb 3 for the merge, no root); local (the row's own
Node and its six neighbours, the storage bounded by 6 N rows per Node
after the merge). The cost to the registered pins, as (4) states it:
every pin that reads a row's position, presence or age at a Node moves,
the whole register but the click's form (the flight's pins, every clock
reading through the age wall's crowd, every tick derived from the flight
table); the Bell family is NOT untouched: the
pair's rows would spread on their way to the settings and the click's
counts at the four settings would change, though the theorem's form
(exact marginals, the rungs) stands and `S(N)` would be recomputed from
the new arrivals; the two-slit fringes keep their form with new
numbers. A hypothesis under its own identity, its pins before any run;
the question for the owner: shall the row split at every Node?

**(5) The verdict for part (5): CLICKS BEHAVE LIKE LORENTZ IN OUR SPACE:
NO.** The hop is a pattern and the resident count is linear. The one
line that decides: every hop of the law is `by_drive` with `at_most` 1
on the whole record (`step_axis`, `walk_step`), the amount never splits
between staying and hopping, so no staying amplitude interferes with a
hopping one in flight, and the only square the law forms in its own
interval is at the click (the flight table's `T_D` is a square of a
length taken once at load, section 5 (v); the keyed squares of the
momentum are the hypotheses' beside the law, not the law's), at the
click over rows that have ended.

## 7. Part (6): is Eq. 14 derived from the conversion? The identity from the walk's dispersion, the factor 3, and the conversion table (the owner's word, record 764, as the Boss relayed it)

**The question, as the owner put it.** The paper's Eq. 14 (its label
`eq:square`), the covariant identity `W = E_0^2 + 3` **p** `.` **p** with
`E'` the largest integer whose square is at most W (DERIVATIONS_BEAM
17.6 M3, 17.7; covariant-readings-v1's gate and pace): is it simply
DERIVED, algebraically, from our equations? His reasoning: Lorentz need
not be put in by hand to reach the equations, because Lorentz was
reached through the clicks (section 0), so writing it into the
equations is permitted and nothing remains to prove; and from there the
equations of motion in the real world, how what is inside the board
passes to what is outside it. This part answers the three questions in
order: (1) the derivation, with the origin of the factor 3 and its
order; (2) the verdict line and its consequence; (3) the conversion
table. Record 764 is cited as the Boss relayed it; it is not yet in the
checked-out log.

**Certification of the inputs.** This part uses only: (1) the click
theorem's two assumptions (A1) and (A2) and its part (ii) (section 0);
(2) the amplitude walk those two assumptions define, `U = S C` on a
two-component amplitude per Node (section 0's proof sketch (d), section
6's Dirac walk), with its exact plane-wave dispersion on one axis, `cos
omega = cos m cos kappa`; (3) the law's own map from a row's phase to an
energy and a momentum, Planck's, already on `main`: `E = h f` with `h`
the family's quantum and the world's `h_A = h_q N` (DERIVATIONS_BEAM 6.4,
24.1 row 25, F08 closed), `lambda = h / p` and the wave number `k = 2 pi
p / h` per Link (23.2), and the rest energy of a family as its rest pair's
turn rate, `E_0 = h n / d`, so that in the identity's whole units (17.6
M3, `E / c^2 = 3 E`) `E'_0 = 3 h n / d = Q S M` by the load-time identity
`3 h n = Q S d` (17.6 M7, N5); (4) the lattice's c, input 9 of 24.1: `c =
1 / sqrt 3` Links per interval, the operator norm of the flight, derived
(13.2 (a), record 186), rounded by the grain to the heading's `c_h = Q /
T_h`, `T_h = isqrt(3 Q^2) = 110` at Q = 64 (input 10; FORM.md 3.1). Lorentz
enters through (A1) and (A2) only, never as an input; Eq. 14 appears
below only as the thing the result is compared with. No reading of a
run is pinned; every number is a formula's value or a registered
reading named by its kind.

**(1) The derivation.**

(a) *The walk's exact invariant and its orders.* Under (A1) and (A2) one
interval of a click's content is `U = S C`, and its plane waves
`exp(i (kappa x - omega t))` on one axis obey, exactly on the lattice,

    cos omega = cos m cos kappa,

m the mass angle of the coin (radians per interval), `kappa` the wave
number (radians per Node), `omega` the frequency (radians per
interval). This is the whole of the dynamics' constraint on
`(omega, kappa, m)`; there is no other. Expanding the cosines,

    omega^2 = m^2 + kappa^2 - m^2 kappa^2 / 3 + O(6)

(the coefficient `-1 / 3` checked on four pairs of small angles, the
residue `(omega^2 - m^2 - kappa^2) / (m^2 kappa^2)` between `-0.3336` and
`-0.3354`; the section's arithmetic, not a run). So the second-order
invariant is `omega^2 - kappa^2 = m^2`, the invariant `u w` of section 0
(b) written on `(omega, kappa)`, and the boost of (b) carries the walk's
plane waves to plane waves of the same m to that order (section 0 (ii));
the exact invariant is the cosine form, `cos m = cos omega / cos kappa`,
which is not a function of `omega^2 - kappa^2` alone and is therefore
not carried by any boost beyond second order. In three dimensions the
second-order form is `omega^2 = m^2 + kappa_x^2 + kappa_y^2 + kappa_z^2`
(the walk's continuum limit is the Dirac equation), the exact form
depending on the order of the three axis shifts (the walk's `kappa^4`
anisotropy, section 0 (ii)), which is why (ii) is stated to second order
in the angles and the three-dimensional exact form is not written here.

(b) *The map to the law's integers.* The conversion's variables are
angles per interval and per Node; the law's are counts. The map is
Planck's, and it is the law's own (input (3)): a row's phase advances
`n / d` turns per interval, so its frequency is `omega = 2 pi n / d` and
its energy `E = h n / d = hbar omega` with `hbar = h / (2 pi)`; its
wave number per Link is `kappa = 2 pi p / h`, so `p = hbar kappa`; and
the coin's mass angle is the family's rest pair, `m = 2 pi n_0 / d_0`,
so `E_0 = h n_0 / d_0 = hbar m`. Multiplying the second-order invariant
by `hbar^2`:

    E^2 = E_0^2 + p_hop^2,

with `p_hop` the momentum in the hop frame's unit, where the unit of
length is the Node hopped and `c = 1` Node per interval (A1). This is
the energy-momentum relation in units `c = 1`, derived from (A1) and
(A2) and the law's own Planck map, and nothing else; the `E_0`, `p`
and E of the law are the same counts multiplied by one common `hbar`,
so in whole units (`E' = 3 E`, `E'_0 = Q S M`, 17.6 M3, 23.2) the
identity reads `E'^2 = E'_0^2 + p'_hop . p'_hop` with the same
conversion on each term.

(c) *Where the factor 3 comes from, exactly.* The hop frame counts
length in Nodes hopped, one per interval, along the axes: a Manhattan
unit. The Beam Law counts length in Euclidean Links and its c is input
9, `c = 1 / sqrt 3` Links per interval: on the body diagonal a row
crosses one axis Link per interval, x then y then z, so three Nodes
hopped are `sqrt 3` Euclidean Links, and the pace is `sqrt 3 / 3 = 1 /
sqrt 3` Links per interval, which the flight table makes isotropic
within `1 / T_D` (`N_l abs(D)_2 / T_D`, prop:pace). So one Euclidean
Link per interval is `sqrt 3` hop-frame units, a momentum of p in the
law's unit (the pace `p / E'` Links per interval, 17.6 M1) is `p_hop =
sqrt 3 p` in the hop frame's, and

    E'^2 = E'_0^2 + 3 p . p:   the 3 is (abs(D)_1 / abs(D)_2)^2 on the body diagonal, 9 / 3, i.e. 1 / c^2 with c^2 = 1 / 3,

the conversion of the momentum's unit from Euclidean Links per interval
to light-Links per interval, and nothing about the three axes beyond
that: in the hop frame's own unit there is no 3, and `abs(kappa)^2 =
kappa_x^2 + kappa_y^2 + kappa_z^2` enters with coefficient 1 on each
axis. Eq. 14's 3 is therefore that factor EXACTLY in the lattice's
isotropic limit (input 9, derived), declared as the pair `[1, 3]` (24.1
row 11); it is a convention of the unit in the sense that it is 1 in
the hop frame and 3 in the Beam Law's Links, and it is not the heading's
own factor, `(T_h / Q)^2 = (110 / 64)^2 = 2.954`, the grain's rounding of
3 (input 10), which 17.6 M3 names as the alternative pair and which
would move the muon's 64th self-creation by 0.7 tick at 0.86 c (M3's
figure, a formula's value).

(d) *Exactly, or to second order.* The derived identity is Eq. 14 to
second order in the angles `(m, kappa)`, i.e. in `n_0 / d_0` and `p / h`
per Link, and not exactly: the exact lattice invariant is the cosine
form, and its fourth-order term makes the walk's frequency fall BELOW
Eq. 14's root,

    E'_walk = E'_14 (1 - m^2 beta^2 / 6 + O(6)),   beta = kappa / E'_14 = sqrt 3 p / E'_14 the identity's own velocity in units of c, m the rest angle in radians per interval,

so the walk's own rate `r = m / omega` is above `E'_0 / E'_14 = sqrt(1 -
beta^2)` by the same relative amount (checked on four pairs of angles,
the ratio to `m^2 beta^2 / 6` between 1.000 and 1.020) and its gate falls
earlier. In the velocity the clicks read, the walk's group velocity `v =
(kappa / omega) (1 - m^2 / 3 + O(4))`, the same fact is section 0 (ii)
as corrected: `r = sqrt(1 - v^2) (1 - kappa^2 / 6 + O(4))`, a correction
of relative order `m^2 v^2 / 6`, second order in v at fixed m; and the
identity's pace `p / E'` is the walk's group velocity only up to that
relative `m^2 / 3`. The
size, on the muon of series S (`E'_0 = 13248`, `p = 3640` and `12856`,
`W = 215 258 304` and `671 339 712`, `E' = 14671` and `25910`, beta
0.4297 and 0.8594, gamma 1.1074 and 1.9558, `T_64 = 1 + floor(63 E' /
E'_0) = 70` and `124`, the register's integers reproduced here from Eq.
14 alone, GAMEBOARD by kind): at a rest angle of one turn in 64
intervals (`m = 2 pi / 64 = 0.0982`, an illustration of the formula, the
muon's own pair not read here) the correction is `2.97 x 10^-4` and `1.19
x 10^-3` of `E'`, 4.4 and 30.7 units of `E'`, and moves `T_64` by 0.02 and
0.15 tick: below one tick, below the pins' two ticks, invisible to the
register at that pair, growing as `m^2`. Eq. 14's EXACTNESS on the record
(`E'^2 <= W < (E' + 1)^2` at every interval, 24.1 row 38) is thus not the
conversion's: the conversion is exact in the cosine form and quadratic
only to second order; the record carries the quadratic form exactly by
declaration (record 270). One remark, not a proposal: the exact cosine
invariant is expressible in the law's own tables C and S at the scale
256 (input 13), `C(omega) x 256 = C(m) C(kappa)` within the tables'
rounding, with no root and no square of the momentum; the owner may
want it named beside the declared square.

**(2) The verdict line.** EQ. 14 IS DERIVED FROM THE CONVERSION (A1,
A2): YES TO SECOND ORDER (in the angles m and kappa; in the velocity,
up to corrections of order `m^2 v^2`). The one line that decides: the conversion's
whole constraint is `cos omega = cos m cos kappa`, whose second order,
`omega^2 - kappa^2 = m^2`, times `hbar^2` in the hop frame's unit and
times 3 on the momentum in the Beam Law's Links, is `E'^2 = E'_0^2 + 3`
**p** `.` **p**, and whose fourth order is `-m^2 kappa^2 / 3`, not zero.
The consequence, stated as a fact for the owner: Eq. 14 enters the law
as the CONVERSION'S identity, licensed by the click theorem, the
identity of what the clicks read of an amplitude that hops under (A1)
and (A2), and not declared bare (record 270's line restated: the
readings built beside the law under their own identity, against the
same pins); but the law's own rows still hop whole (parts (4) and (5):
every hop `by_drive` with `at_most` 1 on the whole record, no staying
amplitude interfering with a hopping one, the walls linear in
`abs(p)_1`), so the law's rows meet (A1) and not (A2), and the identity
is the READING'S, not yet the ROWS' dynamics. The owner's inference holds
in this form: Lorentz may be written into the readings without a
further proof, because the readings are the conversion and the
conversion is Lorentz up to corrections of order `m^2 v^2`; it may not
yet be said of the
rows' motion, which would need the split at every Node (part (5)'s
smallest change) or stand, as it does, as the law's FAIL row beside the
readings (HIGHLIGHTS 5.4, record 270).

**(3) The conversion table: inside the board to outside it.** The
owner's "equations of motion in the real world". Inside: a record at a
Node with its rest count `E'_0 = Q S M` (label units; `E_0 = h n_0 /
d_0` its rest turn rate), its momentum **p** (label units, the pace `p /
E'` Links per interval under the identity, `p / (Q S M + p)` per axis on
`main`), its amount a, its phase f on the circle N, its own count
`n_B`, and the crowd `a_tau` at its Node. Outside: what a detector
reads through clicks, each line an integer formula, its order of
exactness (rung 1 exact on the GameBoard within the accumulator's
remainder; up to `m^2 v^2` where the walk's cosine form is the exact one),
its kind, its inverse where one exists, and the registered readings on
it. The law's forms and the identity's forms are given side by side,
the law's being the FAIL row of record 270.

| Outside (the reading) | Inside (the record) | The formula, the law | The formula, the identity | Order | Kind | Inverse | Registered readings on this line |
| --- | --- | --- | --- | --- | --- | --- | --- |
| the velocity v: Nodes apart over counts apart between two clicks of neighbouring detectors (section 1) | **p**, `E'_0` | per axis `abs(p_a) / (Q S M + abs(p_a))` Links per interval (P9, 4.4), rational, linear on both sides | `p / E'` Links per interval, `beta = sqrt 3 p / E'` in units of c, `E' = isqrt(E'_0^2 + 3 p . p)` | rung 1 within `1 / T` of the count and `1 / T_D` of the pace; the identity's beta within `1 / E'` | DETECTOR (a ratio of two counts) | law: `p = E'_0 v / (1 - v)` exact; identity: `3 p^2 = E'_0^2 beta^2 / (1 - beta^2)`, p the whole root within 1 | series S: beta 0.3040 for the star `s_mz2` at its declared momentum (the identity's pace), 0.2674 under the law's (GAMEBOARD, the drive's pace; the detector reads only 1 + z below) |
| the rate r: the moving record's own count per tick | `E'_0`, `E'` | 1 at every speed, stretched by the crowd alone (`age_wall`, 4.3) | `E'_0 / E' = sqrt(1 - beta^2)` within `1 / E'`; the gate `T_n = 1 + floor((n - 1) E' / E'_0)` (17.7) | rung 1 on its integers; the walk's own r above it by `m^2 beta^2 / 6` | GAMEBOARD (not read as a measurement, section 4; readable only through the two lamps of section 4's world) | `E' = E'_0 / r` | series S: the 64th self-creation at 70 and 124 (GAMEBOARD, the `become` lines; gamma 1.1074 and 1.9558), the pins 71 and 125 within one tick; J4's 64 at every speed under the law (pinned, not run) |
| `1 + z = k_BA`: a lamp on the moving record counted by a detector at rest, the energy it reads `E_read = h f_read = (1 + z) E_emit` | the lamp's rest pair, **p**, r | `1 + v` (r = 1) | `gamma (1 + beta)` within the count's grain | rung 1 within `1 / T` | DETECTOR (the pointer's z at the fixed detector) | law: `v = z`; identity: `beta = ((1 + z)^2 - 1) / ((1 + z)^2 + 1)` from the round trip `k^2 = (1 + beta) / (1 - beta)` | NATURE 4b: G2's `z = 0.2636` at beta 0.2674 under the law (FAIL against nature's 0.315); series S: `z = 0.3674` at beta 0.3040, gamma 1.04967 (`1.04967 x 1.3040 = 1.3688`), the pin 0.369 +- 0.003, PASS under the key in its domain |
| `k_AB`: a lamp at rest counted by the moving transponding record | r, **p** | `1 / (1 - v)` | `sqrt((1 + beta) / (1 - beta))` | rung 1 within `1 / T` | DETECTOR (the record's own count of the arrivals, read through its second lamp) | `v` from `k_AB` and `k_BA` together: `r = k_AB (1 - v)`, the ratio `k_BA / k_AB = (1 - v^2) / r^2` decides r | NOT READ: the missing direction (section 4); pinned from the closed forms only |
| the round trip `k_AB k_BA` | **p** | `(1 + v) / (1 - v)` | `(1 + beta) / (1 - beta)` | rung 1 within `1 / T`, r-free under every r (section 0 (b)) | DETECTOR | `v = (k^2 - 1) / (k^2 + 1)` | none registered; reads nothing of r under any r |
| the arrival: the detector's own count at a row's arrival from a Node D Links away | the release count `n_0`, the line D, the crowd at the detector | intervals of flight `L T_D / (N_l abs(D)_2)` for L Euclidean Links along D, `T_D = isqrt(3 abs(D)^2 Q^2)`, within one interval (the flight table, rem:nodispersion), i.e. `sqrt 3` intervals per Link within `1 / T_D`; the detector's own count at that tick stretched by its crowd (the age wall's member at coefficient 1) | the same flight (the rows are the law's; the identity moves bodies, not rows) | rung 1 | DETECTOR (the count at the click), the tick itself GAMEBOARD | `L` from the count and the pace, within one Link | series S: the products' face clicks at 369 and 345 (DETECTOR; the pins 367 and 345 within two ticks; the decay tick derived back by the flight table, 70 and 124); series T: the crowd's stretch, the ratio 1.907 at the distances 6 and 3 against the pin 1.909 +- 0.05 (DETECTOR, the age word; NATURE 12) |
| the energy of a record read at a click: the count of clicks over many records at one Node | a, f (the amount and the phase) | the click's square `f^T G f` of the summed rows at the Node, normalised by the record's total (6.5, 6.7, 23.2: Born at the click within `1 / (2 N)`) | the same | rung 1 (the click's form; input 12) | DETECTOR (a click) | none: a and f are never read singly, only their square summed at a Node; the phase only through interference at the click | the two-slit and Malus rows (24.3 row 4); not a Lorentz line |

Two facts of the table for the owner. First, every DETECTOR line is a
ratio or a difference of counts, never the tick, so the whole passage
from inside to outside is the click theorem's conversion, and the
identity's column is Lorentz's up to corrections of order `m^2 v^2`
because the conversion is; the law's column differs from it only where r enters (`1` against
`sqrt(1 - beta^2)`), which is the one place the register can decide
(section 4's missing direction). Second, the inverse map exists on
every line but the last: from `(v, 1 + z, the arrival count)` a detector
recovers **p** and `E'_0` up to the accumulator's remainder, but never
the amount a and the phase f of one record; those pass outside only as
the click's square over many records, which is Born's rule at the click
and the reason the board's inside is not the outside's inverse image.

## 8. Part (7): Newton Outside, the same way (the owner's word, record 772, as the Boss relayed it)

**The owner's word, and the two words.** "If you got Lorentz above the
board from the clicks, you will get Newton too, and perhaps more; the
same way: take assumptions and show that under them the formulas come
out; where none comes out, an experiment Inside rises Outside; it is not
exactly a proof, it shows that this is Lorentz; the paper more modern
algebra, fewer experiments." Inside is inside the GameBoard, where no
one measures (the tick, the rows, a body's accumulators, the host's view
of them: GAMEBOARD by kind); Outside is the game above the board, the
detectors and their clicks, which represents reality and is not reality
(DETECTOR by kind). This part does for Newton what section 0 did for
Lorentz: the assumptions as few as the law allows and in its own words,
the formulas that come out Outside under them with their order, and for
each formula SHOWN, MEASURED ONLY or NEITHER, with the one line that
decides. Record 772 is cited as the Boss relayed it; it is not yet in
the checked-out log. One difference from section 0 is stated first:
Lorentz needed (A2), which the law's rows do not have (part (5)), while
every assumption below is on `main` today, so Newton Outside stands
nearer the law than Lorentz Outside does.

**(1) The assumptions, stated as such.** Five, in the law's words, and
one piece of mathematics that is not an assumption.

- (N1) *The crowd.* What a body reads at its Node is the age moment
  `a_tau` of the rays of other numbers there, the sum over those rays of
  amount times age (the clock's word, the owner's decision of record
  394; the paper's P9, its fourth clause; `core.integer.age_wall`'s
  docstring). Each row carries its age, the intervals since its release.
- (N2) *The age wall.* The crowd stretches the wall of a body's
  self-creation count by `a_tau` at coefficient 1: a count at the rate
  `rate` against the wall `wall` becomes the count at `rate x d` against
  `wall x (d + a_tau n)`, `[n, d]` the world's suspension pair
  (`age_wall`; `measured.AGE_WALL_SET = (("owed", 1),)`), so after every
  self-creation the body owes the whole part of `a_tau n / d` intervals
  before the next (the paper's "What is delayed"): its rate is `1 / (1 +
  a_tau n / d)`.
- (N3) *The push.* Per interval a body of content `M_A` gains the
  momentum `-M_A` **V** from the rays arriving at its Node, **V** their
  label flow (the gravity column of `nature_beam.push_form`: "the count
  is `|V M_A|` exactly, the law's `-M_A V_B`"; DERIVATIONS_BEAM 3.3),
  and its pace per axis is `|p_a| / (N_l N_w M_A + |p_a|)` Links per
  interval (the paper's P9, second clause; 4.4).
- (N4) *The flight blind (P9).* A source of content `M_B` releases rows
  at the rate `q` per interval on a fan of K directions, and every row
  flies by the flight table at the pace c of its direction, isotropic
  within `1 / T_D`, reading nothing of the crowd (P9, first clause;
  input 7 of 24.1).
- (N5) *The reading (A1, and record 768).* Nothing leaves the board but
  clicks, one Node per interval at most; a clock Outside is a pulse and
  its return: a lamp's rows read at a detector, `1 + z` the inverse slope
  of the birth ordinal against the click's tick (series T's and X's
  method), or the round trip of section 2; the detector's own count is
  itself stretched by its crowd (N2 at the detector).
- (M) *The spreading, not an assumption.* K beams from one Node cross a
  shell at distance r at K of its `N(r)` Nodes; the mean over the shell
  of what a Node reads is the beam's value times `K / N(r)`, and `N(r) ->
  4 pi r^2` in space (`2 pi r` on the plane), the lattice's count of Nodes
  on a shell with its ripple (Gauss's circle problem, `N(r) = 2 pi r +
  O(r^theta)`, `theta <= 131 / 208`; the paper's `eq:shell`). This is
  the arithmetic of six Ports, not a law: on one beam the flow is the
  same at every Node (`1 / r^0`) and off every beam it is 0; the inverse
  square is the density of beams over a shell, and it exists per Node
  only in the limit of every direction (rung 2, the shell mean; rung 3
  on a fan declared as a cube, whose anisotropy is `3^(3/2)`).

**(2) The formulas that come out Outside.** Each with its assumptions
named and its order: rung 1 exact on the GameBoard; rung 2 a limit (the
shell mean, the Link to zero, `v << c`); rung 3 a limit under a spatial
condition.

(a) *The clock's rate in a crowd.* From N2 alone: `rate = 1 / (1 + k)`,
`k = a_tau n / d`, rung 1, exact at every k, never 0 at a finite count
(no horizon; 5.2). Outside, by N5: the ratio of two lamps' `1 + z` at
one detector is the ratio of their rates, `(1 + k_2) / (1 + k_1)`,
within the count's grain; the detector's own `k_D` divides both alike
and cancels in the ratio (series X's note on record 569).

(b) *The form of k about a source.* From N1, N4 and M: a row of age
`r / c` dwells `tau_L` intervals per Link (`T_D / (N_l |D|)`, 1.72 on a
heading, `sqrt 3` in the limit of every direction), so the presence at
r is `q tau_L / (4 pi r^2)` and the age moment is the presence times the
age, `A(r) = q tau_L / (4 pi c r)` (DERIVATIONS 5.1; the paper's
`eq:fields`): the clock's word falls as `1 / r`, the retarded potential
of the release, and obeys the wave equation with the release as its
source, Poisson's in the static limit; rung 2. Two consequences that
are Newton's theorems and not assumptions: outside a point source the
ratio of two clocks' shifts at the distances 3 and 6 is `2.00` (the
potential's form; the flux's would be 4.00 in the shift's ratio and
1.00 in series T's rate ratio); inside a shell of sources the age
moment is flat and the presence is not (the shell theorem for `1 / r`,
from M applied to every source of the shell: the `1 / r` weights over a
sphere sum to a constant inside), rung 2 with the lattice's ripple.

(c) *The falling body's acceleration.* From N3, N4 and M: the push per
interval in the shell mean is `-M_A <V>` with `<V> = q N_l / N(r) -> q
N_l / (4 pi r^2)`, and at `|p| << N_l N_w M_A` the drive gives the
acceleration `push / (N_l N_w M_A)`, so

    a = - G M_B / r^2,   G = K eta / (4 pi N_w)   (space; on the plane a = - G' M_B / r, G' = K eta / (2 pi N_w)),

`eta` the release per unit of content per direction (3.3; the paper's
`eq:newton`): the inverse square, rung 2 (the shell mean), retarded at
c, with the ripple of M at finite r and the first-order inertia of the
drive (`p = N_l N_w M v / (1 - v)`) beyond `v << c`. On a beam there is
no inverse square (rung 3: `1 / r^0` along the beam). Nothing of A
enters: the equivalence principle is rung 1, exact record by record
(the push is `M_A` times the flow, the drive divides by `M_A`; 3.3's
item 1).

(d) *Kepler's third law.* From (c) and the drive at small p: a circular
orbit has `v^2 / r = G M_B / r^2`, so `T = 2 pi r^(3/2) / sqrt(G M_B)`
in space and `T = 2 pi r / v` with `v` fixed by the momentum on the
plane, `T ~ r` (the `1 / r` force; DERIVATIONS 24.1 row 58, entry 58):
rung 2, `v << c`, the period above the Newtonian by `1 / (1 - v / c)` at
first order under form B's inertia. The ratio at two radii is a
theorem of the force's scale symmetry alone: a `1 / r` force is
invariant under `r -> lambda r, t -> lambda t` at the same speed, so
loops started with the same momentum at `r = 12` and `24` are similar
figures with `T(24) / T(12) = 2` for any eccentricity, a property no
other power of r has (the D3 entry); the pin from the map before the
run, `2.00 +- 0.18`.

(e) *The equivalence of the clock's slowing and the fall.* From (b) and
(c): the clock reads the age moment A and the push reads the flow,
which in the static limit is the gradient of the same field, `a = -(N_l
c / tau_L) grad A` (the paper's "the two fields of one stream"): one
crowd, two readings, the potential and its gradient, rung 2. The
constant between them is the world's: the clock's shift between two
heights h apart is `delta k = (n / d) delta A` and the fall's `g h =
(N_l c / tau_L) delta A`, so `delta k = (n tau_L / (d N_l c)) g h`, where
nature has `g h / c^2`; the law has the FORM of the equivalence (one
field read twice) and its constant is the suspension pair `[n, d]` with
the residence factor, a declared input, not `c^2` (NATURE row 12's
note: the scale is the suspension pair's). Stated as a fact, not a
failure: the paper's G likewise carries Newton's constant through
`N_w`.

**(3) For each formula: SHOWN, MEASURED ONLY, or NEITHER.** SHOWN: it
comes out algebraically under the assumptions at the rung named.
MEASURED ONLY: no closed form Outside; the register's run rises Outside.
NEITHER: no closed form and no reading. The register's rows by kind.

| The formula Outside | Verdict | The one line that decides | The register (DETECTOR unless labelled) |
| --- | --- | --- | --- |
| the clock's rate `1 / (1 + k)`, `k = a_tau n / d` | SHOWN, rung 1 | N2 is the formula: the owed count's whole part of `a_tau n / d` per self-creation | series T: the age word's `1 + z` 2.6517 at 3 and 4.1500 at 6 Links from equal crowds (NATURE 12); series X: the controls 1.0000 exactly |
| the `1 / r` form of k about a point source (the potential, not the flux) | SHOWN, rung 2 (the shell mean, with the ripple) | age times presence: `(r / c) x 1 / r^2` (N1, N4, M) | series T: the ratio of the two shifts 1.907 against the pin `1.909 +- 0.05`, the continuum's 2.00 outside it by the lattice's grain (PASS on the form; the presence word 1.000, FAIL); series X outside: `k(12) / k(4) = 0.6285` against the pin 0.618270 (MET), the continuum's 0.5 outside the tolerance by the grain |
| the shell theorem's flat interior (Poisson's source term) | SHOWN, rung 2 | the `1 / r` weights of a shell sum to a constant inside, the `1 / r^2` weights do not (M on every source) | series X inside: the age word `k(2) / k(4) = 1.0029` against the pin `1.003917 +- 0.02` (MET, flat); the presence word 0.8400 against 0.839989 (MET, not flat: the FAIL the design expected) |
| the ripple of the shell mean at finite r (the departure from `1 / r` and `1 / r^2`) | MEASURED ONLY | `N(r)` is the lattice's count of Nodes on a shell, no closed form at finite r (Gauss's circle problem, an exponent bound and no formula) | series X's 0.6285 against the continuum's 0.5 and T's 1.907 against 2.00, the grain read; series E's shell means (GAMEBOARD, the probes: `k_a r = 36.1` within `+- 15` percent) |
| the inverse square of the fall, `a = -G M_B / r^2` | SHOWN, rung 2; its decisive reading Outside NOT MADE | the push `-M_A <V>` with `<V> -> q N_l / (4 pi r^2)` (N3, M); on the plane `1 / r` | series D3 on the plane: the ratio `T(24) / T(12) = 1.997` (1.82 to 2.18) inside its bracket, consistent with `1 / r` and not decisive (the loops read are not similar figures: the radii 1.4 to 73.2 about 24.2 against 11.0 to 62.3 about 33.7, one recurrence each); the deciding reading (similar loops at a finer grain) not run; series C's `1 / r` on the plane and the exponent `r^-1.83` on the 2616-direction shell: GAMEBOARD, the probes' momenta (records 562, 564) |
| the equivalence principle (the fall independent of `M_A`) | SHOWN, rung 1 | `M_A` multiplies the push and divides the drive, record by record (N3) | series D3: the held mass four times at `r = 24`, 138 of 139 common birth ticks at the same Node (the largest difference 1 Node), `|dT| = 0`, the same escape tick; 3.3's `push_m = m x push_1` for m = 1, 4, 16 (GAMEBOARD) |
| Kepler's third law, `T^2 ~ r^3` in space, `T ~ r` on the plane | SHOWN, rung 2 (`v << c`); the exponent in space NOT READ | the circular orbit under (c) and the drive; the ratio 2 at two radii the `1 / r` force's scale symmetry (entry 58) | series D3: 1.997 for `2.00 +- 0.18` (inside); the periods 19 percent above their circles alike (outside: the loops are not circles, the plane's grain), read as history; entry 58's host check in space `T(24) / T(12) = 2.8284 = 2^(3 / 2)` at S = 512 (GAMEBOARD, not after a detector) |
| the equivalence of the clock's slowing and the fall (one field, the potential and its gradient) | SHOWN in form, rung 2; the constant a declared input | `a = -(N_l c / tau_L) grad A` in the static shell mean; `delta k = (n tau_L / (d N_l c)) g h` | series T and X read the potential's side, D3 the gradient's, on different worlds; no world reads both on one crowd: the one reading that would close the constant is NOT MADE |
| the post-Newtonian terms (the perihelion's `3 / 2` of the potential's square; the clock at second order `1 - k + k^2` against `1 - k - k^2 / 2`; a horizon) | NEITHER (a different law, stated) | the push is bilinear in the flow and the content, no `v^2 / c^2` and no `(G M / r c^2)^2` term (5.3); the clock never stops (5.2) | none Outside; series E's strong-field ratios (k = 2 to 9) GAMEBOARD |
| the value of G (Newton's constant as a number) | NEITHER Outside | `G = K eta / (4 pi N_w)` names it from the world's inputs; no detector reading of G is registered (the paper: "G not read") | none |

**(4) Certification of the inputs.** N1 to N5 are the law's own words
on `main` (record 394 and P9 for N1 and N4; `age_wall` and the owed
count for N2; `push_form` and the per-axis drive for N3; A1 and the
clicks for N5); M is arithmetic (the count of Nodes on a shell). Nothing
Newtonian is an input: no `1 / r^2` is assumed anywhere, it comes out of
M applied to the beams of N4; no potential is assumed, the `1 / r` is
the age carried by the rows (N1) over the spreading (M); no equivalence
is assumed, `M_A` cancels in N3; no Kepler is assumed, the third law is
(c) with the drive; no `c^2` in the equivalence, the constant stays the
world's `[n, d]` and `tau_L`. Where a formula needs the shell mean it is
marked rung 2, and its finite-r departure is MEASURED ONLY. Every number
in the table is a registered reading named by its kind or a pin written
before its run; none is pinned here from a run.

**(5) The verdict line.** NEWTON OUTSIDE FROM THE ASSUMPTIONS: PARTLY.
SHOWN under N1 to N5 and M: the clock's rate `1 / (1 + k)` (exact), the
equivalence principle (exact), the `1 / r` potential and the `1 / r^2`
flow of one stream with Poisson's equation, the shell theorem's flat
interior, the inverse square of the fall, Kepler's third law and the `1
/ r` force's scale symmetry, and the equivalence of the clock's slowing
and the fall as one field read twice (all in the shell mean, rung 2,
`v << c`); and these SHOWN formulas are MEASURED where the register
reads them: the potential's form (T, 1.907; X outside, 0.6285), the flat
interior (X, 1.0029), the equivalence (D3, 138 of 139), the scale
symmetry's ratio (D3, 1.997). MEASURED ONLY: the lattice's departure
from the continuum at finite r (X's 0.6285 against 0.5, T's 1.907
against 2.00, D3's periods 19 percent above their circles), which no
closed form gives and the runs rise Outside. NEITHER: the inverse
square's decisive reading after a detector (D3 consistent, not
decisive, the similar loops not run), the constant of the equivalence
and the value of G, and the post-Newtonian terms, which the law does not
have. The one line: Newton's formulas are the shell mean of five rules
the law already runs, so they are shown and not assumed; what the
lattice adds at finite r is not a formula but a reading.

**Three sentences for the paper (marked as such; the paper coordinator's
to take or leave).** (i) Newton's law is not assumed by the model: the
inverse square is the density of beams over a shell, the potential is
the age the rows carry over that density, and a body's acceleration is
the gradient of the clock's field, all three the shell mean of the rules
P9 and the age wall, exact in the limit of every direction and departing
from it at finite radius by the lattice's count of Nodes on a shell,
which has no closed form and is read (series T, X, D3). (ii) The
equivalence principle is exact on the GameBoard, the content multiplying
the push and dividing the drive, and it is measured after a detector
(series D3, 138 of 139 births at the same Node with the held mass four
times). (iii) What the model does not have it states: no term of the
post-Newtonian order enters the push, the clock in a strong crowd reads
`1 - k + k^2` and never stops, and the value of G is a world's inputs
and is not read.

## 9. Links

[DERIVATIONS_BEAM 4.3](../../DERIVATIONS_BEAM.md#43-a-moving-clock-the-rate-is-one-at-every-speed),
[17.6](../../DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes),
[17.7](../../DERIVATIONS_BEAM.md#177-the-proper-time-gate-without-a-root-two-counters-compared-against-the-whole-root-the-owners-word-2026-09-22-records-642-and-647);
[the clock loop, stage 1](../clock_loop/DERIVATION.md); [NATURE rows 4a, 4b
and 12](../../NATURE.md); [the covariant worlds](../../../examples/events/covariant/README.md);
[HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector).
