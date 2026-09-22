# Newton on the side: the one chain from the click algebra to Newton's form, and the prescription for the side (the world, the detector, the reading; never the law) so that Newton's form is read from clicks (the Newton On The Side Mathematician, 2026-09-22)

The order (the Boss, 2026-09-22, one bounded task, docs only, no code,
no run, no law change): the model owner's word of about 23:00Z on
2026-09-22, in Hebrew, the Boss's translation: "How, how, how, what
needs to be done there algebraically? Check what needs to be done there
algebraically, because algebraically you know how one reaches Lorentz,
and you know how one reaches Newton. So according to that decide what
you do there on the side to bring Newton." This file is that check
written down: the one chain from the click algebra to Newton's form
(section 1), why series D3 did not read it (section 2), the
prescription for the side (section 3), the pins before any run and the
minimal change list on the side (section 4), the three tests (section
5) and what could not be decided (section 6). Base commit
`067b247256942110af7ed5881c8d4c1263523566` (`origin/main`, "Merge pull
request #957"). Nothing in `paper/`, in the law or in a world file is
touched; no engine line is proposed; the engine is not run.

**The kinds of every number** (AGENTS.md, the measurement rule; the
diagnosis's usage): DETECTOR, a click or a record line of a detector,
the only kind pinned or compared; GAMEBOARD, the host's view of the
board (a tick, a body's own record, a body's steps, a presence, an age
moment at a Node, a shell or ring mean, the books), a diagnostic, never
pinned or compared; COMPUTATION, arithmetic on readings or the
algebra's own numbers in closed form, no run; CONVERSION, an Outside
number made from counts by a named reading (a flight count turned into
a distance by the flight table; a ratio of two counts); HOST, a cost or
a time of the machine. Every result is stated as matching a form, never
as being it; Einstein's, Lorentz's and Newton's forms appear only as the
thing compared with (record 817).

**The symbols, named once.** Q the label's scale, 64; S the width of the
push, the world key `width`; M a body's content in units; M_row a
massive row's content per row (the family key `quantum`); m_i = Q S M
the inertial mass in label units; **p** a body's momentum vector and
p_a its component on an axis; p the magnitude of a massive row's label
(the lamp key `momentum_magnitude`); E'_0 = Q S M_row a massive row's
rest energy in whole units and E'_D = isqrt(E'_0^2 + 3 p . p) its pace
wall; c the pace of a light row, 1 / sqrt 3 Links per interval in the
limit of every direction and 32 / 55 on a heading (c_h); v a pace in
Links per interval, and Outside in Nodes per count; u the inward radial
pace of a reader toward a source; k the rung of the ladder of
velocities, a whole number of counts per Node; n / d the suspension
pair (the world key `suspension`); a_tau the age moment a wall reads
(amount times age summed over the rows dwelling at a Node); k_a(b) =
(n / d) a_tau(b) the crowd's stretch of a count at the impact distance
b, read Outside as a count ratio; k_AB and k_BA the two one-way count
ratios of the click theorem (A's ordinals read in B's counts and the
reverse); r a detector's own count per tick, the one number the click
theorem leaves free; n_B a receiver B's own count; L the Links from the
mass's plane to the receiver; alpha the deflection angle; gamma_PPN the
world's input `optical` (0 by default; 1 a declaration); c_f = 1 +
gamma_PPN the flight's coefficient in the age wall's set; G Newton's
constant as the law names it, G = K eta / (4 pi S), K in that formula
the fan's count of directions (the world key `K`, the clock's pair, is
always written in a code span) and eta the release per unit of content
per direction; pi the circle's ratio; Lambda the push's grain, 1 in the
gravity column; beta the speed over the pace of a row, v / c; s the
sign of a packet's direction on an axis; **V** the label flow a push
reads and V_a its component on an axis; S_1 the Manhattan length of a
direction and T_D its period constant; h a height apart and g the
fall's acceleration in the equivalence; g_band the grain of the one
band rule, 1 for a whole-k reading; r_1 and r_2 the distances along the
path from the mass's plane to the emitter and to the receiver; tau the
age of a row; A the ring mean's constant on series D3's plane (1.4838 under the key
`flow_link`, 1.9098 without it), an n-unit being the label of one unit
of content; T a period in counts; H the ring-mean push's invariant
(DIAGNOSIS.md 2.4).

## 0. The decision, at the top

