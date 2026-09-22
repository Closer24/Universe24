# Einstein Outside: the formulas of the special and the general theory brought from inside the GameBoard to above it, each with the transformation of a named detector at a named place (the owner's order, 2026-09-22, about 05:55Z, as the Boss relayed it)

The Einstein Mathematician, 2026-09-22, on the Boss's order of about
05:55Z: a derivation on paper, docs only, no code, no world file, no
run; every number a closed form or a registered reading labelled by its
kind (DETECTOR or GAMEBOARD); a run, where one is named, is the owner's
word. This document builds on the click frame at 3268e7d5 (PR #769, not
yet merged: docs/designs/click_frame/DERIVATION.md, cited below as "the
click frame :line" by its line numbers at that commit) and does not redo
what it shows: the Bondi k-calculus of its sections 0 to 5, Eq. 14 from
the conversion of its section 7, Newton Outside of its section 8. The
boundary with the Light Mathematician (the light-outside derivation):
light's own kinematics and its waves (the arrival, the pace, the phase
in flight, the interference) are that document's; this document takes
light only where a mass acts on it, the bending and the delay (II.11),
and cites the click frame for the rest. Nothing here enters the law; a
hypothesis that needs more than the six verbs is stated under its own
identity, outside the law (skills/workflow.md, "The three tests").

## 0. The owner's order, and the two rules this document obeys

**The order** (2026-09-22, about 05:55Z, by voice, as the Boss relayed
it): "Another mathematician: try to bring Einstein out of the board and
above the board, all the formulas we need. And if a transformation
formula of a click is needed: an emitter and a click are a
transformation formula between place and place. Then I can give the
command to check whether Einstein follows from inside the board to
above the board." And, said for every formula: "a transformation for
each formula, because one passes from inside the board to above the
board; keep consistency: if one wants to measure in another place, the
detector has to move to that other place."

**The two rules, as this document applies them.**

(T) *The transformation rule.* Every formula below is written three
times: INSIDE, a GameBoard quantity from the six verbs with its source
line on `main`; the TRANSFORMATION, a named emitter at a named place A
and a named detector at a named place B, the packet that passes from A
to B and the two counts it is stamped with; and OUTSIDE, the formula in
the detector's own counts alone. The transformation is one object in
every theorem: the place-to-place factor of section 1 (Theorem 1),
whose one-dimensional case is the click frame's k-calculus (:244, :252),
and its radar form (Theorem 2), which is the click frame's section 0 (b)
read as coordinates.

(C) *The consistency rule.* No Outside formula contains a count of a
detector at a place where the detector is not. What is at another place
is read in one of two ways, and the two are one theorem: the detector
sends a pulse there and counts its return on its own record (the clock
of record 768: HIGHLIGHTS 5.4 :402; docs/TERMINOLOGY.md :351-357), or
the detector moves there (the moving detector of record 762, HIGHLIGHTS
:401; the transponding record of the click frame 2 (c), :284-290). Two
detectors at two places compare counts only through rows between them,
never in zero time (the click frame :215-217). Where a formula needs
two clicks at two places at once (a length, II.4), the document names
the detectors and says whether the law can read it.

**Kinds and rungs.** Every number is DETECTOR (a click, a count or a
ratio of counts at a detector) or GAMEBOARD (the tick, a Node, a row's
position, the drive's pace, a body's accumulators, a world's declared
input); only a DETECTOR number is compared with nature (record 281;
docs/TERMINOLOGY.md :334-350). Rungs as the click frame uses them: rung
1 exact on the GameBoard within the accumulators' remainder (within
`1 / T` of a count, `1 / T_D` of a pace); rung 2 a limit (the
continuum, the shell mean, `v << c`); "up to `m^2 v^2`" where the
walk's cosine form is the exact one (the click frame :74-80). Every
result is stated as matching nature, never as being nature (record
762).

**Notation** (skills/workflow.md, "Notation"; a scalar plain, a vector
in bold lowercase). c: the pace of a row, one Node per interval in the
hop frame of the click frame's section 1, `1 / sqrt 3` Links per
interval on the Beam Law's lattice (input 9 of DERIVATIONS_BEAM 24.1),
the unit of every pace below (`c = 1` unless c is written). v, beta: a
record's pace as a fraction of c. **v**: a velocity vector, Nodes per
interval in the lattice's frame (GAMEBOARD). **s**: the unit vector of
a packet's direction from the emitter's Node to the detector's Node.
`r_D`: a detector D's own count per interval against the tick (the
click frame :37-39; GAMEBOARD; two families compare it through clicks).
`k_XY`: the place-to-place factor of a packet from X to Y (Theorem 1;
DETECTOR). gamma: the Lorentz factor `1 / sqrt(1 - v^2)`. T: a
detector's own count between two packets it emits. `n_D`: a detector's
own count. `a_tau`: the age moment, the crowd's sum of amount times age
at a Node (record 394). `[n, d]`: a world's suspension pair;
`k = a_tau n / d` the crowd's owed rate at a Node. `N_l = Q`: the label
scale (64). `N_w = S`: the width of the push (Newton's constant's
place, docs/NATURE.md :79). `tau_L`: the residence factor, the
intervals a row spends per Euclidean Link (`T_D / (N_l abs(D))`, 1.72
on a heading, `sqrt 3` in the limit of every direction; `tau_L c = 1`
in that limit). A: the age-moment field of a source (DERIVATIONS_BEAM
5.1). m: the mass angle of the walk's coin, radians per interval; kappa
its wave number; omega its frequency. `E'_0 = Q S M`: the rest energy
in the identity's whole units, M the content. W: the identity's exact
square. **p**: the momentum vector on a record. h: the family's
quantum; `hbar = h / (2 pi)`. L: a length in Nodes or Links. Y: a
height between two detectors, in Links (the letter h is Planck's here).
theta: an angle. G: Newton's constant as the law names it. g: the
fall's acceleration. b: an impact distance. `c_f`: the coefficient of
the flight in the age wall's set under the key `optical` (`1 + gamma`,
gamma there the post-Newtonian parameter, an input of kind 2,
docs/NATURE.md :80; not the Lorentz factor).

## I. The assumptions, in the law's own words, with their source lines on main

- **(A1) The click.** "A click is the passage of information from Node
  to Node, at most one Node per interval: c is the unit, the same in
  every family, and nothing passes faster" (the click frame :47-50;
  HIGHLIGHTS 5.4 :400, record 749). On `main`: POSTULATES.md section 4
  :264-267 ("Physical influence cannot skip nodes. It travels at most
  one neighboring node per elementary step"); the flight's one carry
  per interval, DERIVATIONS_BEAM 13.2 (a) :3590-3596.
- **(A2) The amplitude.** "A click's content is an amplitude with a
  phase that splits each interval between staying and hopping, the mass
  the staying share" (the click frame :50-53; HIGHLIGHTS :400). The
  law's rows do not have it: they hop whole (the click frame :158-166,
  sections 5 and 6). This document uses (A2) only where it cites
  section 7 (the identity W, II.6) and section 0 (the rate r from the
  walk, II.1); every other theorem uses (A1) and the law's rules alone
  and says so.
