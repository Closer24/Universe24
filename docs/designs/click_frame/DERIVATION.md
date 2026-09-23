# Lorentz from the clicks: Bondi's two factors on the GameBoard, the one line that makes them one, and what the register has read (the owner's order, 2026-09-22, records 723, 725 and 728)

The canonical statement of this algebra is [docs/ALGEBRA.md](../../ALGEBRA.md), section 3 (the click algebra) and 5.1 (the click theorem); this file is kept as the record of 2026-09-22.

The derivation mathematician, 2026-09-22, on the Boss's order of about
04:30Z; a derivation on paper, no run, no code; every number a closed
form or a registered reading labelled by its kind (DETECTOR or
GAMEBOARD); the run, if any, is the owner's word.

## 0. The click theorem (the owner's word, records 745 and 749): the assumptions, the theorem, the proof sketch, the paper's frame

**The stance, first.** Lorentz of the Outside (the game above the
board, which represents reality and is not reality; the owner's word)
is assumed here, not proved: the theorem explains how a click brings Lorentz to a detector,
which amplitudes are needed to convert the clicks back to Lorentz, and
what the board must not contradict. No wall of the law, no declared
identity and no square of a momentum enters; the language is modern
algebra (groups on integer counts), no code and no run.

**Definitions.** Two worlds. The GameBoard: Nodes on the cubic lattice,
integer rows on them, and the tick, the interval's count, which no
detector ever reads. The Outside: detectors and their clicks only. A
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
vector **p** on a record) to motion Outside, the conversion
made by clicks that pass information, with the amplitudes of the
passing packet; the claim is that this conversion is Lorentz. The two
assumptions define the conversion. (A1) A click is the passage of
information from Node to Node, at most one Node per interval: c is the
unit, the same in every family, and nothing passes faster. (A2) A
click's content is an amplitude with a phase that splits each interval
between staying and hopping, the mass the staying share: the packet
that passes is converted by its amplitudes. LOCALITY OUTSIDE (the
owner's word, 2026-09-22, as the Boss relayed it: "velocity in the real
world is passing a click with information to the neighbouring Node and
receiving that packet there, having in effect moved there; the packet
passes from place to place, it cannot jump: a kind of locality also
Outside"): every Outside passage is a chain of clicks between
neighbouring places, so the Outside inherits the Inside's locality
through the conversion. It forbids a reading that would need a jump, a
velocity above one Node per interval of the tick, which in a detector's
own count (the frame's definition of a velocity Outside, section 1) is
`1 / r_D` Nodes per count, `r_D` the detector's own count per tick, so
that light in a crowd reads its c in the detector's stretched count and
not above it (series T's clocks, `r_D = 1 / 2.65` at 3 Links), and a
detector reading at a place no chain of clicks reaches. It is A1 read from above, and it FOLLOWS
FROM A1 ALONE together with the definition of Outside (nothing leaves
the board but clicks, P6): every Outside event is a click, every click
moves information one Node at most, so every Outside passage is a chain
of neighbour steps; a theorem, not an added assumption, with the one
exception the title names, the pair's click, one gather of one record
from both settings, which is not a chain of neighbour steps and is the
law's one non-local operation. THE BASIS INSIDE, THE OPERATION OUTSIDE
(the owner's word, 2026-09-22, as the Boss relayed it, which may become
the paper's foundation): "in the real world we are built of clicks; to
move a click from place to place one puts it into the board and takes
it out; that is motion in the real world, and the transformation must
be done there; the basis is Inside, and we are operated Outside, by
emitters and clicks." Stated as an assumption: what exists Outside is
made of clicks, and every change of place Outside is an emission into
the board (a lamp's birth, a transponder's re-emission), a passage
Inside under the six verbs, and a click out; there is no Outside
dynamics of its own. Whether it is A1 plus the conversion or more: its
first half (every Outside passage is Inside's passage read by clicks)
is A1 with the definition of Outside, as locality Outside is; its second
half (that WE are built of clicks, that the emitters and the detectors
are themselves records of the board and not a second kind of thing) is
MORE than A1: it is the statement that the apparatus is inside the law,
which the law today does not carry (a detector, a lamp and an external
body are declarations of the world file, not records that hop; the
paper's P7 to P8 and the external-body note), so it is an assumption
about the world, or a programme for the law, and not a theorem of the
conversion.

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
motion Outside, one uses clicks that pass information, a
click being the passage of information from Node to Node at most one
Node per interval (A1) and its content an amplitude with a phase that
splits each interval between staying and hopping, the mass the staying
share (A2); Lorentz of the Outside is assumed, and what is shown is
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
emission count `t - x` and its reception count `t + x` (c = 1), that is
`x = (n_r - n_e) / 2` and `t = (n_r + n_e) / 2` with `n_e` the count at
emission and `n_r` at reception. THE DEFINITION ADOPTED, named: this is
Einstein's 1905 light-signal definition of distance and simultaneity
(Bondi's radar convention), the symmetric half of the round trip; the
boost's form as a map of coordinates below rests on it, while the
r-free readings do not (the ratio `k_BA / k_AB`, the round trip, the
composition of boosts, the aberration are ratios of counts and need no
coordinate). B's
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
below only as the thing the result is compared with. In so many words
(the owner's requirement, "part 6 must close W from the assumptions"):
NO SQUARE IS DECLARED ANYWHERE IN THE CHAIN; W's form comes out of the
walk's invariant (`omega^2 - kappa^2 = m^2`, the second order of the
cosine identity, itself the composition of the coin's rotations) and
the Planck map, not from record 270's declaration; and the one input
beyond the six verbs is (A2), the split with phase, which the rows as
built lack (part (5)), so that on the law as built W is still the
declared identity of record 270 for the rows' dynamics and the
conversion's identity for the readings. No reading of a
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
Planck's, and it is the law's own (input (3)), one map for E and p: a
row's phase advances `n / d` steps of the circle N per interval (23.2),
so its frequency is `f = n / (d N)` cycles per interval, `omega = 2 pi
n / (d N)` radians per interval, and its energy `E = h_q n / d = h_A f =
hbar omega` with `hbar = h_A / (2 pi)` (`h_A = h_q N`, 24.1 row 25); its
wave number per Link is `kappa = 2 pi p / h_A`, so `p = hbar kappa` with
p in the law's unit per Link; and the coin's mass angle is the family's
rest pair, `m = 2 pi n_0 / (d_0 N)`, so `E_0 = h_q n_0 / d_0 = hbar m`
(the same with `n / d` read in turns when N is absorbed). The walk's
wave number is per Node hopped, and one hop-frame Node is c times one
interval, `1 / sqrt 3` Link (input 9), so `kappa_hop = c kappa` radians
per Node and `hbar kappa_hop = c p`. Multiplying the second-order
invariant `omega^2 = m^2 + kappa_hop^2` by `hbar^2`:

    E^2 = E_0^2 + c^2 p^2,   c^2 = 1 / 3, p per Link,

the energy-momentum relation, following from (A1) and (A2) and the law's
own Planck map, and nothing else.

(c) *Where the factor 3 comes from, exactly.* From (b), `E^2 = E_0^2 +
c^2 p^2` with p per Link. The identity carries its energy in the whole
unit `E' = E / c^2 = 3 E` (17.6 M3, `E'_0 = Q S M`), so

    W = (E / c^2)^2 = E'_0^2 + p^2 / c^2 = E'_0^2 + 3 p . p:   the 3 is 1 / c^2,

and `1 / c^2 = d = 3` is the dimension of the lattice: on the body
diagonal a row crosses one axis Link per interval, x then y then z, so
d Nodes hopped are `sqrt d` Euclidean Links and `c^2 = 1 / d` (a square
lattice would give 2; the dimension sets it), which the flight table
makes isotropic within `1 / T_D` (`N_l abs(D)_2 / T_D`, prop:pace). In
the hop frame's own unit there is no 3, and `abs(kappa_hop)^2 =
kappa_x^2 + kappa_y^2 + kappa_z^2` enters with coefficient 1 on each
axis. Eq. 14's 3 is therefore `1 / c^2` EXACTLY in the lattice's
isotropic limit (input 9, derived), declared as the pair `[1, 3]` (24.1
row 11); it is a convention of the unit in the sense that it is 1 in
the hop frame and 3 in the Beam Law's Links. The lattice's own `1 /
c_D^2 = (T_D / (N_l abs(D)_2))^2` from `T_D = isqrt(3 abs(D)^2 Q^2)` at
Q = 64: 2.9541 on a heading (`T_D = 110`), 2.9707 on a face diagonal
(156), 3.0000 exactly on the body diagonal (`192 = 3 Q`); the anisotropy
at most 1.5 percent, the root's rounding (input 10), the grain and not
a geometric factor, which 17.6 M3 names as the alternative pair and
which would move the muon's 64th self-creation by 0.7 tick at 0.86 c
(M3's figure, a formula's value). And the pace: `p / E' = c^2 p / E`,
which by (b) is `c^2 hbar kappa / (hbar omega) = c^2 kappa / omega = c
kappa_hop / omega` Links per interval, the walk's group velocity to
leading order (`v_g = (kappa_hop / omega)(1 - m^2 / 3 + O(4))` Nodes per
interval, section 0 (d), times c per Node); so the identity's pace `p /
E'` (17.6 M1) is a RESULT of the conversion, not an input to it.

(d) *Exactly, or to second order: the velocity named.* The derived
identity is Eq. 14 up to corrections of relative order `m^2 beta^2`
(`m^2 beta^2 / 3` on W, `m^2 beta^2 / 6` on `E'` and r), exact in the
continuum limit (the same words as section 0's order statement), and
not exactly: the exact lattice invariant is the cosine form, whose
fourth-order term `-m^2 kappa^2 / 3` is the relative correction `-m^2
beta^2 / 3` to W and makes the walk's frequency fall BELOW Eq. 14's
root,

    E'_walk = E'_14 (1 - m^2 beta^2 / 6 + O(6)),   beta = kappa / E'_14 = sqrt 3 p / E'_14 the identity's own velocity in units of c (kappa the wave number per Node here), m the rest angle in radians per interval.

Three statements are true at once, and the velocity must be named in
each: against Eq. 14's own `beta = sqrt 3 p / E'_14 = kappa / omega_14`
the walk's rate `r = m / omega` is ABOVE `sqrt(1 - beta^2)` by `m^2
beta^2 / 6` (checked on four pairs of angles, the ratio to `m^2 beta^2 /
6` between 1.000 and 1.020); against `kappa / omega_walk` it is above by
`kappa^2 / 6`; against the velocity the clicks read, the group velocity
`v_g = (kappa / omega) (1 - m^2 / 3 + O(4))`, it is BELOW `sqrt(1 -
v_g^2)` by `kappa^2 / 6`, which is section 0 (ii)'s statement, a
correction of relative order `m^2 v_g^2 / 6`, second order in v at fixed
m (at m = 0.01, kappa = 0.03 the three are `+1.50 x 10^-5`, `+1.50 x
10^-4` and `-1.50 x 10^-4`; my arithmetic and the reviewer's agree). The
identity's pace `p / E'` is the group velocity up to the relative `m^2
/ 3` (step (c)). Its gate falls earlier than Eq. 14's. The
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
A2): YES TO SECOND ORDER (up to corrections of relative order `m^2
beta^2`, `m^2 beta^2 / 3` on W and `m^2 beta^2 / 6` on `E'` and r, exact
in the continuum limit; section 0's words). The one line that decides: the conversion's
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

**(3) The conversion table: Inside formulas, Outside formulas, and the
map between them (the owner's word, record 777, as the Boss relayed
it).** The owner's correction of the first draft of this table: `W =
E'_0^2 + 3` **p** `.` **p** is a formula INSIDE the board, on the record,
read by no detector; from an Inside formula one must show which
formulas come out OUTSIDE, and the connections between the two are the
mathematician's to make. So the table has two sides. An Inside formula
is a GameBoard quantity, made of the law's six verbs and nothing
else, with its source line; an Outside formula is a detector reading,
following from an Inside formula by the conversion of (A1) and (A2) and
nothing else, nothing entering from outside the law. Each row: the
Inside formula, the Outside formula, the conversion that joins them
with its order of exactness (rung 1 exact on the GameBoard within the
accumulator's remainder; rung 2 a limit; "up to `m^2 v^2`" where the
walk's cosine form is the exact one), the inverse where one exists, and
the registered reading that sits on the Outside side, by kind. The law's
form and the identity's form are both given where they differ, the
law's being the FAIL row of record 270. The last three rows are part
(7)'s (section 8), in the same shape.

| INSIDE (a GameBoard quantity, from the six verbs; its source) | OUTSIDE (a detector reading) | The conversion, and its order | Inverse | The registered reading on the Outside side (kind) |
| --- | --- | --- | --- | --- |
| the exact square `W = E'_0^2 + 3` **p** `.` **p** on the record and `E'` the whole root kept by comparisons (17.6 M3; 24.1 row 38); on the law no square, the wall `Q S M + p` linear (section 5) | four Outside readings (the paper's "the step beneath and the step above"): (1) `E^2 = E_0^2 + p^2 c^2`, which is W times `c^4` in the whole unit (`E = c^2 E'`, exact on the identity's integers, the factor 3 entering as `1 / c^2` when p is counted per Link); (2) the gate `E'_0 / E'` as `1 / gamma`, the detector's own rate (exact on the identity's integers; the law's `r = 1`), read through the two lamps of section 4; (3) the drive's fraction `p / E'` as the click's velocity, Nodes apart over counts apart (to second order: within `m^2 / 3` of the walk's group velocity, the factor 3 in `beta = sqrt 3 p / E'`); (4) the two Doppler factors `k_BA = gamma (1 + beta)` and `k_AB = sqrt((1 + beta) / (1 - beta))`, the step above read at two detectors (exact in the k-calculus within `1 / T`; the law's `1 + v` and `1 / (1 - v)`); with them the energy a click reads of the record's rows, `E_read = h f_read = (1 + z) E_emit` | (A1), (A2) and the Planck map: `E'^2 - E'_0^2 = 3 p . p` is the walk's `omega^2 - kappa^2 = m^2` times `hbar^2` through the unit chain `E^2 = E_0^2 + c^2 p^2` (p per Link), `E' = E / c^2`, the 3 being `1 / c^2 = d` (part (6) (1) (c)); `r = E'_0 / E' = sqrt(1 - beta^2)` exact on the identity's integers, `sqrt(1 - v^2) (1 - kappa^2 / 6)` in the group velocity: up to `m^2 v^2`, the identity's pace within `m^2 / 3` of the clicks' velocity (the group velocity); the law's `r = 1` rung 1 | `E' = E'_0 / r`; `3 p^2 = E'_0^2 beta^2 / (1 - beta^2)`, p the whole root within 1 | series S: the 64th self-creation at 70 and 124 (GAMEBOARD, the `become` lines; gamma 1.1074 and 1.9558; the design's `70.9 +- 1` and `125.2 +- 1`, the derived 70 and 124, 17.6 M2); r itself NOT READ as a measurement (section 4); J4's ratio 1 under the law pinned, not run |
| the pace `abs(p_a) / (Q S M + abs(p_a))` per axis (P9, 4.4) and the drive's schedule `by_drive(drive, p, D, at_most = 1)` (`step_axis`); under the identity `p / E'` Links per interval (17.6 M1) | the velocity `v`: Nodes apart over counts apart between two clicks of neighbouring detectors (section 1); `beta = sqrt 3 p / E'` in units of c | (A1): one Node per interval at most, the count's ratio the pace within `1 / T` of the count and `1 / T_D` of the pace; rung 1; the identity's `p / E'` is the walk's group velocity only up to the relative `m^2 / 3` | law: `p = E'_0 v / (1 - v)` exact; identity: as above | series S: beta 0.3040 at the star's declared momentum under the identity's pace, 0.2674 under the law's (GAMEBOARD, the drive's pace; the detector reads only `1 + z` below); D3's controls at their pace to the tick (DETECTOR, `x = 60 + r` on every click) |
| the phase per age, the row's declared pair `[n_phi, d_phi]` in steps of the circle N per interval, `omega = 2 pi n_phi / (d_phi N)`; and, separately, the release's identity `E = h_q s` in the lamp's turn s on the K pair (6.4; the click's content `h_q s`), the two equal only by declaration and in no registered light world (content = K, s = 1 in every lamp entry on main); where they coincide `E = h_A f = hbar omega` with `hbar = h_A / (2 pi)`, the momentum `p` with `lambda = h_A / p` (24.1 row 25, 23.2); the rest pair `E_0 = h_q n_0 / d_0` by the same declaration | the frequency a detector counts, `1 + z` (the inverse slope of the birth ordinal against the click's tick, series T's method): `k_BA = (1 + v) / r` for a lamp on the moving record, `k_AB = r / (1 - v)` for a lamp at rest counted by the moving record, the round trip `(1 + v) / (1 - v)` | (A1) and the count: the k-calculus of section 2, rung 1 within `1 / T`; the law `1 + v` and `1 / (1 - v)`, the identity `gamma (1 + beta)` and `sqrt((1 + beta) / (1 - beta))`; the round trip r-free under every r (section 0 (b)) | law: `v = z`; identity: `beta = ((1 + z)^2 - 1) / ((1 + z)^2 + 1)`; r from `k_AB` and `k_BA` together, `k_BA / k_AB = (1 - v^2) / r^2` | NATURE 4b: `z = 0.2636` at beta 0.2674 under the law (DETECTOR, FAIL against nature's 0.315); series S: `z = 0.3674` at beta 0.3040, gamma 1.04967, the pin `0.369 +- 0.003` (DETECTOR, PASS in its domain); `k_AB` NOT READ, the missing direction (section 4) |
| the age wall: the crowd `a_tau` (the sum of amount times age of the rays at the Node, record 394) stretching the self-creation's wall at coefficient 1, `rate x d` against `wall x (d + a_tau n)` (`core.integer.age_wall`; `AGE_WALL_SET`), the rate `1 / (1 + a_tau n / d)` | the clock rate in a crowd read by a pulse and its return (record 768): the ratio of two lamps' `1 + z` at one detector, `(1 + k_2) / (1 + k_1)`, `k = a_tau n / d`; the detector's own `k_D` cancelling in the ratio when the detector's crowd is the same in the two readings (series T); not in series X, whose ratios are host-tick readings | (A1) and the count: the owed intervals are counts the pulses carry; rung 1 within the count's grain | `k = (1 + z) / (1 + z_0) - 1` against a control lamp | series T: 2.6517 at 3 and 4.1500 at 6 Links, the ratio 1.907 against the pin `1.909 +- 0.05` (DETECTOR, the age word; NATURE 12); series X: the controls 1.0000 exactly (DETECTOR) |
| the flight table `T_D = isqrt(3 abs(D)^2 Q^2)` per direction, the pace `N_l abs(D)_2 / T_D` (2.7, 13.2; rem:nodispersion) | the arrival count: the detector's own count at a row's arrival from L Links away (a detector with a body; a face set has no count of its own, record 768, and its tick is GAMEBOARD), `sqrt 3` intervals per Link within `1 / T_D`, and c itself as the one pace every family shares (`c = 1 / sqrt 3` Links per interval, input 9; `32 / 55` on a heading) | (A1): one Node per interval on the Manhattan lattice, the Euclidean pace its shell mean; rung 1 for the count (within one interval), rung 2 for the isotropy | `L` from the count and the pace, within one Link | series S: the products' face clicks at 369 and 345 (DETECTOR; the pins 367 and 345 within two ticks; the decay tick 70 and 124 derived back by the flight table); series K: the bending 0.000 (DETECTOR, the rows blind, under the law without the key; optical-v1's worlds read -1.79 to -4.36 pixels, the register's optical-v1 table) |
| the click's bilinear form `f^T G f`, the one square the law forms, at the click alone over rows that have ended (6.5, 6.7; input 12) | the click's energy and the Born form: the count of clicks over many records at one Node, the probability `abs(sum of amount x exp(i phi))^2` normalised by the record's total, within `1 / (2 N)` (23.2) | (A2) at the click: the square of the summed amplitudes; rung 1 (the click's form) | none: the amount a and the phase f of one record never pass Outside singly | the two-slit fringes and Malus (24.3 row 4; DETECTOR); not a Lorentz line |
| the crowd's spreading over the six Ports: K beams over a shell of `N(r)` Nodes, the presence `q tau_L / (4 pi r^2)` and the age moment `A = q tau_L / (4 pi c r)` in the shell mean (5.1; the paper's `eq:fields`; section 8 (M)) | the clock's field Outside: the ratio of two clocks' shifts at two distances (2.00 for the potential's form), and a shell's flat interior against its rising flux | (A1) and the count, on the age wall's row above; rung 2 (the shell mean, `N(r) -> 4 pi r^2`), the finite-r ripple MEASURED ONLY; the constant `delta k = (n S / d) (g h / c^2)` (section 8 (e)), the Outside image of the two Newton rows' Inside declarations n, S, d, equal to nature's iff `n S = d`, a condition on the declaration and not a meeting point | `r` from the ratio of shifts, in the limit | series T: 1.907 (DETECTOR); series X: inside `k(2) / k(4) = 1.0029` against 1.003917 (flat, MET; the lattice interior's own ripple `+- 2.4` percent by the map, larger than the tolerance 0.02), the presence word 0.8390 (not flat), outside `k(12) / k(4) = 0.6285` against 0.618270 (DETECTOR, host-tick readings; 0.9994 and 0.5134 in the detector's own clock, the convention the owner's) |
| the push `p += -M_A V` from the arriving rays' label flow (`push_form`'s gravity column; 3.3) with the drive above, in the shell mean `<V> -> q N_l / (4 pi r^2)` | the fall: a lamp on the probe read at a line of one-Node detectors, the acceleration as the second difference of the clicks' x, `a = -G M_B / r^2`, `G = K eta / (4 pi N_w)`; the equivalence principle (the same clicks for four times the held mass); the line's one-Node detectors carry no body, so they have no count of their own (record 768): the line's ticks are GAMEBOARD, and the acceleration as the second difference of the clicks' x over them is a GameBoard reading until a body detector counts, while the births' Nodes stay DETECTOR | (A1) and the count: the births' Nodes (DETECTOR) and the line's ticks (GAMEBOARD, no body at the line); the inverse square rung 2, the equivalence rung 1, exact in the gravity column and the drive (`p = M_A sum V` exactly, the step's divisor scaling with `M_A`, the same whole parts and remainders at every momentum) | `G M_B` from `a r^2` in the limit | series D3: 138 of 139 common birth ticks at the same Node with the held mass four times, one Node in one birth, cause not named (the lamp's recoil-cancelling pair is not it), `abs(dT) = 0` (DETECTOR); the inverse square's decisive reading NOT MADE; series C's `1 / r` on the plane GAMEBOARD |
| the circular momentum under the push and the drive, `v^2 / r = G M_B / r^2` (24.1 row 58) | Kepler's period read at the detector line, `T = 2 pi r^(3/2) / sqrt(G M_B)` in space, `T ~ r` on the plane, `T(24) / T(12) = 2` (the `1 / r` force's scale symmetry) | (A1) and the count: the recurrence of the lamp's births at one Node; rung 2 (`v << c`, the shell mean), `main`'s drive's `1 / (1 - v / c)` at first order (form B alike; form B on a branch) | `G M_B` from `T` and `r` | series D3: `T(24) / T(12) = 1.997` in 1.82 to 2.18 (DETECTOR, inside; the loops not similar figures, not decisive); the periods 19 percent above their circles (DETECTOR, outside, the plane's grain) |

Two facts of the table for the owner. First, every Outside formula is a
ratio or a difference of counts at a click, never the tick, so the whole
passage from Inside to Outside is the click theorem's conversion: the
identity's rows are Lorentz's up to corrections of order `m^2 v^2`
because the conversion is, and the law's rows differ from them only
where r enters (`1` against `sqrt(1 - beta^2)`), which is the one place
the register can decide (section 4's missing direction); Newton's rows
need no (A2) and are the shell mean of rules already on `main` (section
8). Second, the inverse map exists on every row but the click's: from
`(v, 1 + z, the arrival count, the shifts, the fall)` a detector
recovers **p**, `E'_0`, `k` and `G M_B` up to the accumulator's
remainder and the shell mean's ripple, but never the amount a and the
phase f of one record; those pass Outside only as the click's square
over many records, which is Born's rule at the click and the reason the
board's Inside is not the Outside's inverse image.

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
and cancels in the ratio ONLY when the detector's crowd is the same in
the two readings (series T: the crowds and the detector fixed, the lamp
moved; series X's controls, no crowd). Where the crowd moves with the
lamp (series X's shell at r = 2, 4 and 12) `k_D` differs by world
(0.0945, 0.0927 and 0.1357 by the map's section E), the register's
ratios are host-tick readings (record 569), and in the detector's own
clock X's ratios are 0.9994 inside and 0.5134 outside; the convention
is the owner's.

(b) *The form of k about a source.* From N1, N4 and M: a row of age
`r / c` dwells `tau_L` intervals per Link (`T_D / (N_l |D|)`, 1.72 on a
heading, `sqrt 3` in the limit of every direction), so the presence at
r is `q tau_L / (4 pi r^2)` and the age moment is the presence times the
age, `A(r) = q tau_L / (4 pi c r)` (DERIVATIONS 5.1; the paper's
`eq:fields`): the clock's word falls as `1 / r`, the retarded potential
of the release, and obeys the wave equation with the release as its
source, Poisson's in the static limit; rung 2, earned as LINEAR in the
rows (the moments are sums over rows), while the source term is the
EFFECTIVE release, the declared rate over `1 +` the source's own count
(series X's fixed point: the shell's sources at 0.536 of the declared
rate), so the equation is nonlinear in the declared rates. Two
consequences that
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
enters: the equivalence principle is rung 1, exact in the gravity
column and the drive (`p = M_A sum V` exactly, `Lambda = 1`; the step's
divisor scales with `M_A`, so the same whole parts and remainders at
every `abs(p)`, not only at `abs(p) << Q S M_A`; 3.3's item 1).

(d) *Kepler's third law.* From (c) and the drive at small p: a circular
orbit has `v^2 / r = G M_B / r^2`, so `T = 2 pi r^(3/2) / sqrt(G M_B)`
in space and `T = 2 pi r / v` with `v` fixed by the momentum on the
plane, `T ~ r` (the `1 / r` force; DERIVATIONS 24.1 row 58, entry 58):
rung 2, `v << c`, the period above the Newtonian by `1 / (1 - v / c)` at
first order under `main`'s drive (form B alike; form B on a branch).
The ratio at two radii is a
theorem of the force's scale symmetry alone: a `1 / r` force is
invariant under `r -> lambda r, t -> lambda t` at the same speed, so
loops started with the same momentum at `r = 12` and `24` are similar
figures with `T(24) / T(12) = 2` for any eccentricity, a property no
other power of r has (the D3 entry); the pin from the map before the
run, `2.00 +- 0.18`.

(e) *The equivalence of the clock's slowing and the fall.* From (b) and
(c): the clock reads the age moment A and the push reads the flow,
which in the static limit is the gradient of the same field: the FLOW is
`V = -(N_l c / tau_L) grad A` (5.1's relation, the paper's "the two
fields of one stream"), and the acceleration is the push over the
drive's divisor, `a = V / (N_l N_w) = -(c / (tau_L N_w)) grad A` (the
first draft of this line wrote the flow's coefficient for the
acceleration, a factor `N_l N_w` off by my count; withdrawn, the
reviewer's correction). With `tau_L = 1 / c` exactly (`tau_L = T_D /
(N_l abs(D))` and `c = N_l abs(D) / T_D`),

    a = -(c^2 / N_w) grad A,

one crowd, two readings, the potential and its gradient, rung 2. The
constant between them: the clock's shift between two heights h apart is
`delta k = (n / d) delta A` and the fall's `g h = (c^2 / N_w) delta A`,
so

    delta k = (n N_w / d) (g h / c^2) = (n S / d) (g h / c^2):

NATURE'S FORM `g h / c^2` times the declared `n S / d`; the constant
equals nature's if and only if `n S = d`, and the registered worlds
(`suspension` `[1, 2^16]`, S = 1) have `n S / d = 2^-16`. So the law has
the form of the equivalence (one field read twice) SHOWN, its constant
a declared input (the suspension pair and the width), NEITHER for its
value, and the condition `n S = d` is named here for the owner. Stated
as a fact, not a failure: the paper's G likewise carries Newton's
constant through `N_w`.

**(3) For each formula: SHOWN, MEASURED ONLY, or NEITHER.** SHOWN: it
comes out algebraically under the assumptions at the rung named.
MEASURED ONLY: no closed form Outside; the register's run rises Outside.
NEITHER: no closed form and no reading. The register's rows by kind.

| The formula Outside | Verdict | The one line that decides | The register (DETECTOR unless labelled) |
| --- | --- | --- | --- |
| the clock's rate `1 / (1 + k)`, `k = a_tau n / d` | SHOWN, rung 1 | N2 is the formula: the owed count's whole part of `a_tau n / d` per self-creation | series T: the age word's `1 + z` 2.6517 at 3 and 4.1500 at 6 Links from equal crowds (NATURE 12); series X: the controls 1.0000 exactly |
| the `1 / r` form of k about a point source (the potential, not the flux) | SHOWN, rung 2 (the shell mean, with the ripple) | age times presence: `(r / c) x 1 / r^2` (N1, N4, M) | series T: the ratio of the two shifts 1.907 against the pin `1.909 +- 0.05`, the continuum's 2.00 outside it by the lattice's grain (PASS on the form; the presence word 1.000, FAIL); series X outside: `k(12) / k(4) = 0.6285` against the pin 0.618270 (MET; a host-tick reading, 0.5134 in the detector's own clock, the convention the owner's), the continuum's 0.5 outside the tolerance by the grain |
| the shell theorem's flat interior (Poisson's source term) | SHOWN, rung 2 with the ripple (the lattice interior's own ripple `+- 2.4` percent by the map, r = 0 to 5, 5009 to 5246, larger than X's tolerance 0.02 and not read at two Nodes) | the `1 / r` weights of a shell sum to a constant inside, the `1 / r^2` weights do not (M on every source); the source term the effective release (the fixed point, 0.536 of the declared rate) | series X inside: the age word `k(2) / k(4) = 1.0029` against the pin `1.003917 +- 0.02` (MET, flat within the tolerance); the presence word 0.8390 against the pin 0.839989 (MET, not flat: the FAIL the design expected) |
| the ripple of the shell mean at finite r (the departure from `1 / r` and `1 / r^2`) | MEASURED ONLY | `N(r)` is the lattice's count of Nodes on a shell, no closed form at finite r (Gauss's circle problem, an exponent bound and no formula) | series X's 0.6285 against the continuum's 0.5 and T's 1.907 against 2.00, the grain read; series E's shell means (GAMEBOARD, the probes: `k_a r = 36.1` within `+- 15` percent) |
| the inverse square of the fall, `a = -G M_B / r^2` | SHOWN, rung 2; its decisive reading Outside NOT MADE | the push `-M_A <V>` with `<V> -> q N_l / (4 pi r^2)` (N3, M); on the plane `1 / r` | series D3 on the plane: the ratio `T(24) / T(12) = 1.997` (1.82 to 2.18) inside its bracket, consistent with `1 / r` and not decisive (the loops read are not similar figures: the radii 1.4 to 73.2 about 24.2 against 11.0 to 62.3 about 33.7, one recurrence each); the deciding reading (similar loops at a finer grain) not run; series C's `1 / r` on the plane and the exponent `r^-1.83` on the 2616-direction shell: GAMEBOARD, the probes' momenta (records 562, 564) |
| the equivalence principle (the fall independent of `M_A`) | SHOWN, rung 1, exact in the gravity column and the drive | `p = M_A sum V` exactly (`Lambda = 1`) and the step's divisor scales with `M_A`: the same whole parts and remainders at every `abs(p)` (N3) | series D3: the held mass four times at `r = 24`, 138 of 139 common birth ticks at the same Node, one Node in one birth, cause not named (the lamp's two rows per birth cancel its recoil, `orbit_lamp/README.md`, so that is not it), `|dT| = 0`, the same escape tick; 3.3's `push_m = m x push_1` for m = 1, 4, 16 (GAMEBOARD) |
| Kepler's third law, `T^2 ~ r^3` in space, `T ~ r` on the plane | SHOWN, rung 2 (`v << c`); the exponent in space NOT READ | the circular orbit under (c) and the drive; the ratio 2 at two radii the `1 / r` force's scale symmetry (entry 58) | series D3: 1.997 for `2.00 +- 0.18` (inside); the periods 19 percent above their circles alike (outside: the loops are not circles, the plane's grain), read as history; entry 58's host check in space `T(24) / T(12) = 2.8284 = 2^(3 / 2)` at S = 512 (GAMEBOARD, not after a detector) |
| the equivalence of the clock's slowing and the fall (one field, the potential and its gradient) | SHOWN in form, rung 2; the constant a declared input; NEITHER for its value | `a = -(c^2 / N_w) grad A` in the static shell mean (`tau_L = 1 / c`); `delta k = (n S / d) (g h / c^2)`, nature's form times the declared `n S / d`, equal to nature's iff `n S = d` (the registered worlds `2^-16`) | series T and X read the potential's side, D3 the gradient's, on different worlds; no world reads both on one crowd: the one reading that would close the constant is NOT MADE |
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
reads them: the potential's form (T, 1.907; X outside, 0.6285, a host-tick reading), the flat
interior (X, 1.0029), the equivalence (D3, 138 of 139), the scale
symmetry's ratio (D3, 1.997). MEASURED ONLY: the lattice's departure
from the continuum at finite r (X's 0.6285 against 0.5, T's 1.907
against 2.00, D3's periods 19 percent above their circles), which no
closed form gives and the runs rise Outside. NEITHER: the inverse
square's decisive reading after a detector (D3 consistent, not
decisive, the similar loops not run), the VALUE of the equivalence's
constant (its form SHOWN, `(n S / d) (g h / c^2)`, nature's iff `n S =
d`) and the value of G, and the post-Newtonian terms, which the law does
not have. The one line: Newton's formulas are the shell mean of five rules
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
equivalence principle is exact on the GameBoard in the gravity column
and the drive, the push `M_A` times the flow exactly and the step's
divisor scaling with `M_A`, the same whole parts and remainders at every
momentum, and it is measured after a detector (series D3, 138 of 139
births at the same Node with the held mass four times, the one Node in
one birth unexplained). (iii) What the model does not have it states: no term of the
post-Newtonian order enters the push, the clock in a strong crowd reads
`1 - k + k^2` and never stops, and the value of G is a world's inputs
and is not read.

## 9. Part (8): the conversion as a map, in the algebra's own words (the owner's question, by voice, 2026-09-22, as the Boss relayed it)

**The owner's question.** "In modern algebra, is there not already a
notion of a transformation from one place to another, which is what we
do: one place is Inside, and Outside is the transformation to the
other place; is it not already defined how all these passages are
done?" This part names, in the algebra's words, what the conversion
Inside -> Outside is: the two structures, the map, what it preserves,
which theorem it satisfies, and which of the algebra's names it earns
exactly, which only in a limit, and which it does not earn. No name
that the objects do not earn.

**Certification of the inputs.** The six verbs (HIGHLIGHTS, "The six
operations"; record 202); the paper's objects (a record's rows at one
Node and label as an element of the group ring `Z[Z_N]`, the pointer
`ev`, the cancel as the quotient by `x^(N/2) + 1`), its lattice Gleason
(`th:gleason`), its isometry (`th:isometry`), its rung (`eq:rung`), its
bijection (`th:bijection`); section 0's click theorem with M3 (the
counts' ratios over Q) and the dilation; the conversion table of section
7 (3). Nothing else enters.

**(0) The three formulas, in one direction (the owner's clauses, as the
Boss relayed them).** "W = E'^2 + 3 p . p is the formula of ONE STEP
beneath the board. One needs the formula of one step ABOVE the board
(which Einstein and Newton already wrote), the formula of one step
beneath the board, and the conversion between them. That is all the
formulas we need; then one can compute anything, without code." And:
"there is no meeting of the step beneath and the step above; the basis
is Inside and everything is derived from Inside." And: "the step
beneath, being what it is, leads to the step above being what it is,
which is Einstein, the most general; and from there we show what the
smallest thing is; then, from the small step, Newton follows; Einstein
follows and Lorentz follows, not 'derived', they follow, without our
putting them into the formulas; we only used the Inside; and formulas
follow that physics cannot get: why the world above is quantized." So
the opening reads in one direction: the Inside step is the axiom, the
conversion is the map, and the Outside step is a theorem, the image of
the Inside step under the conversion, with its quantum a theorem too;
the word throughout is "follows", never "derived" where a form was put
in (the writer's audit).

*(I) THE INSIDE STEP, the axiom: one interval of a record, in closed
form on its state vector, by the six verbs.* A record's state at a Node
is the vector `(x, D, p, tau, f, acc_drive, acc_push, acc_owed)`: its
Node, its direction, its momentum (a body) or phase turn (a row), its
age, its rows' element `f` of the group ring `Z[Z_N]` (the amount at
each phase), and its accumulators. One interval applies, in order, verb
1 (the translation of every accumulator by its rate), verb 6 (the
division with the remainder kept, whose whole part is the event), verb
2 (the bilinear form with the declared matrix, at the push and at the
click), verbs 3 and 5 (the addition in `Z[Z_N]` and the evaluation at
`zeta_N`, where rows are summed at one Node and where they end), and
verb 4 (the permutation, at a collision, none in these worlds):

    hop:    acc_drive <- acc_drive + rate;   e <- sign(acc_drive) min(floor(abs(acc_drive) / wall), 1);   acc_drive <- acc_drive - e wall;   x <- x + e D_hat
            a row:  rate = 2 S_1 N_l, wall = 2 T_D, the accumulator started at T_D (the half-wall start), so the Links by the age are m(tau) = floor((2 tau S_1 N_l + T_D) / (2 T_D)), S_1 = abs(D)_1   (the flight table, P9, walk_step; c = N_l abs(D)_2 / T_D);   a body:  rate = abs(p_a), wall = N_l N_w M + abs(p_a) per axis  (the pace, P9)
    phase:  f <- x^(phi(tau)) f,   phi(tau) = floor((tau + 1) n / d) - floor(tau n / d)   (the turn per interval of age, the row's declared pair [n_phi, d_phi]; the release's identity is E = h_q s in the lamp's turn s on the K pair, 6.4, the click's content h_q s; the two equal only by declaration, in no registered light world: content = K, s = 1 in every lamp entry on main)
    push:   acc_push <- acc_push + M_A V_c;   p <- p + sign(acc_push) floor(abs(acc_push) / Lambda_c^2) (the gravity column: Lambda = 1, p <- p - M_A V exactly)
    crowd:  (rate, wall) of the owed count <- (rate d, wall (d + a_tau n)),   a_tau = sum over the rays present of amount x age   (the age wall, coefficient 1)
    split (A2, at a splitter or a setting):   f -> (a_i x^(t_i) f) on the output d_i,   A = sum a_i^2;   a setting: the label pair by U_s
    sum (rows at one Node):   f <- f + g in Z[Z_N], x^(N / 2) = -1 (the cancel)
    click (a record whose rows have all ended):   R_k = abs(ev f_k)^2 per cell,   rung_k = floor((2 W C_k + C_K) / (2 C_K)) with W the wheel's modulus (N under the wheel [1, N]; L2b's wheel is [2531, 4096]),   the cell with rung_(k - 1) <= u < rung_k;   the record deleted
    age:    tau <- tau + 1

Every line is one of the six verbs on bounded integers, and `W = E'_0^2
+ 3` **p** `.` **p** is not a line of the step: it is the step's
INVARIANT under the identity (kept on the record, `E'` by comparisons,
17.6 M3), the quantity the hop's schedule and the owed count conserve
between pushes, as `omega^2 - kappa^2 = m^2` is the walk's invariant and
not its update. Nothing else is assumed of the board.

*(II) THE OUTSIDE STEP, a theorem: what follows above the board from
(I) under the conversion, Einstein's as the most general.* Under the
conversion of (A1) and (A2) (the map named in (2) below), the Inside
step's invariant and schedule come out Outside as Einstein's rows, and
they FOLLOW; nothing of them was put into (I). One sentence for the
paper's writer to mirror: `W = E'_0^2 + 3` **p** `.` **p** is the
conversion's identity, shown to second order from the six verbs with
(A1) and (A2) (section 7); on the law as built the rows hop whole and
lack (A2) (part (5)), so for the rows' dynamics W remains a declared
identity (record 270), and the paper says which of the two it means at
each use. The rows that follow: `E^2 = E_0^2 + p^2 c^2`
(W times `c^4` in the whole unit, exact on the identity's integers, the
3 entering as `1 / c^2` when p is counted per Link; part (6)); `v = p
c^2 / E` (the drive's fraction as the click's velocity, within `m^2 /
3` of the walk's group velocity); `d tau = sqrt(1 - v^2 / c^2) dt` (the
gate `E'_0 / E'` as `1 / gamma`, the detector's own rate, exact on the
identity's integers; the law's own rows at `r = 1`, part (5)); the
Doppler `nu' / nu = sqrt((1 + beta) / (1 - beta))` (the step above read
at two detectors, the two k-calculus factors, exact within `1 / T`
given the one line `k_AB = k_BA`, section 2); and Lorentz itself, the
group of the click families, from (A1) and that one line (section 0,
up to corrections of relative order `m^2 beta^2` through the walk, exact
in the continuum limit). Every symbol of these formulas is a count at a
click or a ratio of counts (a time a detector's own count, a length
Nodes apart, an energy `h` times a counted frequency, a mass a rest
count), by the closing fact of section 7's table; the general theory's
weak-field rows (the clock at the potential, the geodesic of `g_00 = 1
+ 2 Phi / c^2`) follow at rung 2 as the limit of (IV).

*(III) THE QUANTIZATION OF THE OUTSIDE, a theorem from (A1) and the
conversion alone, no run (the owner's clause: "what is the minimal
distance between a click and a click? the step above as a formula";
"of course I want to show that the Outside is quantized").*

*Theorem.* Under (A1) and the conversion, the Outside has least units,
and they follow from the Inside step's one interval and one Node: (i)
the least separation of two places read is one Link; (ii) the least
time a detector times by itself is a pulse to its neighbour and its
return; (iii) the least step of a moving record is one Node per k
counts, so the Outside velocities are the ratios `1 / k` (M3, over Q)
with the velocity quantum `1 / (k (k + 1))`, and c Outside is one Link
per the least count.

*Proof.* (i) A click moves information one Node at most (A1), so two
places that a chain of clicks tells apart are at least one Link apart;
the law makes a detector's cell one Node (the one-Node `wave` detectors
of series D3, the Bell worlds' counters) or a declared set of Nodes (a
face set), whose clicks are read at the set, so for a set the least
place is the set's own extent. (ii) Two arrivals at one detector can be
one own count apart (series X's controls read `1 + z = 1.0000` exactly,
consecutive births arriving one count apart, DETECTOR), so the least
separation of two clicks at one detector is one count; but a detector
times nothing by its tick, which is GAMEBOARD and never read (section
1); what it times is a pulse and its return (record 768, the owner's
definition of the clock), and the least such is one round trip to its
neighbour: two intervals in the hop frame (one Node each way at c = 1),
and on the Beam Law's lattice exactly two intervals on every line as
well, since a fresh row's first Link falls at its first interval by the
half-wall start (`m(1) = floor((2 S_1 N_l + T_D) / (2 T_D)) = 1` on the
heading, the face diagonal and the body diagonal at Q = 64, checked
here); a single row's consecutive Links are spaced `T_D / (S_1 N_l)` in
the mean, 1.72 on a heading (its Links at the intervals 1, 3, 5, 7, 8,
10), 1.22 on a face diagonal, 1 on the body diagonal, so an earlier "2
to 4 intervals" described one row's Links and not the pulse's return. (iii) A moving record hops one Node at most per
interval (A1, the hop line of (I) with its cap 1), and between two hops
its detector counts k intervals stretched by the crowd, so a velocity
read by clicks is `1 / k` Nodes per count, a ratio of two integers (M3,
in the mean over a hop pattern), never a real number; two neighbouring
velocities differ by `1 / k - 1 / (k + 1) = 1 / (k (k + 1))`, finest near
c and coarsest near rest; and c Outside is one Link per the least
count, the pace of a row (`1 / sqrt 3` Links per interval, `32 / 55` on a
heading), the same in every family by (A1). QED. *The Outside step
formula in these quanta:* for the next click of the same record (a
transponding record re-emitting at each arrival, section 2 (c)),

    place_(j + 1) - place_j = e_j D_hat,   e_j in {0, 1},   count_(j + 1) - count_j = 1 + owed_j   (in the detector's own count),

the image under the conversion of the Inside step's one interval and
one Node (`e_j` the hop's whole part, capped at 1; `owed_j` the age
wall's whole part, the crowd's stretch); read at a distance, the count
between two clicks of the record is multiplied by the k-calculus
factors `k_BA = (1 + v) / r` and `k_AB = r / (1 - v)` (section 2), with r
the record's own count per tick, the one quantity of the step above
that (A1) leaves free: `r = 1` on the law (the whole-record hop),
`sqrt(1 - v^2)` up to `m^2 v^2` under (A2) (section 0 (ii)). *What is
exact and what needs (A2):* the place quantum, the count's quantum, the
velocities' ratios and c are theorems of (A1) and the conversion, exact
(rung 1); the rate r inside the count is the one thing that needs (A2)
or a declaration. *The honest sentence:* the continuum's formulas
(Newton's, Einstein's) cannot say why the world above is quantized,
because in them a place, a time and a velocity are real numbers; this
law says it, and says what the quanta are, because the Outside is made
of counts at clicks and nothing else, so its least units are the
Inside step's one Node and one interval read through the conversion.
*The register, by kind:* the count's quantum is READ by series X's
controls (`1 + z = 1.0000`, one count per birth, DETECTOR) and by series
T (2.6517 and 4.1500 counts per birth at 3 and 6 Links, the crowd's
stretch of the count's quantum, DETECTOR); the place quantum is READ by
series D3 (the one-Node detectors' `x` of each birth, 138 of 139 at the
same Node, DETECTOR); series S's face clicks at 369 and 345 are single
arrival ticks at a face set (DETECTOR), not a spacing; the muon's 70 and
124 are the gate's own count at the 64th self-creation (GAMEBOARD, the
`become` lines), not a click spacing; series W's first-click ages (815,
876, 876; record 754) are the row's own age on its record read at the
click, DETECTOR ("the row's age on its first click, 815, 876, 876
exactly", the ticks 955, 1016, 1016 GAMEBOARD), a first-arrival age and
not a least spacing;
the least spacing of two clicks of one MOVING record at one detector
(the count between a transponding record's re-emissions) is NOT READ,
section 4's missing world.

*(IV) NEWTON, the limit.* From the small step, Newton follows as the
shell mean of (I)'s push, crowd and flight lines under the conversion
(section 8): the clock's rate `1 / (1 + k)` and the equivalence
principle exact, the `1 / r` potential, the `1 / r^2` fall, the shell's
flat interior and Kepler's period at rung 2, and the constant `delta k =
(n S / d) (g h / c^2)` the Outside image of the Inside declarations n,
S, d, "equal to nature's" a condition on the declaration (`n S = d`)
and not a meeting point, since there is no meeting of the step beneath
and the step above: the basis is Inside and everything Outside follows
from it.

*THE CONVERSION*, the map of this part, named in (2) below: four steps
(a ring homomorphism, a pure state's square, a threshold, a count
ratio) with the group of section 0 acting on the result. What this
part shows is that (II), (III) and (IV) are the image of (I) under it
to the stated order, so that, as the owner says, one computes without
code: an Outside number is the conversion applied to the Inside step,
an identity checked against a reading and not a run's output; the run's
place is the register, where the identity is tested and the finite-N
and finite-r departures, which have no closed form, rise Outside.

**(1) The two structures.**

*Inside* (I): the GameBoard's state, at every Node a bounded integer
vector (the Scalars and Vectors of NodeState) advanced by one map of six
verbs per interval: the translation of an accumulator by its rate, the
bilinear form with a declared matrix, the addition in the group ring of
the phase circle, the permutation, the evaluation at the primitive N-th
root of unity, and the Euclidean division with the remainder kept. Where
(A2) holds (the amplitude key), a record's rows at one Node and label are
one element `f = sum_p f_p x^p` of `Z[Z_N]`, `x` one phase step, `f_p` the
amount at the phase p; the merge's cancel identifies `x^(N/2)` with -1,
so the rows after the cancel live in `Z[x] / (x^(N/2) + 1)`, which for N
a power of two (every registered N) is the ring of cyclotomic integers
`Z[zeta_N]`, a free Z-module of rank `N / 2`. A pair's record carries its
labels on two arms with integer weights, an element of `Z[Z_N] (x) Z^2
(x) Z^2` (the tensor product over Z), and a setting s acts on an arm's
label pair by the integer matrix `U_s` (rule R), `U_s^T U_s = n_s I`
exactly. Inside also holds what no click reads: the tick, the record's
ordering (the arms' declared order, the layer), the accumulators'
remainders, and the phase's origin.

*Outside* (O): the clicks. A click is a triple (the set, the detector's
own count `n_D` at the arrival, the cell and label that landed), and for
a pair one row carrying both outcomes at the completion interval; the
counts of one detector add, so a click family `F_D` (section 0) is a
free abelian monoid of counts whose ratios lie in Q, and the velocity,
the Doppler factors and the rates are elements of Q (M3). On the click
families the group G of section 0 acts: the cone-preserving Q-linear
maps of the count pairs, the boosts with rational k, dense in SO(1, 1),
the Lorentz group up to scale their closure. Locality Outside (section
0): every passage in O is a chain of clicks between neighbouring places,
so O inherits I's locality through the map, a theorem of A1 and the
definition of O, with the pair's gather (P6) the one exception; the
bound is one Node per interval of the tick, `1 / r_D` Nodes per the
detector's own count.

**(2) The map, step by step, with its name at each step.** The
conversion `Phi: I -> O` is a composite of four maps, and the algebra
has a name for each; the composite has no single name, which is the
answer's first part.

(a) *The pointer, `ev: Z[Z_N] -> Z[zeta_N]`, `ev(f) = sum_p f_p zeta^p`
(verb 5): a surjective RING HOMOMORPHISM, exactly.* Its kernel is the
ideal generated by `x^(N/2) + 1`, which is the merge's cancel (verb 3): an
antiphase pair cancels on the GameBoard exactly when its pointer is 0.
So the first isomorphism theorem holds here EXACTLY and says: the rows
modulo the cancel ARE the cyclotomic integers, `Z[Z_N] / ker(ev) =
Z[zeta_N]` (the paper's "the GameBoard's cancel and the click's zero are
one relation"), FOR ev AT THE EXACT ROOT; on the tables within their
rounding: the engine's evaluation is the rounded tables C, S at the
scale 256 (`core/phase.py`, built by reduce-and-flip so that `C[p + N /
2] = -C[p]` and `S[p + N / 2] = -S[p]` exactly), a Z-linear map into
`Z^2` that is NOT a ring homomorphism (6.7; at N = 64 `E(e_1)^2 = (64400,
12750)` against `256 E(e_2) = (64256, 12800)`), whose kernel contains the
cancel (by that symmetry) and is larger than it (rank `N - 2` against
the ideal's `N / 2`): an element that cancels nowhere can read a zero
pointer within the rounding, so "one relation, exactly" is the paper's
ev, and on the engine it holds within the tables' rounding. This is the
one place the word "kernel" is earned in the algebraic sense; ev is also a *-homomorphism for the involution
`f*(x) = f(x^(-1))` (the reflection of the phase), carrying `f* f`, the
record's autocorrelation in the group ring, to `abs(ev f)^2`.

(b) *The weight, `R: Z[zeta_N] -> Z_(>= 0)`, `R(f) = abs(ev f)^2` (verb 2,
the click's `f^T G f`): a POSITIVE QUADRATIC FORM on the lattice, and
equivalently a PURE STATE of the group algebra, exactly.* R is not a
homomorphism: it carries products of scalars (`R(a f) = a^2 R(f)`) and
not sums (the parallelogram law, `th:gleason`'s hypothesis (b)). Its
name in the *-algebra's words: the group algebra `C[Z_N]` is a
commutative *-algebra, its characters are the N evaluations `chi_j(f) =
sum_p f_p zeta^(j p)`, and Born's weight is `R(f) = chi_1(f* f)`: the
positive linear functional `omega = chi_1` applied to `f* f`, a pure
state of the commutative algebra. The lattice Gleason theorem
(`th:gleason`) is then the statement that the states the hypotheses
admit are the positive combinations `sum c_j chi_j` of the odd
characters (the Galois conjugates of ev), `R(f) = sum c_j abs(sigma_j
f)^2`, and Born's `c_1 = 1` is the choice of ONE pure state, the one
imported constant (P10). The GNS construction of a character on a
commutative algebra is one-dimensional: `H_omega = C[Z_N] / ker(chi_1) =
C`, and the GNS vector of f is `chi_1(f) = ev(f)`, so the pointer IS the
GNS vector and the click's square its norm: the name fits exactly for
the paper's object, `chi_1` at the exact root, with two honest remarks.
First, the engine realizes it within the tables' rounding: its `f^T G
f` with `G = E^T E` over the rounded entries (`core/phase.py`, "of rank
2, not circulant (the tables' rounding)"; `amplitude.gram_form`) has
`E_rounded = 256 ev + delta` with `abs(delta_p) <= 1 / 2` per entry, so
the relative error of R is at most `sum abs(f_p) / (256 abs(ev f))`, one
part in 256 on a single row and larger where the element nearly
cancels (unbounded at the false zeros); the rotation invariance `R(x f)
= R(f)` likewise holds up to the tables' rounding (6.5's hypothesis
(a)); and Born's frequency is within `1 / N` by the rung on top. Second,
the algebra is abelian, so nothing noncommutative is measured at one
arm. Noncommutativity enters at a
pair with settings, where the label rotations `U_a` and `U_b` generate
`M_2(Z) (x) M_2(Z)` and the CHSH operator lives (part (9)). What R does
not read: the phase's origin (`R(x f) = R(f)`, hypothesis (a)) and its
orientation (`R(f*) = R(f)`), the dihedral symmetry of the circle; these
are R's invariances, not a kernel, since R is quadratic.

(c) *The rung, `eq:rung`: a THRESHOLD, the one non-linear read-out, and
in the probability's words a STOCHASTIC MAP (a Markov kernel) from the
record's weights to its cells, exact within the wheel's grain `1 / N`.*
The cells' weights `R_k` are laid on a ladder, `rung_k = floor((2 N C_k +
C_K) / (2 C_K))`, and the birth's u (the wheel, uniform over N births)
selects the cell: over the N births the cell k is clicked exactly
`rung_k - rung_(k - 1)` times, which is `N R_k / C_K` within one, so the
click's law is `P(k) = R_k / C_K` within `1 / N`, Born's rule as a
frequency, exact in the integers of the rung (6.2: within `1 / (2 N)` on
the cumulative). The wheel `u = ordinal mod N` is a deterministic sweep
(6.2), so "stochastic map" names the frequency law over one wheel, not
a random draw. This step deletes the
record (P6): it is not a morphism of Inside, and it is the reason the
composite is not a homomorphism.

(d) *The schedule's side, on the hop: the count map, `(Nodes apart,
counts apart) -> Q`, exactly.* Under (A1) a record hops at most one Node
per interval by `by_drive` with `at_most` 1, and a detector reads Nodes
apart over counts apart: a ratio of two integers, a REPRESENTATION of
the counts' monoid in Q by ratios in the mean (M3). On this side the
group G acts: the cone-preserving Q-linear maps of the count pairs, an
ACTION of the Lorentz group up to scale (dense in SO(1, 1) over Q) on
the click families, exactly (section 0 (i)); on the amplitudes of (a)
the same group acts as the Dirac walk's covariance only up to
corrections of order `m^2 v^2` (section 0 (ii)): a representation in the
limit, not on the lattice.

**(3) Which names fit, exactly, in a limit, or not at all.**

| The name | Fits | Where, and what it says |
| --- | --- | --- |
| a ring homomorphism with a kernel; the first isomorphism theorem | EXACTLY, for `ev` at the exact root; on the tables within their rounding (the engine's E is Z-linear, not a homomorphism, its kernel larger than the cancel) | `Z[Z_N] / (cancel) = Z[zeta_N]`; the cancel is the kernel; the pointer the quotient |
| a positive quadratic form on a lattice | EXACTLY, for the click's weight at the exact root; on the tables within their rounding (`G = E^T E` of rank 2, not circulant) | `th:gleason`: forced in form, free in its Galois constants; `c_1 = 1` Born |
| a state on a *-algebra, the GNS construction | EXACTLY, for Born at one arm at the exact root, the engine within one part in 256 per row (larger near a cancel); the algebra abelian | `R(f) = chi_1(f* f)`, `chi_1` a pure state of `C[Z_N]`; the GNS space C, the pointer the GNS vector; Gleason = the admissible states are the positive combinations of the odd characters |
| a stochastic map (a Markov kernel), a measurement | EXACTLY within `1 / N` (`1 / (2 N)` on the cumulative, 6.2), as a frequency law over one deterministic wheel, not a random draw | the rung with the sweeping wheel: `P(k) = R_k / C_K` within the grain; the one deletion |
| a group action, a representation of the Lorentz group up to scale | EXACTLY over Q on the click families; IN THE LIMIT on the amplitudes | section 0 (i) and (ii); the 48 of the lattice contain no boost, so the action is on Outside and not on Inside |
| "Outside is Inside modulo a kernel" for the WHOLE conversion | DOES NOT FIT | the composite is quadratic then thresholded, not a homomorphism; what no click reads (the tick, the ordering, the remainders, the integers beyond their ratios, the scale r of the dilation, the phase's origin) is a set of invariances and unread coordinates, not an ideal |
| a functor between two categories | DOES NOT FIT | Inside's morphisms are the verbs (bijective but the click) and Outside's are the boosts; the click is not a morphism of Inside and no boost is a morphism of Inside (the 48); one honest category exists on the Outside side alone (finite sets and stochastic maps, where the rung lives) |

**(4) What the map preserves, and which theorem it satisfies.** Under
`ev`: sums and products of the rows (a ring homomorphism), the cancel
exactly. Under R: the total at every declared split (`th:isometry`, `A =
sum a_i^2`) and at every rotation up to the tables' rounding
(`n_s / 65536`), the phase rotation and the reflection; the marginals of
a pair exactly `1 / 2` unless a tie of the rung (`2 N R(+, +) / C_K` an
odd integer), then `N / 2 + 1`, with no tie at N = 8 to 1024 nor at the
CHSH labels up to 4096 (`th:marginals`, no-signalling; the register's
`32 / 64` in all 4096 setting pairs, record 105, a computation, and
`2048 / 4096` on the run world), which is the theorem the composite
satisfies at a pair. Under the rung: the
frequencies within `1 / N`. Under the count map: the ratios in Q, the
round trip `(1 + v) / (1 - v)` under every r, the one-way factors up to
the dilation r that Outside does not fix (section 0 (b)): the scale is
what the map forgets, and it is the whole of the Lorentz question
(sections 2 to 5). What the map does NOT preserve, by construction: the
tick (never read), the record after its click (deleted), and the phase's
absolute value (only differences reach R).

**(5) The theorem: why the measured quantities obey the algebra (the
owner's clause, as the Boss relayed it: "one only needs to show WHY
physics behaves like modern algebra, otherwise one is just showing
formulas in modern algebra").** Stated and proved in the algebra's
words from the law's objects alone; what is assumed of the world and
what is the law's construction are separated at the end.

*Theorem.* Let a world be run under the law with a detector family
`F_D` (section 0). Then (i) every Outside quantity is a rational number
computed from clicks by addition, subtraction and division of counts;
(ii) every Inside quantity is an integer computed from the world file
by the six verbs, so every relation among Inside quantities is an
identity of Z; (iii) the map from (ii) to (i) is the composite of (2),
whose first factor is a ring homomorphism at the exact root (on the
engine within the tables' rounding) and whose last is a ratio of
counts, so every identity of (ii) that survives the kernel of (2) (the
cancel) and the invariances of R (the phase's origin and orientation)
is carried to an identity of Q among the quantities of (i), exact up
to three grains: the rung's `1 / N`, the accumulators' remainders `1 /
T`, and the tables' rounding at the scale 256 (one part in 256 per row
and larger near a cancel, the engine's evaluation Z-linear and not a
homomorphism, section 9 (2) (a) and (b));
(iv) the maps between two detector families that preserve the
conversion form the Lorentz group up to scale (section 0), so the
identities of (iii) are the same in every family up to that group; and
(v) the click's statistics are fixed by the state `chi_1` of the group
algebra, whose tables are computed from N at the declared scale (the
circle's tables C, S at `1 / 256`, input 13; HIGHLIGHTS 5.4's row "a
probability is the Gram weight, the click's frequency over records as
the wheel sweeps"), so the frequencies Outside are the values of one
positive functional on Inside's algebra, and not a distribution added
to the law. Hence every result of the paper is an identity of the
algebra (a relation among the values of (i) forced by (ii) through
(iii), invariant under (iv), with its probabilities from (v)), checked
against a reading, and never a formula fitted to readings.

*Proof.* (i) is (A1) with the definition of a click: a click is a
triple (the set, `n_D`, the cell), `n_D` an integer count that advances
by one per interval and is stretched by the age wall's integer count;
a velocity is Nodes apart over counts apart, a rate a ratio of two
counts, a Doppler factor a ratio of counts over T, a probability a
count of clicks over the record's total, an energy `h_q s`, the lamp's
turn s counted at the click (the row's phase per age a separate
declaration, 6.4); no Outside quantity is anything else (the closing fact
of section 7's table), and Q is closed under these operations. (ii) is
P1 to P4 with the six verbs: the state is bounded integers, the update
is the six operations on them, and the world file supplies integers;
so any equation among Inside quantities (the invariant W, the walls,
the age moment, the flow's shell mean at a fixed lattice) is a
polynomial identity in Z, or a limit of such identities as the lattice
grows (rung 2), never a fitted relation. (iii): `ev` is a ring
homomorphism at the exact root, on the engine within the tables'
rounding (section 9 (2) (a)), so an identity `P(f, g, ...) = 0` in
`Z[Z_N]` holds in `Z[zeta_N]` after ev, and an identity in `Z[zeta_N]`
that is invariant under `f -> x f` and `f -> f*` holds for R = `abs(ev
f)^2` (section 9 (2) (b)); the rung carries R's ratios to counts within
`1 / N` (section 9 (2) (c)); the schedule's side carries the drive's
integers to Nodes apart over counts apart within `1 / T` (section 9 (2)
(d)). Composing, an identity Inside becomes an identity among Outside's
rationals up to the three grains (the rung's, the accumulators', the
tables'), which is the only sense in which
"exact" is ever claimed here (rung 1). (iv) is section 0's theorem (i)
with M3. (v): by `th:gleason`, the hypotheses on the reading (the phase
rotation, the balanced splitter's conservation, non-negativity, the
empty reads zero, some input reads) force `R(f) = sum c_j abs(sigma_j
f)^2`; with P10 (`c_1 = 1`) the reading is `chi_1(f* f)`, a state of
the group algebra computed from N alone through the tables; so the
click's frequencies over the wheel are `chi_1(f_k* f_k) / sum_k
chi_1(f_k* f_k)` within `1 / N`, a functional of the state, and no
probability law is imported beyond the choice of the pure state. The
conclusion follows: every Outside relation the paper states is (iii)
applied to an identity of (ii), is invariant under (iv), and takes its
probabilities from (v); the register's readings test it and cannot
alter it, and where the lattice's finite N or finite r leaves no
closed form, the reading is a reading and is labelled so (MEASURED
ONLY). QED.

*What is assumed of the world, and what is the law's construction.*
Assumed of the world: (A1), that a click is the passage of information
from Node to Node at most one Node per interval, c the unit in every
family; (A2), that a click's content is an amplitude with a phase that
splits each interval between staying and hopping (held by the rows
under the amplitude key, not by the law's whole-record hop, part (5));
and P10, that the reading is the pure state `c_1 = 1` (which harmonic
is a relabelling; the constants beyond it not derived). The law's
construction, needing no assumption about the world: the six verbs on
bounded integers (P1 to P4), the click as the one read-out (P6), the
tables computed from N (P7), the age wall at coefficient 1, the flight
table and the pace (P9, chosen among few), the rung with the wheel.
So the reason physics Outside behaves like modern algebra is not that
the algebra was put in: the algebra is what counts at clicks can do (Q
under ratios, a group acting on click families), what integers under
six verbs can do (identities of Z and of the group ring), and what the
one square at the click can do (a state of a *-algebra), and the paper's
formulas are the identities these three structures share.

**The statement (record 777), in the map's own words.** Every Inside
formula is made of the six verbs on the record's integers; every Outside
formula is an Inside one carried by this map and nothing else: on the
amplitude, `Outside = rung o (chi_1 of f* f) o ev` on the record's
group-ring element (a homomorphism, then a pure state's square, then a
threshold); on the schedule, `Outside = (Nodes apart) / (counts apart)`
in Q, on which the Lorentz group up to scale acts; both sides are read at
the detector's own count, which is the age wall's member at coefficient
1. The passages are all defined, each by a name the algebra already has;
what the algebra does not already have is the composite, and that is the
law's own, the click.

## 10. Part (9): entanglement, Bell and CHSH by the algebra (the owner's word, by voice, 2026-09-22, as the Boss relayed it)

**The owner's word.** "Entanglement, Bell, CHSH, all these can be shown
in formulas, in modern algebra; no need to show them on the board at
all, I think." This part is in the shape of section 0: the assumptions
first, in the law's own words; then the theorem; then what the paper
needs; then SHOWN / MEASURED ONLY / NEITHER with the register's numbers
by kind, what the algebra gives that no run can and what the run gives
that the algebra cannot, and the locality sentence in the algebra's
words. The paper, the register and NATURE.md are not touched.

**Certification of the inputs.** The registered pair as it is built
(`examples/events/amplitude/bell_0_8.json` and its siblings: the lamp's
`arms` 2 and `branches` `[[0, 1], [3, 1]]`, the joint labels 00 and 11
with the weights `(1, 1)`, Alice's arm the arm 0; the four counters
reading `sum` with `phase_window` a and b, the channels + and -; the
README's L3 and L6; `expectations.json` under `pair` and `pair_n`); the
paper's rule R (the rotation `U_s` on the label pair with the half-angle
tables `C'[s], S'[s]`, `theta_s = pi s / N`), its `eq:joint` (`J(o_A,
o_B) = sum_l c_l U_a[o_A][l] U_b[o_B][l]`, `R = J^2`), `eq:rung`, P6 (the
click of a pair is one gather of one record from both settings, the
law's one non-local operation), P10 (Born's `c_1 = 1`), `th:isometry`,
`th:marginals`, `th:bell`; section 9's names (the group ring, the state
`chi_1`, the rung as a stochastic map); NATURE row 1a and the register's
L6 entry for the numbers by kind. Cited as mathematics and not as the
law's: Cirel'son 1980 (the bound) and Landau 1987 (the identity of the
CHSH operator's square). Nothing else enters; every number below is a
closed form from these definitions, checked here by my own arithmetic on
the paper's formulas (not a run), or a registered reading named by kind.

**(1) The assumptions, in the law's words.**

- (B1) *The pair's record.* One record, born at the lamp (rule B) with
  two arms and two joint labels of weight 1 each: as an element of
  Inside it is `psi = 1 . (00) + 1 . (11)` in `Z^2 (x) Z^2`, tensored
  with its phase in `Z[Z_N]`; the weights are carried unchanged and the
  phase by verb 1 (the flight's translation of the phase) on each arm's rows and
  by verb 3 (the merge) where rows meet; nothing of one arm is written
  on the other in flight.
- (B2) *The settings.* A detector's setting is the integer s of its
  `phase_window`; at the set the labels are rotated by the integer matrix
  `U_s = [[C'[s], S'[s]], [-S'[s], C'[s]]]` (rule R, verb 2 with a
  declared matrix), `U_s^T U_s = n_s I` exactly, `n_s = C'[s]^2 +
  S'[s]^2` (`th:isometry`); Alice's arm reads `U_a`, Bob's `U_b`.
- (B3) *Born at the click* (section 7's row 6, section 9 (b)): the cell
  `(o_A, o_B)` has the weight `R = J^2` with `J` the pair's summed
  pointer at that cell, and the click is one gather of the one record
  from both arms at completion (P6), the cell selected by the wheel's u
  through the rung (`eq:rung`).
- (B4) *What is assumed of the world, not supplied by the law:* that
  the settings a, b are chosen freely of the record (the choosers), and
  that a detector's reading is the click with `c_1 = 1` (P10). No
  Hilbert space is assumed: the objects are integer lattices with the
  click's quadratic form, and the tables' cosine is `C'[s] / 256` within
  `1 / 512`.

**(2) The theorem.**

*(i) The correlation.* With `c_l = (1, 1)`, `J(o_A, o_B) = (U_a
U_b^T)_(o_A o_B)`, so `J(+, +) = J(-, -) = C'[a] C'[b] + S'[a] S'[b]` and
`J(+, -) = -J(-, +) = C'[a] S'[b] - S'[a] C'[b]`: before the tables'
rounding, `256^2 cos(theta_a - theta_b)` and `-256^2 sin(theta_a -
theta_b)`; the weights `R` are their squares, `C_K = 2 n_a n_b`, and

    E(a, b) = (R_++ + R_-- - R_+- - R_-+) / C_K = cos^2 - sin^2 = cos(2 (theta_a - theta_b)) = cos(2 pi (a - b) / N),

an identity of the rotation's algebra, exact on the tables' cosine;
with the tables' rounding within `4 delta = 0.01108 < 0.0111` and with the rung
within `2 / N` (`th:bell`, `eq:ebound`). In the algebra's words: the
observable of the setting a is the involution `A_a = U_a^T diag(1, -1)
U_a / n_a` in `M_2(Q)` (`A_a^2 = I` by `th:isometry`), the pair's state
the vector `psi = (00) + (11)`, and `E(a, b) = <psi | A_a (x) B_b | psi> /
<psi | psi>`: the textbook's expectation, computed on `Z^2 (x) Z^2` with
the Euclidean form, which is exactly what the click's `J^2 / C_K` is.
The marginals: `sum_(o_B) R = n_a n_b` for each `o_A` (the rows of `U_b`
orthogonal on the integers), so Alice's + count is exactly `N / 2` for
every (a, b) and every N, and Bob's is `N / 2` off a tie
(`th:marginals`, rung 1, exact): no-signalling as an identity of the
integers, not of a limit.

*(ii) The CHSH sum at the optimal settings.* At the labels `(a, a', b,
b') = (0, N / 4, N / 8, 3 N / 8)`, `2 (theta_a - theta_b)` runs over
`-pi / 4, -3 pi / 4, pi / 4, -pi / 4`, so

    S = E(a, b) - E(a, b') + E(a', b) + E(a', b') = sqrt 2 / 2 + sqrt 2 / 2 + sqrt 2 / 2 + sqrt 2 / 2 = 2 sqrt 2

as an identity of the cosine; on the lattice `S(N)` is the exact
rational the rung gives, and `abs(S(N) - 2 sqrt 2) <= 8 / N + 0.0444`
(`th:bell`). Computed here from the definitions (rule R, `eq:joint`,
`eq:rung`; my arithmetic, no engine): `S(64) = 11 / 4 = 176 / 64`,
`S(256) = 45 / 16 = 720 / 256`, `S(1024) = 181 / 64 = 2896 / 1024`,
`S(4096) = 181 / 64 = 11584 / 4096`, the marginals `N / 2` at every pair:
the register's rationals reproduced from the formulas alone.

*(iii) Tsirelson's bound, a theorem of the operator algebra, cited as
mathematics.* For self-adjoint involutions `A, A'` and `B, B'` with `A`'s
commuting with `B`'s, the CHSH operator `X = A (x) (B + B') + A' (x) (B -
B')` satisfies `X^2 = 4 . 1 - [A, A'] (x) [B, B']` (Landau 1987), so
`norm(X)^2 <= 4 + norm([A, A']) norm([B, B']) <= 4 + 2 . 2 = 8` and
`abs(<X>) <= norm(X) <= 2 sqrt 2` in every state (Cirel'son 1980). In
the law's objects the involutions are the `A_a` above in `M_2(Q)`, the
commutator `[A_a, A_a']` is `2 sin(2 (theta_a - theta_a'))` times the
rotation by a quarter turn (nonzero unless `a - a'` is a multiple of `N
/ 2`: this is where the noncommutativity of section 9 (b) sits, in
`M_2 (x) M_2` on the labels, not in the abelian phase algebra), and the
bound applies EXACTLY to the pre-rounding correlations `cos(2 pi (a - b)
/ N)`, which are a quantum state's expectations on `C^2 (x) C^2`. It does
NOT bound the finite-N rational: `S(16) = S(32) = 3 > 2 sqrt 2`
(`th:bell`), because the rung's rounding of the four cells by up to `1 /
N` each is not a state's expectation; the bound is a statement about the
identity of (i), and the lattice's departure from it is the wheel's
grain, two-sided about `2 sqrt 2` (the plateau `181 / 64` below it by
`3.02 x 10^-4`, `5793 / 2048` above at 16384).

*(iv) Entanglement, in the algebra's words.* The pair's state `(00) +
(11)` in `Z^2 (x) Z^2` has tensor rank 2 (it is not `u (x) v` for any
integer vectors u, v: its coefficient matrix is the identity, of rank
2), which is the Schmidt rank of the maximally entangled state; a
product state has rank 1 and gives `E(a, b) = E_A(a) E_B(b)` with `abs(S)
<= 2` (Bell's inequality, the CHSH form). So the violation `S > 2` is the
statement that the record's coefficient matrix has rank 2, an integer
fact of Inside, and the reading of that rank Outside is the four
correlations at two clicks.

**(3) What the paper needs: the certification as for Lorentz.** If a
Hilbert space, a state vector and Born's rule are assumed, (i) to (iii)
are the textbook's. What the law supplies of them, exactly: the state
(the record's integer weights on two arms, B1), the observables (the
rotations `U_s`, integer matrices, B2), Born (the click's square `J^2`
per cell and the rung, B3; the pure state `chi_1` of section 9), the
tensor product (the two arms of one record, gathered once), and the
marginals exactly `1 / 2`. What is assumed of the world: the free
settings and `c_1 = 1` (B4). What is NOT assumed: a Hilbert space (an
integer lattice with a quadratic form; the complex field enters only as
the tables' cosine within `1 / 512`), continuity, or any limit; the
limit `N -> infinity, N_t -> infinity` is where the lattice's numbers
meet the textbook's `2 sqrt 2`.

**(4) SHOWN / MEASURED ONLY / NEITHER.**

| The formula Outside | Verdict | The one line that decides | The register (kind) |
| --- | --- | --- | --- |
| `E(a, b) = cos(2 pi (a - b) / N)` within `2 / N + 0.0111` | SHOWN (rung 1 within the two grains) | `J = U_a U_b^T` and `R = J^2`: `cos^2 - sin^2` | L6: `E x 1024 = 724, -724, 724, 724` at N = 1024 (DETECTOR, the run of 2026-09-20, "every count the reading's") |
| the marginals exactly `1 / 2`, no-signalling | SHOWN, rung 1 exact | the rows of `U_b` orthogonal on the integers, `C_K = 2 n_a n_b` (`th:marginals`) | the rule over all 4096 setting pairs at N = 64, `32 / 64` in every pair (record 105, a computation over the 64 x 64 pairs: GAMEBOARD by kind); the registered worlds' rows `32 / 64` at N = 64 and `N / 2` on every plateau world, `256 / 512`, `1024 / 2048`, `2048 / 4096`, `4096 / 8192` (DETECTOR) |
| `S = 2 sqrt 2` at the optimal settings | SHOWN as an identity of the cosine; on the lattice the exact rational `S(N)` | four cosines of `pi / 4` | NATURE 1a: `S = 176 / 64 = 2.75` at N = 64 (DETECTOR; Hensen 2015's `2.42 +- 0.20`, PASS, 0.33 above it, 1.65 of its standard error; 0.078 below the bound); L6: `2896 / 1024` and `11584 / 4096 = 2.828125` (DETECTOR), `3.02 x 10^-4` below `2 sqrt 2`, the paper's one prediction (24.4) |
| Tsirelson's `abs(S) <= 2 sqrt 2` | SHOWN as mathematics for the pre-rounding correlations; NOT a bound on `S(N)` | Landau's identity `X^2 = 4 - [A, A'] (x) [B, B']` | `S(16) = S(32) = 3` above the bound by the rung's grain (`th:bell`, a computation, GAMEBOARD by kind: no run at 16) |
| the rise `S(N)` to the plateau `181 / 64` | SHOWN by the closed form at every N (a computation from the definitions, not a run); MEASURED at 64, 512, 1024, 2048, 4096, 8192 and 16384 | the rung on the fixed correlations, `S(N) = 8 (c_1 + c_1') / N - 4` | the seven engine values equal to the closed form's (DETECTOR: `176 / 64`; `1448 / 512` of 2026-09-21; `2896 / 1024` and `11584 / 4096` of 2026-09-20; `S x N = 5792, 23168, 46344` at 2048, 8192 and 16384, the Bell plateau runs of 2026-09-22, record 736, every count its pinned count); computed and not run only at 256 and the N that are not powers of two |
| the loophole-free geometry (space-like separated settings) | NEITHER | the pair's click is one gather at completion; "the near party's outcome is written at the far party's tick"; the arms' order a declaration | none; `bell_16_24_far` reads the same counts with Bob 116 Links farther (no maintenance), not a spacetime test |
| unequal weights, more than two labels | NEITHER (open) | `th:marginals`' scope | none |

**What the algebra gives that no run can:** the bound, why `2 sqrt 2`
and not more (Landau's identity is an operator fact, true in every state
of every dimension; no finite run reaches "every"), and the limit (the
joint limit of `S(N)` in N and `N_t` is `2 sqrt 2`; with the tables fixed
`186034 / 65773`). **What the run gives that the algebra cannot:** that
the six verbs' integers reach it (that the engine's rows, merges,
rotations, squares and rungs compose, interval by interval on a
GameBoard of 21 Nodes, to the closed form: the bijection theorem plus
the run, and the seven engine values equal to the formula's, at 64, 512,
1024, 2048, 4096, 8192 and 16384), the
finite-N rise `S(N)` at the N actually built, and the marginals read from
rows rather than proved.

**The locality sentence, in the algebra's words.** The title says the
law is local and the read-out is not. The non-locality sits in ONE
object: the pair's record, an element of `Z[Z_N] (x) Z^2 (x) Z^2` of
tensor rank 2, carried by local verbs on two arms (each row at its own
Node with its six neighbours; no Node keeps anything beyond the events
there, P4, the law of events) and read by ONE gather at two clicks (P6,
the one non-local operation). In the textbook's words: the state is
entangled (not a product), the local observables commute (`A_a (x) 1`
with `1 (x) B_b`), the correlation violates CHSH, and the partial trace
is the uniform marginal: no-signalling. The law has that structure with
Z in place of C, and its one departure from the textbook is the rung,
whose grain is what a finite N adds.

**Three sentences for the paper (marked as such; the coordinator's to
take or leave).** (i) Bell's correlation is an identity of the rotation's
algebra on the record's two labels, `E(a, b) = cos(2 pi (a - b) / N)`
before the tables' rounding and within `2 / N + 0.0111` after it, the
marginals exactly `1 / 2` for every setting pair, and `S = 2 sqrt 2` at
the CHSH labels is four cosines of `pi / 4`. (ii) Tsirelson's bound is
a theorem of the operator algebra on the labels' `M_2 (x) M_2` and bounds
the pre-rounding correlations, not the finite-N rational, which the rung
rounds two-sided about `2 sqrt 2` (3 at N = 16 and 32, `181 / 64` on the
plateau). (iii) The non-locality is the tensor rank 2 of one record read
by one gather at two clicks; the rows are local and no Node keeps
anything, so the law is local and its read-out is not.

## Cut on 2026-09-22 (the owner's word: delete what no longer applies; everything gets shorter)

The later statement is the canonical text; the earlier is kept as one
line with its pointer. No verdict, number or record's citation is
deleted.

- "The real world" for the game above the board: superseded by the
  owner's two words, Inside and Outside (section 8's head; Outside
  represents reality and is not reality); replaced in this file's own
  prose, kept inside the owner's quotations.
- Section 0's order statements "to second order in the velocity, the
  corrections from the fourth order on": superseded by M4 (the
  correction of relative order `m^2 v^2 / 6`, second order in v at fixed
  m, vanishing as m -> 0; the fourth order kept for the three-dimensional
  anisotropy alone), folded at fe498362 in sections 0, 6 and 7.
- The dilation's two readings (`lambda = gamma` with `1 / b = 1 + v`,
  `lambda = k` with `b = 1 + v`): reconciled in section 0 (b) as one
  parenthesis; the round trip r-free in either.
- Part (6)'s first step (c), the `sqrt 3` conversion of p: withdrawn at
  0d0b30b3 and superseded by the unit chain (`E^2 = E_0^2 + c^2 p^2` with
  p per Link, `E' = E / c^2`, the 3 = `1 / c^2` = d), section 7 (1) (c).
- Section 8 (e)'s first constant (`a = -(N_l c / tau_L) grad A`): withdrawn
  at e26c1f43 (the flow's coefficient written for the acceleration) and
  superseded by `a = -(c^2 / N_w) grad A`, `delta k = (n S / d)(g h /
  c^2)`.
- Part (8)'s first opening (three formulas with a "meeting" of the two
  steps and the quantum as a paragraph): superseded at 964711b4 by the
  owner's one direction (the Inside step the axiom, the Outside step a
  theorem, the quantization of the Outside a theorem, Newton the limit)
  and replaced whole.
- Part (4)'s first draft (r = `E_0 / E'` taken from W as an input,
  "Lorentz from Lorentz"): withdrawn and superseded by section 5's
  certified inputs (the withdrawal stated there).
- The clock loop's stage 1, once written here as a section 28 of
  DERIVATIONS_BEAM and reverted: lives in
  [the clock loop](../clock_loop/DERIVATION.md); cited, not repeated.
- "Derived" where a form was put in: replaced by "follows" (the writer's
  audit), the section 7 title kept in the owner's own question.

## 11. Links

[DERIVATIONS_BEAM 4.3](../../DERIVATIONS_BEAM.md#43-a-moving-clock-the-rate-is-one-at-every-speed),
[17.6](../../DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes),
[17.7](../../DERIVATIONS_BEAM.md#177-the-proper-time-gate-without-a-root-two-counters-compared-against-the-whole-root-the-owners-word-2026-09-22-records-642-and-647);
[the clock loop, stage 1](../clock_loop/DERIVATION.md); [NATURE rows 4a, 4b
and 12](../../NATURE.md); [the covariant worlds](../../../examples/events/covariant/README.md);
[HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector).