**The chain reaches Newton's form from clicks in one line: a click's
count ratio at a moving detector carries (1 + u / c) exactly (Lorentz's
k_BA, the clicks' own); Einstein's step converts that count into a
count ratio in a crowd, (1 + k_X) / (1 + k_Y); the shell mean of that
ratio is the 1 / r of the potential, and the second difference of a
mover's arrival Nodes over its own ordinals is the fall; Newton's form
is the value r = 1 of the mover's own count and the value u / c -> 0 of
the click count's term. Two things must be arranged on the side, and
nothing in the law: (i) the moving detector must be one whose push
carries no click-count term, or whose pace on the ladder makes the term
smaller than the band; (ii) the reading must be a ratio of counts on a
detector's own record, never the tick. The prescription (section 3):
the moving detector WITH MASS of records 1043 and 1046, a massive row
released at rest past a held mass and read at a receiver BODY under
`clock_stamp`, on the rung k = 19 of the ladder exactly (M_row = 21, p =
71: E'_D = 1349 = 19 x 71, the row makes one Link per 19 counts with no
remainder, u / c = 0.0912 a name for the ratio of two count ratios);
its reading Newton's advance, the arrival count 40.5 counts earlier than
the control's 979 (COMPUTATION conditional on one click reading, k_a(b)
= 6.95 x 10^-4 by the lamp at b), and the centroid 4.39 pixels toward
the mass, both the same under either count of the deciding question
(the row's push reads the arrivals at its Node); beside it, the light
row of the same world, whose lever-arm centroid -4.63 against -5.47
pixels (bracket 0.5) is the one reading that separates the click
count's term from the ring mean alone. The orbit of series D3 re-read
on the ORDINALS (the body's own count) at a slow launch on the rung k =
17 is the second side, for the ring mean's scale symmetry (the ratio of
the first turns 2.00 +- 0.20) and the term's signature on a body (the
advance per turn); it reads Newton's form on the plane, not Newton from
the chain. Whether a free row's read at a body is a click is the
owner's word, not the algebra's: under "no" (TERMINOLOGY's sense, the
Boss's recommendation) the presence count of `newton-presence-v1` is an
admissible option outside the law and is not a verdict here.**

## 1. The chain, one page: from the click count to Newton's form, each quantity a click [C] or a declaration [D] (or a computation [K] on them)

**Step 1, the click count and its ratio.** A detector D is a body with
its own count n_D [C], one accumulator advanced by one per interval and
stretched by the age wall at coefficient 1 (TERMINOLOGY, "A detector's
clock"; record 768); no Node holds a detector's time. A click is the
arrival at D of a row another detector released: the triple (the Node
[C], n_D at the arrival [C], the ordinal the row carries [C], the
emitter's own count at the release). A velocity Outside is Nodes apart
over counts apart between two clicks, a ratio of two integers [K], on
the ladder 1 / k with the quantum 1 / (k (k + 1)) (record 1050; the
click frame section 9 (III)). The moving detector's k_a(b): a lamp at
rest at the impact distance b from a held mass, its rows counted at a
rest receiver against a control lamp in the receiver's own crowd, gives
the count ratio 1 + k_a(b) [C] (series T's method), k_a(b) = (n / d)
a_tau(b) with n, d declared [D] and a_tau(b) Inside (GAMEBOARD, never an
input): the one reading every number of section 4 hangs on. A
declaration: the detectors, the lamps, the families and the pair [n, d]
of the world file [D].

**Step 2, Lorentz's factors from the count ratio (the click theorem's
statement, cited, not its proof).** The click frame section 0: the
transformations between click families that keep (A1), one Node per
interval at most, form the Lorentz group up to scale, exactly over the
rationals on the counts; the two one-way factors on the law are k_AB =
1 / (1 - v / c) and k_BA = 1 + v / c [K, ratios of counts C]; their
round trip k_AB k_BA = (1 + v / c) / (1 - v / c) is free of r and
exact within 1 / T in the mean; the one line k_AB = k_BA is r^2 = 1 -
v^2 / c^2, Lorentz's scale, the thing compared with; the law as built
has r = 1 [D, the whole-record hop]. Nothing below expands in v / c.

**Step 3, where the velocity term enters as the clicks' own.** The count
k_BA = 1 + v / c is the count of a rest stream's rows a detector meets
while moving toward it: DERIVATIONS_BEAM 2.2, exact over whole Links of
the mover's path, 183 = 128 + 55 rows in 128 intervals at the rung k =
4 (32 Links) against 128 at rest, 73 = 128 - 55 away [K from (A1) and
the flight table]; after a detector it is the Doppler, NATURE row 4b's z
= 0.2636 at beta 0.2674 [C]. So (1 + u / c) is produced by the click
algebra for every count that is a click (NEWTON_FROM_CLICKS section 2,
(i) and (ii)); it is not added by any rule. Which counts of the law are
such counts is a declaration [D]: BEAM_LAW note 48 declares that "the
threshold, the window, the click and the push read the same `met`", so
a BODY's push counts crossings and carries the term; a ROW's push and
every wall count what is present at the Node (`CrowdMoments`), a count
with no term at first order (NEWTON_FROM_CLICKS section 2 (iv)).

**Step 4, Einstein's step in the middle.** The place-to-place count ratio
(the Einstein Outside Theorem 1 as NEWTON_FROM_CLICKS 1.3 cites it):
k_XY = (r_Y / r_X) (1 - s . v_X / c) / (1 - s . v_Y / c) [K on C], with
its two corollaries: two records at rest in crowds read k_XY = (1 + k_X)
/ (1 + k_Y) [C against a control], and a detector accelerating at g
away from the packet's direction, Y Links above the emitter, reads k_XY
= 1 / (1 - g Y / c^2). The equivalence, at rest: the clock reads the
crowd (the presence class, no term) and the fall reads the crossings;
the constant between the two shifts is delta k = (n S / d) (g h / c^2),
nature's form times the declared n S / d [D], equal to nature's iff n S
= d (the click frame section 8 (e)). Einstein's step is the conversion
of the mover's own count to the rest detector's, the rate r; for a
moving reader the one field is two (NEWTON_FROM_CLICKS section 2).

**Step 5, Newton's form from the same chain.** (a) The 1 / r of the
potential: the shell mean of step 4's count ratio about a source at
rest, k_a(r) = k_a(b) b / r, READ by series T's 1.907 for 2.00 at 3 and
6 Links [C]; the mean itself is a GAMEBOARD limit and not an input. (b)
The inverse square of the fall Outside: the second difference of a
mover's arrival Nodes over its own ordinals, x(n + 1) - 2 x(n) + x(n -
1) in Nodes per own count squared [K on C], which the law's push rule
maps to the record's momentum by declaration [D], p_a(t + 1) - p_a(t) =
-M_A V_a(t) (DERIVATIONS_BEAM 3.3, Lambda = 1), and in the shell mean a
= -G M_B / r^2 with G = K eta / (4 pi S) (on the plane -G' M_B / r);
its click reading is the second difference at two distances, NOT READ.
(c) Newton's inertia in one form, **p** = m_i **u** with **u** the Nodes
apart over the mover's own counts apart, exact at every speed; Newton's,
Einstein's and the drive's forms differ only by the rate r of that count
(1, sqrt(1 - v^2 / c^2), 1 - v; NEWTON_FROM_CLICKS 1.4 (b)). (d) Kepler
on the plane: T proportional to r, the 1 / r force's scale symmetry,
T(24) / T(12) = 2 read as the recurrence of the arrival Nodes on the
ORDINALS of an orbiting lamp [C when read; NOT READ on the ordinals]. So
Newton's form is the chain's own value at r = 1 (the mover's count
against the tick) and at u / c -> 0 (the click count's term below the
band); neither is a low-velocity limit taken in the algebra, both are
values the side must arrange. The velocity term stays where the
declaration puts it: on a body's push (crossings), not on a row's push
(arrivals) and not on any wall (presence).

## 2. Why series D3 did not read it: each cause against the chain's step it breaks

Series D3 (`examples/events/orbit_lamp/`, the pins `expectations_flow.json`):
a probe of content 2^12 + 2^20 with a lamp, launched at the whole n = 8
under `flow_link` (A = 1.4838) at r = 12 and 24 on a 121 x 121 plane
about a source releasing one row per direction every 10 intervals on
the fan of 120; the width S = 32; `suspension` 0; a fixed line of 121
one-Node detector bodies at y = 20 clicking the lamp's rows; the period
the recurrence of the clicks' x across the centre column on the line's
tick; the ratio 1.677 against the pin 2.00 (DIAGNOSIS.md, the whole).

| The cause (DIAGNOSIS.md) | Its kind | The chain's step it breaks | Why |
| --- | --- | --- | --- |
| the launch pace 0.2 Links per interval, 0.34 c (u reaching 0.6 c on the loops) | COMPUTATION (the drive's closed form) | step 3 and step 5 (d): the term (1 + u / c) is 1.34 to 1.6 on the in-falls, not below the band | the pin's ring mean A / r took the term as 1 (P2, v << c); the chain says the term is the click count's, exact, and Newton's form is its value below the band, which the pace did not arrange: the loops opened by a factor of order two per turn (the map of DIAGNOSIS 2.5), the probes touched the line and left through a face |
| the count at the body a read and not a click: the probe's push counts the source's free rows by `read` (the rows go on); note 48's declaration puts the crossing count on that push | DECLARATION (note 48) | step 3: the term sits on the reader; step 1: the reader's count was never on its own record | a free row's read is not a click in TERMINOLOGY's sense (a click is a paid row's units merged by `measure`), so the body's push count is Inside, GAMEBOARD, and is not in the chain's reading set; the chain reads the fall only through a lamp's arrival Nodes over its ordinals, which D3 had (the lamp) but read on the tick |
| the GameBoard period as the reading: the recurrence of x on the line's tick | GAMEBOARD (the tick) | step 1: a velocity or a period Outside is a ratio of a detector's own counts; the tick is read by nothing | the ordinal (`record` mod 2^32, the probe's birth count) was on every click line and is DETECTOR; at `suspension` 0 its value equals the tick, so the number is the same and its kind is not; the register pinned the tick's |
| `suspension` 0 | DECLARATION | step 4 (Einstein's step): no crowd stretches any count, so k_X = 0 everywhere, no count ratio in a crowd is read, and the equivalence's constant (n S / d) is 0 | the chain passes through a count ratio in a crowd; D3 had none: its Newton bypassed Einstein's step, which is the step the owner names in the middle |
| the fixed line at y = 20 inside the loops: the contacts at the ticks 808 and 633 took the probe's whole y momentum (GAMEBOARD); the escapes at 1208 and 2452 through faces (DETECTOR, face clicks the tool did not print) | GAMEBOARD; DETECTOR | step 5 (d): the recurrence read was of loops re-made by a wall and ended at a face | the periods 588.7 and 987.3 are means of two and three spacings of loops never closed; the ratio 1.677 is not a reading of the force's exponent (DIAGNOSIS 3.1) |
| the grain's seed: the first apocentre 18.7 at r = 12 against the map's 13.8 (kicks of whole n-units, up to seven rows in one read) | GAMEBOARD (the records) | step 5 (b): the second difference over the ordinals is exact only in the mean over the accumulators' period; single turns carry the grain's band | not separable from the term on two loops of one realization each (DIAGNOSIS 4 (2)); the ratio of first turns is the robust reading, the single turns are reported |

What D3 did read from clicks and the chain keeps: the equivalence
principle, 138 of 139 common births at the same Node with the held mass
four times (DETECTOR, the births' Nodes); the place quantum, the
one-Node detectors' x (DETECTOR); the 1 / r form of the ring mean, NOT
refuted, within 5 per cent between 12 and 48 (COMPUTATION, DIAGNOSIS
2.2).

## 3. The prescription for the side, in the algebra's terms

### 3 (a) Which count is the click

Two counts are candidates for "the click" of Newton, and the algebra
sorts them.

1. **The arrival click of the moving detector with mass (records 1043
   and 1046).** A massive row of `massive-rows-v1` released by a lamp A
   at rest in a declared direction past a held mass M_B, arriving at a
   receiver B, a BODY at rest with its own count n_B: the click is the
   triple (B's Node [C], n_B at the arrival under `clock_stamp` [C], the
   row's ordinal [C], A's count at the release). This is a click in
   TERMINOLOGY's sense (a paid row's units merged into a body's record
   by `measure`), the one-way border; every number of the chain is read
   from it. The row in flight IS the moving detector (record 1043): its
   push reads the arrivals at its own Node (`CrowdMoments`, the presence
   class), a count with NO velocity term at first order under the law as
   coded, so its fall carries Newton's form without (1 + u / c) whichever
   way the deciding question goes; its wall reads the presence too. What
   it gives: Newton's advance and Newton's bending of a slow particle,
   with Einstein's light forms at v = c in the same world by value
   (NEWTON_FROM_CLICKS section 3 (c) and (d)), the constant n S / d in
   front of both.

2. **The body as a detector with mass reading the source's free rows
   (D3's probe, the orbit).** The body's push counts the free rows it
   MEETS by `read`; the rows go on. Is that read a click? The two
   options and what each gives, the owner's word (NEWTON_FROM_CLICKS
   section 2, "what the algebra cannot decide" (a)):
   - *Yes, a read is a click (an arrival, hence a crossing).* Then the
     body's push count is a click count, the term (1 + u / c) on it is
     the clicks' own by step 3, the law as built is what the click
     algebra says for a body, and Newton's velocity-free form is read
     from a body only where the term is below the band: the side must
     put the body's pace on a high rung k (3 (b)). No law change, no
     hypothesis; the loops' opening at 2 pi v / c per turn is a
     prediction of the law, read as the advance per turn (3 (c)).
   - *No, a read is not a click (TERMINOLOGY's sense: a click is a paid
     row's units merged by `measure`; a read leaves the rows going on;
     the Boss's recommendation, record 1095 (6)).* Then the body's push
     is not a click count, the click algebra is silent on which count
     the push takes, and the presence count of `newton-presence-v1`
     (the rows present at the reader's Node, each at its line's rate 2
     S_1 Q over its wall 2 T_D; DIAGNOSIS section 6; the reviewer's read
     N: generic PASS, local PASS, vector PASS subject to the declared
     form) is an admissible rule of the code under its own identity,
     outside the law, which would remove the term from a body's push at
     first order and make the orbit's ring mean A / r the law's own.
     That is a change of a rule, not of the side; it is stated here as an
     option beside the side's prescription and is not a verdict: the
     side below is written so that Newton's form is read under the law
     as it stands, under either answer.

The decision for the side: the click of Newton is candidate 1, the
arrival click of the released massive row at a receiver body; candidate
2's reading (the orbit on the ordinals) is the second side, kept
because it is the only reading of the ring mean's scale symmetry and of
the term's signature on a body, and because its change list is a
readings tool and a generator's two numbers.

### 3 (b) The pace on the ladder: which rung k, and why

The pace Outside is a ratio of counts, Nodes apart over counts apart
(step 1); u / c is a name for the ratio of two such ratios, the mover's
Links per count over the light row's 32 Links per 55 counts on the same
line (the control light world of series K: the mean age 89.40 at the
screen for 52 Links, DETECTOR, 52 / 89.40 = 32 / 55). No velocity is an
input anywhere (record 1047).

**Side A, the massive row.** The row's flight is one accumulator at the
rate 2 abs(**p**_D)_1 against the wall 2 E'_D, started at E'_D (the
half-wall start), so its Links by the age tau are m(tau) = floor((2 tau
p + E'_D) / (2 E'_D)) on a heading; it sits exactly on the rung k of the
ladder when E'_D = k p, and then m(tau) = floor((2 tau + k) / (2 k)):
one Link per k counts with no remainder, the pattern of period k exactly
(the moving detector design's "k only"). The registered massive family
(`slits_matter`: M_row = 64, p = 220, E'_D = 4113) sits at E'_D / p =
18.695, between the rungs 18 and 19, its Links at gaps 18 and 19 mixed
(the mean 972.2 counts for 52 Links). The rung chosen here: **k = 19,
with M_row = 21 and p = 71** (S = 1): E'_0 = 64 x 21 = 1344, E'_D =
isqrt(1344^2 + 3 x 71^2) = isqrt(1806336 + 15123) = isqrt(1821459) =
1349 = 19 x 71 exactly (COMPUTATION; 1349^2 = 1819801 <= 1821459 <
1350^2 = 1822500). Why 19: (i) it is the nearest whole rung to the
registered pace, so every form of NEWTON_FROM_CLICKS section 3 carries
over with u / c = (1 / 19) / (1 / sqrt 3) = 0.0912 in the limit of every
direction (0.0905 against c_h on the heading); (ii) the quantum of the
ladder at k = 19 is 1 / (19 x 20) = 1 / 380 Links per count, and the one
band rule (PREREGISTRATION_V2 section 5: abs(R_read - R) <= 2 g_band /
(ordinals apart), g_band = 1 for a whole-k reading) on a pace read over W
ordinals apart is 2 / W, so a whole rung makes the pace's reading exact
over any window and the control's arrival count exact to the count,
where a mixed pattern carries the remainder; (iii) the slow row's
condition of the straight-path forms, k_a(b) << v^2 / c^2, holds at the
same margin as the registered pace, k_a(b) / (v^2 / c^2) = 6.95 x 10^-4
/ 0.00831 = 0.084 (the 8 per cent first-order margin), with the held
mass at M_B = 2^10; (iv) the pushed row's bound: Q d M_row = 64 x 4096
x 21 = 5.5 x 10^6 per component of the whole momentum **P** under the
pair [1, 4096], under the working bound's 2^24.7 = 2.7 x 10^7 of the
price note. Other exact rungs near it, for the physicist's choice, all
COMPUTATION: k = 17 at (M_row, p) = (23, 87) (E'_D = 1479), k = 23 at
(19, 53) (E'_D = 1219), k = 29 at (19, 42) (E'_D = 1218), k = 37 at (26,
45) (E'_D = 1665, u / c = 0.0468). The turns before a face do not apply:
the row's path is straight, 52 Links in 979 counts on a 57-Link board;
a face click of the row is the control's FAIL.

**Side B, the orbit on the ordinals.** The body's pace on a heading
under the per-axis drive is v = abs(p_a) / (Q S M + abs(p_a)) Links per
self-creation, exactly 1 / k when abs(p_a) = Q S M / (k - 1), whole when
k - 1 divides Q S M (M = 2^12 + 2^20 = 1052672 in D3); the circular
balance n^2 / (S + n) = A with n = p / (Q M) = S / (k - 1) gives S = A k
(k - 1). The rung chosen here: **k = 17, S = 404, p = 4 x 404 x M**
(COMPUTATION: A k (k - 1) = 1.4838 x 272 = 403.6; at S = 404 the balance
reads A = 404 / 272 = 1.485, 0.1 per cent off, inside the 9 per cent
band; k - 1 = 16 divides Q = 64). Why 17: u / c = (1 / 17) / (32 / 55) =
0.101 on the heading, so the term's growth of the ring-mean invariant is
2 pi v / c = 0.64 per turn (DIAGNOSIS 2.4's estimate; 2.2 per turn at
D3's 0.34 c), which is the smallest pace at which the advance per turn
(3 (c)) is still readable in three turns and the largest at which the
first-turn ratio is not moved by it beyond its band; the period T_1 =
2 pi r k on the ordinals is 1282 counts at r = 12 and 2564 at r = 24
(COMPUTATION, the circle's; the records' seed adds about 19 per cent),
so a run of 4000 intervals holds three turns at r = 12 and one and a
half at r = 24; the board's face at 60 Links from the centre allows,
with the radial excursion growing by the amplitude factor sqrt(1 + 2
pi v / c) = 1.28 per turn from the records' seed (6.7 Links at r = 12,
7.8 at r = 24), about nine turns at r = 12 and seven at r = 24 before a
face (COMPUTATION, the diagnosis's estimate), so the face is not the
bound at this rung; the run's length is (HOST). For the ring mean's
Newton alone (closed loops over several turns) the rung would be k = 65
(S = 6173, k - 1 = 64 dividing Q, u / c = 0.026, the growth 0.17 per
turn, T_1(24) = 9802 counts), where the term's signature is below the
grain: stated as the alternative, not chosen, since the owner's word is
Newton out of the clicks and not a slow-orbit run (record 1044).

### 3 (c) The reading: the ratio of DETECTOR counts that is Newton's form

**Side A (the reading that brings Newton).** Two ratios of counts on
B's record, both against the control world (the same world with no
mass):

1. *Newton's advance.* The arrival count of a row, n_B at the click less
   its ordinal [C], averaged over the clicks of the window, in the mass
   world over the control's: (T_mass - T_control) / T_control. The
   chain's closed form (NEWTON_FROM_CLICKS 3 (b) and (d), rung 2 in the
   shell mean, given the one click reading k_a(b)):

       (T_mass - T_control) / T_control = k_a(b) (b / L) ln(4 r_1 r_2 / b^2) x [ c_f - (1 - v^2 / c^2) (1 + gamma_PPN v^2 / c^2) (c / v)^2 ],

   the first term the wall's delay (Shapiro's form at v = c, Einstein's
   light row) and the second the push's advance (Newton's advance of a
   slow particle in a 1 / r potential, -(G M / v^3) ln(4 r_1 r_2 / b^2),
   the thing compared with), every factor a ratio of counts: k_a(b) the
   lamp-at-b count ratio less 1 [C], b / L and ln(4 r_1 r_2 / b^2) the
   declared geometry [D], c / v the light row's count ratio over the
   massive row's on the same line [C]. The mark of Newton's form is the
   (c / v)^2: the advance of the massive row over the delay of the light
   row in the same world is (c / v)^2 (1 - v^2 / c^2) (1 + gamma_PPN
   v^2 / c^2) / c_f, 60 at k = 19 and c_f = 2 (COMPUTATION), the ratio
   that says the row fell as a slow particle and the light row did not.
2. *Newton's bending.* The centroid of the arrival Nodes on B's plane in
   the mass world less the control's [C], in pixels toward the mass:
   alpha L with alpha = 2 k_a(b) (c^2 / v^2) (1 + gamma_PPN v^2 / c^2),
   Newton's 2 G M / (b v^2) for a slow particle as the thing compared
   with, the light row's 2 (1 + gamma_PPN) k_a(b) beside it.

Which reading separates the chain (the click count's term) from the
ring mean alone: NOT these two on the massive row, whose push reads the
arrivals at its Node as coded; under the crossing count the centroid
moves by alpha (pi b / 4) (v / c), 0.07 pixel at k = 19, inside the
bracket 0.5, as NEWTON_FROM_CLICKS 3 (c) found for the registered pace
(4.25 against 4.32). The separating reading is the **light row's
lever-arm centroid in the same world with the light family in the
lamp: -4.63 pixels under the arrivals count against -5.47 under the
crossing count, the bracket 0.5 (the design's back-reaction -4.73 to
-4.81 inside it)**, NEWTON_FROM_CLICKS 3 (e); it is the reading of the
deciding question on a ROW. On a BODY the separating reading is Side
B's advance per turn.

**Side B (the ring mean's scale symmetry, and the term's signature on
a body).** On the ordinals alone (`record` mod 2^32 on every click line
of the fixed detector bodies, the lamp's birth count, the probe's own
count): the recurrence of the clicks' x across the centre column
against the ordinal, T_1(12) and T_1(24) in the probe's own counts [C];
the ratio of the first turns T_1(24) / T_1(12) = 2.00 +- 0.20 is the 1 /
r force's scale symmetry (the ring mean; the comparison Kepler's T
proportional to r on the plane); the advance per turn, T_2 / T_1 [K on
C], is the term's signature: under the ring mean alone the turns are
equal within the grain (the map's 400, 412, 394 at D3's pace), under
the click count's term on the body's push the second turn is longer
than the first and the loop leaves within a few turns (DIAGNOSIS
section 6 (b), the falsifier that holds: a loop whose turns stay equal
within the band refutes the term on the body). This reads Newton's
FORM on the plane and the term's presence; it does not pass through
Einstein's step unless the world declares `suspension` [n, d] with n >
0, under which the probe's count is stretched and the ordinal parts
from the tick (section 6 (e) names what that declaration does to the
lamp's rows).

### 3 (d) What stays GAMEBOARD and is only a diagnostic

The tick on every line; a body's momentum, drive accumulators and
steps (`step` lines); the presence and the age moment at any Node
(`CrowdMoments`, the world's `a_tau`); the shell mean and the ring mean
(A / r, k_a(r) = k_a(b) b / r as means); the books; a pushed row's push
accumulator **W** and its error accumulator **c** in the snapshot; the
`waiting` and `cancelled` lines of a massive record; the contacts; the
design's k_a(b) = 0.0445 at (2^16, b = 6) and its scaling to 2^10, a
GAMEBOARD age moment until the lamp at b reads it; the map's loops
(newton_map.py, COMPUTATION) as the comparison's side. Each may be
printed beside a pin, labelled GAMEBOARD, and none is pinned or
compared.

## 4. The pins BEFORE ANY RUN, by the algebra alone (COMPUTATION), and the exact minimal change list on the side

### 4.1 Side A, the massive row on the rung k = 19 past a held mass

The world (section 4.3 lists the keys): series K's geometry (an open
57 x 41 x 41 box; the lamp A at (2, 26, 20), b = 6 above the axis; the
held mass at (28, 20, 20), a fixed body of the free family `m` at the
amount 2^10 releasing on series E's fan of 290 at series K's release;
the receiver plane at x = 54, L = 26 = r_1 = r_2 from the mass's plane,
52 Links from A), the lamp's family a massive family (M_row = 21, p =
71) releasing one row per birth on [1, 0, 0], the pair `suspension` [1,
4096], `optical` 1 declared (c_f = 2), `clock_stamp` true, the
receivers measured events (bodies) whose table measures the massive
family; the control the same world with no mass. Every number below is
COMPUTATION; the ones marked "conditional" hang on the one click
reading k_a(b) = 6.95 x 10^-4 (the lamp at b against a control, series
T's method), taken here by the linear scaling of the gr_rows pin
world's 0.0445 at 2^16 to 2^10 and re-derived by the same forms once
read.

| The reading | The control (no mass) | The mass world | Kind | PASS | FAIL |
| --- | --- | --- | --- | --- | --- |
| the arrival count, n_B at the click less the ordinal, per click | 979 exactly (19 x 52 - 9, the half-wall start; the least age with m(tau) >= 52), every click alike; 960 with the receiver at x = 53 (L' = 51), the difference 19 exactly, the least step of record 1050 (iii) | 979 - 40.5 = 938.5 (the push's advance -41.2, the wall's delay +0.68), conditional; the ratio -0.0414 | DETECTOR (n_B under `clock_stamp`; the tick GAMEBOARD) | the control at 979 within one count of the birth's convention, every click the same; the mass world earlier by 40.5 +- 3.5 counts (the first-order margin 8 per cent) | a control off 979, or two clicks of the control differing (the rung not whole); the mass world later than the control (the wall without the push: no fall); an advance off by more than the margin |
| the pace over the window, Links apart over counts apart | 1 / 19 exactly; under the one band rule abs(v_read - 1 / 19) <= 2 / W over W ordinals | the same to first order (the push's radial part raises v by 4 per cent over the path in the mean, inside the band over a short window and outside over a long one: reported, not pinned) | DETECTOR (a ratio of counts) | inside the band | outside it in the control |
| the centroid of the arrival Nodes on the receiver plane, pixels toward the mass | 0.00 (the line's end Node) | 4.39 (alpha = 0.1687 radians at c_f = 2, gamma_PPN = 1; 4.46 under the crossing count), the bracket 0.5 | DETECTOR (the click's Node); the value conditional | 4.39 +- 0.5 | off both counts by more than the bracket; a control off its Node |
| the light row of the same world (the lamp's family the light family, everything else the same, M_B = 2^16 as the design) | the mean age 89.40 at the screen | the centroid -4.63 under the arrivals count against -5.47 under the crossing count, the bracket 0.5; the wall's delay +3.97 counts, no advance | DETECTOR; the values conditional on the read k_a(b) at 2^16 | -4.63 +- 0.5 (the law as coded) or -5.47 +- 0.5 (the crossing count on a row) | a centroid off both; an advance on the light row (a light row sped up) |
| k_a(b), the one reading the numbers hang on: a lamp at b against a control in the receiver's crowd | 1.0000 | 1 + 6.95 x 10^-4 at 2^10 (1.0445 at 2^16) | DETECTOR when read | a read k_a(b) re-derives every conditional number above by the same forms and refutes nothing | none |
| the count ratio of consecutive clicks at B | 1.0000 | 1.000 within 0.1 per cent (B in no crowd at 2^10 to that order) | DETECTOR | inside | off by more than 1 per cent |

The edge case: the click whose row was born in the interval of A's
first self-creation (the birth's convention, one count) and the click
whose row's last Link and the receiver's owed count fall in one interval
(the count's grain, one); both inside the margin; a control that reads
979 on every click but one says which convention the line carries.
What PASS means: the reading matches Newton's form for a slow particle
(the advance's (c / v)^2 and the bending's 2 G M / (b v^2)) beside
Einstein's light forms in the same world, with the constant n S / d in
front; it is not a comparison with nature's G. What FAIL means: the
law's massive row does not fall as a slow particle, or the flight's
rung is not whole, or the wall acts without the push.

### 4.2 Side B, the orbit on the ordinals at the rung k = 17

The world: series D3's plane and source (121 x 121, the source at (60,
60) releasing its fan of 120 every 10 intervals), the probe as
registered but S = 404 and p = 4 x 404 x M on the launch axis (the whole
n = 25.25 at the balance), `clock_stamp` true, the detector line as
registered but moved to y = 2 (58 Links below the source, beyond the
apocentres the estimate of 3 (b) allows within the turns the run
holds; whether a pericentre reaches it is the map's to say before the
run) or the loops read at the source's Node as the lamp worlds do; the
period read on the ordinals.

| The reading | COMPUTATION | Kind | PASS | FAIL |
| --- | --- | --- | --- | --- |
| the ratio of the first turns on the ordinals, T_1(24) / T_1(12) | 2.00 +- 0.20 (the 1 / r ring mean's scale symmetry; the map's 1.99 at D3's pace) | DETECTOR (ordinals apart) | inside | outside: the plane's force is not 1 / r at these radii, or the loops are not one loop |
| the first turns themselves | 1282 and 2564 (the circle's 2 pi r k) with the records' seed of about +19 per cent: REPORTED, not pinned | DETECTOR | | |
| the advance per turn, T_2 / T_1 at r = 12 | above 1 by the term (its size only through the map at this rung; the map to be printed before the run); the falsifier: turns equal within the band refute the term on the body | DETECTOR | the second turn longer; or equal turns, which refutes the term | neither decides the term's size |
| the controls (no source) | the probe leaves through the face +y at the 61st Link at the pace 1 / 17, the count 1037 +- 6 on its own count | DETECTOR (a face click) | inside | a control that moves |
| the least step | the probe's Node changes by one per 17 counts, read through the ordinals at the line: at most one Node per count | DETECTOR | | two Nodes in one count |

### 4.3 The exact minimal change list on the side (no engine line)

Side A, one generator and one readings tool, no world file touched by
this task (the physicist writes them on the owner's word):

- The world file keys (a new pair of worlds beside
  `examples/events/lensing/`, written by a generator as series K's
  `make_worlds.py` writes its four): `massive_rows: true`; `age_bound`
  at least 2048; `action` 1024 (required with `massive_rows`); `width`
  1; `suspension` [1, 4096]; `optical` 1 (declared, not a default);
  `flow_link` stated either way (false here, as series K); `clock_stamp:
  true`; `N` 64; `boundary` open; `shape` [57, 41, 41]; the family
  `matter` {`quantum` 21, `massive` true, a phase circle, no
  `phase_per_link`} and the family `m` {`quantum` 0, no phase, `charge`
  0}; the receiver family `wall` (a paid family of one unit as D3's
  line uses). The lamp A: a measured event of `matter` at (2, 26, 20),
  fixed, its content equal to the world's `K` (the clock's pair, so that
  the turn is exactly 1 at the birth), `lamp`
  {`rate` [1, 1], `wheel` [2531, 4096], `directions` [[1, 0, 0]],
  `momentum_magnitude` 71}, `table` {`m`: `pass`}. The held mass: a
  measured event of `m` at (28, 20, 20), fixed, `amount` 1024, series
  E's fan under `directions`, the world's `release` as series K's. The
  receivers: 1681 measured events of `wall` on the plane x = 54, fixed,
  `table` {`matter`: {`rule`: `measure`, `reads`: `age`}, `m`: `pass`}
  (a detector set without a body has no count, record 768, so the
  screen's pixels are bodies here and not series K's `wave` sets). The
  control: the same file without the held mass. The light-row world:
  the same file with the lamp's family the light family of series K
  (no `massive`, no `momentum_magnitude`) and the mass at 2^16 as the
  gr_rows pin world, for the lever-arm pin.
- The detector: the receiver bodies' `click` lines (`node`, `measured`,
  `record`, `clock` under the key, `age`, `push`); the `gather` line
  for the placed quantum.
- The readings tool: `tools/lensing_readings.py` extended (or one
  beside it) to read, per click, `clock` less `record` mod 2^32 (the
  arrival count), its mean and spread over the window, the pace L over
  that count, the centroid of the click Nodes in y and z less the
  control's, the count ratio of consecutive clicks at one receiver; the
  tick printed beside as GAMEBOARD; nothing of the engine.
- The register: `expectations.json` with the pins of 4.1 and their
  `derivation` fields (this file's sections), written before the run.

Side B, two numbers in a generator and one branch of a readings tool:

- `examples/events/orbit_lamp/make_worlds.py`: S = 404 and the launch
  momentum p = 4 x 404 x M for a new pair of worlds (`r12_k17`,
  `r24_k17`) under the key or not as the owner chooses, `clock_stamp:
  true`, the detector line at y = 2; the registered worlds untouched.
- `tools/orbit_lamp_readings.py`: the period's recurrence read on
  `record` mod 2^32 (the ordinal) in place of the tick, the tick printed
  beside as GAMEBOARD; and the escape of a source world printed (the
  defect of DIAGNOSIS 3.1, lines 481 to 490 print it for controls only).
- The register: the pins of 4.2 before the run.

Neither side adds an engine line, a key, a verb or a rule.

## 5. The three tests for anything proposed here that is a rule

Nothing proposed in section 3 or 4 is a rule of the law: the world keys
are declarations, the receiver bodies and the rung are values of
declared integers, the readings tool is Outside arithmetic on clicks
(HOST), and the re-read on the ordinals changes a number's kind, not a
number. The three verdicts are still stated, one line each, for the
side as arranged:

- Generic: no family name and no kind is read anywhere; the massive
  row's flight, wall and push are the one primitive per family by value
  (the triple (2 abs(**p**_D)_1, 2 E'_D, E'_D) and the weight formed at
  load); the receivers are bodies with a table as any. PASS.
- Vector: no verb is touched; the rung k = 19 is a value at which verb 6
  (the Euclidean division) leaves no remainder on the flight, and the
  ratios are formed Outside. PASS.
- Local: the receivers read the arrivals at their own Node and their
  own count; the lamp releases from its own Node; the tick is read by
  nothing above the board. PASS.

The one item that would be a rule is the option of 3 (a), the presence
count on a body's push under `newton-presence-v1`: it is a hypothesis
under its own identity, outside the law, with the reviewer's three
verdicts as cited (generic PASS, local PASS, vector PASS subject to the
declared form, the common wall as per-direction accumulators or a
declared rounding at load); it enters nothing by this file and is
named as the option the owner's "no" would open.

## 6. What could not be decided, one line each

- Whether a free row's read at a body is a click: the owner's word; the
  algebra fixes the count of every click and note 48's declaration
  puts the crossing count on the push.
- The exact factor of the crossing count off the axis on the lattice:
  exact on the axis over whole Links; no click has read it off the axis.
- Which count the ROW should carry (the arrivals at its Node as coded,
  or the crossings): separable only by the light row's lever-arm pin, a
  run on the owner's word.
- k_a(b) at M_B = 2^10: a linear scaling of the gr_rows world's
  GAMEBOARD age moment; every conditional number of section 4 waits on
  the lamp at b.
- Side B under `suspension` [n, d] with n > 0: the lamp's paid rows are
  then pushed by the source's crowd (the generic entry) and their
  arrival x on the line shifts; whether the centre-column recurrence on
  the ordinals is moved by that shift is a walk of the fan not done here.
- The advance per turn at the rung k = 17: its size needs the map
  (newton_map.py) run at that pace, a COMPUTATION not made here; only
  its sign and its falsifier are pinned.
- The massive row's completion under a fan of directions (several rows
  per record, the ladder's choice at the end): avoided here by one
  direction per birth; a fan world needs the ladder's pin.
- The HOST cost of 1681 receiver bodies with tables on the plane, and
  of the pair [1, 4096] with the mass's crowd on the row's line under
  the working bound at the declared p, M_row and d (the price note's
  line (i)): the physicist's check before any run.
- The value of G and the condition n S = d: declarations; the side
  carries n S / d = 1 / 4096 in front of every form.

## 7. Links

- [NEWTON_FROM_CLICKS.md](NEWTON_FROM_CLICKS.md): sections 1 to 3, 5
  and 6 (the chain, the deciding question, the massive row's forms and
  pins, the audit).
- [MASSIVE_RELEASE_INVENTORY.md](MASSIVE_RELEASE_INVENTORY.md): the
  inventory and the shortest list of declarations.
- [DIAGNOSIS.md](../newton_diagnosis/DIAGNOSIS.md): sections 0, 2, 3, 4
  and 6 (why D3 fell; the map; the cart's pins; `newton-presence-v1`).
- [The click frame](../click_frame/DERIVATION.md): sections 0, 4, 8 and
  9 (the click theorem, the missing direction, Newton Outside PARTLY,
  the conversion and the ladder of record 1050).
- [The moving detector](../moving_detector/DESIGN.md) and
  [PREREGISTRATION_V2.md](../moving_detector/PREREGISTRATION_V2.md): the
  k worlds, the radar coordinate, the one band rule.
- [The flow weight algebra](../flow_weight/ALGEBRA.md) section 5;
  [DERIVATIONS_BEAM](../../DERIVATIONS_BEAM.md) 2.2, 3.3, 4.3 and 4.4;
  [BEAM_LAW](../../BEAM_LAW.md) notes 17 and 48; [the gr_rows
  design](../gr_rows/DESIGN.md) section 4 (the pin world's k_a(b)).
- [The log](../../LOG_2026-09-20.md): records 1043, 1044, 1046, 1047,
  1050 and 1053 on `main`; records 1094 and 1095 on the branch
  `claude/universe24-new-3ytqde` (read there, not on `main` at the base
  commit).
- The registered worlds cited for their keys: `examples/events/massive_rows/slits_matter.json`,
  `examples/events/lensing/mass.json`, `examples/events/moving_detector/cart_k17.json`,
  `examples/events/orbit_lamp/` (none touched).
