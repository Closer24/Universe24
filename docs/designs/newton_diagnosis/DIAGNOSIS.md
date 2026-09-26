# Why Newton's rows fell: the diagnosis of series D3's ratio 1.677 (the one constant) and 1.512 (the line drive) against the pin 2.00 (the Newton Diagnostician, 2026-09-22; docs only, no law change, no new hypothesis built)

The order (the Boss, 2026-09-22, on the model owner's word of record 1014
of [the log](../../LOG_2026-09-20.md), "understand why Newton fell"):
about ninety minutes, docs only, no law change, nothing built; the
frame added on the owner's word of record 1016 ("Newton comes from the
algebra, but one has to see it in a detector moving on Nodes. That is the
test"): section 3.4 names the detector behind every Newton row, and the
one proposal of section 6 is the moving-detector test of Newton on the
cart of PR #834. Base `044b13d0` (origin/main at the first commit; main
merged in after; the branch `newton-diagnosis`). The sources: [the flow weight design](../flow_weight/DESIGN.md)
and [its algebra](../flow_weight/ALGEBRA.md) (section 5, Newton's rows by
formula), [the click frame's section 8](../click_frame/DERIVATION.md)
(Newton Outside, PARTLY), [DERIVATIONS_BEAM 3.3](../../DERIVATIONS_BEAM.md)
(Newton's law and G's place), [the line drive's default](../drive_b/DEFAULT.md),
the register of series D3 (the README (`examples/events/orbit_lamp/README.md`, deleted 2026-09-26),
the pins (`examples/events/orbit_lamp/expectations_flow.json`, deleted 2026-09-26),
the readings (`examples/events/orbit_lamp/run_flow.out`, deleted 2026-09-26)), the
same README on the branch `drive-default` (PR #907, the line drive's
re-run), the engine (nature_beam.py (`src/event_universe/events/nature_beam.py`, deleted 2026-09-26):
`push_form`, `CrowdMoments`, `optical_turn`, the flight's `walk_step`;
engine.py (`src/event_universe/events/engine.py`, deleted 2026-09-26): `step_axis`,
`_move`; [world.py](../../../src/event_universe/events/world.py):
`step_divisor`, `bresenham_line`; BEAM_LAW notes 17 and 48), and the two
flow worlds replayed once on the engine at head (section 3).

Every number below is labelled by kind (the physics-rule reviewer's kinds
of 2026-09-22): DETECTOR (a click or a record line), GAMEBOARD (the host's
view of the board, a diagnostic, never pinned or compared with nature),
COMPUTATION (arithmetic on readings, or the algebra's own numbers),
CONVERSION (a click turned into a length by the flight table), HOST (the
run's record of itself). Newton's and Kepler's forms appear only as the
things compared with. Nothing here is compared with nature; every
"matches" is a match of a reading with a formula of the law.

## 0. The verdict, at the top

**Newton's rows fell because the pinned reading, a closed orbit's period
T = 2 pi r (S + n) / n with T proportional to r, is the law's ring-mean
algebra in the limit of a slow body, and at the width S = 32 the body is
not slow: its launch pace 0.2 Links per interval is 0.34 of the rows'
pace c = 64 / 110, and the push the law runs counts the rows a body
MEETS, once each at the crossing of the world lines (the crossing rule),
so a body falling toward the source meets the outgoing shells at the
rate (1 + u / c) times a resting body's, u its inward speed, and the
push is A (1 + u / c) / r, not A / r. That velocity term raises the
ring-mean push's invariant at every phase of the motion, in and out
alike, the circular orbit is unstable, and every radial excursion grows by a factor
of order two per turn (the map of section 2: the apocentres 12.0, 13.8,
15.6, 21.3, 51.4 Links from the whole-8 launch alone; 24.0, 27.5, 31.2,
42.2, 99.3 at r = 24). The records (section 3) show that growth on the
board and two things the register does not say: the probe of `r12_flow`
touched the detector line at the tick 808 (the wall's entry took its
whole y momentum, 7.75 n-units, GAMEBOARD) and LEFT THE BOARD through
the face +y at the tick 1208 (a face click of the probe, DETECTOR);
the probe of `r24_flow` touched the line at 633 (3.00 n-units taken) and
left through the face -x at 2452. The register's "none in 4000
intervals" for both escapes is not what the record holds (the readings
tool prints a source world's escape nowhere; section 3.1). So the two
periods 588.7 and 987.3 are the mean of two and three spacings of loops
that opened from the first quarter turn, were re-made by the line's
contact and ended at a face; their ratio 1.677 is not a reading of the
force's exponent, and neither is the line drive's 1.512 (the same
anatomy: the contacts at 917 and 1400, the escapes at 2096 and 1949,
registered on the branch). What stays undecided: how much of the loops'
opening in the first quarter turn is the grain's shot noise (the kicks
of about one n-unit, up to seven rows in one interval) and how much the
whole-8 launch, since both are present and the records do not separate
them; and whether the arrival rate's factor is exactly (1 + u / c) on
the lattice, read here as consistent at r = 12 (the rate 1.28, 1.66,
2.76 at u / c = -0.4, 0, +0.4) and within the noise at r = 24. The 1 / r
form of the ring mean itself is NOT refuted by these rows: the lattice's
ring mean falls as 1 / r within 5 per cent between 12 and 48
(COMPUTATION, section 2.2), and the periods scale with the loops' own
mean radii (T over the mean radius 24.2 and 26.3, the register's own
line).**

## 1. The question, and the pins as the generator derived them

Series D3 (Newton after a detector) launches a lamp-carrying probe of
content M_total = 2^12 + 2^20 (the reservoir R = 2^12 and the held mass
M_held = 2^20 of the free family `m`) at (60 + r, 60) on a plane of 121
x 121 Nodes about a fixed source at (60, 60) that releases one ray per
direction every 10 intervals on the fan of 120 primitive in-plane
directions (a, b, 0) with a^2 + b^2 <= 64, the flux q = 12 units per
interval. The probe's tangential momentum is **p** = n Q M_total label
units with n the momentum per unit of content in units of the label
scale Q = 64 ("n-units" below: one n-unit is the label of one unit of
content, 64 label units, and a body's momentum in n-units is n =
|**p**| / (Q M_total)). The detector line at y = 20 clicks the lamp's
rows with their age; the period T is the recurrence of the clicks' x
across the centre column (DETECTOR), the ratio T(24) / T(12) a
COMPUTATION on two such periods.

**The pins, and how the generator derived them** (`make_worlds.py`,
`expectations(flow=True)`): the ring mean of the push on a body of
content M at radius r is, per interval, A Q M / r label units with A = q
L C / (2 pi) = 1.9098 as built (L = 1.0000 the fan's mean |**u**_D| / Q,
C = 1.00 series C's flow constant) and A / F_plane = 1.4838 under the
key `flow_link` (F_plane = 1.2871 the plane fan's mean of S_1 / |**D**|,
the Nodes per Euclidean Link of a digital line, which the key removes
from every push); the per-axis drive's pace is v = n / (S + n) Links per
interval on a heading (BEAM_LAW note 17); the circular balance n v = A
gives n^2 / (S + n) = A, the real root n = 8.83 as built (the whole 9)
and 7.672 under the key (the whole 8); the period is the circle's, T = 2
pi r / v = 2 pi r (S + n) / n = 376.99 at r = 12 and 753.98 at r = 24
at the whole 8 (the design's 384 / 768 at 7.818, the same formula on the
whole 9's balance; both round to 8), the band 9 per cent (the continuum
map's own margin, DERIVATIONS_BEAM 12b.2); the ratio T(24) / T(12) =
2.00 +- 0.18, "unchanged: the same fan at both radii and the weight of a
line a constant of the line, not of r". This is the algebra of
DERIVATIONS_BEAM 3.3 and the click frame's section 8 (2)(c) and (d): the
1 / r force on the plane (a flat rotation curve, v the same at every r,
T proportional to r), rung 2 (the shell mean) and `v << c`.

The three assumptions in it, named: (P1) the push is the ring mean A /
r, a function of the place alone; (P2) the body is slow, `v << c`, so
the flight's pace c enters nowhere; (P3) the loop the probe makes is a
circle or a near-circle, so its recurrence is the circle's period and
the 1 / r force's scale symmetry (r to lambda r, t to lambda t at the
same speed) makes the two loops similar figures with the ratio 2. The
diagnosis below finds P1 and P2 false at S = 32 by the law's own
algebra, and P3 false on the record.

## 2. The algebra first: the push as the code runs it, and what it gives

### 2.1 The push, integer by integer

Per interval, after the body's step, the body reads at its Node the
rows of the free family that it met this interval (`nature_beam`, step
4; the crossing rule, BEAM_LAW note 48, C1 to C3''): a row and a body
meet ONCE, at the crossing of their world lines (the swap, the entered
row moving against the body, the arrival at the body's Node, and never a
row that came over the body's own Link behind it). For that group the
gravity column of `push_form` adds to the body's momentum, per axis,

    push = - M_A x V,     V = sum over the rows met of (amount x f_D),

M_A the reader's gravity charge (its held content M_held = 2^20 here;
the reservoir does not push, DEFAULT.md (e)), **f**_D the flow label of
the row's direction under the key (the integer vector nearest Q **D** /
S_1, `direction_flight`; **u**_D, the vector nearest Q **D** / |**D**|,
without it): exact integers, Lambda = 1, no remainder. One row of the
heading (1, 0, 0) carries **f** = (64, 0, 0) and moves the body by one
n-unit toward the source (M_held / M_total = 0.996 of one); a row of
(7, 1, 0) carries (56, 8, 0), 0.884 n-units; the fan's mean kick per row
is 0.783 n-units under the key (1.000 as built), between 0.707 and 1
(COMPUTATION, the engine's own table read by `direction_flight`).

The step (`_move`, `step_axis`, `by_drive`): per axis the drive
accumulator gains p_a per self-creation against the divisor D_a = Q S M
+ |p_a| (`step_divisor`; M the content, here M_total) and fires one Link
when it holds D_a, the remainder kept; at a constant momentum one Link
per D_a / |p_a| intervals, the pace v_a = n_a / (S + n_a) per axis with
n_a = p_a / (Q M). No root, no float, no ladder enters the body's
motion: `square_ladder` is the wall of a PUSHED ROW's momentum
(`momentum_pair`), never a body's; the dwell T_D / (S_1 Q) is the
flight's, read by the clock's age moment and the wall, and the push
reads arrivals, not presence, so the dwell integer's floor enters no
push (DESIGN.md 1.1). Under the line drive (the branch `drive-default`)
the three accumulators gain p_a Q against the one wall Q^2 S M + |**p**|_1
T_h (T_h = 110), the pace 64 n_a / (64 S + 110 |**n**|_1); the push is the
same.

The rows (`Flight.walk_step`): a row of direction **D** makes the S_1
unit steps of one period of its digital line (`bresenham_line`), one
Manhattan step per interval when its accumulator holds 2 T_D, so it
advances |**D**| Euclidean Links in T_D / Q intervals: the pace c_D = Q
|**D**| / T_D, 64 / 110 = 0.582 Links per interval on a heading and
within the isqrt's grain of it on every line. The source releases one
row per direction every 10 intervals (the release [1, 2^32 x 10] on the
content 2^32, `by_clock`): the rows go out in shells, one every 10
intervals, each shell one row per line.

### 2.2 The ring mean, and the closed form of the circle with the grain

Over a ring of unit thickness at r the fan's 120 digital lines cross the
ring's N(r) Nodes at S_1 / |**D**| Nodes each, so summed over the ring
one shell delivers 120 x F_plane x 0.783 = 121 n-units of inward impulse
under the key, and per ring Node per interval the mean push is 121 / (10
N(r)) with N(r) -> 2 pi r: A / r with A = 1.4838 n-units x Links per
interval, the generator's balance. On the lattice itself (COMPUTATION,
the 120 lines walked by `bresenham_line` through the rings |sqrt(x^2 +
y^2) - r| <= 1 / 2, the kicks by the engine's flow labels):

| r | Nodes on the ring (2 pi r) | Nodes on no line | impulse per shell over the ring, n-units | per ring Node, times r |
| --- | --- | --- | --- | --- |
| 12 | 68 (75.4) | 8 | 112.35 | 19.83 |
| 24 | 144 (150.8) | 24 | 124.76 | 20.79 |
| 36 | 228 (226.2) | 80 | 121.37 | 19.16 |
| 48 | 304 (301.6) | 140 | 132.49 | 20.92 |

The ring mean falls as 1 / r within 5 per cent from 12 to 48 (the
per-Node impulse times r 19.2 to 20.9; the continuum's 121 / (2 pi) =
19.3); between 12 and 24 the lattice's push is 4.6 per cent shallower
than 1 / r, which moves a circle's period ratio from 2.00 by about 2 per
cent, not 16. So P1's form, as far as the RING MEAN goes, is what the
lattice gives at these radii. What the ring mean hides is stated in 2.3
and 2.5.

**The circle's period in integers at r = 12 and 24.** With the ring-mean
push A / r and the per-axis drive, the closed form is the generator's,
T = 2 pi r (S + n) / n: 376.99 and 753.98 at n = 8. The per-axis drive
is anisotropic (the Euclidean pace at 45 degrees is sqrt 2 x (n / sqrt
2) / (S + n / sqrt 2), 6.9 per cent above the heading's at n = 8, the
register's own line), so the "circle" is a rounded square whose period
the closed form does not give; the map of 2.5, the law's continuum
algebra with the per-axis drive and no other term, integrated in the
engine's order (the step by the momentum after the interval before,
then the push at the new place) gives T = 402.8 at r = 12 and 807.6 at
r = 24 from the whole-8 launch (r from 11.6 to 13.5 and from 23.4 to
27.0, the loops similar figures), the ratio 2.005: the anisotropy and
the whole-n grain together move each period by 7 per cent and the
ratio by half a per cent. **DECIDED by the algebra: neither the drive's
step nor the whole-n launch nor the lattice's ring mean can move the
ratio from 2.00 to 1.68; the 1 / r force's scale symmetry holds for
all three (the same n at both radii, the push a function of r alone,
the map's loops similar).**

### 2.3 The velocity term: the crossing rule makes the push (1 + u / c) A / r

The shells go out at c, one every 10 intervals, spaced 10 c Links
apart along every line. A body at rest at r meets one shell per 10
intervals. A body moving toward the source at the inward radial speed u
meets them at the rate (c + u) / (10 c) per interval, since the crossing
rule counts each row once at the crossing of the world lines and the
crossings of a body with the outgoing shells are the Doppler count: the
k-th shell is at c (t - 10 k) and the body at r(t), so the shells
crossed by the time t number (t - r(t) / c) / 10, whose rate is (1 - dr /
dt / c) / 10 = (1 + u / c) / 10. Each crossing delivers the lines'
impulse through the body's Node, in the ring mean 121 / N(r) n-units
inward. So the push the law runs, in the ring mean, is

    d n_r / dt = - (A / r) (1 + u / c),    u = - dr / dt,

a velocity-dependent force, and NOT the place function A / r of P1. In
the limit `v << c` (P2) the factor is 1 and the pins' algebra returns;
at S = 32 the launch pace is 0.2 = 0.344 c, and on the loops the records
show u reaches 0.6 c (section 3.2). This term is not a lattice effect
and not a grain: it is the continuum limit of the law's rule that a body
reads what it meets per interval (record 158, the crossing rule, built
because before it "a reader read k rows per k intervals toward and away
alike"). Every derivation of Newton's rows (3.3, the click frame's (c)
and (d), ALGEBRA.md section 5) took the ring mean at rest and stated
`v << c`; none carried the factor.

### 2.4 What the term does: the circular orbit is unstable at this v / c

Write H for the invariant of the ring-mean push under the per-axis
drive, H = sum over the axes of (|n_a| - S ln(1 + |n_a| / S)) + A ln r
(its derivative along the drive's pace is v_a = n_a / (S + n_a) per axis,
so d H / dt = 0 when the push is A / r and nothing else; A ln r is the
plane's logarithmic potential). Under the push with the factor, d H / dt
= (A / r)(u / c) u = (A / r) u^2 / c, non-negative at EVERY phase (the
physics-rule reviewer's read N, folded): under the ring-mean push with
the factor H rises monotonically, on the out-goings too, since the
conservative part of the force is already in A ln r and what the factor
adds is (A / r)(u / c) along the motion whichever way the body moves; so
Delta H per cycle = the integral of (A / r)(u^2 / c) dt > 0. The records'
falls of H on the out-goings (-0.59 at r = 12; -0.30 and -0.65 at r =
24, section 3.2) are not the algebra's but the grain's and the drive's
torque. For
a small radial oscillation about a circle at the pace v_c this is of the
order of Delta H / H_radial = 2 pi v_c / c per turn (a first-order
estimate), 2.2 at v_c / c = 0.344: the radial excursion grows by a factor
of order two per turn. The circle is
linearly unstable; no loop closes; the "period" of any loop is the
recurrence of a figure that changes every turn. This is the sign
opposite to the drag a repulsive stream gives (the Poynting-Robertson
sign): the stream here is attractive, so meeting more of it while
falling in feeds the fall.

### 2.5 The map: the law's continuum algebra integrated, no lattice (COMPUTATION)

newton_map.py (`docs/designs/newton_diagnosis/newton_map.py`, deleted 2026-09-26) integrates the ring-mean push with the
per-axis (or line) drive, with and without the factor, in the engine's
order, one interval per step, from the register's launch, and reads the
period as the tool reads it (the mean spacing of the centre column's
crossings in one direction over 4000 intervals). Its output is
[newton_map.out](newton_map.out).

| The case | r = 12: the apocentres in order (Links) | r = 24: the apocentres | the tool's T(12), T(24), the ratio |
| --- | --- | --- | --- |
| A / r alone, n = 8 (the pins' algebra with the anisotropy and the whole 8) | 12.0, 13.3, 13.4, 13.4, 13.5 ... (stable) | 24.0, 26.6, 26.7, 26.8, 26.9 ... | 402.8, 807.6, **2.005** |
| A / r with (1 + u / c), n = 8 | 12.0, 13.8, 15.6, 21.3, 51.4, then 969 | 24.0, 27.5, 31.2, 42.2, 99.3, then 308 | 556, 1100, 1.98 (loops leaving the plane) |
| the same launched exactly at the balance 7.672 | 12.0, 12.5, 12.4, 11.8, 13.0, 14.1, 17.4, 30.0 | 24.0, 24.9, 24.9, 23.5, 25.7, 27.9, 34.1, 56.6 | 425, 836, 1.97 |
| as built, A = 1.9098, n = 9, with the factor | 12.0, 13.1, 13.1, 14.6, 19.3, 45.2 | 24.0, 26.2, 26.1, 22.8, 29.0, 38.2, 87.0 | 464, 918, 1.98 |
| the line drive, A = 1.9098, n = 10, with the factor | 12.1, 12.4, 13.2, 15.1, 21.4, 58.8 | 24.1, 24.8, 26.3, 30.2, 41.9, 100.0 | 498, 835, 1.68 |

The pericentres fall as the apocentres rise (12.0, 11.2, 9.7, 7.4, 2.7
at r = 12 under the key). Read: (i) without the factor the loops are the
pins' loops, similar figures with the ratio 2.00 within half a per cent
and the periods 7 per cent above the closed form; (ii) with the factor
every loop opens, the growth per radial cycle rising from 1.2 to 3.8 as
the eccentricity grows, from the whole-8 seed alone, and even from the
exact balance (where the per-axis anisotropy alone seeds it); (iii) the
map's loops leave an infinite plane within four turns at r = 12 and
within five at r = 24; on the board they meet a face or the detector
line first, which is what the records show. The map's own ratios (1.98,
1.97, 1.68) are ratios of two opening loops read over a fixed 4000
intervals, r = 12's further along its growth than r = 24's (twice the
turns in the same time); they are not periods of anything and are not
compared with the register's 1.677 and 1.512 as predictions, only as the
same kind of number.

## 3. The records, by kind

### 3.1 The one short run: the two registered flow worlds replayed (HOST)

`examples/events/orbit_lamp/r12_flow.json` and `r24_flow.json` as
committed (PR #879, merged at `7682c57d`), run once on the engine at
`044b13d0` (`tools/run_series.py --jobs 2`, Python 3.14.0rc2, numpy
2.5.3, headless; 40.5 and 42.6 s on this host), 4000 intervals each,
completed and conserved at every tick. The digests (state, audit,
events) `0ea77ef65795`, `f7f1665f5440`, `68b713ddfd7b` (`r12_flow`) and
`5e8c8a49508f`, `40b90c718659`, `7821c7a1a39f` (`r24_flow`): **equal
byte for byte to the registered run's** (run_flow.out, record 966). No
world changed, nothing pinned, the run made to read the record's
`step`, `read`, `contact` and face `click` lines, which the register
did not keep (the 24-hour retention). The reader is
newton_records.py (`docs/designs/newton_diagnosis/newton_records.py`, deleted 2026-09-26), its output
[newton_records.out](newton_records.out).

**The escapes, DETECTOR (a face click of the probe, `measured` its
number).** `r12_flow`: `face:+y` at the tick 1208 from the Node (97,
120), the momentum (409391096, 1674431176, 0). `r24_flow`: `face:-x` at
the tick 2452 from (0, 96), the momentum (-57917368, -270319908, 0).
The register (run_flow.out, the README's table, record 966, the paper's
row 14 on PR #802: "stays on the plane for 4000 intervals at r = 12 and
24 (DETECTOR: no escape)") says "none in 4000 intervals" for both. The
record says otherwise. The cause in the tool: `orbit_lamp_readings.py`
reads the face click (line 329) but prints the escape only in the
controls' branch of `report` (lines 481 to 490); a source world's escape
is read and never printed, and the README's column was filled from the
absence of a line. The registered per-axis run's escapes (698, 1239)
and the line drive's (2096, 1949) were reported by their runners; this
one was not. The lamp's births confirm it: 150 `birth` lines in
`r12_flow` (one per 8 intervals to 1200) and 145 clicks on the line; 305
births in `r24_flow`. So the period 588.7 rests on 2 down and 2 up
crossings within 1208 intervals, and 987.3 on 3 and 2 within 2452.

**The contacts, GAMEBOARD (a `contact` line).** `r12_flow`: at the tick
808 the probe stepped from (31, 21) onto (31, 20), the detector line's
Node of the wall entry 34, whose `measure` entry for the probe's family
took the whole y component, -522063804 label units = 7.75 n-units (the
contact rule of 2026-09-20), the probe going on with **p** = (-71593408,
0, 0). `r24_flow`: at 633 from (71, 21) onto (71, 20), the entry 74
taking -202115808 = 3.00 n-units. The same as the line drive's
registered contacts (917 and 1400 on the branch): the design's line at
y = 20 lies inside the loops the law gives at S = 32 (the README on
`drive-default` says so for the line drive; it holds under the key as
well and the flow README does not say it). After the contact each loop
is a different loop, rebuilt by the push from a momentum with no y.

### 3.2 The probe's path, momentum and kicks (GAMEBOARD, a diagnostic)

The `step` lines give the Node per interval; the `read` lines the push
per interval (the momentum rebuilt from them and the contact equals the
escape click's momentum to the label unit, the reader's check). r is
the distance from the source's Node in Links, n the momentum in
n-units, H the invariant of 2.4 with A = 1.4838, L = x n_y - y n_x the
angular momentum, u / c the inward radial speed over the rows' pace
(over a window of 40 intervals).

**The kicks.** `r12_flow`: 125 reads in 1207 intervals, the mean kick
1.154 n-units, every kick toward the source (the radial part -1.154,
the tangential mean 0 within the digital line's half Link); 1 to 7 rows
in one read, so single kicks up to about 5 n-units, 60 per cent of the
launch's 8. `r24_flow`: 163 reads in 2451 intervals, the mean 0.863
n-units, 1 to 3 rows per read. The kicks' ticks mod 10 are spread (the
lines' paces differ by the isqrt's grain, so a shell reaches a ring over
about 10 intervals): the burst of "shells every 10 intervals" is smeared
at r >= 12, and the grain is the count of rows met per interval (0, 1,
..., 7), a shot noise with the variance of its mean.

**The loops, turn by turn.**

| World | the extrema (kind, tick, r, n, H, L) |
| --- | --- |
| `r12_flow` | apo 115: r 18.68, n 5.30, H 4.746, L 98.6; peri 282: 7.21, 14.36, 5.593, 103.3; apo 447: 25.18, 3.85, 5.004, 87.2; peri 600: 7.28, 17.45, 6.599, 126.7; apo 818: 48.60, 0.86, 5.774, -41.8 (after the contact at 808); peri 1034: 3.61, 30.44, 11.855, 100.0; at 1200: r 68.3, n 25.6, H 13.24; the escape at 1208 after 2.16 turns |
| `r24_flow` | apo 183: 31.76, 6.04, 5.649, 191.5; peri 415: 17.00, 13.04, 6.308, 221.2; apo 712: 43.91, 5.21, 6.005, 228.8 (after the contact at 633); peri 1051: 18.11, 12.83, 6.347, 232.4; apo 1460: 55.57, 5.23, 6.357, 290.1; peri 1898: 23.00, 14.47, 7.186, 332.6; apo 2427: 70.18, 3.93, 6.533, 271.0; the escape at 2452 after 2.41 turns |

Read against the algebra: (i) the first apocentre at r = 12 is 18.7
Links (a 55 per cent excursion within a fifth of a turn) where the map
without noise reaches 13.8: the grain seeds a large eccentricity at
once, in the first shell crossings (the launch reads the heading's
line alone until it leaves the axis; the first kicks are whole
n-units). (ii) From there the apocentres grow 18.7, 25.2, 48.6, 68 at
r = 12 (the factors 1.35, 1.93, 1.4) and 31.8, 43.9, 55.6, 70.2 at r =
24 (1.38, 1.27, 1.26), the pericentres fall (7.2, 7.3, 3.6; 17.0, 18.1,
23.0 with the contact between), the map's growth in the map's order.
(iii) H, constant under A / r and rising at every phase under the
factor (2.4), rises over the run: at r = 12 +0.85 (115 to 282), -0.59
(282 to 447), +1.60 (447 to 600), then the contact; 4.55 at the launch
to 13.2 at the escape. At r = 24, where u / c stays within 0.2, the
changes are +0.66, -0.30, +0.34, +0.01, +0.83, -0.65: a net rise of 1.0
in six half cycles. The falls on the out-goings are not the algebra's
(which rises monotonically) but the grain's shot noise and the per-axis
drive's torque (iv), which H does not account for. (iv) L is not conserved: the per-axis
drive's velocity is not parallel to the momentum (the torque v_x n_y -
v_y n_x, up to 0.25 n-units x Links per interval at n = 8 and larger at
the pericentres' n = 14 to 30, where the drive is far from the slow
limit), and the contact removed 7.75 n-units of p_y at (31, 20). The
loops are not Keplerian figures at any stage.

**The arrival rate against the radial speed (the test of 2.3).** The
kicks per interval times r (the 1 / r of the ring mean taken out),
binned by u / c:

| u / c | `r12_flow`: intervals, kicks x r per interval, impulse x r per interval | `r24_flow`: the same |
| --- | --- | --- |
| -0.4 (moving out) | 177, 1.28, 1.25 | - |
| -0.2 | 222, 1.38, 1.54 | 938, 2.01, 1.70 |
| 0.0 | 235, 1.66, 2.20 | 795, 2.34, 1.96 |
| +0.2 | 242, 1.91, 2.19 | 667, 2.20, 2.01 |
| +0.4 (falling in) | 83, 2.76, 3.33 | - |
| +0.6 | 72, 3.10, 3.14 | - |

At r = 12 the rate at u / c = +0.4 is 2.2 times the rate at -0.4
(the factor (1 + u / c) gives 1.4 / 0.6 = 2.3) and the impulse 2.7
times; at u / c = +0.6 against -0.6 the rate 2.9 (4.0 by the factor,
on 61 and 72 intervals). At r = 24 the loop's radial speeds stay within
0.2 c and the three bins differ by less than their noise (53, 60, 48
kicks). **Read as consistent with the crossing rule's (1 + u / c) at r
= 12, not as a measurement of the factor** (the bins are 60 to 240
intervals of one loop, the kicks Poisson-like, the speed a 40-interval
difference of a stepped path).

### 3.3 The registered numbers, by kind, restated

DETECTOR (the register's, unchanged): T(12) = 588.7 (2 down, 2 up
crossings, the spacings 445 to 732), T(24) = 987.3 (3, 2; 789 to 1184);
the amplitudes 32.5 and 45; omega^2 7.775e-5 and 3.112e-5; the controls
inside (x = 60 + r on every click, the escape 305). CONVERSION: the
radii at the births 3.2 to 68.3 about 24.3 and 17.0 to 71.0 about 37.6.
COMPUTATION: the ratio 1.677; T over the mean radius 24.2 and 26.3
(the register's line: the periods scale with the loops' own mean radii
within 9 per cent). DETECTOR, read here and not in the register: the
escapes at 1208 (face +y) and 2452 (face -x). GAMEBOARD: the contacts
at 808 and 633; the loops of 3.2. The line drive's row (the branch
`drive-default`, PR #907): T 674 / 1019, the ratio 1.512; the contacts
at 917 (3.75 n-units of p_y taken, the README's -252640524 on the n = 10
world's scale of 67371008 label units per n-unit) and 1400 (9.75 taken); the escapes at 2096 (face +y) and 1949 (face +x); the
equivalence outside after the closest passes (the reservoir's 0.3 per
cent, the register's own cause).

### 3.4 Which detector produced each Newton row, and whether it moves on Nodes (the owner's frame, record 1016)

One line per row, by kind. The owner's sense: a detector that moves
across Nodes and clicks, reading its own count, its Node and the ordinal
the packet brings (the cart of PR #834; records 816, 824, 1016); the
body's own record is GAMEBOARD (record 991).

| The row | The detector that produced the reading | Moving on Nodes? | Kind |
| --- | --- | --- | --- |
| Series D, `orbit/` `s32_r12`, `s32_r24` (T 289 / 829 at p = 576 as registered; the line drive's 480, 762 / 924 on the branch) | none: the probe's own `step` lines and momentum (records 562, 564) | no detector clicks; the moving body's own record | GAMEBOARD, a diagnostic, never compared with nature |
| Series D's lamp worlds `s32_r12_lamp`, `s32_r24_lamp` (the pins 371 / 742 under form B, written 2026-09-21; run under the line drive on `drive-default`: 525, 712 / 952, the ratio 1.81) | the fixed one-Node detector `source` at the source's Node, clicking the probe's rows that reach it (the tick and the row's label, whose reverse is the probe's direction) | no: the detector is fixed at the centre; the emitter (the probe's lamp on the whole fan) moves | DETECTOR, read on the detector's tick, not on a moving count |
| Series D3 as registered (the per-axis drive, n = 9: T 407 / 813, the ratio 1.997; the paper's row) | the fixed line of 121 one-Node detectors of the family `wall` at y = 20, each clicking the lamp's rows toward -y with their age (`measure`, `reads: "age"`) | no: the detectors are fixed on a line; the lamp on the probe moves, and a click gives where the light came from (x) and when (the tick less the age) | DETECTOR (the clicks' x, tick, age); the escape a face click; the probe's path GAMEBOARD |
| Series D3 under `flow_link` (PR #879: 588.7 / 987.3, the ratio 1.677) | the same fixed line at y = 20 | no, as above; and the line is also a wall the probe touched (the contacts of 3.1) | DETECTOR; the escapes at 1208 and 2452 face clicks not read by the tool; the contacts GAMEBOARD |
| The line-drive read (`drive-default`, PR #907: 674 / 1019, the ratio 1.512) | the same fixed line at y = 20 | no, as above (the contacts at 917 and 1400, the escapes at 2096 and 1949, registered there) | DETECTOR and GAMEBOARD as above |

So no Newton row on the tree was read by a detector moving on Nodes:
every reading is a fixed detector clicking a moving lamp's rows (the
lamp worlds, D3 in its three runs) or the body's own record (series D).
In the owner's sense of the test, Newton has not been tested yet; what
the rows read is the fixed detectors' view of a moving emitter, in the
detectors' own tick. The reading that would be the test is section 6.

## 4. The candidates, DECIDED or NOT DECIDED

1. **The force law's falloff on the lattice steeper or shallower than
   1 / r at these radii (the ring mean).** DECIDED, not the cause: the
   120 lines' incidence on the rings gives the per-Node impulse times r
   19.8 at 12 and 20.8 at 24 (COMPUTATION, 2.2), 4.6 per cent shallower
   than 1 / r, worth 2 per cent on a circle's ratio; the design's
   F_plane cancels line by line as ALGEBRA.md 5 says. The 1 / r form of
   the ring mean stands.
2. **The flow's directional grain at small r (the kicks of whole
   n-units on few lines; the Nodes on no line).** DECIDED as present
   and as the seed: the first apocentre 18.7 at r = 12 against the
   map's 13.8 without noise; 8 of the ring's 68 Nodes at r = 12 on no
   line and 24 of 144 at r = 24; single reads of up to 7 rows. NOT
   DECIDED as a quantity: its share of the loops' opening against the
   whole-8 launch and the velocity term is not separable on two loops
   of one realization each (a run at a finer grain, the register's own
   named reading, would; not ordered).
3. **The dwell integer's floor, the ladder's rounding.** DECIDED, not
   the cause: the body's step is `by_drive` on exact integers with the
   remainder kept; the ladder is the pushed row's wall and never the
   body's; the dwell is the clock's and the wall's, and the push reads
   arrivals (2.1). The flow label's rounding at load is at most 1.6 per
   cent on one line and 0.03 per cent in the fan's mean (DESIGN.md
   1.2).
4. **The drive's step (the per-axis anisotropy 6.9 per cent; the line
   drive's 12.6 per cent the other way; the whole-n launch 4.3 per cent
   above the balance).** DECIDED, not the cause of the ratio: the map
   with all of them and nothing else gives similar loops and the ratio
   2.005 (2.2, 2.5); they move each period by about 7 per cent, inside
   the 9 per cent band.
5. **The wall's bound at r = 24 (the board's faces, the detector line).**
   DECIDED, present at BOTH radii: the contact with the line at 808 and
   633 took 7.75 and 3.00 n-units of p_y (GAMEBOARD); the escapes at
   1208 and 2452 (DETECTOR) ended the loops. The register's "none in
   4000 intervals" is not what the record holds (3.1).
6. **The arrival rate's velocity term, (1 + u / c) from the crossing
   rule (2.3, 2.4).** DECIDED as the algebra's cause of the loops'
   opening: derived from the law's own rule with no lattice, it makes
   every loop grow by a factor of order two per turn at v / c = 0.34
   (the map, 2.5), and the records show that growth (the apocentres
   and H, 3.2) and a rate against u / c consistent with the factor at
   r = 12. NOT DECIDED to the per cent: the factor's exact size on the
   lattice (the r = 24 loop reads it within the noise; a loop launched
   with a radial speed at rest, or a body on a heading toward the
   source with its reads counted, would read it directly; not
   ordered).
7. **The pins' derivation itself (T proportional to r; the ratio 2
   "carrying no constant").** DECIDED: right in the ring mean at rest
   and `v << c` (rung 2), as its authors stated; not the law's algebra
   at S = 32, where the push is (1 + u / c) A / r and no closed orbit
   exists to carry a period. The generator's 384 / 768 and 377 / 754
   are GAMEBOARD by formula for a body the law does not have at this
   width.

What the records cannot decide: a candidate that would need a run and
is not ordered. (a) The size of the velocity term's factor on the
lattice (6). (b) The grain's share of the seed (2). (c) Whether a loop
at a width where v / c is small (S = 128 gives v / c = 0.10 at the
balance's n, the growth 0.6 per turn; S = 512 gives 0.03) closes over
several recurrences, which is the reading that would test T
proportional to r on this law; such a world is a new world and its
periods are 4 to 16 times longer.

## 5. The verdict, one paragraph

Newton's rows fell because the pinned reading was a closed orbit's
period under the ring-mean push A / r of a slow body, and the law at S
= 32 gives neither the closed orbit nor the slow body: the push the code
runs counts the rows a body meets, once each at the crossing of the
world lines, so a body falling toward the source meets the outgoing
shells at (1 + u / c) times a resting body's rate and the push is (1 + u
/ c) A / r, a velocity term that feeds every in-fall and makes the
circular orbit unstable, the radial excursion growing by a factor of
order two per turn at the launch pace of 0.34 c (the map: the
apocentres 12.0, 13.8, 15.6, 21.3, 51.4 from the whole-8 launch alone);
on the board the grain of the push seeded the eccentricity at once (the
first apocentre 18.7 at r = 12), the loops grew as the map says (18.7,
25.2, 48.6, 68 and 31.8, 43.9, 55.6, 70.2; the invariant H of the
ring-mean push rising from 4.5 to 13.2 and from 5.6 to 7.2), were
re-made by the detector line's contact at the ticks 808 and 633 (the
wall taking 7.75 and 3.00 n-units of p_y) and left the board at 1208
and 2452, which the register reads as no escape, so the periods 588.7
and 987.3 are the mean of two and three spacings of loops that were
never closed and their ratio 1.677 (and the line drive's 1.512, the
same anatomy) is not a reading of the force's exponent, as far as the
records decide; the ring mean's 1 / r form is not refuted (the lattice's
ring mean within 5 per cent of 1 / r, the periods scaling with the
loops' own mean radii); the grain's share of the seed against the
launch's, and the velocity factor's exact size on the lattice, remain
undecided. Where the fall is: in the algebra first (the velocity term is
the law's own continuum, present with no lattice at all), in the
lattice's grain second (the seed of the eccentricity, the first
apocentre 18.7 against the map's 13.8), and in the detector that read it
third (a fixed line that the loops crossed and touched, whose tool did
not print the escape; not a detector moving on Nodes, so not the test
the owner names).

## 6. One proposal, under its own identity, NOT ORDERED: newton-cart-v1, the moving-detector test of Newton

**The identity.** `newton-cart-v1`: the cart with a click of PR #834
(branch `moving-detector-build` at `8f5b42fbbcf6240d096052832db21c4e330d2ec2`,
HELD by the owner's scope word of record 920, read here and not touched)
carried ON the orbit of series D3 at r = 12 and 24, so that the orbit is
read by a detector moving on Nodes, on its own count, and not by a fixed
line in the tick. Stated as the one candidate; nothing of it is built, run
or pinned by this file; it needs PR #834's key `clock_stamp` on main and
enters nothing without the reviewer's gate and the owner's word. It
replaces nothing in the law: no rule, no verb, no key of a hypothesis
(the key `flow_link` may be on or off as the owner chooses; the pins
below are written for both).

**The world (the design's words, PR #834 sections 1, 3, 4, 7, turned to
the orbit; the reviewer's read P folded, lines (iv) and (v)).** Series
D3's plane (121 x 121, the source `m` at (60, 60) releasing its fan of
120 every 10 intervals, the width 32, `suspension` 0), with three
changes and no other: (i) the probe becomes the cart D: the registered
probe's body as it is (the paid family `probe`, the reservoir R = 2^12
and the held mass M_held = 2^20, M_total = 2^12 + 2^20 = 1052672, so the
generator's launch at the whole n = 8 under the key is the registered
538968064 label units and the pins' n is the cart's), its lamp REMOVED
(it read nothing without a post and would have cost content, moving the
drive's divisor; a body has its own count without a lamp, the `clock`
field), its table measuring the family `lamp` (`measure`, `reads:
"age"`); (ii) a lamp A at rest, one measured event of the paid family
`lamp` at the Node (60, 61) beside the source (two events cannot share a
Node), releasing one row per direction of the same fan of 120 every 10
intervals (the register's q; its content by the generator so that the
lamp never falls silent, 2^17 units for 48000 rows over the run); (iii)
the world key `clock_stamp` true, so every click the cart writes carries
`clock`, the cart's own count of self-creations (PR #834 section 7 (c);
the click line already carries the reader's number, the Node, the row's
label as its push, the ordinal in `record`, the age and the tick, the
reviewer's read P). The line at y = 20 is removed (no wall on the plane;
the faces stay open, the escape a face click). The post R of PR #834
(the radar) is not carried. A's rows push the cart at their click (a
paid family's push is the label itself, `push_form`), about 10^-6
n-units per click against the source's kicks of about one: GAMEBOARD,
stated, negligible.

**What the cart reads, DETECTOR, on its own record.** At every click of
A's rows: its own count `clock`, its Node, the ordinal of the row (A's
count at the emission, `record` mod 2^32) and the row's label **f**_D
(its direction from A, the reverse of the cart's direction from the
centre). From them, on the cart's count alone: the direction theta of
the centre at every click (the label's reverse); the flight's count,
`clock` less the ordinal (A's count is the tick here, no crowd stretches
it, and so is the cart's; the reading is written on the cart's count and
would stand in a crowd), which the flight table turns into the distance
r = c_D x (clock - ordinal) Links (CONVERSION, the register's `links_of`);
the period T as the recurrence of theta through 2 pi on the cart's count
(the click frame's method, section 0: a velocity Outside is Nodes apart
over counts apart); r's minima and maxima per turn (the loop's opening
or closure); the cart's Node at each click against its count (the least
step, one Node per count at most). A's rows reach the cart where its
Node lies on a fan line through (60, 61): 28 of the 68 ring Nodes at r =
12 and 16 of 144 at r = 24 (the orbit register's count for the source's
Node; the same fan), one shell every 10 intervals, so about one click
per 25 intervals at r = 12 and one per 90 at r = 24 on a circle, more on
a wide loop (every Node of the plane is on some line of the fan within
radius 8 of the axis' angle grain). The source's free rows push the cart
as today (`read`) and are not clicks.

**The pins it needs before any run (GAMEBOARD by formula until run; the
cart's clicks the measurement; the reviewer's read P folded, lines (i)
to (iii)).** The map of 2.5 (newton_map.py (`docs/designs/newton_diagnosis/newton_map.py`, deleted 2026-09-26), the law as
it stands: the ring mean with the arrival rate's factor, the per-axis
drive, the launch at the whole 8 under the key or 9 as built) now
prints the recurrence of theta through 2 pi, 4 pi and 6 pi on the count
([newton_map.out](newton_map.out)), and the record reader prints the
same recurrence off the replayed records
([newton_records.out](newton_records.out)); the numbers below are those
files' and not hand-written:

| Launch | the first three turns' counts at r = 12 (the spacings) | at r = 24 | the first apocentres, Links |
| --- | --- | --- | --- |
| the key on, n = 8 (A = 1.4838), the map | 399, 919, 1667 (399, 520, 748) | 794, 1830, 3288 (794, 1036, 1458) | 13.8, 15.6, 21.3 and 27.5, 31.2, 42.2 |
| the same launch on the board, the registered records replayed (GAMEBOARD, 3.2) | 473, 1044 (473, 571), the escape at 1208 | 939, 1898 (939, 959), the escape at 2452 | 18.7, 25.2, 48.6 and 31.8, 43.9, 55.6 |
| as built, n = 9 (A = 1.9098), the map | 349, 782, 1387 (349, 433, 605) | 694, 1555, 2737 (694, 861, 1182) | 13.1, 13.1, 14.6 and 26.2, 26.1, 22.8 |
| the ring mean alone (no factor), n = 8: the comparison, not the law's pin | 400, 812, 1206 (400, 412, 394) | 798, 1623, 2412 (798, 825, 789) | 13.3, 13.4, 13.5 and 26.6, 26.7, 26.8 |

The records' first turns, 473 and 939, sit 19 and 18 per cent above the
noiseless map's 399 and 794 at both radii alike, because the grain
seeds the loop's opening from the first shell crossings (3.2 (i): the
first apocentre 18.7 against the map's 13.8); their ratio 939 / 473 =
1.985. So the single turns carry the grain's band and the ratio is the
robust reading. The pins:

- (a) **The ratio of the first turns**, T_1(24) / T_1(12) = 2.00 +-
  0.20, the deciding reading (the map's 1.99; the records' 1.985 on the
  same plane, source, fan and launch): the plane's 1 / r ring mean's
  scale symmetry read on the first turn by a detector moving on Nodes on
  its own count. **The single first turns are REPORTED, not pinned**:
  against the map's 399 and 794 with the departure the records show
  (+19 and +18 per cent; the grain's seed), and against the records'
  own 473 and 939 (the same world but the detector; a first turn off
  those by more than 10 per cent would say the cart's reading and the
  fixed line's do not see one loop).
- (b) **The opening as the velocity term's signature**: the second turn
  longer than the first (the map's factors 1.30 at r = 12 and 1.30 at r
  = 24; the records' 1.21 and 1.02, the r = 24 loop touched by the line
  between), and the loop leaving the board before its fourth turn, as
  every record and the map have it. The apocentres are REPORTED beside
  the map's and the records' (the table), not pinned to the noiseless
  map (the records' first apocentre is 36 per cent above it). The
  falsifier that HOLDS: a loop whose turns stay at the no-factor row's
  400, 412, 394 (798, 825, 789), within the grain, refutes the term,
  since d H / dt = (A / r) u^2 / c >= 0 under the term and a loop that
  keeps its turns has no such term. The converse does not hold as
  written: turns growing by factors other than the map's say the
  noiseless loop is not the lattice's, not that the term is absent or
  present; the term's SIZE is read from the growth only through the
  map with the grain's band, not decided by one loop.
- (c) r from the clicks at the first turn: REPORTED against the
  records' 3.6 to 48.6 at r = 12 and 17.0 to 55.6 at r = 24
  (CONVERSION); the first pericentre and apocentre within 25 per cent
  of the records'.
- (d) The least step: the cart's Node changes by at most one per count
  between consecutive clicks (PR #834's pin), and the cart's own count
  between clicks is at least the clicks' Nodes apart.
- (e) The controls: the same worlds without the source (no push): the
  cart leaves through the face +y at the 61st Link of the pace 8 / 40,
  the count 305 +- 6 (the registered controls' tick, now on the cart's
  own count), its clicks of A's rows at the ordinals and counts the
  flight table gives on a straight path (A's rows reach the cart's
  column x = 60 + r only where a fan line through (60, 61) crosses it).

Refuted if the ratio leaves 2.00 +- 0.20, if a loop keeps its turns (no
term), or if a control moves; every other line above is a report by
kind beside the map and the records. Nothing is compared with nature:
Kepler's T proportional to r on the plane is the comparison side of pin
(a) only.

**The three tests (one line each; the diagnostician's reading before
the reviewer's).** Generic: no rule is added; the cart is a measured
event with a lamp and a `measure` entry as any, the world key
`clock_stamp` a record field of every measured event's own count (PR
#834 section 7 (c)), no family name, no kind. Vector: no verb touched;
the push, the step and the flight as they stand; the conversion of a
count into a length is the reading tool's, after the run. Local: the
cart reads what arrives at its Node and its own count; A releases from
its own Node; the tick is read by nothing above the board (the cart's
count equals it here, and the reading does not use that).

**What it decides that the present rows cannot.** (1) Newton read in a
detector moving on Nodes, on its own count: the period as a recurrence
of clicks the moving detector makes, the owner's test, which no row on
the tree has (3.4). (2) Whether the velocity term is there (the
falsifier of (b)); its size on the lattice only through the map with
the grain's band (the undecided (b) narrowed, not closed). (3) The
grain's share (the undecided (a)): the map's deterministic loop against
the cart's read loop, turn by turn, on the same count. (4) The 1 / r
ring mean's scale symmetry on the first turn at two radii by the ratio,
which the present rows read on loops already opened, touched and
escaped. The reviewer's closing line, taken as the design's own words:
the first-turn reading is Newton's test in the owner's sense as to the
detector (a detector moving on Nodes reading its own count); as to the
law it tests the plane's 1 / r ring mean's scale symmetry (T
proportional to r, the ratio 2) on a loop the grain has already opened
by its first turn, so the ratio is the reading that decides and the
single turns carry the grain's band. What it cannot decide: the value of G (a world's
inputs, the click frame's table), the inverse square in space (the
plane's 1 / r only), and r, the count's rate in a crowd (`suspension` 0
here). The cost, HOST: the key from PR #834 (about eight lines, held),
the world files by the generator, the reading tool's orbit branch (the
recurrence of a label's reverse on a count), four worlds of about 25 s
each; the reviewer's short second read of these pins before any world
file. NOT ORDERED.

**A named alternative, not ordered: newton-presence-v1.** Named here
because the owner was told of it (records 1022 and 1024) and the
physics-rule reviewer read it; which road to take is his decision. The
form: a body's push reads the rows PRESENT at the reader's Node in the
interval, each at its line's rate 2 S_1 Q over its wall 2 T_D (the pair
the flight already holds per direction, the inverse of the dwell), in
place of the rows met; a resting reader takes the same mean push per
row as today, and a reader in motion reads the stream's density where
it is, with no velocity term at first order (the factor of 2.3 removed).
The reviewer's verdict on the three tests (read N): generic PASSES;
local PASSES; vector PASSES SUBJECT TO the declared form: the exact
common wall as the lcm of 2 T_D over the fan is beyond the working
bound and not available (T_D runs from 110 to 887 on the 120 lines), so
the two admissible forms are per-direction accumulators (exact; fixed
work and storage times the fan's count for a fixed K) or the rounding at
load of 2 S_1 Q / (2 T_D) to a declared grain as **f**_D is rounded; no
root and no float at run time under either. The pins it would need,
from the map without the term (2.5, the first row): T(12) = 403 and
T(24) = 808 within 9 per cent, the ratio 2.00 +- 0.18, no contact with
the line and no escape in 4000 intervals, at least eight and four
recurrences agreeing. The order the Boss recommends to the owner:
newton-cart-v1 first (no law change, the owner's test), the presence
form only if the cart's reading shows the velocity term's signature.

## 7. Links

- newton_map.py (`docs/designs/newton_diagnosis/newton_map.py`, deleted 2026-09-26), [newton_map.out](newton_map.out): the continuum map (COMPUTATION).
- newton_records.py (`docs/designs/newton_diagnosis/newton_records.py`, deleted 2026-09-26), [newton_records.out](newton_records.out): the replay's record read (GAMEBOARD, DETECTOR the face clicks).
- PR #834's design and register on the branch `moving-detector-build` at `8f5b42fb`: `docs/designs/moving_detector/DESIGN.md`, `examples/events/moving_detector/README.md` (read there; not on main).
- [The flow weight design](../flow_weight/DESIGN.md) and [algebra](../flow_weight/ALGEBRA.md) section 5; [the click frame](../click_frame/DERIVATION.md) section 8; [the line drive's default](../drive_b/DEFAULT.md); [DERIVATIONS_BEAM 3.3](../../DERIVATIONS_BEAM.md).
- Series D3's register (`examples/events/orbit_lamp/README.md`, deleted 2026-09-26), run_flow.out (`examples/events/orbit_lamp/run_flow.out`, deleted 2026-09-26), expectations_flow.json (`examples/events/orbit_lamp/expectations_flow.json`, deleted 2026-09-26); the branch `drive-default` (PR #907) for the line drive's rows.
- [The log](../../LOG_2026-09-20.md): records 574, 594, 630, 648, 655 (series D3 and its causes), 816, 824, 872, 886, 915, 923, 962, 966, 981, 991, 1006, 1007, 1014, 1016.

> The scripts of this folder (`newton_map.py`, `newton_records.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/newton_diagnosis/<script>`).
