# The tick algebra: how a tick of a clock Outside follows from a tick of a clock Inside, with the crowd, and the light clock's closed forms (the Tick Algebraist, 2026-09-23; docs only, no run)

The model owner's word (record 1232, 2026-09-23 03:30Z, as the Boss
relayed it): "What you can still compute in the algebra, with the crowd
too because it affects the clock: how a tick of a clock Outside follows
from a tick of a clock Inside, with all its parameters; see whether it
helps the computation." And his point to hold: the moving detector
carries its held mass with it and the packet returns to where the mass
is now; the resting detector's mass returns to the same point.

This file: the definitions with their kinds (section 1); the tick
Outside per tick Inside as an exact function of the detector's
parameters, and from it the light clock's tick Outside along the motion
and across it, with the crowd's terms hop by hop (section 2); the owner's
point as one return condition (section 3); the table for k = 3, 5, 9, 17
and L = 20, 60, 120 (section 4); which pins become closed forms and which
need the run (section 5); the convergence, Newton at the zeroth order
and Einstein's forms at the second, from the board to above the board
(section 6); the three tests (section 7). Nothing enters the
law: no key, no identity, no verb. Einstein's forms appear only as the
thing compared with. The Light Clock Runner's file
`LIGHT_CLOCK.md` (branch light-clock, beside this file once merged) holds
the light clock's pins and worlds; this file moves none of them. The
Sagnac transponder file `PINS_R2.md` (branch new-rows-r2, the New Rows
Scout's, PR pending) is cited as the arrangement of the receiver body E;
neither is linked until it is on main.

Notation, as in [PINS.md](PINS.md) and [ALGEBRA.md](../../ALGEBRA.md):
every symbol is named at its first use; a scalar plain, a vector in bold
lowercase (**p** the momentum vector). The kinds: GAMEBOARD (the host's
view: the tick, a row's Node), DETECTOR (a click line's stamped count),
COMPUTATION (the algebra's closed form, before any run), CONVERSION (a
ratio formed from readings by a named definition), HOST (the machine's
cost); NATURE marks the thing compared with. Code lines are of
`src/event_universe/events/nature_beam.py` (written `nature_beam.py
:NNNN`), `events/engine.py`, `events/world.py`, `events/measured.py` and
`core/integer.py` at main `a3e33469`. The named symbols: Q the label's
scale (64, `world.py` :348); T_h the flight period of a heading
(isqrt(3 Q^2) = 110, `world.py` :475-478); c the pace of a light row on a
heading, Q / T_h = 32 / 55 Link per interval; D = (d_x, d_y, d_z) an
integer direction of the fan, T_D = isqrt(3 abs(D)_2^2 Q^2) its flight
period and c_D = Q abs(D)_2 / T_D its Euclidean pace (ALGEBRA 4.2); k the
whole number of intervals per hop of the moving body, v = 1 / k its pace
in Links per interval; beta = v / c = 55 / (32 k) the speed as a
fraction of c; gamma = 1 / sqrt(1 - beta^2) the Lorentz factor, only as
the thing compared with; L the receiver's distance in Links; M a body's
content, S the push's width, **p** its momentum, p = Q S M / (k - 1) on
one axis (the moving-detector worlds' rung); [n, d] the world's
`suspension` pair; A the age moment (the sum of amount x age) of the rows
of other numbers at a Node, one interval retarded; k_crowd = A n / d the
crowd's stretch of a count (ALGEBRA's notation; the FAIL rows write it
k); gamma_PPN the key `optical`'s declared strength and c_f = 1 +
gamma_PPN the flight's coefficient in the age wall's set (1 with the key
absent); N_0, N_par, N_perp the light clock's counts at rest, along the
motion and across it.

## 1. Definitions, with kinds

**The tick Inside** (GAMEBOARD, the host's tick): one engine interval of
the GameBoard, `self.tick += 1` and the interval's steps in their order
(`engine.py` :577-633: the frame, the bodies' steps, the law's walk,
readings, collision, measured events and releases, the merge). No
detector reads it (records 281, 1196, 1217). Two hops are counted in
it, both GAMEBOARD arithmetic:

- **The packet's hop.** A row on the direction D advances by its
  flight accumulator, the rate 2 S_1 Q against the wall 2 T_D from the
  start T_D (S_1 = abs(D)_1 its Manhattan length): its Links by its age
  tau are m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D))
  (`nature_beam.py` :829-831; the per-interval carry `by_drive_rows` at
  :3882, at most one Link per interval, Euclidean division with the
  remainder kept on the row). On a heading, S_1 = 1 and T_h = 110: the
  pace c = 128 / 220 = 32 / 55 Link per interval, one Link per 55 / 32
  intervals in the mean, the k-th Link at the interval ceil((2 k - 1)
  55 / 64) (ALGEBRA 4.1). In a crowd the wall is stretched: the pair
  becomes (2 S_1 Q d, 2 T_D (d + c_f n A)) (`nature_beam.py` :3877-3882,
  `age_wall` at `core/integer.py` :209, the coefficient c_f =
  `flight_coefficient` at `world.py` :1319-1323), so the pace is c_D /
  (1 + c_f k_crowd) along the path.