- **(W1) The age wall.** `core/integer.py:118-153` (`age_wall`: "a
  count at the rate `rate` against the wall `wall` becomes the count at
  the rate `rate x d` against the wall `wall x (d + c x a_tau x n)`,
  `[n, d]` the world's `suspension`"); the declared set
  `events/measured.py:344` (`AGE_WALL_SET = (("owed", 1),)`: "Today the
  set is the body's clock alone, c = 1"); the owed count
  `events/engine.py:154-178` (`count_owed`). The rate of a body's
  self-creations in a crowd is `1 / (1 + a_tau n / d)`, `a_tau` the age
  moment by default (record 394). A detector's own count is the same
  member at coefficient 1 (record 709; HIGHLIGHTS :399). The click
  frame's N1 and N2 (:937-949).
- **(W2) The push and the drive.** `events/nature_beam.py:2932-2988`
  (`push_form`, the gravity column: "the count is `|V M_A|` exactly, the
  law's `-M_A V_B`"); `events/engine.py:119-150` (`step_axis`: "`drive
  + p` is compared with `D = Q x S x M + |p|`", the count primitive
  `by_drive` with `at_most` 1); `core/integer.py:79-115` (`by_drive`).
  The pace `abs(p_a) / (Q S M + abs(p_a))` Links per interval per axis
  (DERIVATIONS_BEAM 4.4 :1109-1112; the paper's P9, main.tex:160-165).
  The click frame's N3 (:950-955).
- **(W3) The flight blind.** `events/nature_beam.py:745-760` (`Flight`:
  "one world constant per direction: v, `S_1`, `T_d = isqrt(3 |v|^2
  Q^2)`, the Bresenham line"); `events/measured.py:344-362`: the row's
  flight is not a member of the age wall's set on `main`, it joins
  only under the world key `optical` at the coefficient `1 + gamma`
  (`FLIGHT_MEMBER`, `age_wall_set`), and the phase per age is never a
  member (`AGE_WALL_NEVER`, :345: "a stretched phase per age would
  redshift light in transit"); DERIVATIONS_BEAM 5.4 :1251-1258 ("On
  `main` a row reads nothing of the crowd: a row is neither bent nor
  delayed beside a mass, exactly"); the paper's P9 (main.tex:160-162,
  "the flight is blind to the crowd, a row's rate in transit constant
  and its wall the direction's `T_D`"). The click frame's N4
  (:956-960).
- **(W4) The reading by clicks.** Nothing leaves the board but clicks;
  a number Inside is a GameBoard reading, a click Outside a detector
  reading (docs/TERMINOLOGY.md :334-350; HIGHLIGHTS :379, :402;
  POSTULATES.md section 10). The click frame's N5 (:961-966).
- **(W5) The clock: a pulse and its return.** "What the detector emits
  and receives back, counted on its own record; a detector at rest
  receives its row back at its own Node, a moving one at the next; the
  emission at the detector's own self-creations, stretched by the
  crowd; no Node holds a detector's time" (docs/TERMINOLOGY.md
  :351-357; HIGHLIGHTS :402, record 768).
- **(M) The spreading**, arithmetic and not an assumption: K beams over
  a shell of `N(r)` Nodes, `N(r) -> 4 pi r^2` (the click frame
  :967-977).
- **(K) The declared inputs** that the formulas below carry as
  constants, all of kind 2 (a number the law does not fix): the
  suspension pair `[n, d]`, the width `S = N_w`, the release `eta` per
  unit of content per direction, the fan's K and the label scale `Q =
  N_l` (docs/NATURE.md :72-81); and, beside the law under the key
  `optical`, the coefficient `c_f = 1 + gamma` (docs/NATURE.md :80).

**What is not an input.** No Lorentz transformation, no metric, no
gamma, no potential, no inverse square, no `c^2` beyond the conversion
of a unit (the click frame 7 (c), :775-799). Section III certifies this
theorem by theorem.

## 1. The transformation: an emitter and a click as the map between two places

**Definition (the click of a packet, and the transformation it is).**
An emitter X at a place A (a record at rest or hopping) emits a packet
(a row) at its own count `n_X`; a detector Y at a place B receives it at
its own count `n_Y`. The emitter's count rides on the packet (a lamp's
birth ordinal on the record, docs/TERMINOLOGY.md :371-377); the
detector's count is stamped at the click. The transformation of the
packet is the map `n_X -> n_Y`; between two packets it is the ratio of
the two counts apart,

    k_XY = (n_Y apart) / (n_X apart),

DETECTOR on both sides (a ratio of two counts of one detector each,
compared through the packets and never in zero time). It is the click
frame's `k_AB` and `k_BA` when X is at rest and Y moves on the axis
(:244, :252); the general form is Theorem 1.

**Theorem 1 (the place-to-place factor).** Let the packet move at c
((A1): one Node per interval in the hop frame; the flight table's
Euclidean pace, isotropic within `1 / T_D`, on the Beam Law's lattice);
let X move at **v**_X and Y at **v**_Y (Nodes per interval in the
lattice's frame, both below c, GAMEBOARD); let **s** be the unit vector
from X's Node at the emission to Y's Node at the arrival; let `r_X`,
`r_Y` be the two records' own counts per interval (GAMEBOARD). Then,
exactly in the mean over many packets (rung 1: the remainders of the hop
accumulators are bounded and periodic in the rational slopes, the click
frame 2 (a) :233-241),

    k_XY = (r_Y / r_X) x (1 - s . v_X) / (1 - s . v_Y)        (c = 1; in general s . v / c).

*Proof.* The packet emitted at the tick `t_n` from **x**_X(`t_n`)
arrives at the tick `t_a` at **x**_Y(`t_a`) with `abs(x_Y(t_a) -
x_X(t_n)) = t_a - t_n`. For the next packet, `t_n + dt_n` and `t_a +
dt_a`, the difference of the two distances is **s** `. (v_Y dt_a - v_X
dt_n)` at first order in the displacements (exact when **s** is
constant: on an axis, and at closest approach), so `dt_a (1 - s . v_Y)
= dt_n (1 - s . v_X)`; the counts are r times the ticks. On the lattice
the mean is over the period of the rational slopes and the pace is the
table's, within `1 / T_D` (the click frame :241-249). QED.

*Corollaries.* (i) X at rest, Y receding at v on the axis, **s**
forward: `k = r_Y / (1 - v)`, the click frame's `k_AB` (:244); Y at
rest, X receding, **s** backward: `k = (1 + v) / r_X`, its `k_BA`
(:252). (ii) The round trip X to Y to X, Y transponding (the click frame
2 (c)): `k_XY k_YX = (1 - s . v_X)(1 + s . v_Y) / ((1 - s . v_Y)(1 + s .
v_X))`, r-free for every pair of rates (the click frame :112-114 on the
axis). (iii) The transverse case, `s . v_X = 0` with Y at rest: `k = 1 /
r_X`, the emitter's own rate alone. (iv) Two records at rest in crowds,
`k_X = a_tau n / d` at X and `k_Y` at Y (W1): `k_XY = (1 + k_X) / (1 +
k_Y)`, the click frame (2)(a) (:986-991). (v) Composition: a packet X
to Y to Z with Y transponding gives `k_XZ = k_XY k_YZ` exactly, Y's
count being the middle term of two ratios, and the direct packet X to Z
gives the same by the formula, the factors `(1 - s . v_Y)` cancelling.

*What the theorem is not.* `r_X` and `r_Y` are GAMEBOARD and no single
factor reads either alone: the round trip (ii) reads none, a one-way
factor on the axis reads r with the pace mixed in (the click frame
section 4), the transverse factor (iii) reads `r_X` alone and needs the
geometry (**s** perpendicular to **v**_X, which a line of detectors at
rest fixes by the emitter's Node at the emission). The law fixes `r = 1
/ (1 + k)` at every speed (DERIVATIONS_BEAM 4.3 :1083-1094: "a clock
slows by what it reads, never by its speed"); the identity
covariant-readings-v1 fixes `r = E'_0 / E'` in no crowd (17.6 M1); the
click theorem's (A2) fixes `r = sqrt(1 - v^2) (1 - kappa^2 / 6 + O(4))`
(the click frame :74-80). Every Outside formula below is written in r,
and at each the three r are stated. Where a crowd and a speed act
together the law's r is `1 / (1 + k)` alone; the cross term of the
identity's r with the crowd's is the identity's own declared order of
its two owed counts, not the law's, and it is of the post-Newtonian
order that II.12 finds absent in any case.

**Theorem 2 (the radar reading: the clock of record 768 as
coordinates).** A detector D emits a pulse at its own count `n_e` and
receives its return at `n_r` from a transponding record at another
place (rule (C)). It assigns to the reflection the two numbers

    x_D = (n_r - n_e) / 2,     t_D = (n_r + n_e) / 2        (c = 1; in Links x_D = c (n_r - n_e) / 2),

both DETECTOR, both on D's own record. (a) For D at rest in no crowd
(`r_D = 1`, the pulse one Node per interval each way) `x_D` is the
reflection's Node and `t_D` its tick, exactly within the hop's
remainder: the radar of a rest detector is the lattice's own
coordinates, GAMEBOARD numbers made DETECTOR by the pulse. (b) For D
moving at v on the axis with the rate `r_D`, a reflection at the
lattice Node X at the tick `t_1` (both GAMEBOARD) has, from the two
legs `t_1 - t_e = X - v t_e` and `t_r - t_1 = X - v t_r`,

    x_D = r_D (X - v t_1) / (1 - v^2),     t_D = r_D (t_1 - v X) / (1 - v^2),

that is, `(t_D, x_D) = lambda x Lorentz_v (t_1, X)` with `lambda = r_D /
sqrt(1 - v^2) = r_D gamma`: the moving detector's radar coordinates are
the Lorentz boost times the dilation `lambda`, which is the click
frame's `lambda = sqrt(a b) = r / sqrt(1 - v^2)` (:112-116) read as a
map of coordinates and not redone here; `lambda = 1` if and only if
`r_D = sqrt(1 - v^2)`, the click frame's one line `k_AB = k_BA`
(:265-267); under the law `lambda = gamma` (:119). Rung 1 in the mean.
*Proof of (b):* eliminate `t_e` and `t_r`: `t_e = (t_1 - X) / (1 - v)`,
`t_r = (t_1 + X) / (1 + v)`; then `n_r - n_e = r_D (t_r - t_e) = 2 r_D
(X - v t_1) / (1 - v^2)` and `n_r + n_e = 2 r_D (t_1 - v X) / (1 -
v^2)`. QED. (c) The transverse leg: a co-moving transponder at the
lattice offset `Y_0` across the motion is reached in `Y_0 / sqrt(1 -
v^2)` ticks each way (`(t_1 - t_e)^2 = Y_0^2 + v^2 (t_1 - t_e)^2`), so
D reads its transverse distance as `y_D = r_D gamma Y_0` and its
longitudinal distance to a co-moving transponder at the lattice offset
`L_0` (from (b) with `X = v t_1 + L_0`) as `x_D = r_D gamma^2 L_0`.

**The one fact the two theorems share, stated once.** A ratio of two
counts of ONE detector is r-free (the round trip, a radar velocity, a
radar angle); a ratio of counts of TWO detectors carries `r_Y / r_X`
(a one-way Doppler factor, a rate, an energy). Every Einstein formula
below falls on one side of this line: the r-free ones come out of (A1)
alone, exactly and under every r, and are Lorentz's already on the law
as it stands; the ones with a scale hang on r, which the law fixes at
1, the identity at `E'_0 / E'`, and (A2) at `sqrt(1 - v^2)` up to
`m^2 v^2`. This is the click frame's "the Lorentz group up to scale"
(section 0 (i), :62-70) applied formula by formula, and the reason the
verdict of section IV is what it is.

## II. The theorems: each formula Inside, its transformation, and Outside

Each theorem: INSIDE (the GameBoard formula and its source), the
TRANSFORMATION (the named emitter at A, the named detector at B, the
packet and its two counts), OUTSIDE (the formula in the detector's own
counts), its ORDER, its INVERSE where one exists, and the REGISTERED
reading by kind with the verdict against its pin or against nature.
Names of places used throughout: A the Node of the emitter or of the
detector at rest (Node 0, in no crowd unless said); B the place of the
other record; G a ground detector at rest at A; R a moving record that
carries momentum and transponds (the click frame 2 (c), the three tests
at :284-290: a lamp keyed to arrivals, the release verb, its own record
and Node); L a line of one-Node detectors at rest along an axis (the
Newton session's form, series D3).

### II.1 Time dilation: the rate r

**Inside.** The moving record's own count per interval, r: on the law 1
at every speed, the counter stretched by the crowd alone
(DERIVATIONS_BEAM 4.3 :1083-1094; HYPOTHESES 21); under the identity
`r = E'_0 / E'` with `E'` the whole root of W (17.6 M1, M3); under (A2)
the walk's `r = m / omega = sqrt(1 - v^2) (1 - kappa^2 / 6 + O(4))`,
`kappa^2 = m^2 v^2 / (1 - v^2)` (the click frame :74-80, :812-820).

**Transformation.** The emitter is R at B, moving at v on the axis away
from G; it carries a lamp that emits one record every T of its own
count. The detector is G at A, at rest. G's own count between two
arrivals over T is `k_RG = (1 + v) / r` (Theorem 1 (i)). By rule (C)
the second direction is read by the same G through R transponding: G's
lamp at A emits every T of G's count, R re-emits at each arrival, and
R's own count of the arrivals rides on its records (the click frame
section 4, :365-388): `k_GR = r / (1 - v)`.

**Outside.** From the two factors read at G alone,

    v = (k_GR k_RG - 1) / (k_GR k_RG + 1)   (the round trip, r-free),
    r = sqrt((1 - v^2) k_GR / k_RG) = sqrt((1 - v^2) x k_GR / k_RG),

the moving record's own count per interval, DETECTOR: time dilation is
this r, and nothing else Outside is. Under the line `k_GR = k_RG` it is
`sqrt(1 - v^2) = 1 / gamma`, nature's; under the law `k_GR / k_RG = 1 /
(1 - v^2)` and r = 1 (no dilation); under the loop's resident count `r
= 1 - v` (the click frame section 3). **Order:** rung 1 within `1 / T`
(the counts); the identity's r exact on its integers; the walk's up to
`m^2 v^2 / 6`. **Inverse:** `k_GR = r / (1 - v)`, `k_RG = (1 + v) / r`
from (v, r). A second road to r, with no transponder: Theorem 1 (iii),
a detector G' at rest at the transverse distance from R's track reads
`k = 1 / r` at R's closest approach (the emission's Node fixed by the
line L), nature's transverse Doppler gamma; the law's 1 (DERIVATIONS
2.7 :832: "exactly 1, the classical value").

**Registered.** r itself NOT READ as a measurement (the click frame
:347-364): series J4's `become` at 64 at every speed is pinned and not
run (NATURE 4a :100, FAIL against gamma 29.33, the ratio 1); series S
under the identity reads the 64th self-creation at 70 and 124
(GAMEBOARD, the `become` lines; the derived 70 and 124, the design's
70.9 and 125.2 within one tick) and the products' face clicks at 369
and 345 (DETECTOR, the pins 367 and 345 within two ticks, the decay
tick derived back by the flight table: MET in the identity's domain,
gamma <= 2), the law's row the FAIL beside it (docs/EXPERIMENTS.md
:6652-6735). The transverse factor NOT READ. Verdict: the Outside
formula SHOWN (rung 1); r MEASURED only through the identity's clicks
(S, MET); on the law FAIL (4a).

### II.2 The relativistic Doppler and the round trip (cited, not redone)

**Inside.** The phase per age `n / d` turns per interval, the row's
energy `E = h n / d` (DERIVATIONS_BEAM 6.4; the click frame :889).
**Transformation.** The lamp on R at B, the detector G at A: `k_RG = (1
+ v) / r` (Theorem 1 (i)); the reverse `k_GR = r / (1 - v)`; the round
trip `k_GR k_RG = (1 + v) / (1 - v)` under every r (Theorem 1 (ii)).
**Outside.** `1 + z = k_RG`: on the law `1 + v`, under the identity
`gamma (1 + beta)`, under the line `sqrt((1 + v) / (1 - v))`; the round
trip `(1 + v) / (1 - v)` r-free, nature's radar Doppler exactly. The
whole of this is the click frame's sections 0 (b), 2 and 4 and its
table's third row (:889); nothing is added. **Order:** rung 1 within
`1 / T`. **Inverse:** the law `v = z`; the identity and the line `beta
= ((1 + z)^2 - 1) / ((1 + z)^2 + 1)`. **Registered.** NATURE 4b :101:
`z = 0.2636` at beta 0.2674 under the law (DETECTOR, FAIL against
nature's 0.315); series S: `z = 0.3674` at beta 0.3040, gamma 1.04967,
the pin `0.369 +- 0.003` (DETECTOR, MET in its domain;
docs/EXPERIMENTS.md :6715-6725); `k_GR` NOT READ, the missing direction;
the round trip NOT READ, its pins `3, 5/3, 9/7, 17/15` at v = 1/2, 1/4,
1/8, 1/16 under every r (the click frame :383-388). Verdict: the round
trip SHOWN r-free; the one-way factor SHOWN in r, MEASURED under the
identity (MET), FAIL on the law (4b).

### II.3 The composition of velocities: the k factors multiply

**Inside.** Velocities in the lattice's frame add as Nodes per interval
add: R at `v_R`, a second record R' at `v_R'`, GAMEBOARD, Galilean, no
formula of the law beyond the hop.

**Transformation.** The detector is D, moving at v on the axis with the
rate `r_D` (a body record: the moving detector of record 762). It reads
the velocity of R (at the lattice velocity `v_R`, transponding) by two
radar readings (Theorem 2) and forms `w = delta x_D / delta t_D` on its
own record. Equivalently by the factors: D's round trip to R and back is
`k_DR k_RD` (Theorem 1 (ii)), and w is the velocity the r-free round
trip assigns.

**Outside.** From Theorem 2 (b) with `X = v_R t_1 + X_0`: `delta x_D =
r_D (v_R - v) delta t_1 / (1 - v^2)`, `delta t_D = r_D (1 - v v_R)
delta t_1 / (1 - v^2)`, so

    w = (v_R - v) / (1 - v v_R),     and inversely   v_R = (w + v) / (1 + w v):

Einstein's composition of velocities, exactly and under every `r_D`
(the rate cancels in a ratio of D's own counts), from (A1) and the
transponding rule alone. By the factors: `(1 + w) / (1 - w) = k_DR
k_RD = (1 - v)(1 + v_R) / ((1 - v_R)(1 + v))`, the same w by one
division; and the round-trip factors compose as `k_GR' k_R'G = (k_GR
k_RG)(k_RR' k_R'R)` for G at rest, which is `(1 + v_R') / (1 - v_R')
= (1 + v_R)(1 + w) / ((1 - v_R)(1 - w))`: the k factors multiply, and
their multiplication is the composition law. **Order:** rung 1 in the
mean, within `1 / T` on the counts and `1 / T_D` on the pace; on the
Beam Law's lattice the axis case exact and the isotropy within `1 /
T_D`. **Inverse:** as written. The one-way velocity a line L at rest
reads of R (Nodes apart over counts apart between two neighbouring
detectors, the click frame :30-33, :216-217) is `v_R` itself, the lattice's;
for D at rest (v = 0) the two readings agree.

**Registered.** NOT READ: no world with a moving radar detector is
registered; the transponding record is the click frame's missing
direction (:365-388). The pins, before any run, from the formula: a
radar detector at v = 1/2 reading a record at `v_R = 3/4` on the axis
reads `w = (3/4 - 1/2) / (1 - 3/8) = 2/5`, and at `v_R = 1/4` reads
`w = -1/3` (each within `1 / T`); a rest line L reads 3/4 and 1/4.
Verdict: SHOWN, r-free, rung 1; NOT READ.

### II.4 Length contraction: what it needs, and whether the law can read it

**Inside.** Nothing contracts: a rod is two records `L_0` Nodes apart
that hop in step, and Nodes are Nodes (DERIVATIONS_BEAM 12c.3 :3385
"no contraction"; 21.4 row E3 :6235). GAMEBOARD.

**Transformation.** A length is two places read at one time, so by rule
(C) it needs either two detectors at the two ends, whose counts are
compared only through pulses, or one detector reading both ends by
pulses: the radar of Theorem 2 with the two ends transponding (an
emitter is a detector at its own Node, HIGHLIGHTS :381, record 569).
Two readings, and only two, are possible: (a) the ground detector G at
A, at rest, reads a moving rod (the ends at `v t + X_1` and `v t + X_1
+ L_0`, GAMEBOARD) by two pulses returned at equal `t_G`; (b) the
moving detector D, co-moving with the rod at the rate `r_D`, reads its
own rod by two pulses (Theorem 2 (c)), and reads a rod at rest of the
lattice length `L_0` by two pulses returned at equal `t_D`.

**Outside.** By Theorem 2 (a) G's radar is the lattice's coordinates:
(a) G reads the moving rod as `L_G = L_0`. By Theorem 2 (c) the rod's
own length, read by its co-moving D, is `L_own = r_D gamma^2 L_0`. By
Theorem 2 (b) at equal `t_D` (so `delta t_1 = v delta X`), D reads a
rest rod of lattice length `L_0` as `L_D = r_D (L_0 - v^2 L_0) / (1 -
v^2) = r_D L_0`. So the two contractions Outside are

    L_G / L_own = (1 - v^2) / r_D     (a rest detector reading a moving rod),
    L_D / L_0   = r_D                 (a moving detector reading a rest rod),

and they are equal, and both `1 / gamma`, if and only if `r_D^2 = 1 -
v^2`: the same line as II.1, in a length. Under the law (`r_D = 1`) a
rest detector reads a moving rod at `1 - v^2` of its own length (3/4 at
v = 1/2) while a moving detector reads a rest rod at 1 of its own: the
two directions differ, which is the lattice's preferred frame in a
length (DERIVATIONS_BEAM 4.5 :1147). Under the identity's r both are
`sqrt(1 - beta^2)` on its integers. **Order:** rung 1 in the mean,
within one Node (the hop's remainder) on each end. **Inverse:** `r_D`
from either ratio with v from the round trip. **Can the law read it?**
Yes, with no new rule: the transponding lamp (the click frame 2 (c))
on the rod's two ends and a body detector that emits and receives
(record 768); a run is the owner's word. Not by two clicks "at once"
at two places: the law has no simultaneity at two Nodes but the pulse
(rule (C)), and the equal-`t_D` condition above is that pulse.

**Registered.** NOT READ. Pins from the formulas, before any run, at
v = 1/2, 1/4, 1/8: under the law `L_G / L_own = 3/4, 15/16, 63/64` and
`L_D / L_0 = 1`; under the line both `0.8660, 0.9682, 0.9922`; each
within one Node of `L_0`. Verdict: SHOWN in r, rung 1; NOT READ; on
the law FAIL in form against nature's one symmetric `1 / gamma`
(which no experiment reads directly, the contraction being inferred
in nature from the Doppler and the dilation; NATURE has no row for it).

### II.5 Aberration

**Inside.** A packet's direction is a world constant of the flight
table (W3); a moving lamp releases on the fan's directions in the
lattice's frame, no aberration of the emission on `main`
(DERIVATIONS_BEAM 2.5 :787-793; the aberrated release of 12.2
:2886-2960 is a rule proposed with its integer form and its cost, not
built). GAMEBOARD.

**Transformation.** An angle Outside is a ratio of two lengths, so by
rule (C) it is read by one moving detector D with two co-moving
transponders: a pinhole P and, `L_0` lattice Nodes behind it along the
motion, a screen of transponders. A packet of lattice direction
`(cos theta, sin theta)` (theta against D's velocity axis, GAMEBOARD)
enters at P at the tick `t_1` and, moving straight, meets the screen
at the lattice offset `y_hit = L_0 sin theta / (cos theta - v)` across
the motion (the screen has moved `v` per interval meanwhile; the
classical aberration in Nodes, GAMEBOARD, under every r). D reads the
two lengths by pulses: `L_0` as `r_D gamma^2 L_0` and `y_hit` as `r_D
gamma y_hit` (Theorem 2 (c)).

**Outside.** The angle D reads, `tan theta_D = y_D / x_D`, is

    tan theta_D = sin theta / (gamma (cos theta - v)),

Einstein's aberration exactly, under every `r_D` (the rate cancels in
the ratio), from (A1) and the pulse alone: the gamma is the ratio of
D's transverse and longitudinal radar scales (Theorem 2 (c)), not an
input. At first order in v it is Bradley's `delta theta = v sin theta`
(the Earth's 20.5 arcseconds at `v = 10^-4`, docs/NATURE.md :103), at
second order the gamma. A detector that reads the angle in lattice
Nodes instead (the pinhole's and the hit's Nodes as the host sees
them) would read the Galilean `tan theta = sin theta / (cos theta - v)`,
but that is a GAMEBOARD number, not a reading (record 281). **Order:**
rung 1 in the mean, within one Node on `y_hit`, `1 / T_D` on the
direction. **Inverse:** `tan theta = sin theta_D / (gamma (cos theta_D
+ v))`, the same map with `-v`. **Registered.** NOT READ (no moving
detector world). Pins before any run: at v = 1/2 and theta = 90
degrees (the packet transverse in the lattice's frame), `tan theta_D =
1 / (gamma x (-1/2)) = -sqrt 3`, `theta_D = 120` degrees, i.e. the
moving detector sees the transverse packet 30 degrees ahead. Verdict:
SHOWN, r-free, rung 1; NOT READ.

### II.6 The energy-momentum relation, and E_0 = m c^2

**Inside.** The identity's exact square `W = E'_0^2 + 3` **p** `.`
**p** on the record, `E'` its whole root kept by comparisons (17.6 M3;
24.1 row 38); on the law no square, the drive's wall `Q S M + abs(p)`
linear (the click frame section 5, :389-497). Under (A1) and (A2) the
walk's `cos omega = cos m cos kappa` gives `omega^2 - kappa^2 = m^2` to
second order, and the law's own Planck map (`E = hbar omega`, `p = hbar
kappa`, `E_0 = hbar m`) gives `E^2 = E_0^2 + c^2 p^2` in the hop frame
and, in the identity's whole unit `E' = E / c^2`, `E'^2 = E'_0^2 + 3`
**p** `.` **p**, the 3 being `1 / c^2` in the Beam Law's Links (the
click frame section 7, :726-830; the reviewer's record 781). Cited,
not redone.

**Transformation.** The detector G at A reads R (moving at v, at B,
transponding) by the two factors of II.1 and the round trip of II.3,
all on G's own record: r and v. Nothing else of R passes Outside but
its clicks.

**Outside.** Define on G's record the energy and the momentum of R as
`E = E_0 / r` (the click frame's inverse of its first row, `E' = E'_0
/ r`, :887) and `p = E v` (the group velocity of the walk, `v = c^2 p /
E`, the click frame :144-148 and record 781). Then

    E^2 - p^2 = E_0^2 (1 - v^2) / r^2,

so the energy-momentum relation `E^2 = E_0^2 + p^2` holds Outside if
and only if `r^2 = 1 - v^2`: it is the click frame's one line (`k_GR =
k_RG`, :265-267) in the energy's words, and the Inside identity W is
its image on the record under (A2) (section 7). Under the law (`r =
1`): `E = E_0` at every speed and `p = E_0 v`, no invariant, no energy
of motion (DERIVATIONS_BEAM 4.5 :1146: "the law has no energy of
motion"). Under the identity: exact on its integers, `E'^2 <= W <
(E' + 1)^2` at every interval (series S, 10 827 lines). **Order:** the
line rung 1; the identity's form exact by declaration; the
conversion's up to `m^2 v^2` (section 7 (d)). **Inverse:** `r = E_0 /
E`, `v = p / E`.

**What m is Outside, and whether `E_0 = m c^2` is a formula of the
conversion or a unit, said exactly.** Inside, m is the mass angle, the
staying share of the walk's coin, `m = 2 pi n_0 / (d_0 N)` radians per
interval, the family's rest pair (the click frame :769-773; record 781
(2)); Outside, the interval is never read, so m is read only as a
ratio of two rest rates, the body's rest phase rate against a
reference clock's: a mass Outside is a mass RATIO (docs/NATURE.md
:598-605, the conversion table's masses), and the one formula the
conversion gives is

    E_0 = h f_0 = hbar m:   a body's rest energy is its rest frequency times the family's quantum,

Compton's relation, from the Planck map on `main` (DERIVATIONS_BEAM 6.4,
`E = h f` from the release, reached) and (A2). That is a formula of
the conversion. `E_0 = m_i c^2` with `m_i` the inertial mass of the
drive, `m_i = Q S M` in label units (the wall the momentum is compared
with, `step_axis`; DERIVATIONS_BEAM 4.4 :1113-1115 "with `m = Q S M` as the
mass"), is a different statement: it ties the rest pair's phase rate
`h n_0 / d_0` to the drive's wall `Q S M`, and on the tree that tie is
the load-time identity `3 h n = Q S d` of the identity
covariant-readings-v1 (17.6 M7, N5; the click frame :719-722), a
declared unit checked at load and reported where a family is off it
(series S: "25 paid families off `3 h n = Q S d` reported, no
refusal", docs/EXPERIMENTS.md :6715-6716). On `main` the content M and the
phase rate are untied (DERIVATIONS_BEAM 4.5 :1146: "no operation
carries a body's speed into its content or its clock; content is
invariant"). So, exactly: `E_0 = hbar m` is SHOWN by the conversion;
`E_0 = m_i c^2` is a UNIT, the declaration that the family's quantum
and rest pair and the drive's wall measure one thing, not derived by
the conversion and not on the law; and `c^2` in it is the unit
conversion of the click frame 7 (c), the 3 of the Beam Law's Links.

**Registered.** Series S (DETECTOR, the face clicks 369 and 345; the
pointer's `z = 0.3674`) reads the identity's E' through r and v
(II.1, II.2) and MEETS its pins; the load identity is a load report,
GAMEBOARD; NATURE 4a and 4b are the law's FAIL rows. Verdict: the
relation SHOWN as the line (r-dependent), MEASURED under the identity
(MET), FAIL on the law; `E_0 = hbar m` SHOWN; `E_0 = m_i c^2` a unit,
NEITHER on the law.

### II.7 The relativistic momentum against the law's pace and the drive

**Inside.** The law's drive: `v = p / (Q S M + p)` per axis, exactly,
so `p = m_i v / (1 - v)` with `m_i = Q S M` (DERIVATIONS_BEAM 4.4
:1109-1135); form B's directional drive on its branch: `beta = u /
(E_0 + u)`, `u = abs(p)_1 T_h / Q`, the same form in the Manhattan
momentum (the click frame :424-431); the identity's pace `p / E'`
with W: `sqrt 3 p = E'_0 beta / sqrt(1 - beta^2)`, i.e. `p = gamma
m_i v` exactly on its integers (the click frame :887, the inverse
`3 p^2 = E'_0^2 beta^2 / (1 - beta^2)`). All GAMEBOARD: the drive's
integer p is on the record and no detector reads it.

**Transformation.** The line L at rest reads R's births' Nodes and
ticks: v (one-way, the lattice's) as Nodes apart over counts apart;
the momentum passes Outside only as `p = E v` with E from r (II.6) or
through what R gives up in a push or a collision, which no registered
world reads as a detector reading.

**Outside.** Compare the law's `p_law = m_i v / (1 - v)` with nature's
`p_nat = m_i v / sqrt(1 - v^2)` at the same v:

    p_law / p_nat = sqrt(1 - v^2) / (1 - v) = sqrt((1 + v) / (1 - v)) = k,

Bondi's factor exactly: the law's drive charges, for a given pace,
k times the relativistic momentum. Both are `m_i v` at leading order
(Newton, DERIVATIONS_BEAM 3.3); the law's next term is `m_i v^2`, the
relativistic `m_i v^3 / 2`, so they agree at first order in v only and
part at the second, the law's `p(v)` being the click frame's linear
wall (:424-431) and nature's the square (:483-497). The identity's
`p = gamma m_i v` agrees exactly, by the square declared in its wall
(the Minkowski norm, the click frame 5 (v) :483-497), not by
derivation. **Order:** rung 1 (the drives as declared). **Inverse:**
the law `v = p / (m_i + p)`; the identity `v = p / E'`. **Registered.**
The pace is GAMEBOARD everywhere it is quoted: series S's beta 0.3040
under the identity and 0.2674 under the law at one declared momentum
(the drive's pace; the detector reads `1 + z` alone, docs/EXPERIMENTS.md
:6715-6725; the click frame :888); D3's controls at their pace to the
tick (DETECTOR, `x = 60 + r` on every click, the birth ordinal against
the Node). What the register reads of `p(v)` is v only; p is never a
reading. Verdict: on the law FAIL at second order (a different law,
4.4's table :1117-1122: 0.500 against 0.707 at `p = m_i`); under the
identity SHOWN by declaration (the square in the wall); the momentum
itself NEITHER (no reading).

### II.8 The mass-energy of a crowd

**Inside.** A bound set's mass is its total content, read after a
detector as the escaped content of the give (DERIVATIONS_BEAM 19.1
:5739-5766; record 115, binding-v1); a row in flight carries content 0
as a source: it is read by no row and pushes nothing (5.5 (ii)
:1305-1307, "gravity does not gravitate"); a row's energy is `h f`
(6.4). GAMEBOARD until a detector clicks.

**Transformation and Outside.** A detector at A reads the crowd of a
source at B as the age moment of the rows that reach it (W1), amount
times age, and its clock is stretched by it (II.10); a detector reads
the energy of the crowd's rows as `h f` at each click. The two
readings of one crowd (its energy `h f` per row and its weight on a
clock, the age moment) are not one number: the law has no formula
that turns the rows' `h f` into a source of push or into an inertia,
and the energy of a bound set's field is not in the set's mass beyond
the content given up (19.1). Nature's `E = m c^2` for a crowd (the
binding energy as a mass defect, NATURE 7a :105, BOUND; the energy of
the field gravitating, 21.4 row E16 :6248) is therefore NEITHER on the
law, one line: the rows carry no content as a source and no operation
turns a row's energy into a body's content (4.5 :1146). Under
the identity, E15 and E16 (:6247-6248) name what would be added
(`field-source-v1`, not decided). Verdict: NEITHER.

### II.9 The equivalence principle (cited), and the accelerated detector's redshift

**Inside.** The push `-M_A` **V** and the drive dividing by `M_A`: the
fall independent of the content, exact record by record (W2; the click
frame (2)(c) :1006-1019 and its table :1063, SHOWN rung 1); the
registered reading series D3, the held mass four times, 138 of 139
common birth ticks at the same Node, `abs(dT) = 0` (DETECTOR;
docs/EXPERIMENTS.md :7285-7292). Cited, not redone: that is the weak
equivalence, the universality of the fall.

**Transformation, Einstein's half.** Einstein's equivalence is the
other half: a detector that accelerates reads the same shift as a
detector in a crowd. From Theorem 1 with no crowd: the emitter X at
the floor A and the detector Y at the ceiling B, `Y` Links above it on
the axis, both at rest at the emission and both accelerating at g
(Links per interval squared, GAMEBOARD) away from the packet's
direction; the packet takes `Y / c` intervals, in which Y gains the
velocity `g Y / c`; so `s . v_X = 0` at the emission and `s . v_Y = -g
Y / c^2` at the arrival (the ceiling recedes), and

    k_XY = 1 / (1 - g Y / c^2) = 1 + g Y / c^2 + O((g Y / c^2)^2)   (r_X = r_Y, the same rule for both):

the ceiling counts the floor's packets slow by `g Y / c^2`, the
redshift of an accelerated detector, from (A1) alone, with the
constant `1 / c^2` and no input. Rung 2 (first order in `g Y / c^2`,
the geometry taken at the emission and the arrival). **Outside.** `1 +
z = 1 + g Y / c^2`, DETECTOR (Y's count between two arrivals over X's
between two emissions, Y read by pulses). The crowd's counterpart is
II.10; whether the two are one is II.10's constant.

### II.10 The gravitational redshift and the clock's slowing

**Inside.** The age wall (W1): the rate `1 / (1 + k)`, `k = a_tau n /
d`, rung 1 exact at every k, never 0 (the click frame (2)(a) :984-991;
DERIVATIONS_BEAM 5.2 :1212-1235); about a source, `A(r) = q tau_L / (4
pi c r)` in the shell mean (5.1 :1168-1200; the click frame (2)(b)
:993-1005), rung 2.

**Transformation.** The emitter is a lamp at A in the crowd `k_A`, the
detector G at B in the crowd `k_B`, both at rest; the packet's count
ratio is Theorem 1 (iv): `k_AG = (1 + k_A) / (1 + k_B)`. The
detector's own `k_B` is read against a control lamp at B's own crowd
(series X's controls), by rule (C) never by asking the Node.

**Outside.** `1 + z = (1 + k_A) / (1 + k_B)`, DETECTOR, rung 1 within
the count's grain; at first order `z = k_A - k_B = (n / d) (A(r_A) -
A(r_B))`, the potential's form `1 / r` (the click frame's table :1059,
SHOWN rung 2; series T's 1.907 against the pin `1.909 +- 0.05`,
DETECTOR, MET; series X's `0.6285` against `0.618270`, MET;
docs/EXPERIMENTS.md :6808, :6947-6952). Cited. Nature's is `1 + z =
sqrt((1 - 2 U_B / c^2) / (1 - 2 U_A / c^2))`, `U = -G M / r`, which is
`1 + (U_B - U_A) / c^2` at first order: the same form (SHOWN) with a
constant to be compared, and at second order `1 - k + k^2` against `1
- k - k^2 / 2` (5.2 :1219-1222, a different law, NEITHER, II.13).

**The constant: a unit's fact or a mismatch, said exactly.** Between
two heights `Y` apart at the fall's acceleration g (II.9's g, the same
crowd read twice), the law's shift is `delta k = (n / d) delta A`
with, from the push, `g = (c / (S tau_L)) abs(grad A)`: the flow the
push reads is **V** `= -(Q c / tau_L) grad A` (DERIVATIONS_BEAM 5.1
:1196-1198) and the acceleration is `-` **V** `/ (Q S)` (3.3 :938-946;
the click frame (2)(c) :1006-1010, `push / (N_l N_w M_A)`), so `delta
A = g Y S tau_L / c` and

    delta k = (n S tau_L / (d c)) g Y,     against nature's   g Y / c^2   (II.9's accelerated detector has exactly this, with no input),

so the dimensionless ratio that decides is

    delta k / (g Y / c^2) = (n S / d) x (tau_L c) = n S / d   in the limit of every direction (tau_L c = 1).

(The click frame writes this constant as `n tau_L / (d N_l c)` (:1043,
its (2)(e)); the chain through its own (2)(c) and 5.1 gives `N_w` in
the numerator where it has `N_l` in the denominator; the correction is
for the click frame's writer and moves no verdict, the constant being
a declared input under either spelling.) So: the law has the FORM of
Einstein's equivalence for clocks (one field read twice: the clock by
the potential, the fall by its gradient) and its constant is the
world's `n S / d`, an input of kind 2 (K), where nature has 1 with no
input (II.9's `1 / c^2` comes out of (A1), the crowd's does not). It
is a UNIT'S FACT in this sense: one declaration, `n S = d`, makes the
law's clock in a crowd and the law's accelerated detector read the
same shift exactly in the continuum limit, and the same declaration
closes the Shapiro constant of II.11. It is a MISMATCH in this sense:
nature forces the equality and the law does not, so Einstein's
equivalence for clocks is a PIN on the inputs and not a theorem of the
six verbs. The registered clock worlds sit at `n S / d = 2^20 / 2^16 =
16` (series T: `suspension [1, 65536]`, `width 1048576`,
`examples/events/clock_word/age_3.json`; GAMEBOARD, the world's
declared inputs), sixteen times nature's constant for the same g, and
no world reads a clock's shift and a fall on one crowd (the click frame
:1065: "the one reading that would close the constant is NOT MADE").
Pin for that world, before any run: on one crowd with the fall's g read
at L and the shift read by two lamps, `delta k / (g Y)` in Links and
intervals equals `(n S / d) tau_L / c` within the count's grain and the
shell's ripple; at `n S = d` it equals `1 / c^2` and matches nature's
Pound-Rebka form (NATURE row 12 :116). **Inverse:** `k_A - k_B` from
z; `n S / d` from the ratio. Verdict: the shift SHOWN in form (rung 1
in k, rung 2 in r), MEASURED (T, X: MET); its constant a declared
input, MEASURED ONLY when read, NOT MADE.

### II.11 The bending of light by a mass, and the Shapiro delay

**Inside: does the flight feel the crowd at all?** Derived from (W3)
and (W1), rung 1, by the declared set. The one wall function of the
crowd stretches "the wall of every accumulator of a declared set"
(`core/integer.py:118-153`); the set on `main` is `AGE_WALL_SET =
(("owed", 1),)`, the body's clock alone (`events/measured.py:344`);
the row's flight is an accumulator of the linear block (the Manhattan
accumulator of `walk_step`, `Flight`) whose wall is the direction's
`T_D`, a world constant, and it is not in the set; the row's phase per
age is never in the set (`AGE_WALL_NEVER`); the row's direction is a
constant of the table. Hence a row's path from A to B is the Bresenham
line of its direction and its arrival count is `L tau_L` intervals
within `1 / T_D`, at every Node alike, whether or not a crowd lies on
the path: the flight reads nothing of the crowd, exactly, on `main`.
This is a declaration (the paper's P9, "a rule chosen among few";
main.tex:160-162), not a theorem of the six verbs: the same function
`age_wall` stretches the flight the moment the flight is declared a
member, which is the key `optical` (`age_wall_set(optical)`,
`events/measured.py:352-362`, the coefficient `c_f = 1 + gamma`), an
identity beside the law, off by default (optical-v1; DERIVATIONS_BEAM
5.4 :1251-1291). So there are two Inside predictions, one the law's
and one the key's, and the document gives both.

**Transformation.** The emitter is a lamp at A far from the mass, the
detector G at A itself (the round trip, the Shapiro reading: G sends a
pulse past the mass at the impact distance b to a transponder at C
beyond it and counts the return on its own record, W5) and a screen S
of detectors at B behind the mass (the bending: the beam's centroid on
the screen, series K's form). The controls: the same G and S with the
mass absent, or the pulse at a second impact distance. The mass at M
is a source of content `M_B` releasing on a fan of every direction
(W3, M): its crowd at the distance r from it is `A(r) = q tau_L / (4 pi
c r)` in the shell mean.

**Outside, on the law.** G's round-trip count is `2 L tau_L r_G`
intervals of its own count for a path of L Links, with or without the
mass: the delay `delta t = 0`, and the screen's centroid is the unbent
Node: the deflection `alpha = 0`. Both rung 1, exact by the declared
set. Against nature: Eddington's 1.75 arcseconds at the Sun's limb
(`4 G M / (b c^2)`; the VLBI `0.99992 +- 0.00012` of it,
docs/NATURE.md :115, :80) and the Shapiro delay `(2 G M / c^3) ln(4
r_1 r_2 / b^2)` (about 240 microseconds at the Sun's limb for a round
trip to Mars; the Cassini test of its coefficient to `2.3 x 10^-5`,
docs/NATURE.md :80): FAIL, by the whole of both effects. Registered:
series K, `examples/events/lensing/`, the deflection `0.000` pixel in y
and z at `M = 2^12` and `2^13`, `b = 6` and 3, the rows' age at the
screen 89.40 in every world, the difference 0.00 (DETECTOR, the
screen's clicks and the rows' age at them; docs/EXPERIMENTS.md
:3062-3141; DERIVATIONS_BEAM 5.4 :1253-1258). The law's Inside
prediction is 0 and 0, its Outside number is 0 and 0, and the register
reads 0 and 0: the FAIL is shown, measured and honest.

**Outside, under the key `optical` (an identity, not the law).** With
the flight a member at `c_f`, a row's wall per Link is `T_D (1 + c_f
a_tau n / d)`, so it spends `tau_L c_f (n / d) a_tau` extra intervals
per Link at a Node of crowd `a_tau`; along a straight path past the
mass at the impact distance b, from `r_1` on one side to `r_2` on the
other (`r_1, r_2 >> b`), with `A(r)` in the shell mean and `q / (4 pi)
= S G M_B` (G as 3.3 names it, `G = K eta / (4 pi S)`),

    delta t = c_f (n / d) tau_L x integral of A ds = c_f (n S / d) (tau_L^2 / c) G M_B ln(4 r_1 r_2 / b^2)
            = c_f (n S / d) (G M_B / c^3) ln(4 r_1 r_2 / b^2)   in the limit tau_L c = 1,

which is Shapiro's form, nature's `(1 + gamma_PPN) (G M / c^3) ln(4 r_1
r_2 / b^2)`, with the coefficient `c_f (n S / d)` in place of `1 +
gamma_PPN`; and the bending, by Fermat's principle on the same delay
field (the wavefront's differential delay across the beam,
`alpha = integral of the transverse gradient of the delay per Link`),

    alpha = c_f (n / d) tau_L x integral of (dA / db) ds = 2 c_f (n S / d) G M_B / (c^2 b),

nature's `2 (1 + gamma_PPN) G M / (c^2 b)`, Einstein's `4 G M / (c^2
b)` at `gamma_PPN = 1`. Both rung 2 (the shell mean, the straight-path
integral, `r_1, r_2 >> b`); the lattice's ripple at finite b MEASURED
ONLY. Two facts: the form of both is the potential's, the logarithm
and the `1 / b`, because the wall reads the age moment (the potential)
and not the flow (the meeting key's `M / b` phase, a different law, 5.4
:1268-1284); and the constant is the same pin as II.10's, `n S = d`,
times the declared `c_f`: at `n S = d` and `c_f = 2` the key's numbers
are Einstein's, and at `c_f = 1` (the time part alone) they are half,
the "1 + gamma" of NATURE row 13. Whether the key's turn table
realises Fermat's limit is the key's own design (optical-v1's reviews),
outside this document. Registered under the key: NATURE row 13 :115,
the centroid `-1.993 / -3.989` pixels at `gamma = 0 / 1`, the ratio
2.00 within the pinned 0.25; the delays `2.95 / 4.94` intervals, the
ratio 1.67 outside `2.00 +- 0.25` by 0.08 (DETECTOR): NOT COMPARED,
the ratio reads the declared `c_f` back, and the numbers are the
declared inputs' (`n S / d` and `c_f`), not nature's. The generic
entry of the bending into the law is the owner's own course with the
chief physicist (HIGHLIGHTS :388; EVERY_FAMILY.md section 6) and is
not touched here. **Inverse:** `G M_B (n S / d) c_f` from `alpha b`
or from `delta t / ln`, in the limit. Verdict: on the law FAIL (0
against 1.75 arcseconds, 0 against the delay); under the key SHOWN in
form, rung 2, its constant a declared input, NOT COMPARED.

### II.12 The perihelion precession: NEITHER or FAIL

**Inside.** The push is bilinear in the flow and the content, with no
term of order `v^2 / c^2` and none of order `(G M / (r c^2))^2`
(DERIVATIONS_BEAM 5.3 :1236-1250; the click frame's table :1066,
"NEITHER (a different law, stated)"): the field's part of Einstein's
advance (five sixths of `6 pi G M / (c^2 a (1 - e^2))`, the
nonlinearity, 21.4 row E12 :6244) has no source on `main`. That part
is NEITHER, and this document agrees. But the drive is not Newton's
either: the pace `abs(p_a) / (Q S M + abs(p_a))` per axis (W2) departs
from `p / m_i` at FIRST order in v (II.7: `p = m_i v / (1 - v)` on
each axis), and it does so with the lattice's symmetry (per axis on
`main`; the Manhattan `abs(p)_1` under form B on its branch): the
body's inertia is `dp / dv = m_i / (1 - v)^2` along each axis
separately. An orbit under the inverse square with such a drive is not
Newton's ellipse: in the continuum limit its equations are those of a
Hamiltonian `H = sum over axes of f(p_a) + U(r)` with `f'(p) = abs(p) /
(m_i + abs(p))`, `f(p) = p^2 / (2 m_i) - abs(p)^3 / (3 m_i^2) + ...`,
whose first correction `-(abs(p_x)^3 + abs(p_y)^3) / (3 m_i^2)` is not
a function of `abs(p)` alone: it has the square's symmetry, the
Runge-Lenz vector is not conserved, and the apsides of a bound orbit
at the pace beta move per revolution by an angle of order beta times
a function of the ellipse's orientation to the axes with that
symmetry. The coefficient is a closed computation by the averaging of
that term over the Newtonian ellipse and is not made here (this
order's time did not hold it); its order in beta and its symmetry are
exact statements, and they decide.

**Transformation.** The lamp on the orbiting body R, the line L at
rest (D3's form): the orbit as the births' Nodes and ticks, the
apsides from the clicks' radii, the advance per revolution as the
angle between successive apsides, DETECTOR.

**Outside.** The law: an apsidal motion of order beta per revolution,
anisotropic, where nature has `3 pi beta^2` per revolution for a
circular orbit (Mercury: beta `1.6 x 10^-4`, `5.0 x 10^-7` radians per
revolution, 43 arcseconds per century, isotropic): the law's term is of
the wrong order (about 300 times nature's at Mercury's pace) and the
wrong symmetry. Under the identity (the pace `p / E'`, the isotropic
W): the special-relativistic advance `pi beta^2` per revolution, one
sixth of Einstein's (21.4 row E12 :6244, "from the readings alone"),
SHOWN in form, FAIL in number by a factor 6; the field's five sixths
NEITHER. **The decision: FAIL, not NEITHER, on the law**, because
NEITHER is the word for a quantity the law says nothing about, and
here the law says something a detector line can read, of the wrong
order and symmetry; the field's nonlinearity alone is NEITHER.
**Registered.** Series D3's loops are not similar figures and the
periods are 19 percent above their circles (DETECTOR, read as history,
not as a precession; docs/EXPERIMENTS.md :7285-7292); series D's orbit
"no orbit closed by D's criterion" (5.3 :1246-1250, not read as a
precession). The deciding reading, the apsides of a lamp's orbit at
two orientations to the axes, NOT MADE; its pin, before any run: an
apsidal motion per revolution of order beta that changes with the
orientation and does not with the mass held.

### II.13 Gravitational waves, horizons, the field equations: NEITHER, one line each

- **Gravitational waves.** The law's field is the retarded scalar wave
  equation of the release (DERIVATIONS_BEAM 5.1 :1185-1195, reached), a
  monopole wave of the clock's field at c; nature's waves are
  transverse-traceless (a tensor) and carry energy from the source (the
  binary's decay), and the law has no tensor field, no energy carried
  by the field's own content and no self-source (5.5 (i), (ii)
  :1303-1308): NEITHER; a strain reading between two detectors would be
  II.4's radar length, which no world runs.
- **Horizons.** The clock's rate `1 / (1 + k)` is never 0 at a finite
  count (5.2 :1219-1222; the click frame :1066) and the flight on
  `main` reads nothing (II.11); under the key the flight's rate `1 / (1
  + c_f k)` is never 0 either: nothing stops a clock or a row; a
  different law stated, NEITHER.
- **The field equations.** The law has Gauss's law of the stream at
  every instant and Poisson's equation in the static limit, linear and
  additive over sources (5.5 :1293-1313, reached for the weak-field
  flux form); it has no tensor source, no self-gravitation, no metric
  for the rows (the flight blind, II.11) and no cosmological term
  (series G2's `q = -0.108` coasting, `+0.345` under the key, against
  nature's `-0.53`, NATURE row 3 :99, FAIL): Einstein's equation
  NEITHER, its weak static limit SHOWN (section 8).

## III. Certification: no Lorentz, no metric, no c^2 assumed as input

The circularity guard of the click frame's section 5 (the owner's
word, record 732: "make sure Lorentz is not already in the formula"),
applied theorem by theorem. The inputs of this document are (A1) and
the law's rules (W1) to (W5) with the arithmetic (M) and the declared
inputs (K); (A2) enters only where cited (II.1's walk r, II.6's W).

| Theorem | Inputs used | Where gamma or a square could have entered, and did not |
| --- | --- | --- |
| Theorem 1 (the factor) | (A1), the counts (W4) | the pace c is the unit, the same for every family (A1); r is a free symbol; no square |
| Theorem 2 (the radar) | (A1), (W5), Theorem 1 | the boost appears as the RESULT of two legs at one Node per interval; the dilation `r_D gamma` is left free; the `sqrt(1 - v^2)` of (c) is the Pythagorean crossing time of the transverse leg on the isotropic pace (rung 2 on the lattice's isotropy, `1 / T_D`), not Lorentz's |
| II.1 (dilation) | Theorems 1, 2; the three r cited | r is READ from two factors; `sqrt(1 - v^2)` appears only as the value under the line, never as an input; the law's `r = 1` and the identity's `E'_0 / E'` are cited as what they are |
| II.2 (Doppler) | the click frame's sections 0, 2, 4 | cited |
| II.3 (composition) | Theorems 1, 2 | r-free: Einstein's law comes out with no gamma anywhere |
| II.4 (contraction) | Theorem 2, the transponding rule | r-dependent; no contraction is assumed Inside (Nodes are Nodes) |
| II.5 (aberration) | Theorem 2 (c) | the gamma in the result is the ratio of two radar scales of one detector, computed, not assumed |
| II.6 (energy-momentum) | the click frame's section 7 (A1, A2, the Planck map); the definitions `E = E_0 / r`, `p = E v` | W is compared with, never used; `E'^2 = E'_0^2 + 3 p . p` is the RESULT under the line; `c^2` is the unit conversion of 7 (c) alone; `E_0 = m_i c^2` is named a declared unit, not derived |
| II.7 (momentum) | (W2) as declared | the square in the identity's wall is named as the declaration it is (the click frame 5 (v)) |
| II.8 (crowd's mass-energy) | (W1), (W3), 19.1 | nothing assumed; NEITHER |
| II.9 (equivalence) | (W2); Theorem 1 for the accelerated detector | the `1 / c^2` of the accelerated redshift is (A1)'s pace, no potential and no metric |
| II.10 (redshift) | (W1), 5.1, 3.3, (M) | no potential is assumed: `A(r)` is the age carried over the spreading (section 8); the constant is named an input |
| II.11 (light) | (W3), (W1), (M); under the key `c_f` | no metric: the delay is the wall's stretch summed along the path; Fermat's principle is the limit of the wavefront's differential delay, not an assumed geodesic; on the law nothing enters and the result is 0 |
| II.12 (perihelion) | (W2), 3.3 | no post-Newtonian term assumed; the first-order term is the drive's own |
| II.13 | 5.1, 5.2, 5.5 | cited |

Three statements for the guard. (1) The word gamma is written in this
document only as the value of `1 / r` under the click frame's one line
or as the computed ratio of two radar scales; it is never an input. (2)
The only squares are the identity's W (compared with, II.6, II.7),
the Pythagorean crossing time of a transverse leg (Theorem 2 (c), the
isotropic pace's), and `v^2` where it arises from two legs' product
`(1 - v)(1 + v)`. (3) `c^2` appears as the unit conversion of the
click frame 7 (c) (the 3 of the Beam Law's Links) and in nature's
formulas on the comparison side; the law's own constants are the
declared inputs (K), and where nature has `1 / c^2` (II.10, II.11) the
document says which input stands in its place.

## IV. The verdict

SHOWN: the Outside formula comes out algebraically under the named
assumptions at the rung named. MEASURED: a registered detector reading
sits on it (MET or FAIL against its pin; against nature per NATURE's
row). MEASURED ONLY: no closed form, the run rises Outside. NEITHER:
no formula and no reading. FAIL: the law's formula gives a number a
detector reads and nature's reading differs. One line per formula.

| The formula Outside | Verdict | The one line that decides | The register (kind) |
| --- | --- | --- | --- |
| the place-to-place factor `k_XY = (r_Y / r_X)(1 - s.v_X) / (1 - s.v_Y)` | SHOWN, rung 1 | Theorem 1: two legs at one Node per interval, the counts r times the ticks | NATURE 4b, series S (DETECTOR) on its axis case |
| the radar coordinates: Lorentz times the dilation `r_D gamma` | SHOWN, rung 1 | Theorem 2: the two legs of one pulse | NOT READ (no moving radar detector) |
| time dilation, r | SHOWN in r; MEASURED under the identity (MET); FAIL on the law | `r = sqrt((1 - v^2) k_GR / k_RG)`, two one-way factors, or `1 / k` transverse | 4a FAIL (pinned); S 369 / 345 MET (DETECTOR), 70 / 124 (GAMEBOARD); r NOT READ |
| the Doppler `1 + z = (1 + v) / r`; the round trip `(1 + v) / (1 - v)` | SHOWN (the round trip r-free); MEASURED (MET under the identity; FAIL on the law) | the click frame's sections 0, 2, 4 | 4b 0.2636 FAIL; S 0.3674 MET (DETECTOR); `k_GR` NOT READ |
| the transverse Doppler `1 / r` | SHOWN; FAIL on the law (1 against gamma) | Theorem 1 (iii) | NOT READ |
| the composition of velocities `w = (v_R - v) / (1 - v v_R)` | SHOWN, r-free, rung 1 | a ratio of one detector's counts; the k factors multiply | NOT READ; pins 2/5 and -1/3 |
| length contraction: `(1 - v^2) / r` and r | SHOWN in r; FAIL in form on the law (asymmetric) | Theorem 2 at equal `t_D` | NOT READ; pins 3/4, 15/16, 63/64 and 1 |
| aberration `tan theta_D = sin theta / (gamma (cos theta - v))` | SHOWN, r-free, rung 1 | the ratio of the transverse and longitudinal radar scales | NOT READ; pin 120 degrees at v = 1/2 |
| `E^2 = E_0^2 + c^2 p^2` | SHOWN as the line (r-dependent); MEASURED under the identity (MET); FAIL on the law | `E^2 - p^2 = E_0^2 (1 - v^2) / r^2` | S (DETECTOR) through r and v |
| `E_0 = hbar m` (the rest energy the rest frequency) | SHOWN (the Planck map on `main`) | `E = h f` and the mass angle | mass ratios only (NATURE :604) |
| `E_0 = m_i c^2` (the drive's mass) | a UNIT (the load identity `3 h n = Q S d`); NEITHER on the law | the content and the phase rate untied on `main` (4.5) | the load report (GAMEBOARD) |
| `p = gamma m_i v` | FAIL on the law at second order (`p_law = k p_nat`); SHOWN by declaration under the identity | the linear wall against the square | the pace GAMEBOARD; p never a reading |
| the mass-energy of a crowd | NEITHER | the rows carry no content as a source; no operation ties energy to content | none |
| the equivalence principle (the fall) | SHOWN, rung 1; MEASURED (MET) | `M_A` cancels record by record | D3 138 of 139 (DETECTOR) |
| the accelerated detector's redshift `g Y / c^2` | SHOWN, rung 2 | Theorem 1 with the ceiling receding at `g Y / c` | NOT READ |
| the gravitational redshift `(1 + k_A) / (1 + k_B)`, the `1 / r` form | SHOWN, rung 1 in k, rung 2 in r; MEASURED (MET) | the age wall; the age over the spreading | T 1.907; X 0.6285, 1.0029 (DETECTOR) |
| the clock's constant against `g Y / c^2` | SHOWN in form; the constant a declared input, `n S / d`; the reading NOT MADE | `delta k = (n S tau_L / (d c)) g Y`; equality at `n S = d` | T's world at `n S / d = 16` (GAMEBOARD, an input) |
| the bending of light, `4 G M / (c^2 b)` | FAIL on the law (0); SHOWN in form under the key, its constant an input | the flight not in the age wall's set on `main` | K 0.000 (DETECTOR); NATURE 13 NOT COMPARED under the key |
| the Shapiro delay | FAIL on the law (0); SHOWN in form under the key (`c_f (n S / d) G M ln(4 r_1 r_2 / b^2) / c^3`) | the same set; the wall's stretch summed along the path | K 89.40 in every world, 0.00 (DETECTOR) |
| the perihelion advance `6 pi G M / (c^2 a (1 - e^2))` | FAIL on the law (a first-order anisotropic term); one sixth SHOWN under the identity; the field's five sixths NEITHER | the drive parts from Newton at first order with the lattice's symmetry; the push bilinear | D3, D: loops not closed, read as history (DETECTOR); NOT MADE |
| gravitational waves | NEITHER | a scalar monopole wave, no tensor, no energy carried | none |
| horizons | NEITHER (a different law) | `1 / (1 + k)` never 0; the flight blind | none |
| the field equations | NEITHER beyond the weak static limit | no tensor source, no self-source, no metric for the rows, no cosmological term | G2's q FAIL (DETECTOR) |

**The verdict lines.**

EINSTEIN OUTSIDE FROM THE BOARD: SPECIAL RELATIVITY: PARTLY. The one
sentence: every formula of the special theory that is a ratio of one
detector's own counts (the round-trip Doppler, the composition of
velocities, aberration) comes out of (A1) and the pulse exactly and
under every rate, Lorentz's already on the law as it stands; every
formula that carries a scale (time dilation, length contraction, the
one-way Doppler, the energy-momentum relation, the momentum's form)
is one and the same unknown, the moving record's own rate r, which the
law fixes at 1 (FAIL: 4a, 4b, the transverse factor, the momentum's
second order), the identity at `E'_0 / E'` by the square declared in
its wall (MET in series S's domain), and (A2) at `sqrt(1 - v^2)` up to
`m^2 v^2`, which the law's rows do not have.

EINSTEIN OUTSIDE FROM THE BOARD: GENERAL RELATIVITY: PARTLY at first
order, NO beyond it. The one sentence: the clock in a crowd, the
equivalence of the fall and the potential's form come out of the age
wall, the push and the spreading (section 8, cited) and are measured
(T, X, D3), with the clock's constant a declared input where nature
has `1 / c^2` (closed by the one pin `n S = d`, not by a theorem);
light on the law reads nothing of a mass, so the bending and the delay
are 0 against 1.75 arcseconds and the Shapiro delay (FAIL, registered
0.000), the perihelion is a first-order lattice term against nature's
second-order isotropic one (FAIL), and waves, horizons and the field
equations have no source in a linear scalar field read by clocks and
pushes alone (NEITHER).

**The Highlights, kept.** This document keeps 281, 562, 678, 709,
745, 749, 762, 768, 772, 777 and P9 as they stand; it proposes no
change. Two facts it puts before the owner, as options and not
proposals: the pin `n S = d` (one declaration closing the clock's
equivalence and the key's Shapiro constant at once), and the
transponding lamp with a moving body detector as the one world that
reads r, the composition, the contraction and the aberration together
(II.1, II.3, II.4, II.5), each with its pin written above.

## V. Three sentences for the paper (marked as such; the paper coordinator's to take or leave)

(i) Every formula of the special theory that a detector forms from its
own counts alone, the radar Doppler, the composition of velocities and
the aberration, comes out of the one assumption that a click passes
one Node per interval, exactly and whatever the moving record's own
rate, so that the clicks are Lorentz's up to a scale; the scale is the
moving record's own rate, on which time dilation, length contraction,
the one-way Doppler and the energy-momentum relation all hang alike,
and which the law as built fixes at one, the covariant identity at
`E'_0 / E'`, and the amplitude of a click at `sqrt(1 - v^2)`.

(ii) The general theory comes out at first order from the age wall,
the push and the spreading, the clock in a crowd and the fall being
one field read twice, and is measured after a detector (series T, X,
D3); its constant is the world's suspension pair and width where
nature has `1 / c^2`, one declaration, `n S = d`, making the clock in
a crowd and the accelerated detector read one shift.

(iii) What the model does not have it reads as zero: light on the law
is neither bent nor delayed by a mass (0 against 1.75 arcseconds and
the Shapiro delay, registered 0.000), the orbit's apsides move at
first order with the lattice's symmetry and not at nature's second
order, and gravitational waves, horizons and the field equations have
no source in a linear scalar field.

## Links

[The click frame at 3268e7d5](https://github.com/Closer24/Universe24/blob/3268e7d5bff7b27d7d8adf2062f0f51a356bcbe5/docs/designs/click_frame/DERIVATION.md) (PR #769, not yet on main);
[DERIVATIONS_BEAM 4.3](../../DERIVATIONS_BEAM.md#43-a-moving-clock-the-rate-is-one-at-every-speed),
[4.4](../../DERIVATIONS_BEAM.md#44-a-bodys-speed-the-step-rules-dispersion),
[5.1](../../DERIVATIONS_BEAM.md#51-the-two-fields-of-one-stream-and-the-equation-they-obey),
[5.2](../../DERIVATIONS_BEAM.md#52-the-clock-the-gravitational-redshift),
[5.4](../../DERIVATIONS_BEAM.md#54-light-no-optical-metric-on-main-the-meetings-turn-as-a-key),
[21.4](../../DERIVATIONS_BEAM.md#214-the-einstein-map-every-result-of-the-special-and-the-general-theory-its-status-today-what-the-six-give-what-must-be-added-the-pin);
[NATURE rows 4a, 4b, 12, 13](../../NATURE.md); [the register: series S, T, X, D3, K](../../EXPERIMENTS.md);
[the clock audit](../clock_audit/AUDIT_2026-09-22.md) (tier (b) in PR #777);
[EVERY_FAMILY.md](../one_wall/EVERY_FAMILY.md) (the generic bending's steps);
[HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector); [TERMINOLOGY, the readings](../../TERMINOLOGY.md#the-readings).
