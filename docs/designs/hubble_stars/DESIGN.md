# Series G2, the physicist's design: is dark energy needed? Stars on the Hubble diagram behind the detector

The model owner, 2026-09-20: "Can you run on a separate machine a test of
whether dark energy is needed? What comes out of an experiment in our model?
A star has to be placed there." And, the same day, through the Boss: "send
it to the physicist" (the design before the runs) and "the mathematician
and the physicist must use the click and the quantum in their checks,
because they are behind a detector". This is the physicist's read-only
design under [physics-rule validation](../../../skills/physics-rule-validation/SKILL.md)
and [field development](../../../skills/field-development/SKILL.md): it
changes no law; it says what is measured, how, and what would count against
the model; the worlds, the tool and the readings are in
examples/events/hubble_stars/ (`examples/events/hubble_stars/README.md`, deleted 2026-09-26).

**The order as it happened, stated plainly.** The two briefs from the Boss
(the design first; every reading a record click) were queued at 11:32 and
11:54 UTC and read only after the first nine worlds had been run on the
base engine (the branch's law without the key `amplitude`) and reported.
Those runs stand as the first registration of the series, as series G's
first throw stands in its README; this design was then written, and the
worlds re-run under the record click on the branch `claude/amplitude-impl`
at commit `62369cb8` with the readings taken from the gather lines. Nothing
of the first registration was moved; its brackets were the ones this
design pins, since they were written before any run.

## 1. What "dark energy is needed" means operationally in this model

In nature the statement rests on the Hubble diagram of type Ia supernovae:
the luminosity distance against the redshift, whose second-order term is
the deceleration parameter q_0 = -(a a'') / a'^2 today. Matter alone gives
q_0 = Omega_m / 2 > 0; a coasting universe (Milne, a proportional to t)
gives q_0 = 0; the Pantheon+ Hubble-flow sample (1580 light curves, full
covariance; Scolnic et al., ApJ 938, 113 (2022); Brout et al., ApJ 938, 110
(2022); the release's own flat LambdaCDM fit Omega_m = 0.334, q_0 = Omega_m
/ 2 - Omega_Lambda = -0.50; the value -0.55 for Omega_m = 0.3 is the one
series G compared with) reads q_0 about -0.5: the expansion accelerates,
and "dark energy" is the name of whatever makes q_0 negative. The old
manuscript of this project ([paper/redshift/main.tex](../../../paper/redshift/main.tex))
put the same sample against the old engine's load histories and was behind
flat LambdaCDM by Delta chi^2 = 106 and 64; it concluded that nothing there
removes dark energy, the acceleration becoming "a load history not yet
derived".

In this model the question is operational only behind a detector. The
detector at the centre of a throw of stars reads, per star:

- **the redshift** z: the rate at which the star's light arrives with its
  clock phase advancing, against the star's own turn per self-creation
  (rho = 1 step): 1 + z = Delta t / Delta u over a window of clicks, t the
  click's interval and u the birth phase the record carries;
- **the distance** in the light-travel time: the age of the record at its
  click, tau, and d = m(tau) Links on the flight table (series E's
  reading, `reads: "age"`);
- **the luminosity**: the star's clicks per interval.

"Dark energy is needed" then means: the diagram of z against tau read at
the detector has q < 0 by the fit below where the model's own gravity
predicts q > 0. "Not needed" means either q >= 0 as read, or that the
model's gravity itself gives q < 0 (an acceleration from the law; there is
no term for one, section 2.3), or that the reading cannot decide (section
5), which is a result to register and not to smooth.

**The fit, stated so it can be attacked.** The family a ~ t^n in the
light-travel time, 1 + z = (1 - (1 + q) H tau)^(-1 / (1 + q)), fitted with
H and q both free by least squares in z over every star of a window (q = 0
is Milne, +0.5 Einstein-de Sitter, -1 the exponential form); beside it the
three fixed forms with H free (q = +0.5, 0, -0.55 flat Omega_m = 0.3). The
criterion is validated before the runs on the exact expected form at the
worlds' own taus (the tool prints it: q = 0.000, H (t_0 + T_0) = 1.0000 on
the exact coasting throw), and the grain's effect on q is measured on that
form (0.003 in z and one interval in tau move q by 0.07, one standard
deviation over sixty draws). What would count against the model: a coasting
throw read as q outside +- 0.25, or a gravitating throw read as q < 0 with
the momenta falling (an acceleration in the light the law does not carry),
or the three crowds not in the order coasting < gravity < double.