- **A body's hop.** The drive accumulator per axis, drive_a += p_a
  against the wall Q S M + abs(p_a) (`engine.py` :917-920, the divisor
  `step_divisor` at `world.py` :472): one Link per (Q S M + p) / p
  self-creations, k self-creations at p = Q S M / (k - 1). The drive
  advances only at a self-creation (`engine.py` :835), so per interval
  the body's pace is v = 1 / k where nothing is owed and v / (1 +
  k_crowd) where the crowd owes it counts (section 2.1). The step comes
  before the law in the interval (`engine.py` :586-590); the body's
  Nodes and its position move together (:1009-1011) and its held
  content moves with the record (`entry.held`, the drive's M).

**The tick Outside** (DETECTOR, the detector's own count): one
self-creation of the detector's record under the age wall, `entry.age
+= 1` in an interval where it owes nothing (`engine.py` :699-706: an
owed interval pays one count and creates nothing). It is the number the
key `clock_stamp` writes on the click line, `click_line["clock"] =
entry.age` (`nature_beam.py` :5549-5550; the rerelease line :5472-5473;
the `home` line at :5244-5257 carries no clock). It is the one clock a
measurement has (records 678, 709, 768, 1217): a detector at rest
receives its own packet back at its own Node, a moving one at the Node
its held mass has reached. For a light clock the tick Outside is the
return of the detector's own packet to the place of its held mass,
read as a click there: the count stamped on the return's click line
less the count n_0 at the birth (PENDING: at the base the birth line
carries no clock, `nature_beam.py` :6060-6078; the Birth Stamp
Implementer's line, branch birth-stamp, puts the clock on the birth line
under `clock_stamp`, and its line and ENGINE.md's row are cited here
when merged; until then n_0 is the birth's interval, a GAMEBOARD number
the detector's own count converts) (the packet's own number comes
`home` unstamped, RUNS.md finding 1, so the return is read through a
transponder body E that re-stamps it with its own number, as
`PINS_R2.md` arranges; a detector reads every number but its
own).

**Times are atomic** (the owner, record 1234): every time in a pin is a
whole number of the detector's own ticks, the difference of two stamped
counts on two lines, n_1 - n_0, an integer per ordinal (DETECTOR; n_0's
stamp pending as above).
The closed forms below are the means of those integers over a window of
ordinals, exact in the mean with the remainder bounded (the accumulators'
carries, ALGEBRA 4.1); per ordinal the whole count lies between the
floor of the closed form and its ceiling plus the band, and the mean
over the window is the fraction the pin states. An interval count T in
this file is the host's tick, GAMEBOARD, a diagnostic that the
detector's own count floor(r_D T) converts, never a number compared.

## 2. The derivation

### 2.1 The detector's count per engine interval

After each self-creation the body owes the crowd at its Node
`by_drive(acc_owed, A n, d)` intervals (`engine.py` :735-743 with the
count row `("owed", 1)` of `measured.py` :350; the same integers as
`count_owed`, `engine.py` :178-182: `age_wall(1, 1, 1, A, [n, d])` =
(d, d + A n), the excess A n over d): acc_owed += A n; owed =
floor(acc_owed / d); acc_owed -= owed d. The owed intervals are paid one
per frame with no count, no step, no release (`engine.py` :699-703). So
one self-creation costs 1 + A n / d intervals, exactly in the mean (the
accumulator's carry, ALGEBRA 4.1, the remainder below one interval), and

    the tick Outside per tick Inside:  r_D = d / (d + A n) = 1 / (1 + k_crowd),   k_crowd = A n / d,

with A the age moment of the rows of other numbers at the detector's
Node (one interval retarded, `nature_beam.py` :3877 and the crowd's
moments; the body's own rows and its own held content are not in it, the
one reading set), [n, d] the world's `suspension` (r_D = 1 exactly at n =
0, `engine.py` :179-180: the count equals the tick in number, the
registered moving-detector and Sagnac worlds), and the age wall's
coefficient 1 for the count (`measured.py` :350). The parameters that do
NOT enter: k, the drive (the count is the same for a moving and a
resting body, the law as built has no rate by motion, r = 1 in the click
theorem's terms, [DERIVATION.md](../click_frame/DERIVATION.md) section 3
and ALGEBRA 5.1: records 1217); the held mass M (it is content on the
record, not a row at the Node, and enters only the drive's wall Q S M
and, through the mass rows the body releases under its own number, the
crowd of OTHER readers at its Node); `age_bound` (it bounds the ages of
rows in the store, never a body's count, `world.py` :1779-1787 and
`nature_beam.py` :6530-6533; it enters the count only by bounding the
ages summed in A, and it bounds the light clock's L, section 2.5).
COMPUTATION; a detector's own count over T intervals is floor(r_D T)
with the accumulator's remainder, DETECTOR at the click, and this is the
row the crowd-clock designs read (crowd_clock DESIGN section 1 and
decision 1, k_crowd = 4 F / 2^16 under the presence word; clock_age NOTE
section 2 and 6, A = 22 F at 3 Links under the age word; reader_clock
DESIGN decision 4: a reading in the reader's own clock is a ratio of two
counts).

The same crowd slows the body's drive with its count (the drive advances
only at a self-creation): its pace per interval is v r_D = 1 / (k (1 +
k_crowd)) (crowd_clock DESIGN section 1: a lamp slowed by 1 + k inside a
crowd moving at v moves at v / (1 + k)). The packet's pace along the path
is c_D / (1 + c_f k_path), k_path = A_path n / d the crowd's term along
the path. These three numbers, the count's rate, the body's pace and the
packet's pace, are all the light clock needs.

### 2.2 The light clock along the motion, hop by hop

The arrangement: the detector D (a body of content M, its lamp on +x, its
table `measure`) and a receiver E, a body of its own number that clicks
the packet and re-emits it on its declared direction (`rerelease` on -x;
PINS_R2's body E in front instead of behind) at L Links ahead on the
bar. There is no mirror on the board (the owner, record 1234): the far
end of every light clock here is this receiver, and its count delta_E
enters the closed forms as the term the owner named, 0 at suspension 0
by the code (step 3). Every interval count below is GAMEBOARD arithmetic; the count the
detector reads is r_D times it, DETECTOR.

1. The birth (GAMEBOARD): at D's self-creation of count n_0 the packet is
   born at D's Node (`nature_beam.py` :6188-6203, age 0, on the
   body's Node after its step).
2. The out leg (COMPUTATION): the packet's Links m(t) = floor((128 t +
   110) / 220) on the heading; E's Node x_E(t) = x_0 + L + floor(t / k)
   in the mean (the drive's carry). The meeting m(t) = L + t / k gives
   t_out = L / (c - v) = 55 k L / (32 k - 55), exact in the mean, the
   remainder below one hop of E (k intervals) plus one Link of the
   packet (55 / 32 intervals). The factor 1 / (1 - beta) is the packet's
   gain c - v per interval on a receding receiver: the one-way factor k_AB
   of the click theorem at r = 1.
3. The dwell at E (GAMEBOARD): E takes the packet into its pending rows
   (`nature_beam.py` :5216) and re-emits it at its next self-creation
   (:5967) on -x under its own number: delta_E intervals. By the code
   the re-emission is in the arrival's interval: the walk (:3427), the
   tables (:5704, `rerelease` to the pending rows :5413) and `_release`
   (:3454, :6214) run in one call, every creating event with pending
   rows is visited (:6240-6250) and the rows are re-created at age 0
   (:5812); a row at age 0 steps at its first walk, its accumulator
   starting at T_D (:838-842). So delta_E = 0 exactly at suspension 0.
   In a crowd delta_E is the number of owed intervals E still has to
   pay at the arrival (an owed interval skips the release, :6241-6250):
   0 <= delta_E <= E's owed count, never one count by itself (Reviewer
   3's gate 2; PINS_R2's "+ 1" is not the code's).
4. The back leg (COMPUTATION): the packet closes on the approaching D at
   c + v: t_back = L / (c + v) = 55 k L / (32 k + 55); the factor 1 /
   (1 + beta) is 1 / k_BA at r = 1.
5. The click (DETECTOR): D's `measure` clicks E's row at D's Node as D
   stands now (`nature_beam.py` :3318-3323, the detector's set after its
   step), the line stamped n_1 = n_0 + floor(r_D T_par) with

    T_par = L / (c - v) + L / (c + v) + delta_E = 2 L c / (c^2 - v^2) + delta_E = (2 L / c) gamma^2 + delta_E   (intervals, GAMEBOARD),

    with gamma^2 = 1 / (1 - beta^2) = 1024 k^2 / (1024 k^2 - 3025) an exact fraction.

The resting clock, the same instrument at v = 0 (D and E at rest, L
apart, E a transponder with the same dwell): T_0 = 2 L / c + delta_E =
55 L / 16 + delta_E intervals. In the detector's own count, N_par =
r_D T_par and N_0 = r_0 T_0, r_0 the resting detector's rate. The ratio,
COMPUTATION:

    N_par / N_0 = (r_D / r_0) (2 L c / (c^2 - v^2) + delta_E) / (2 L / c + delta_E) = (r_D / r_0) gamma^2 (1 - (1 - 1 / gamma^2) delta_E / T_0)   exactly,

    = gamma^2 = 1024 k^2 / (1024 k^2 - 3025) at r_D = r_0 = 1 and delta_E's share dropped (it falls as 1 / L; at L = 20, k = 3 and delta_E = 1 it is 0.0048 of the ratio, at L = 120 0.0008).

**The receiver's count in the ratio** (the owner, record 1234, the term
kept in the form). At r_D = r_0 = 1:

    (N_par + delta_E) / (N_0 + delta_E) = (T_0 gamma^2 + delta_E) / (T_0 + delta_E) = 1 + beta^2 gamma^2 T_0 / (T_0 + delta_E),   T_0 = 55 L / 16,

the factor T_0 / (T_0 + delta_E) on the beta^2 term: at suspension 0
delta_E = 0 by the code (step 3) and the factor is 1 exactly, the ratio
gamma^2 with nothing to cancel; in a crowd, with delta_E owed intervals
at the arrival, the factor is below 1 (at delta_E = 1: 275 / 279 at L =
20, 825 / 829 at L = 60, 825 / 827 at L = 120), a change of order v^2
and of order 1 / L, negative, and at order v^0 nothing (both ratios 1 at
v = 0); across the same with gamma_x = T_D / (T_h d_y) in gamma^2's
place, (N_perp + delta_E) / (N_0 + delta_E) = 1 + (gamma_x - 1) T_0 /
(T_0 + delta_E). The exact fractions of the form at delta_E = 1 are the
third table of section 4.

Where the gamma squared comes from, hop by hop: one gamma from the two
legs' sum (1 / (1 - beta) + 1 / (1 + beta)) / 2 = gamma^2 with the
length L uncontracted, which Einstein's form compares with by the
contracted length L / gamma (ALGEBRA 5.1, L_D / L_0 = r_D); one gamma
from the count's rate r_D = 1 where Einstein's moving clock counts at 1
/ gamma. Einstein's form as the thing compared with: the moving clock
reads its own period 2 L / c in its own time, the ratio 1. The law as
built at r = 1 reads gamma^2, as record 1226 expected (the Boss's
report), and the click theorem's line r^2 = 1 - beta^2 would take one
gamma off (the count) and the radar length the other; neither is in the
law as built, and neither enters here.

### 2.3 The light clock across the motion

Across, the packet must reach a receiver that moves with D, so its heading
needs the x-pace v exactly: a direction D_f = (d_x, d_y, 0) of the fan
with Q d_x / T_D = 1 / k, that is k Q d_x = isqrt(3 Q^2 (d_x^2 +
d_y^2)), a Diophantine condition on the fan (no root at run time: the
isqrt is the table's, taken at load). The first such direction per k,
by the check of section 5 (COMPUTATION):

| k | D_f = (d_x, d_y, 0) | abs(D_f)_1 | T_D | x-pace Q d_x / T_D | y-pace Q d_y / T_D | c_D |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | (70, 99, 0) | 169 | 13440 | 1/3 | 33/70 = 0.47143 | 0.57737 |
| 5 | (24, 65, 0) | 89 | 7680 | 1/5 | 13/24 = 0.54167 | 0.57741 |
| 9 | (111, 566, 0) | 677 | 63936 | 1/9 | 566/999 = 0.56657 | 0.57736 |
| 17 | (72, 703, 0) | 775 | 78336 | 1/17 | 703/1224 = 0.57435 | 0.57735 |

D_f = (70, 99, 0) needs `direction_bound` 169 (the default 64); the Light
Clock Runner's worlds declare (41, 58, 0) at k = 3 and (17, 46, 0) at k
= 5 within 64, whose x-paces 2624 / 7873 and 1088 / 5436 are off 1 / k
by -4.2 x 10^-5 and +1.5 x 10^-4, both right by the code for their own
declaration (Reviewer 3's gate 2); the registered fans reach abs(D)_1 <=
330 (RUN_10's `direction_bound`), so k = 3 and k = 5 are within a
registered fan's reach at the exact pace and k = 9 and k = 17 need a fan
declared to 677 and 775; the second solution per k is the
double of the first (k = 3, 5, 17) or another pair (k = 9: (212,
1081)).

The out leg on D_f: the packet makes d_y y-Links per T_D / Q intervals,
so it crosses L Links in t = L T_D / (Q d_y) intervals, during which the
mass moves t / k = L d_x / d_y Links, the packet's own x-Links on its
Bresenham line to within one Node; the back leg on (d_x, -d_y, 0),
re-emitted by E on that declared direction, the same. So, COMPUTATION:

    T_perp = 2 L T_D / (Q d_y) + delta_E,   N_perp / N_0 = (r_D / r_0) T_D / (T_h d_y)   (delta_E's share dropped),

an exact fraction: 448 / 363, 768 / 715, 15984 / 15565, 39168 / 38665
at k = 3, 5, 9, 17. It factors as (c / c_D) x gamma_D with gamma_D = 1 /
sqrt(1 - v^2 / c_D^2): gamma across from the count's rate alone (r_D =
1 where Einstein's clock counts at 1 / gamma; Einstein's ratio 1 as the
thing compared with), times the comb's anisotropy c / c_D = 1.0077 (the
heading's pace 32 / 55 over the near-diagonal direction's, ALGEBRA 4.2:
1 / c_D^2 = 2.954 on a heading, 3.000 on a body diagonal). At k >= 9
the anisotropy's 0.77 percent exceeds gamma - 1 (0.19 and 0.05 percent),
so the across clock reads the comb before it reads gamma unless the
resting clock is read on the same direction class (a resting packet on
D_f and back: then the ratio is gamma_D alone, still a root in the
limit, a fraction on the table). Where the packet returns: exactly to
E's Node when d_y divides L, otherwise within one Node (the remainder of
the Bresenham line against the drive's carry), which a body E of one
Node does not click; section 5.

### 2.4 The crowd's terms, with the sign and the order in v

Three crowd terms: k_b = A_b n / d at the bodies' Nodes (D and its
co-moving E share it, else they drift apart and the clock is not rigid;
PINS_R2's E and D have identical accumulators), k_p = A_p n / d along
the path, k_m the receiver's own when it is at rest apart from D. They
enter through the three paces of section 2.1:

    v_eff = v / (1 + k_b),   c_eff = c / (1 + c_f k_p),   r_D = 1 / (1 + k_b),   0 <= delta_E <= E's owed count at the arrival (0 at suspension 0),

and every closed form above holds with these in place of v, c, 1:

    N_par = (2 L c_eff / (c_eff^2 - v_eff^2) + delta_E) / (1 + k_b),   N_0 = (2 L / c_eff + delta_E) / (1 + k_b),

    N_par / N_0 = 1 / (1 - beta_eff^2),   N_perp / N_0 = (c_eff / c_D,eff) gamma_D,eff,   beta_eff = beta (1 + c_f k_p) / (1 + k_b).

So: (i) A UNIFORM crowd (k_p = k_b, c_f = 1) changes nothing: the packet,
the drive and the count are all slowed by the same 1 + k_b, the
intervals stretch by it and the count's rate divides by it; N_0, N_par,
N_perp and both ratios are the no-crowd numbers exactly (the across
direction D_f the same). (ii) A crowd at the bodies' Nodes alone (the
registered form: series U's sources send their rows through the lamp's
Node, the bar between free) LOWERS both ratios toward Einstein's 1:
beta_eff = beta / (1 + k_b), the ratio along 1 + beta^2 / (1 + k_b)^2 +
O(beta^4), the change -2 k_b beta^2 at first order in k_b, exact as the
factor 1 / (1 + k_b)^2 on beta^2; across, half of it, -k_b beta^2. (iii)
A crowd along the path alone RAISES them: +2 c_f k_p beta^2 along, +c_f
k_p beta^2 across. In (ii) and (iii) alike the crowd moves beta_eff and
never the form: the ratio is the classical light clock's 1 / (1 -
beta_eff^2) at every crowd, the departure from Einstein's form (the
whole beta_eff^2 term) unchanged, no crowd term at order v, and none
makes r depend on the momentum; a crowd at the bodies is not a dilation
by motion. (iv) The order in v: every crowd term multiplies
beta^2; there is no term of order v (the two legs' first orders cancel
as in the Sagnac sum). (v) The receiver's count delta_E, 0 at
suspension 0, lowers the ratio along in a crowd by (1 - 1 / gamma^2)
delta_E / T_0 = beta^2 delta_E c / (2 L) + O(beta^4), order beta^2 / L,
negative, and by half that across; it is E's owed intervals at the
arrival, at most its owed count. (vi) The held mass M
enters no ratio: it sets p = Q S M / (k - 1) for the declared k and it is
the crowd of no reader at D's own Node (its mass rows carry D's number).
Every statement of this section is COMPUTATION; the numbers of section
4 carry k_b as the registered worlds have it.

### 2.5 The bounds the parameters set

The packet's age at each leg's end is that leg's intervals (a re-emitted
row is born fresh at age 0, `nature_beam.py` :6188), so the clock runs
only while L / (c_eff - v_eff) <= age_bound (the merge refuses a run
whose row carries an age beyond it, :6530-6533): on a bar with an open
axis the default age_bound is twice the flight bound, 2 ceil(ceil(X + Y
+ Z - 2) T_h / Q) on a heading, 3.44 times the bar's diameter
(`world.py` :1707-1726, :1787): at k = 3 the out leg is 165 L / 41 =
4.02 L intervals, so L up to 0.85 of the diameter fits (L = 120 on the
bar 240 x 3 x 3 of the registered worlds); at k = 17 it is 935 L / 489
= 1.91 L; a periodic bar needs age_bound declared (PINS_R2's 1500).

## 3. The owner's point as algebra: one return condition

Let x_D(t) be the Node of D's held mass at the interval t: x_D(t) = x_0
+ floor(t v_eff) with the drive's remainder (the drive moves the record,
its position, its Nodes and its held content together, `engine.py`
:1009-1011; `entry.held` travels on the record). Let x_r(t) be the
returning packet's Node. The click that ends the light clock's tick is
the one event

    x_r(t*) in the detector's set as it stands at t*   (the set of x_D(t*), `nature_beam.py` :3318-3323, after the step of t*),

read as the stamped click at t* (`measure`, :5549-5550). At rest v_eff =
0, x_D(t*) = x_0: the packet returns to the Node it left. In motion
x_D(t*) = x_0 + floor(t* / (k (1 + k_b))): the packet returns to the Node
the mass has reached, one Node per k self-creations. It is one rule, the
return to the held mass, with the resting clock as its value v = 0, not
a second rule: the engine branches on nothing (the same `node_event`
lookup for every body, every interval), the closed forms of section 2
are one formula in v with T_0 = T_par at v = 0 and T_0 = T_perp at v = 0
(D_f = (0, 1, 0), T_D = T_h), and the owner's two sentences are its two
values. What the rule is NOT: a return to the emission Node (a
GameBoard place, read by nothing), nor a return to the detector's number
(the own number comes `home`, :4642-4694, unstamped; the click is E's
number at D's set).

**Is our mass and the mass of the Inside the same mass? "We are in the
store"** (the owner, record 1234). The one quantity Inside is `content`,
the integer M in the family's units, the mass (TERMINOLOGY, Content): on
a row it is the store's column `content` per unit beside `amount`, the
number of identical units, the carried content amount x content
(`nature_beam.py` :2004-2005; a free family's row carries content 0); on
a body it is `entry.held[family]`, summed as `entry.content`
(`measured.py` :706-708), the M the drive's wall Q S M reads (`world.py`
:472) and the M the mass rows it releases draw down (the release
`by_drive(acc, held x n, d)`, `nature_beam.py` :5788-5811); the books'
content line balances both, on the bodies and in transit, at every
interval (GAMEBOARD, TERMINOLOGY, Books). So "our mass", the moving
detector's held M (the cart's 2^22 units of the free family `mass` plus
its 2^13 units of light of its own paid family,
`examples/events/moving_detector/make_worlds.py` :64-69, :153), and "the mass of the Inside" are one integer in one column: a
body's held mass IS the content of its own record, kept in the same
ledger as every row's, and there is no second mass. The Outside knows
it only when a click reads a record: a row of a family without the flag
`massive` places its units, content and label where it ends, the pair
(f_F, q_F) = (1, 0), and its content joins the detector's held at the
click (`entry.held[family] += group_content - waiting_content`,
`nature_beam.py` :5496-5498); a massive family places nothing at the
arrival and its quantum M at the record's completion, the pair (0, M)
(`FamilyFlight.placed` and `quantum`, :1019-1050; `_place_completion`
:6616); the click line's `content` is the only content Outside.
The light packet is a row of the cart's own paid family (`cart`,
quantum 1, `make_worlds.py` :199), one unit of content 1, no flag
`massive`: it carries one unit of the lamp's light, which the receiver
gains at its click and spends again at the re-emission, and it never
carries the held mass, which stays on the record. In the owner's
picture, then, "the mass returns to the detector" means the detector's
own record, its held content and its Nodes, staying with it as it moves
(`engine.py` :1009-1011), so that the packet's Node meets the record's
set; it does not mean the packet's content coming back (one unit of
light returns under E's number, no mass rides the packet). No new rule,
no new noun.

**The receiver at rest on the bar against the co-moving receiver.** With E at
rest at L ahead of the emission Node the out leg is L / c and the back
leg L (1 - beta) / (c + v): T = 2 L / (c + v), the ratio 1 / (1 + beta)
= 32 k / (32 k + 55), first order in v, Doppler's form and not
Einstein's; with E at rest L behind, 2 L / (c - v) and 1 / (1 - beta);
the two together (a receiver fore and one aft, both at rest, PINS_R2's
arrangement turned outward) sum to 4 L c / (c^2 - v^2) = 2 T_0 gamma^2,
the along clock's gamma squared again, and differ by 2 T_0 beta gamma^2,
the Sagnac difference of PINS_R2 (its ratio beta, r-free). Across, a
receiver at rest on the bar returns the packet to the emission Node; the
mass has moved 2 L / (c k) Links from it and the packet misses the
detector's set (no click, the clock does not close), which is the
owner's point in one line: only a receiver that moves with the held mass
(E as PINS_R2's body, the same accumulators) brings the packet back to
where the mass is now, and only then do the closed forms of 2.2 and 2.3
hold.

## 4. The table (COMPUTATION, no run; every number an exact fraction and its decimal)

c = 32 / 55 on a heading, v = 1 / k, beta = 55 / (32 k), the co-moving
receiver E at L Links; the receiver's count delta_E = 0 at suspension 0
by the code (2.2 step 3), so N_0, N_par and N_perp carry no dwell (in a
crowd add E's owed intervals to each, 2.4 (v)); the across counts on the
direction D_f of section 2.3, where L is a multiple of d_y for the exact
return and within one Node otherwise. N_0 = 55 L / 16; N_par = 3520 k^2
L / (1024 k^2 - 3025); N_perp = L T_D / (32 d_y). The whole-tick
integer per ordinal, as the runner's pins write it: N_0 = 2 a(L) with
a(L) = ceil((2 L - 1) 55 / 64) the interval of the L-th Link (ALGEBRA
4.1), 68, 206 and 412 at L = 20, 60, 120 beside the means 275 / 4, 825 /
4 and 825 / 2. The two things
compared with: gamma^2 and gamma (NATURE's form, Einstein 1905, whose
own ratios are 1 and 1), the across fraction beside (c / c_D) gamma_D.

**Without a crowd** (`suspension` 0, the registered moving-detector and
Sagnac worlds: r_D = 1, the count equals the tick):

| k | L | N_0 | N_par | N_perp | N_par / N_0 | gamma^2 | N_perp / N_0 | gamma | (c / c_D) gamma_D |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 20 | 275/4 = 68.75000 | 633600/6191 = 102.34211 | 2800/33 = 84.84848 | 9216/6191 = 1.48861 | 1.48861 | 448/363 = 1.23416 | 1.22009 | 1.23416 |
| 3 | 60 | 825/4 = 206.25000 | 1900800/6191 = 307.02633 | 2800/11 = 254.54545 | 9216/6191 = 1.48861 | 1.48861 | 448/363 = 1.23416 | 1.22009 | 1.23416 |
| 3 | 120 | 825/2 = 412.50000 | 3801600/6191 = 614.05266 | 5600/11 = 509.09091 | 9216/6191 = 1.48861 | 1.48861 | 448/363 = 1.23416 | 1.22009 | 1.23416 |
| 5 | 20 | 275/4 = 68.75000 | 70400/903 = 77.96235 | 960/13 = 73.84615 | 1024/903 = 1.13400 | 1.13400 | 768/715 = 1.07413 | 1.06489 | 1.07413 |
| 5 | 60 | 825/4 = 206.25000 | 70400/301 = 233.88704 | 2880/13 = 221.53846 | 1024/903 = 1.13400 | 1.13400 | 768/715 = 1.07413 | 1.06489 | 1.07413 |
| 5 | 120 | 825/2 = 412.50000 | 140800/301 = 467.77409 | 5760/13 = 443.07692 | 1024/903 = 1.13400 | 1.13400 | 768/715 = 1.07413 | 1.06489 | 1.07413 |
| 9 | 20 | 275/4 = 68.75000 | 5702400/79919 = 71.35224 | 19980/283 = 70.60071 | 82944/79919 = 1.03785 | 1.03785 | 15984/15565 = 1.02692 | 1.01875 | 1.02692 |
| 9 | 60 | 825/4 = 206.25000 | 17107200/79919 = 214.05673 | 59940/283 = 211.80212 | 82944/79919 = 1.03785 | 1.03785 | 15984/15565 = 1.02692 | 1.01875 | 1.02692 |
| 9 | 120 | 825/2 = 412.50000 | 34214400/79919 = 428.11346 | 119880/283 = 423.60424 | 82944/79919 = 1.03785 | 1.03785 | 15984/15565 = 1.02692 | 1.01875 | 1.02692 |
| 17 | 20 | 275/4 = 68.75000 | 20345600/292911 = 69.46001 | 48960/703 = 69.64438 | 295936/292911 = 1.01033 | 1.01033 | 39168/38665 = 1.01301 | 1.00515 | 1.01301 |
| 17 | 60 | 825/4 = 206.25000 | 20345600/97637 = 208.38002 | 146880/703 = 208.93314 | 295936/292911 = 1.01033 | 1.01033 | 39168/38665 = 1.01301 | 1.00515 | 1.01301 |
| 17 | 120 | 825/2 = 412.50000 | 40691200/97637 = 416.76004 | 293760/703 = 417.86629 | 295936/292911 = 1.01033 | 1.01033 | 39168/38665 = 1.01301 | 1.00515 | 1.01301 |

The ratio along equals gamma^2 to every digit (it is gamma^2 as an
exact fraction); the ratio across exceeds gamma by the comb's factor c /
c_D = 1.0077 and equals (c / c_D) gamma_D to every digit.

**With the crowd as the registered worlds have it**, at the bodies'
Nodes and not along the path: series U's `still_3` crowd under the age
word (clock_age NOTE section 6; `examples/events/crowd_clock/`), two
sources at 3 Links each releasing F = 4915 units per interval, the age
moment at the lamp's Node A = 22 F = 108130, `suspension` [1, 65536]:
k_b = 108130 / 65536 = 54065 / 32768 = 1.64993, 1 + k_b = 86833 / 32768,
r_D = 32768 / 86833 = 0.37737 counts per interval; the same crowd at the
resting clock (r_0 = r_D). Then N_0 = (55 L / 16) (32768 / 86833), v_eff
= 32768 / (86833 k), beta_eff = beta (32768 / 86833), and the ratio along
is 1 / (1 - beta_eff^2), exact. The across count needs the direction D_f
with x-pace v_eff = 32768 / (86833 k), which is on no registered fan
(section 5), so N_perp is given as its limit gamma_eff (a root, not a
pin) beside the exact ratio along:

| k | L | N_0 | N_par | N_par / N_0 | 1 / (1 - beta_eff^2) | beta_eff | N_perp / N_0 in the limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 20 | 2252800/86833 = 25.94405 | 1760556441600/64687786601 = 27.21621 | 67859729001/64687786601 = 1.04903 | 1.04903 | 56320/260499 = 0.21620 | 1.02422 |
| 3 | 60 | 6758400/86833 = 77.83216 | 5281669324800/64687786601 = 81.64863 | 67859729001/64687786601 = 1.04903 | 1.04903 | 56320/260499 = 0.21620 | 1.02422 |
| 3 | 120 | 13516800/86833 = 155.66432 | 10563338649600/64687786601 = 163.29727 | 67859729001/64687786601 = 1.04903 | 1.04903 | 56320/260499 = 0.21620 | 1.02422 |
| 5 | 20 | 2252800/86833 = 25.94405 | 195617382400/7413092193 = 26.38810 | 7539969889/7413092193 = 1.01712 | 1.01712 | 11264/86833 = 0.12972 | 1.00852 |
| 5 | 60 | 6758400/86833 = 77.83216 | 195617382400/2471030731 = 79.16429 | 7539969889/7413092193 = 1.01712 | 1.01712 | 11264/86833 = 0.12972 | 1.00852 |
| 5 | 120 | 13516800/86833 = 155.66432 | 391234764800/2471030731 = 158.32857 | 7539969889/7413092193 = 1.01712 | 1.01712 | 11264/86833 = 0.12972 | 1.00852 |
| 9 | 20 | 2252800/86833 = 25.94405 | 15845007974400/607565618609 = 26.07950 | 610737561009/607565618609 = 1.00522 | 1.00522 | 56320/781497 = 0.07207 | 1.00261 |
| 9 | 60 | 6758400/86833 = 77.83216 | 47535023923200/607565618609 = 78.23850 | 610737561009/607565618609 = 1.00522 | 1.00522 | 56320/781497 = 0.07207 | 1.00261 |
| 9 | 120 | 13516800/86833 = 155.66432 | 95070047846400/607565618609 = 156.47700 | 610737561009/607565618609 = 1.00522 | 1.00522 | 56320/781497 = 0.07207 | 1.00261 |
| 17 | 20 | 2252800/86833 = 25.94405 | 56533423513600/2175879355521 = 25.98187 | 2179051297921/2175879355521 = 1.00146 | 1.00146 | 56320/1476161 = 0.03815 | 1.00073 |
| 17 | 60 | 6758400/86833 = 77.83216 | 56533423513600/725293118507 = 77.94562 | 2179051297921/2175879355521 = 1.00146 | 1.00146 | 56320/1476161 = 0.03815 | 1.00073 |
| 17 | 120 | 13516800/86833 = 155.66432 | 113066847027200/725293118507 = 155.89124 | 2179051297921/2175879355521 = 1.00146 | 1.00146 | 56320/1476161 = 0.03815 | 1.00073 |

**The form at delta_E = 1, the value in a crowd of one owed interval at
E** (not the value at suspension 0, where delta_E = 0 and the first table
stands; the ratios then depend on L):

| k | L | (N_par + 1) / (N_0 + 1) | gamma^2 | (N_perp + 1) / (N_0 + 1) | N_perp / N_0 | T_0 / (T_0 + 1) |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 20 | 2559164/1727289 = 1.48161 | 1.48861 | 11332/9207 = 1.23080 | 1.23416 | 275/279 = 0.98566 |
| 3 | 60 | 7627964/5132339 = 1.48625 | 1.48861 | 11244/9119 = 1.23303 | 1.23416 | 825/829 = 0.99517 |
| 3 | 120 | 7615582/5119957 = 1.48743 | 1.48861 | 11222/9097 = 1.23359 | 1.23416 | 825/827 = 0.99758 |
| 5 | 20 | 285212/251937 = 1.13208 | 1.13400 | 3892/3627 = 1.07306 | 1.07413 | 275/279 = 0.98566 |
| 5 | 60 | 282804/249529 = 1.13335 | 1.13400 | 11572/10777 = 1.07377 | 1.07413 | 825/829 = 0.99517 |
| 5 | 120 | 282202/248927 = 1.13367 | 1.13400 | 11546/10751 = 1.07395 | 1.07413 | 825/827 = 0.99758 |
| 9 | 20 | 23129276/22297401 = 1.03731 | 1.03785 | 81052/78957 = 1.02653 | 1.02692 | 275/279 = 0.98566 |
| 9 | 60 | 68748476/66252851 = 1.03767 | 1.03785 | 240892/234607 = 1.02679 | 1.02692 | 825/829 = 0.99517 |
| 9 | 120 | 68588638/66093013 = 1.03776 | 1.03785 | 240326/234041 = 1.02685 | 1.02692 | 825/827 = 0.99758 |
| 17 | 20 | 82554044/81722169 = 1.01018 | 1.01033 | 198652/196137 = 1.01282 | 1.01301 | 275/279 = 0.98566 |
| 17 | 60 | 81772948/80941073 = 1.01028 | 1.01033 | 590332/582787 = 1.01295 | 1.01301 | 825/829 = 0.99517 |
| 17 | 120 | 81577674/80745799 = 1.01030 | 1.01033 | 588926/581381 = 1.01298 | 1.01301 | 825/827 = 0.99758 |

One owed interval at E pulls every ratio toward 1 by the factor T_0 /
(T_0 + 1) on its excess, 1.4 percent of the excess at L = 20 and 0.24
percent at L = 120; at suspension 0 the factor is 1.

Read: the crowd at the bodies' Nodes cuts every count by 1 + k_b =
2.650 (the age word's pin for series U at 3 Links, 1 + z = 2.650,
clock_age NOTE section 6, is this same 1 + k_b read as a rate) and cuts the ratios' excess over
Einstein's 1 by (1 + k_b)^2 = 7.02 (k = 3: 1.489 to 1.049); a uniform
crowd along the path as well would restore the first table exactly. A
crowd that moves with the bodies (the mass rows a body releases read by
the OTHER body: E reads D's mass rows where they pass its Node) is a k_b
of the registered mass worlds' own making, not assumed here; its value
is A = amount x age of D's rows at E's Node, and the algebra above takes
it as it comes.

## 5. What helps the computation: the pins that close and the ones that need the run

Closed by this algebra (COMPUTATION, exact fractions, no run; the band
per pin the lattice's remainder as PINS_R2 section 3 states it, one hop
of the body plus one Link of the packet per meeting; delta_E = 0 at
suspension 0):

1. The resting clock N_0 = 2 L / c + delta_E = 55 L / 16 + delta_E, at
   any suspension divided by 1 + k_b.
2. The along clock with a co-moving receiver, N_par = 2 L c / (c^2 - v^2) +
   delta_E = 3520 k^2 L / (1024 k^2 - 3025) + delta_E, and its ratio
   gamma^2 = 1024 k^2 / (1024 k^2 - 3025) exactly (section 4), the dwell's
   share as written; with the crowd's three terms as in 2.4.
3. The along clock with a receiver at rest, fore 2 L / (c + v) and aft 2 L
   / (c - v), the ratios 1 / (1 + beta) and 1 / (1 - beta), their sum 2
   T_0 gamma^2 and their difference the Sagnac's (PINS_R2's pin stands
   beside it, not moved).
4. The tick Outside per tick Inside r_D = d / (d + A n) for any world,
   and the count over a run floor(r_D T) with the remainder: a stamped
   click's `clock` can be pinned from the tick and A alone.
5. The across clock's direction D_f per k and its ratio T_D / (T_h d_y)
   where D_f is on the fan and d_y divides L (k = 3: L a multiple of 99;
   k = 5: of 65; k = 9: of 566; k = 17: of 703; none of L = 20, 60, 120),
   and its factorisation (c / c_D) gamma_D, which says before any run
   that the across clock at k >= 9 measures the comb's anisotropy before
   gamma.

Needing the run (the algebra gives the form and the band, not the
integer): delta_E, 0 at suspension 0 by the code, E's owed intervals at
the arrival in a crowd, a run's reading; the meeting's remainder per
ordinal (the closed forms are exact in the mean over a window, as the
click theorem's rung 1); the across return where d_y does not divide L
(within one Node; for the runner's fans at L = 60 the reviewer's residue
table shows every residue returning on both legs, so E of one Node
clicks it there, and another L or fan is LIGHT_CLOCK.md's to declare);
the
across clock inside a crowd at the bodies alone (its D_f, with the
x-pace 32768 / (86833 k), is on no fan with d_x <= 2000 at any of the
four k, by the same search); a crowd
that moves with the bodies (the mass rows' A at E's Node, a run's
reading). The one cheap check allowed, the direction search that confirms
the closed form of 2.3 (HOST, under one second, no world, no engine):

```
$ python3 -c "
from math import isqrt
Q=64
for k in (3,5,9,17):
    f=[(x,y,isqrt(3*(x*x+y*y)*Q*Q)) for x in range(1,2000) for y in range(max(1,isqrt((k*k-3)*x*x//3)-1),isqrt((k*k-3)*x*x//3)+3) if k*Q*x==isqrt(3*(x*x+y*y)*Q*Q)]
    print(k,f[:2])
"
3 [(70, 99, 13440), (140, 198, 26880)]
5 [(24, 65, 7680), (137, 371, 43840)]
9 [(111, 566, 63936), (212, 1081, 122112)]
17 [(72, 703, 78336), (144, 1406, 156672)]
```

COMPUTATION: the first direction per k with k Q d_x = T_D, the fan's
own isqrt; the table of 2.3 is read off it, and every fraction of
section 4 is formed from these integers and the closed forms by exact
arithmetic.

## 6. The convergence: Newton at low speed, Einstein's forms at the second order, from the board to above the board

The owner's word (record 1235, as the Boss relayed it): the algebra of
the tick at low speeds gives Newton, at higher speeds Einstein, and this
must converge in the formulas; how does one derive, by the tick,
Einstein from the board to above the board. Newton's and Einstein's
forms below are the things compared with, never the law's.

**(a) The expansion in v.** The tick Outside is the exact function of
the tick Inside and v = 1 / k of section 2: r_D = 1 / (1 + k_b) counts
per interval, and for the light clock's return N = r_D T with T the
closed forms of 2.2 and 2.3. In the continuum limit of the fan (c
isotropic, c_D -> c, the anisotropy c / c_D -> 1 within 1 / T_D; ALGEBRA
4.2) the ratios expand in beta = v / c as, with the receiver's count
dropped (its factor T_0 / (T_0 + delta_E) on every beta term, 1 at
suspension 0, section 2.2):

| The quantity, in the detector's own count | The law as built, exact | at order v^0 | at order v^2 | at order v^4 | Einstein's form (compared with) | its v^2 | its v^4 | Newton's (compared with) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| The moving detector's own count per resting count (the click theorem's r) | r = 1 (r_D / r_0 at equal crowds) | 1 | 0 | 0 | 1 / gamma = 1 - beta^2 / 2 - beta^4 / 8 | -1/2 | -1/8 | 1 |
| N_par / N_0, the path along | gamma^2 = 1 / (1 - beta_eff^2) | 1 | +1 | +1 | 1 (its own time; the ground reads gamma: +1/2, +3/8) | 0 | 0 | 1 |
| N_perp / N_0, the path across | gamma = 1 / sqrt(1 - beta_eff^2) | 1 | +1/2 | +3/8 | 1 (the ground reads gamma) | 0 | 0 | 1 |
| N_par / N_perp, the quotient in the detector's own count | gamma | 1 | +1/2 | +3/8 | 1 (Michelson and Morley's null) | 0 | 0 | 1 |

with beta_eff = beta (1 + c_f k_p) / (1 + k_b) carrying the crowd's term
separately: the coefficient at v^2 is multiplied by ((1 + c_f k_p) / (1
+ k_b))^2 and at v^4 by its square (no crowd: 1). The zeroth order is
Newton's, every ratio 1, absolute time: the tick Outside equals the tick
Inside times r_D whatever the motion, and the light clock's period is 2
L / c whatever the motion. The second order is where Einstein's forms
live, and it is there, at order v^2 and not later, that the law as
built departs from Einstein's form: by the term +beta^2 along and
+beta^2 / 2 across in the detector's own count, which is exactly the
count's missing rate (the law's r = 1 against 1 / gamma, the click
theorem's one free number: DERIVATION.md sections 2 and 3) and, along,
the uncontracted length (ALGEBRA 5.1, L_D / L_0 = r_D). The click
theorem's correction of relative order m^2 v^2 / 6 is NOT this
departure: it is what would remain of Einstein's form under the
hypothesis (A2) once the line k_AB = k_BA is imposed, an amplitude's
correction beyond the law as built, which has no such line; the law's
departure is the whole beta^2 term. The v^4 coefficients follow the
same two roots: along 1 = gamma^2's, across 3 / 8 = gamma's. On the
lattice one factor stands outside the expansion: the comb's c / c_D =
1.0077 on the across path, of order v^0, an anisotropy of the fan and
not a term in v (section 2.3).

**(b) The convergence in numbers.** The exact fractions beside gamma
and gamma^2 as k grows (COMPUTATION; the across fraction on the
direction D_f of section 2.3, extended by the same search to k = 33, D_f
= (38, 723, 0), T_D = 80256, and k = 65, D_f = (138, 5177, 0), T_D =
574080):

| k | beta = 55 / (32 k) | N_par / N_0 exact | 1 + beta^2 | gamma^2 | N_perp / N_0 exact | c / c_D | gamma_D | gamma | 1 + beta^2 / 2 | N_par / N_perp exact | gamma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 55/96 = 0.57292 | 9216/6191 = 1.48861 | 1.328234 | 1.488613 | 448/363 = 1.23416 | 1.007704 | 1.224724 | 1.220087 | 1.164117 | 52272/43337 = 1.20617 | 1.220087 |
| 5 | 11/32 = 0.34375 | 1024/903 = 1.13400 | 1.118164 | 1.133998 | 768/715 = 1.07413 | 1.007634 | 1.065988 | 1.064893 | 1.059082 | 2860/2709 = 1.05574 | 1.064893 |
| 9 | 55/288 = 0.19097 | 82944/79919 = 1.03785 | 1.036470 | 1.037851 | 15984/15565 = 1.02692 | 1.007724 | 1.019049 | 1.018750 | 1.018235 | 2988480/2957003 = 1.01064 | 1.018750 |
| 17 | 55/544 = 0.10110 | 295936/292911 = 1.01033 | 1.010222 | 1.010327 | 39168/38665 = 1.01301 | 1.007738 | 1.005231 | 1.005150 | 1.005111 | 2629220/2636199 = 0.99735 | 1.005150 |
| 33 | 5/96 = 0.05208 | 9216/9191 = 1.00272 | 1.002713 | 1.002720 | 1216/1205 = 1.00913 | 1.007738 | 1.001380 | 1.001359 | 1.001356 | 173520/174629 = 0.99365 | 1.001359 |
| 65 | 11/416 = 0.02644 | 173056/172935 = 1.00070 | 1.000699 | 1.000700 | 57408/56947 = 1.00810 | 1.007737 | 1.000355 | 1.000350 | 1.000350 | 11844976/11932515 = 0.99266 | 1.000350 |

Read: the along ratio is gamma^2 exactly at every k (the fraction is
gamma^2), and gamma^2 approaches 1 + beta^2, Newton's 1 plus the second
order, as k grows (k = 3: 1.489 against 1.328; k = 65: 1.000700 against
1.000699): the approach of Einstein's second order to Newton's zeroth,
in the law's own fractions. The across ratio approaches not 1 but c /
c_D = 1.0077: at k >= 9 the lattice's anisotropy is the whole excess
(k = 65: 1.00810 against gamma 1.00035), and the quotient N_par / N_perp
falls below 1 from k = 17 on for the same reason (0.9927 at k = 65
against Einstein's 1 and the law's continuum gamma 1.00035): it is
gamma^2 / ((c / c_D) gamma_D), near gamma_D / (c / c_D), only because
the resting clock and the along arm are on the heading while the across
arm is on D_f, and it is gamma_D exactly when both arms and the control
are on one direction class (Reviewer 3's gate 2). Divided
by c / c_D the across fraction is gamma_D to six digits at every k, so
the convergence across is Einstein's gamma once the fan's grain is
declared out, and the comb otherwise; the resting clock read on the
same direction class removes it (section 2.3).

**(c) The chain in one paragraph, from the board to above the board.**
Inside (GAMEBOARD): the packet hops at c on the board, m_D(tau) =
floor((2 tau S_1 Q + T_D) / (2 T_D)) Links by its age (`nature_beam.py`
:829-831, the carry :3882), and the body hops one Link per k
self-creations by its drive (`engine.py` :917-920, the wall `world.py`
:472), its held content on its record moving with it (:1009-1011). The
first arrow, one declared step: the detector's count under the age wall,
`entry.age += 1` where nothing is owed and one interval paid per owed
count (`engine.py` :699-706, :735-743), r_D = d / (d + A n), the same
primitive for the resting and the moving body, no rate from outside.
The second arrow, one declared step: the return of the detector's own
packet to its held mass, the click of the re-stamped row at the
detector's set as it stands now (`nature_beam.py` :3318-3323, the click
:5533-5572, the stamp :5549-5550), n_1 - n_0 a whole number of the
detector's own ticks (Outside, DETECTOR; n_0's stamp on the birth line
pending on branch birth-stamp, section 1). From these two arrows the
closed forms of section 2 follow by arithmetic alone: T_par = 2 L c /
(c^2 - v^2) + delta_E, T_perp = 2 L T_D / (Q d_y) + delta_E, N = r_D T,
and their ratios gamma^2, (c / c_D) gamma_D and gamma; their expansion
in v is Newton's at the zeroth order and Einstein's forms at the second,
with the law's coefficients of table (a) against Einstein's as the
things compared with. Nothing above the board is added: no rate, no
metric, no c^2 as an input; every arrow is a code line of the law as
built, and Einstein's form is reached in the comparison, not derived
from nothing (record 1097's words).

**(d) What was done once already, cited and not repeated.** The click
theorem ([DERIVATION.md](../click_frame/DERIVATION.md) sections 0 to 3):
the conversion from the lattice's momentum to motion read by clicks is
Lorentz up to corrections of relative order m^2 v^2 / 6 under (A2),
exact in the continuum limit, given the line k_AB = k_BA, and the law
as built has r = 1 with the two one-way factors 1 / (1 - v) and 1 + v.
[Einstein Outside](../einstein_outside/DERIVATION.md) section IV: SR
PARTLY (every r-free ratio of one detector's counts is Lorentz's on the
law; every scaled formula is the one unknown r, fixed at 1 by the law),
GR PARTLY at first order (the clock in a crowd the image of the age
wall). [Newton from the clicks](../newton_clicks/NEWTON_FROM_CLICKS.md)
section 0: Newton's form shown exactly in the algebra of the clicks with
no expansion in the velocity, its scale the click theorem's r. This tick
algebra agrees with all three where they meet (r = 1 on the law, the
ratios r-free or carrying r alone, the crowd's clock the age wall's
image) and adds what they did not carry: the crowd's three terms as
exact factors on beta^2 with their signs and their cancellation when
uniform, the receiver's count delta_E as the factor T_0 / (T_0 +
delta_E) on the ratios' excess, 1 at suspension 0 and below 1 by order
beta^2 / L in a crowd, the across clock's exact lattice direction and the comb's
factor c / c_D that dominates it at k >= 9, and the atomic tick (every
pin a whole number of the detector's own ticks, the closed form its
mean).

## 7. The three tests, on every rule used; nothing enters the law

No rule is added: every step above is a reading of rules already in the
law (the self-creation under the age wall, the flight's carry, the
drive's carry, the transponder's re-emission, the click at the
detector's set), each of which passed the three tests where it entered
(BEAM_LAW section 3; clock-age-v1, NOTE section 7; PINS_R2 section 7).
Stated again, one line each, for the rules this algebra reads:

- The count under the age wall (`by_drive(acc_owed, A n, d)`): generic,
  one primitive with the declared pair [n, d] and no family name;
  vector, the translation of an accumulator by its rate with the
  remainder kept, no root; local, its own record and the reading set of
  its Node, nothing kept at the Node.
- The flight's and the drive's carries: generic (the tables' declared
  integers), vector (the same translation, at most one Link), local (the
  row's own residue; the body's own drive).
- The return as a click at the detector's set as it stands now: generic
  (every body alike, the engine branches on no name); vector (the
  evaluation at the arrival, the click's one-way border); local (the
  detector's own Nodes and what arrives there).
- The across direction D_f: a declaration of the fan (the world's
  `directions`), not a rule; its isqrt is taken at load as every T_D is.

The closed forms of sections 2 to 6 are COMPUTATION, the law's own
numbers before any run; gamma, gamma^2, Einstein's ratio 1 and Newton's
absolute time are NATURE's forms, the things compared with; a run that reads the clicks would show
whether the law as built matches nature here (it is expected not to,
gamma^2 and (c / c_D) gamma against 1), and nothing in this file says
that it is nature. The light clock's pins are the Light Clock Runner's
(`LIGHT_CLOCK.md`); this file moves none and adds none.

## 8. Links

- `PINS_R2.md` (the transponder E, the closed forms t_- and
  t_+, the band, the style of the pins); [PINS.md](PINS.md) section 2 and
  [RUNS.md](RUNS.md) section 4 (a row of the own number is `home`, not a
  click).
- [The click frame](../click_frame/DERIVATION.md) sections 0 to 3 (the
  click theorem; r = 1 on the law; the two one-way factors);
  [ALGEBRA.md](../../ALGEBRA.md) 4.1, 4.2 and 5.1.
- [The crowd clock](../crowd_clock/DESIGN.md), [the clock's word](../clock_age/NOTE.md),
  [the moving detector](../moving_detector/DESIGN.md) and its
  [preregistration](../moving_detector/PREREGISTRATION_V2.md), [the
  reader's clock](../reader_clock/DESIGN.md): what they derived is cited
  above and not repeated.
- [ENGINE.md](../../ENGINE.md) (the world keys `clock_stamp`,
  `suspension`, `age_bound`; what comes home); [BEAM_LAW.md](../../BEAM_LAW.md)
  section 3 (the interval's six steps); [TERMINOLOGY.md](../../TERMINOLOGY.md)
  (Inside and Outside; a detector's clock).
- [Einstein Outside](../einstein_outside/DERIVATION.md) section IV;
  [Newton from the clicks](../newton_clicks/NEWTON_FROM_CLICKS.md)
  section 0 (cited in section 6 (d), not repeated).
- Highlights 5.4, the lines of records 678, 709, 768, 1139, 1196, 1201,
  1216 and 1217; the owner's words of records 1232, 1234 and 1235 as the
  Boss relayed them.