## 2. The star as the law has it, and what the detector reads

### 2.1 The star

A star is ONE measured event ([the catalog](../../ENTITY_CATALOG.md), "the
sun, a star of content M", placed here as one event for the first time
since the held content landed, [BEAM_LAW note 31 (viii)](../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):

- its family is a paid family of its own (`s_px1` .. `s_mz4`, `quantum` 1),
  its light: 4096 units of `amount`, and a `lamp` of `rate` [1, 1] on the
  one heading toward the centre; at every self-creation with a turn s > 0
  it releases one unit costing `quantum` x s = 1 content (E = h f: the cost
  is the phase rate), carrying the star's clock phase at birth; under the
  key `amplitude` that unit is born as ONE RECORD of one row of amount 1
  (the lamp's rate must be [1, 1] under the key, which it is), its
  identity the star's number x 2^32 + the birth's ordinal, its birth phase
  u the clock's phase;
- it `held`s a mass, `{"mass": 2^22}` (2^23 in the double crowd) of the
  free family `mass` (`charge` 0, `phase` false): the universal gravity
  column, value 1 with the sign minus, is every family's, so the star's
  content on that column is 4096 + M, the content the push reads (M_A) and
  the step rule reads; the held free family is released at the world's
  `release` [1, 2^16] on the event's `directions`, the two headings of its
  axis: F = M / 2^16 = 64 rows per direction per self-creation, its gravity
  (a free release costs nothing and takes no recoil);
- its clock turns one step of N = 64 per self-creation (K = 4096 + M, the
  turn `by_clock(age, content, K)` = 1 while the light spent, at most 400
  of the 4096, is 1e-4 of K) and, under `suspension` [1, d], owes
  `by_clock(age, counted, d)` intervals after each self-creation, `counted`
  the presence of the other numbers' rays at its Node (`scalar`, d = 2^16)
  or their age moment (`age`, d = 2^23, every entry `reads: "age"`): series
  E's reading, the clock under its own crowd, weak by design (k about
  0.01); with `suspension` 0 (`none`) the clock counts nothing.

### 2.2 The Hubble flow as integer momenta

Twenty-four stars on the six axes of an open 301^3 cube, the detector at
the centre c. The star at the initial distance r_0 Links has the speed v =
r_0 / T_0 Links per interval, T_0 = 90: every star as if thrown from the
centre 90 intervals before the run, one point and no offsets (series G's
artefact, section 3). r_0 = 3 .. 26, one integer per star, dealt round-robin
over the axes in Port order, so on each axis the farther star is the faster
and none overtakes another. The momentum is the label p = round(Q S M_total
v / (1 - v)) with Q = 64, S = `width` = 2^20, M_total = 4096 + M (BEAM_LAW
section 3 step 5: one Link per (Q S M + p) / p self-creations); the speeds
run from 0.057 c to 0.497 c, c = 32 / 55 Links per interval on a heading
read off the flight table. The momenta are integers between 3.6e12 and
5.7e13, within the label bound; the generator prints the table.

### 2.3 The mutual gravity as the coupling on the columns

The push a star takes from a group of another star's mass rows is the one
signed inner product over the columns (BEAM_LAW step 4, note 31; series C
measured it on the plane, series D on the orbit): with one column, gravity,
push_A = -M_A V_B per axis, V_B the label flow of the arriving rows (amount
x Q on a heading), toward the emitter. The speed changes by (1 - v)^2 x
amount / S per row whatever M_A (the equivalence principle): "mass" here is
the rows a star releases. On an axis a beam does not dilute (series C), so
every star's rows reach every star on its line, the opposite chain included
(they pass the detector: `read` on a fixed event pushes nothing and lets
the rows go on), and the six chains are three independent lines of eight.
The net pull on a star is the rows from the stars nearer the centre and
from the whole opposite chain minus the rows from the stars farther out on
its own chain: inward, growing with the rank, the one-dimensional "mass
inside". There is no term in the law that pushes two masses apart: q < 0
cannot come from the coupling; if the detector reads it, it comes from the
reading (section 3, section 5). The controls: `pass` on the mass rows at
every star (the coupling off; the rows still pass and the clocks still
count them) and M doubled.

### 2.4 What the detector reads

The detector is one measured event of the paid family `detector`
(releasing nothing) at the centre, declared as the detector `centre` of one
Node; its table entry for every star's light is `{"rule": "measure",
"reads": "age"}`. Every other star's light passes a star (`pass`); the
inner stars are transparent.

**Under the record click (the reading this design binds; the owner: "the
mathematician and the physicist must use the click and the quantum").** The
world key `amplitude` is true; the detector reads `sum` (the record's
scope: one record's rows over its lifetime, no pointer gate); every unit of
a star's light is one record of one row, and its click at the centre is
the completion of that record: the layer writes one `gather` line per
record with the record's identity, its family (the star), its birth phase
`u`, the interval `arrived` and the set chosen, and one `click` line with
the record's `age` (its flight time) and `reading` (the age moment). These
lines are the world's rows, and EVERY reading of the series is taken from
them:

- z per star per window: the least-squares slope of the unwrapped u
  (forward on the circle of N) against `arrived` over the gathers of the
  window, 1 + z = rho / slope with rho = 1;
- tau per star: the mean `age` of the window's clicks, d = m(tau) Links
  through the engine's `flight_table`; the emission interval of a click,
  `arrived - age`, gives the star's clock rate k and its speed v / c from
  the same lines (the reading's formula 1 + z = (1 + k)(1 + v / c) as a
  check on the lines themselves);
- the luminosity: gathers per interval, expected 1 / (1 + z) of the lamp's
  rate;
- the fits of section 1 over the window's stars.

What is NOT a reading: the rows in flight, the stars' momenta, their steps,
their `read` lines, the homes, the books. These GameBoard quantities appear
in the tool and the register as labelled controls only (the momentum left,
the push taken, the step rule's stalls and bursts), never in a comparison
with nature and never as evidence of what the world contains.

**The first registration** (before this design was read) took the same
numbers from the `record` lines of the detector under `wave` (the pointer's
phase per interval) and the `click` lines' age moments; under `sum` the
same clicks happen at the same intervals (the lattice is unchanged under
the key: the flight, the collision, the merge; a record of one row cancels
with nothing), so the two readings are expected equal to the last digit,
which the re-run checks.

**The meeting.** These worlds declare no `meeting` key, so the known limit
of the branch ([record 97](../../LOG_2026-09-20.md#97-k-under-the-record-click-the-offers-are-the-crowd-the-click-reads-the-shared-phase):
under the meeting the birth phase u is shared with the meeting's register
and the click reads the sharing; the fix in progress makes u the record's
own field) does not touch them: nothing here turns a row by its phase.
When the one click lands on main (the key removed, the record form the
only click), the worlds are re-run on main and the numbers compared.

## 3. Series G's artefact and how this design avoids it

Series G's pinned criterion was "the nearest of the three forms at the
NEAR fit's H", H fitted through the origin on z <= 0.2. The physicist's
review ([record 60](../../LOG_2026-09-20.md#60-recorded-series-gs-surprise-is-not-a-finding))
found (i) that the near fit reads the Milne form's own curvature, z = H tau
+ (H tau)^2 + ..., as a larger H (1.15 t_0 for an exact coasting throw), so
the far part of the coasting form itself lies below the coasting form at
that H and q = -0.55 is "the nearest" for a pure coasting throw: the
criterion would have failed on the expected form; (ii) that the sources'
initial distances r_0 shifted every source's Milne form by r_0 / c, the far
ones three times the near ones'; (iii) that the pushing crowd's clocks were
three to four orders above nature's with a distance gradient nature's
sources lack; (iv) that at z <= 0.6 the three forms with H free differ by
0.0055 rms, below the grain, so the ranking separated nothing. A false
surprise: "the detector sees acceleration while nothing accelerates".

This design: (a) a throw from ONE point (r_0 = v T_0), no offsets; (b) H
free in every fit, and the deceleration read off the two-parameter family
(H, q), not off a ranking of three; (c) the criterion validated on the
exact expected form at the worlds' own taus before the runs, and the
grain's effect on q measured there; (d) the ranking of the three forms
printed and NOT pinned in the coasting crowd; (e) the controls: the coupling
off (the same crowd, the same clocks, nothing pushes), the mass doubled,
the scalar and the age clock, and the clock-free world (`suspension` 0,
added after the first six runs read the clocks' scatter, k of 0 to 0.07 per
window: the world with no clock at all). A world "with no expansion at all"
(every momentum 0) reads z = 0 at every star by the reading's formula and
was not run: a star at rest at r_0 clicks at the constant gap of one
interval with u advancing one step per interval, 1 + z = 1 exactly, the
identity of the reading and not a control of the throw; the coupling-off
world is the control that keeps the throw and removes the physics.

## 4. The expected integers before any run, and the sizes

Pinned in `expectations.json` by the generator (the table per star: r_0, v,
v / c, p; the derived points per crowd and window; the brackets), before
any run:

- the coasting crowd: the exact Milne form from one point, z = v / c at
  tau = (v / c)(t_0 + T_0) / (1 + v / c): q within +- 0.25 (three and a
  half of the grain's 0.07), H (t_0 + T_0) within 0.9 .. 1.1, |p(end)| /
  p(0) within 1 +- 0.01, k within 0 .. 0.05;
- the gravity and double crowds: a continuum derivation of the line's push
  (F rows per direction per interval; the rows of l reaching j at the
  acoustic rate F (c - u_r) / (c - u_s); a row moving j's speed by (1 -
  |v_j|)^2 F / S toward l; the outward rows of a moving star partly taken
  home at the fraction |v|): q = +0.245 (bracket +0.04 .. +0.44) and
  +0.594 (+0.30 .. +0.89) at t_0 = 350, H (t_0 + T_0) within 10 % of the
  derived 0.933 and 0.854, |p(end)| / p(0) within the derived spread
  widened by half (0.51 .. 1.16; 0.00 .. 1.41), the nearest of the three
  forms q = +0.5 or 0 and the farthest -0.55;
- every world: the reading's formula within 2 %, the luminosity 1 / (1 + z)
  within 5 %, the ordering coasting < gravity < double with gaps above 0.1,
  q = -0.55 not the nearest form.

The integer form of every reading: u and `arrived` are integers on the
gather line, `age` on the click line; z is rho x (a least-squares slope of
integers), tau a mean of integers, d = m(round(tau)) an integer of the
flight table; the fits are floats over these. The sizes: 301^3 open, 400
intervals, the windows [100, 200), [200, 300), [300, 400) with the late
window registered; 36 to 39 s per world on one core (the per-interval
arrays of 301^3), nine worlds in five minutes on three cores; the tool 15 s.

## 5. What the run cannot decide

- **The closed against the open GameBoard.** The cube is open (the faces
  detectors; a closed GameBoard is refused under the Beam Law), so nothing
  returns and no global topology enters; the old paper's closed rows and
  their "delay growth" are not this engine.
- **The clock's load history of the old paper.** The old engine's redshift
  came from a load that slowed transport and not clocks; here a clock beside
  a crowd slows (series E), and its count is bursty (k of 0 to 0.07 per
  window against a mean of 0.01): a load history is not derived here
  either, and the clock-free control removes it.
- **The distance ladder.** There is no luminosity distance: a beam does not
  dilute, so a star's click rate is 1 / (1 + z) of its lamp's rate at every
  distance; the observable that decides q in nature is not readable, and
  the light-travel time stands in for the distance.
- **The three-dimensional crowd.** The gravity is a line's (beams on the
  axes, Doppler-weighted by the emitter's recession), three independent
  lines with different crowds; the shell theorem of a homogeneous crowd is
  not tested.
- **Found on the engine after the first registration, to be re-read under
  the record click** (the worlds' README, "What the law lacked"): a body's
  own motion does not Doppler what it reads (measured on a bar: 1.000 row
  per interval at rest, receding at 0.45 or approaching at 0.30), so the
  pinned derivation's reader factor is not the law's (a derivation with the
  emitter's factor alone is written beside it, not pinned); and the step
  rule's count `floor(age |p| / D)` read at the current momentum stalls
  and bursts under a falling momentum, so a decelerating star's light
  carries the Doppler of a jerky motion. Whether the gravitational q is
  readable at all is therefore the first question the record-click re-run
  answers, and it is registered as read either way.
