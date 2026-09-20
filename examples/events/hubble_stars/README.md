# Series G2: the Hubble diagram with stars behind the detector, under the Beam Law, in space

Nine worlds of one base, written by `make_worlds.py` with their expectations
(`expectations.json`, written before the runs); the register entry is
drafted at the end of this page and is NOT in
[the experiments register](../../../docs/EXPERIMENTS.md) until the model
owner says so. The model owner's question (2026-09-20): "Can you run on a
separate machine a test of whether dark energy is needed? What comes out of
an experiment in our model? A star has to be placed there." So: on the Beam
Law engine as it is, a Hubble diagram whose sources are STARS of the
catalog's kind ([the catalog](../../../docs/ENTITY_CATALOG.md), "the sun, a
star of content M"): a measured event with content, the universal gravity
column with the sign minus, that is also a lamp (it releases light on its
clock, each unit costing it E = h f). Twenty-four stars thrown from a centre
with a Hubble-flow initial condition (speed proportional to distance, the
momenta as labels), the model's own gravity between them acting (the
coupling on the columns), a detector at the centre reading the arrivals with
`reads: "age"`; per star the redshift z from the arrival gaps against the
flight-time distance, the luminosity (the click rate), and a fit of the
deceleration q: decelerating, coasting or accelerating; against the observed
q about -0.55, the matter-only q > 0 and the coasting q = 0; gravity on,
gravity off (the coasting control) and a doubled mass; the clock choice
(scalar, age, and none) as series G did. A research run under the
[experimenter skill](../../../skills/experimenter/SKILL.md), made once,
never a test; the design, the derivation and the expectations were written
before the runs; a reading outside its expectation is reported with its
numbers, never moved. Every number is labelled a **detector reading** (the
record of the detector's set or of a measured event: the only kind reality
has) or a **GameBoard reading** (the host's view: a star's position, steps,
momentum, the rows it read, the books; the picture and the checks, never
the measurement).

Series G's lesson ([G](../../../docs/EXPERIMENTS.md#g-the-hubble-diagram-behind-the-detector-2026-09-20),
its follow-up and [record 60](../../../docs/LOG_2026-09-20.md#60-recorded-series-gs-surprise-is-not-a-finding))
shaped the reading: the sources are thrown from ONE point (a Hubble flow, so
no initial-distance offsets), every form is fitted with H FREE over every
point (the near fit through the origin read the coasting form's own
curvature as a larger H), the deceleration is read off a two-parameter
family (H and q free) and not off "the nearest of three forms", the
criterion was validated on the exact expected form at the worlds' own taus
before the runs (the tool prints that validation), and the grain's effect
on q was measured on the exact form (0.07, one standard deviation) before
the brackets were set.

## The throw

An open cube of 301^3 Nodes, the centre c = (150, 150, 150), `"law": "beam"`,
N 64, 400 intervals, `width` S = 2^20, `release` [1, 2^16].

- **The stars.** Twenty-four measured events, each of a paid family of its
  own (`s_px1` .. `s_mz4`: the axis and the rank, so that the detector's
  record tells the star by the family of its light), each ONE measured
  event that holds a mass and is a lamp: `held` {"mass": M} (the free family
  `mass`, `charge` 0, no phase circle; M = 2^22, or 2^23 in the `double`
  crowd) and `lamp` {"rate": [1, 1], "directions": [the heading toward the
  centre]} on 4096 units of its own light (each unit released costs
  `quantum` x turn = 1 content, E = h f, and carries the star's clock phase
  at birth; 400 of the 4096 are spent over the run). The star's gravity is
  its mass rows, released at every self-creation on the two headings of its
  axis (`directions`): M x `release` = F = 64 rows per direction per
  self-creation (128 in `double`), each a row of amount F (one row, amount
  64). The catalog placed the sun as TWO events at adjacent Nodes; since
  `held` landed ([BEAM_LAW note 31 (viii)](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
  one event pulls and shines, and this series is the first to place it so.
- **The Hubble flow.** The star at the initial distance r_0 has the speed
  v = r_0 / T_0 Links per interval with T_0 = 90 intervals: every star as
  if thrown from the centre 90 intervals before the run. r_0 = 3 .. 26
  Links, one integer per star, dealt round-robin over the six axes in Port
  order (+x gets 3, 9, 15, 21; -x 4, 10, 16, 22; ... -z 8, 14, 20, 26), so
  the farther star on an axis is the faster and none overtakes another
  (a step onto an occupied Node is a contact). The speeds run from 0.057 c
  to 0.497 c (c = 32 / 55 Links per interval on a heading, read off the
  flight table). The momentum is the label p = Q S M_total v / (1 - v)
  ([BEAM_LAW section 3](../../../docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
  step 5; M_total = 4096 + M, the content the step rule reads; the table
  `make_worlds.py` prints). The clock turns ONE step of the circle per
  self-creation: K = M_total.
- **The detector.** ONE measured event of the paid family `detector` (it
  releases nothing) at the centre declared as the detector `centre` of one
  Node reading `wave`; its table entry for every star's light is `{"rule":
  "measure", "reads": "age"}`, so every click record carries the age moment
  of the row (its flight time) and the `record` line the pointer's phase
  (the star's clock at birth). The mass rows reach the detector too and go
  on (`read` on a fixed event: the push taken by nothing) to the other side
  of the line. The light of every other star passes a star (`pass`): the
  inner stars are transparent; the clock counts it all the same.
- **The gravity between the stars.** On an axis a beam does not dilute
  (series C), so every star's rows reach every other star on its line, the
  opposite chain included: the model's own gravity here is the gravity of a
  line, a constant pull per row whatever the distance, toward the emitter
  (kappa = -M_A). The net pull on a star is the rows from the stars nearer
  the centre and from the whole opposite chain minus the rows from the
  stars farther out on its own chain: inward, growing with the rank, the
  one-dimensional "mass inside" (Newton's shell theorem holds in one
  dimension, and the six chains are three independent lines, x, y and z,
  each of eight stars). A star's speed changes by (1 - v)^2 x amount / S
  per row whatever its mass (the equivalence principle): what "mass" means
  here is the rows a star releases.

## Three crowds, three clocks: the nine worlds

| World | The mass a star holds | F | The `mass` entry at a star | The clocks count | `suspension` |
| --- | --- | --- | --- | --- | --- |
| `coasting_<clock>` | 2^22 | 64 | `pass` (the coupling off: the rows pass, the clock counts them, nothing pushes) | nothing / the presence / the age moment | 0 / [1, 2^16] / [1, 2^23] |
| `gravity_<clock>` | 2^22 | 64 | `read` (the push taken, the rows go on) | the same | the same |
| `double_<clock>` | 2^23 | 128 | `read` | the same | the same |

The clocks (series E's pair): every star's clock owes `by_clock(age,
counted, d)` intervals after each self-creation, `counted` the presence of
the rays of other numbers at its Node (`scalar`) or their age moment
(`age`; every table entry `reads: "age"`); a star that owes neither
releases nor steps that interval, so its clock slows its light and its
motion alike. The `none` clock (`suspension` 0) was added after the first
six runs read the clocks' scatter (below) as the control that isolates the
throw and the push from the clocks; it runs under the same brackets.

## The derivation, before the runs

**The redshift.** The star turns rho = 1 step per self-creation and
releases one light row per self-creation; over a window the arrivals'
pointer turns Delta Phi steps in Delta t detector intervals, so 1 + z =
Delta t / Delta Phi = (1 + k)(1 + v / c), k the clock's owed count per
self-creation and v the star's speed at emission: the acoustic Doppler of
a source receding through the GameBoard times the emitter's clock (series
G's formula, 288 of 288 inside there). The distance: a row clicked at the
age tau crossed m(tau) Links on its heading (the flight table); tau is the
light-travel time.

**The luminosity.** The click rate of a star's light per detector
interval is the lamp's rate (1 per self-creation) times the emitter's rate
1 / (1 + k) times the Doppler 1 / (1 + v / c) = 1 / (1 + z): expected 1 /
(1 + z) within 5 %. A beam does not dilute, so the click rate carries NO
distance beyond the redshift: the luminosity distance, the observable that
decides q in nature, this world cannot read (the paper's 1 / D^2 dilution
was an assumption there too; [HYPOTHESES section 7](../../../docs/HYPOTHESES.md)).

**The coasting throw from one point is the Milne form exactly.** A star of
speed v from the centre at the time -T_0 is observed at t_0 with 1 + z =
1 + v / c at tau = (v / c)(t_0 + T_0) / (1 + v / c), so z = H tau / (1 -
H tau) with H = 1 / (t_0 + T_0): q = 0 and H (t_0 + T_0) = 1 exactly, no
offset (the tool's validation prints this at the worlds' own taus: the
power-law family reads q = 0.000, H (t_0 + T_0) = 1.0000, rms 0; the
near fit through the origin would read H (t_0 + T_0) = 1.15, series G's
bias, printed and not used).

**The forms.** Three exact forms in the light-travel time, each with its
best H over every point: q = +0.5 (Einstein-de Sitter), q = 0 (Milne) and
q = -0.55 (flat Omega_m = 0.3, what is observed today); and the power-law
family a ~ t^n, 1 + z = (1 - (1 + q) H tau)^(-1 / (1 + q)), with H and q
free, whose q is the reading of the deceleration. At z <= 0.5 the three
fixed forms with H free differ by less than the grain (series G's
follow-up: 0.005 rms at z <= 0.6), so "the nearest of the three" is
printed and not pinned in the coasting crowd; q of the free fit is.

**The grain.** The digital step's grain (0.003 in z and one interval in
tau, series G's) moves q by 0.07 (one standard deviation over sixty draws
on the exact form) and H (t_0 + T_0) by 0.01: the coasting bracket on q
is +- 0.25, three and a half of that.

**The pushing throw (the continuum derivation, `throw_derivation` in the
generator; a GameBoard expectation).** On each line every star releases F
rows per direction per interval; the rows of a star l reach a star j at
the acoustic rate F (c - u_r) / (c - u_s) (u_s, u_r the two speeds along
the row's heading) once the first row has crossed the distance between
them; a row moves j's speed by (1 - |v_j|)^2 F / S toward l; the outward
rows of a moving star are partly taken home (a star that steps into the
Node of the row it just released, the fraction |v|, re-created half inward
and half outward: the outward beam (1 - |v|) / (1 - |v| / 2) of F, the
inward 1 / (1 - |v| / 2)); the clocks, the flight table's grain and the
step rule's grain are ignored and flagged. The light of each star at the
window's centre t_0 leaves at the t_e with t_e + |x(t_e)| / c = t_0; z =
|v(t_e)| / c, tau = t_0 - t_e. Derived at t_0 = 350: `gravity` q = +0.245,
H (t_0 + T_0) = 0.933, |p(end)| / p(0) from 0.67 to 1.11 (the inner stars
of the fast lines GAIN speed: the rows of the receding opposite chain
arrive at the reduced acoustic rate while the slowly receding outer stars
of the own chain pull nearly in full); `double` q = +0.594, H (t_0 + T_0)
= 0.854, |p(end)| / p(0) from 0.28 to 1.27. At the first design (M = 2^20,
F = 16) the derivation read q = +0.05, within the grain's reach of the
coasting form, which is why M is 2^22.

## The criteria, pinned before the runs (`expectations.json`)

- A record check (fails the tool): every run completed, the books balanced
  at every tick.
- **The windows**: the record read over [100, 200), [200, 300) and the late
  window [300, 400), t_0 the window's centre; every star with at least ten
  `record` lines in the window is a point; the late window is the
  registered reading.
- **The reading's formula** (every world, star and window): 1 + z from the
  pointer's turn against (1 + k)(1 + v / c) with k and v from the same
  record: within 2 %.
- **The luminosity** (every world, star and window): the click rate times
  (1 + z) = 1 within 5 %.
- **The coasting crowd** (the late window): q of the free fit within
  -0.25 .. +0.25; H (t_0 + T_0) within 0.9 .. 1.1; the nearest of the
  three forms any of the three (not pinned); |p(end)| / p(0) within 1 +-
  0.01 (GameBoard); k within 0 .. 0.05.
- **The gravity and double crowds** (the late window): q within the
  derived q +- the larger of 0.2 and half the derived deceleration
  (`gravity` +0.04 .. +0.44, `double` +0.30 .. +0.89); H (t_0 + T_0) within
  10 % of the derived (0.84 .. 1.03; 0.77 .. 0.94); the nearest of the
  three forms q = +0.5 or q = 0 and the farthest q = -0.55; |p(end)| /
  p(0) within the derived spread widened by half of itself (0.51 .. 1.16;
  0.00 .. 1.41) (GameBoard); k within 0 .. 0.05.
- **The ordering** (per clock): q_coasting < q_gravity < q_double with
  every gap above 0.1.
- **What is observed today** (every world): whether q = -0.55 is the
  nearest of the three forms. Expected NOT the nearest in every world.
- **The bend of the age clock** (each pair): z_age - z_scalar per star,
  reported, no bracket.

## Run and read

```bash
PYTHONPATH=src python examples/events/hubble_stars/make_worlds.py          # the worlds and expectations.json
PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/hubble_stars examples/events/hubble_stars/*_none.json examples/events/hubble_stars/*_scalar.json examples/events/hubble_stars/*_age.json
PYTHONPATH=src python tools/hubble_stars_readings.py artifacts/hubble_stars [--png DIR] [--json FILE]
PYTHONPATH=src python examples/events/hubble_stars/make_worlds.py --after  # derivation_after_the_runs.json (below)
```

`tools/hubble_stars_readings.py` reads the engine's own record
(`events.jsonl`, `run.json`, `initialization.json`) and the flight table
through the engine's own function, prints the validation of the criterion
on the exact coasting form at the worlds' taus, the record checks, the
table per star per window (v / c declared; z, k, v / c, tau, d and the
click rate from the record; v / c from the `step` lines, the push taken
over p(0), |p(end)| / p(0), the step rule's longest stall and burst), the
fits (the three forms with H free, the power-law family with H and q free,
the near fit and the free quadratic for continuity with series G), the
Doppler part alone, the bends, and every criterion inside or outside; the
runs take 36 to 39 s each (the 301^3 GameBoard's per-interval arrays), the
tool 15 s. `tests/test_hubble_stars_readings.py` pins the tool to the
engine on a bar of 61 Nodes and the shipped worlds to the generator.

## What the law lacked for this experiment (found while making it)

1. **A body's own motion does not Doppler what it reads.** Measured on a
   bar before the analysis (the scratchpad probe, 700 intervals): a fixed
   source releasing one row per interval toward a free body of content
   2^20; the body at rest, moving away at 0.30 and 0.45 Links per interval
   or toward the source at 0.30 reads exactly 1.000 row per interval in
   every case (200 in 200 intervals), where the flux through a moving
   surface would be (c - v) / c = 0.48 and 0.23 receding and (c + v) / c =
   1.52 approaching. The law reads the rows that STEP INTO the body's Node
   in the interval (BEAM_LAW step 4, the arrivals), and a body that steps
   onto a Node misses the rows there, so its own motion neither adds nor
   removes any: the rate is the beam's density times c, F c / (c - u_s),
   the EMITTER's Doppler alone. The derivation pinned before the runs had
   the acoustic factor (c - u_r) on the reader too; with it dropped
   (`make_worlds.py --after`, `derivation_after_the_runs.json`, not
   pinned) the derived |p(end)| / p(0) is 0.47 .. 0.90 for `gravity` and
   0.03 .. 0.79 for `double`, against the measured 0.42 .. 0.86 and 0.01 ..
   0.73 (the pinned 0.67 .. 1.11 and 0.28 .. 1.27 are outside on the low
   side, since no star gains speed once the reader's factor is gone), and
   the derived q is +0.86 and +1.50.
2. **The step rule under a changing momentum stalls and bursts.** The
   count of Links a body has made is `floor(age x |p| / (Q S M + |p|))`
   read at the CURRENT momentum (BEAM_LAW step 5, note 17: "the count is
   the whole part off the clock", "nothing is kept at a Node"), and a step
   fires when that whole part is one more than at age - 1. Under a
   momentum that falls steadily the argument age x |p| / D barely moves
   (age grows, |p| falls), so the body stalls for tens of intervals while
   its count stands still, then, when the argument sits just above an
   integer, fires at EVERY interval: `s_px1` in `gravity_none` stepped at
   the ticks 30, 62, 98, 141, 196, 297, 304 and then 321, 322, 323, 325,
   326, five Links in six intervals at a momentum that says 0.019 Links per
   interval; over the late window the longest stall is 42 intervals and
   the longest burst 4 Links (`gravity_none`), 85 and 11 (`double_age`),
   against 30 and 1 in the coasting crowd. The body's position tracks age
   x v_now: a decelerated star ends near where a coasting one would (`s_px1`
   at x = 165 against 166) although its momentum halved. The light a star
   releases while it stalls carries no Doppler and the light of a burst
   carries one beyond c: the detector's z per star per window is the
   average of a jerky motion, not of the momentum. The deceleration is in
   the momenta, not in the motion, and not in the light.
3. **The clocks' counts come in bursts.** The rows pass a star in the
   digital line's pattern, so the count a clock owes over a window is 0 to
   7 intervals where the design's mean is 1 (k of 0 to 0.068 per window;
   the whole-run rates 0.0025 to 0.0225): the scalar and age clocks scatter
   every star's z by up to 0.07 in a window, larger than the grain by an
   order, which is why the `none` clock was added.
4. **A moving star takes its outward rows home** (series G's finding): 832
   to 8416 rows per star came home over the run (the fraction v of the
   outward rows), re-created half inward and half outward.
5. **The gravity of a line, Doppler-weighted by the emitter only.** A beam
   does not dilute, so the crowd's pull is one-dimensional and constant per
   row; the six chains are three independent lines whose crowds differ
   (the x line's inner stars at 3 and 4 Links decelerate most), so the
   diagram is three diagrams superposed; the receding opposite chain pulls
   less (its rows arrive at the rate c / (c + v_l)) and the slowly receding
   own chain more: in three dimensions with dilution this is the shell
   theorem's failure under a retarded, rate-read gravity, which this world
   can only hint at.
6. **No luminosity distance**: the click rate is 1 / (1 + z) of the lamp's
   rate at every distance (631 of 648 inside 5 %), so the observable that
   decides q in nature is not readable here.

## The readings (2026-09-20, measured against expected)

Source fingerprint
`b4d074f2b762e58d15037a46b614e89609a48bcee2211eaf471af16e3d4923d1` (the
checkout of `claude/universe24-new-3ytqde` at `80e1776`, the trimming's
landing, with the worlds and the tool of this series on
`claude/series-g2-stars`), Python 3.14.0rc2, numpy 2.5.3, headless, four
cores, `--jobs 3`; every run completed in 36 to 39 s with the books
balanced at every tick; the tool: 0 record checks failed, the reading's
formula 648 of 648 inside 2 %, the luminosity 631 of 648 inside 5 % (the
17 outside all in the pushing crowds, where a star's stall or burst inside
a window moves its z against a click rate averaged over the window), 34
pinned readings inside and 29 outside, registered, none moved.

**The late window [300, 400), t_0 = 350** (detector readings unless
marked; the derived columns and the momenta are GameBoard readings):

| World | q (free fit) at t_0 = 150 / 250 / 350 | H (t_0 + T_0) at t_0 = 350 (Milne 1) | rms in z | nearest of the three forms | the Doppler part alone, q | k per star | p(end) / p(0) (GameBoard) | longest stall / burst (GameBoard) | q pinned | q derived, pinned (acoustic) | q derived after the runs (the source rule) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `coasting_none` | -0.22 / -0.08 / **-0.11 inside** | **1.026 inside** | 0.0019 | q = 0 | -0.08 | 0 | 1.000 inside | 30 / 1 | -0.25 .. +0.25 | 0.00 | 0.00 |
| `coasting_scalar` | -0.95 / -0.63 / **-0.10 inside** | **1.070 inside** | 0.0213 | q = -0.55 | -0.33 | 0.000 .. 0.068 outside | 1.000 inside | 31 / 1 | -0.25 .. +0.25 | 0.00 | 0.00 |
| `coasting_age` | -0.22 / -0.40 / **-0.09 inside** | **1.048 inside** | 0.0136 | q = 0 | -0.17 | 0.000 .. 0.054 outside | 1.000 inside | 30 / 1 | -0.25 .. +0.25 | 0.00 | 0.00 |
| `gravity_none` | +0.10 / +0.53 / **-0.76 outside** | 1.034 outside | 0.0479 | q = -0.55 | -0.64 | 0 | 0.423 .. 0.856 outside | 42 / 4 | +0.04 .. +0.44 | +0.24 | +0.86 |
| `gravity_scalar` | -0.95 / +0.58 / **-0.22 outside** | 0.956 inside | 0.0417 | q = -0.55 | +0.39 | 0.000 .. 0.048 inside | 0.417 .. 0.858 outside | 32 / 5 | +0.04 .. +0.44 | +0.24 | +0.86 |
| `gravity_age` | +0.04 / +0.63 / **+1.19 outside** | 0.818 outside | 0.0291 | q = +0.5 | +1.50 | 0.000 .. 0.035 inside | 0.433 .. 0.855 outside | 79 / 3 | +0.04 .. +0.44 | +0.24 | +0.86 |
| `double_none` | +0.64 / +1.50 / **+1.50 outside** | 0.664 outside | 0.0839 | q = +0.5 | +1.50 | 0 | 0.016 .. 0.707 inside | 68 / 10 | +0.30 .. +0.89 | +0.59 | +1.50 |
| `double_scalar` | -0.95 / +0.54 / **+0.54 inside** | 0.813 inside | 0.0992 | q = +0.5 | +1.50 | 0.000 .. 0.048 inside | 0.018 .. 0.728 inside | 60 / 12 | +0.30 .. +0.89 | +0.59 | +1.50 |
| `double_age` | +0.03 / +1.50 / **-0.11 outside** | 1.072 outside | 0.1525 | q = 0 | +0.02 | 0.000 .. 0.055 outside | 0.008 .. 0.700 inside | 85 / 11 | +0.30 .. +0.89 | +0.59 | +1.50 |

(q = +1.50 is the edge of the fit's grid; -0.95 its other edge.) The
ordering q_coasting < q_gravity < q_double: outside under every clock (the
none clocks read -0.11, -0.76, +1.50; the scalar -0.10, -0.22, +0.54; the
age -0.09, +1.19, -0.11). What is observed today, q = -0.55, is the nearest
of the three forms in 4 of the 9 worlds (`coasting_scalar`, `gravity_none`,
`gravity_scalar` and, by less than the grain, none of the others): outside
the expectation in those four.

**Per star, the late window, the two clock-free worlds:**

| star | v / c declared | `coasting_none`: z read | tau | the exact Milne z at that tau (H = 1 / 440) | `gravity_none`: z read | tau | v / c (steps) | p(end) / p(0) | stall / burst |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| s_px1 | 0.0573 | 0.0611 | 22.6 | 0.0542 | 0.1701 | 21.0 | 0.1383 | 0.423 | 17 / 3 |
| s_mx1 | 0.0764 | 0.0745 | 30.0 | 0.0732 | 0.0397 | 23.2 | 0.0362 | 0.549 | 2 / 1 |
| s_py1 | 0.0955 | 0.0937 | 37.1 | 0.0922 | 0.2382 | 42.9 | 0.2122 | 0.690 | 33 / 4 |
| s_my1 | 0.1146 | 0.1146 | 44.1 | 0.1113 | 0.0890 | 38.7 | 0.0747 | 0.748 | 26 / 2 |
| s_pz1 | 0.1337 | 0.1353 | 50.7 | 0.1302 | 0.1336 | 51.2 | 0.1383 | 0.831 | 18 / 2 |
| s_mz1 | 0.1528 | 0.1533 | 57.1 | 0.1493 | 0.1556 | 60.5 | 0.1618 | 0.856 | 15 / 2 |
| s_px2 | 0.1719 | 0.1706 | 63.4 | 0.1683 | 0.0824 | 53.4 | 0.0747 | 0.449 | 42 / 2 |
| s_mx2 | 0.1910 | 0.1905 | 69.4 | 0.1872 | 0.1867 | 63.6 | 0.2122 | 0.502 | 35 / 4 |
| s_py2 | 0.2101 | 0.2102 | 75.0 | 0.2056 | 0.1324 | 72.8 | 0.1185 | 0.576 | 20 / 2 |
| s_my2 | 0.2292 | 0.2264 | 80.7 | 0.2245 | 0.2408 | 79.9 | 0.2363 | 0.614 | 16 / 3 |
| s_pz2 | 0.2483 | 0.2478 | 86.2 | 0.2435 | 0.2435 | 78.8 | 0.2363 | 0.671 | 13 / 2 |
| s_mz2 | 0.2674 | 0.2636 | 91.6 | 0.2628 | 0.1967 | 90.4 | 0.2096 | 0.689 | 11 / 2 |
| s_px3 | 0.2865 | 0.2857 | 96.7 | 0.2816 | 0.1943 | 89.5 | 0.2363 | 0.494 | 18 / 3 |
| s_mx3 | 0.3056 | 0.3039 | 101.7 | 0.3008 | 0.2321 | 99.3 | 0.2096 | 0.522 | 14 / 2 |
| s_py3 | 0.3247 | 0.3257 | 106.7 | 0.3203 | 0.2928 | 100.8 | 0.2865 | 0.576 | 12 / 2 |
| s_my3 | 0.3438 | 0.3450 | 111.3 | 0.3387 | 0.3167 | 113.5 | 0.3532 | 0.606 | 9 / 2 |
| s_pz3 | 0.3628 | 0.3654 | 115.8 | 0.3572 | 0.2969 | 110.5 | 0.2902 | 0.645 | 8 / 2 |
| s_mz3 | 0.3819 | 0.3822 | 120.6 | 0.3775 | 0.3603 | 115.6 | 0.3532 | 0.657 | 7 / 2 |
| s_px4 | 0.4010 | 0.3999 | 124.7 | 0.3957 | 0.3136 | 122.0 | 0.3125 | 0.539 | 9 / 2 |
| s_mx4 | 0.4201 | 0.4179 | 128.9 | 0.4141 | 0.3196 | 127.4 | 0.3532 | 0.561 | 7 / 2 |
| s_py4 | 0.4392 | 0.4368 | 133.0 | 0.4332 | 0.3964 | 128.7 | 0.3581 | 0.597 | 7 / 2 |
| s_my4 | 0.4583 | 0.4583 | 136.8 | 0.4513 | 0.3724 | 129.5 | 0.3581 | 0.617 | 6 / 2 |
| s_pz4 | 0.4774 | 0.4743 | 140.9 | 0.4708 | 0.4647 | 140.2 | 0.4297 | 0.650 | 6 / 2 |
| s_mz4 | 0.4965 | 0.4922 | 144.5 | 0.4891 | 0.4117 | 142.0 | 0.4174 | 0.663 | 5 / 2 |

- **The reading's formula** (expected within 2 %): 648 of 648 inside, in
  every world, star and window: the redshift the detector reads of a star's
  light is the Doppler of its motion times its clock, exactly as derived.
- **The luminosity** (expected 1 / (1 + z) within 5 %): 631 of 648 inside;
  the click rate carries no distance beyond the redshift (a beam does not
  dilute).
- **The coasting crowd** (expected q within +- 0.25, H (t_0 + T_0) within
  10 %): inside under every clock. `coasting_none` reads the exact Milne
  form to the grain: q = -0.11 (the grain's 0.07 is one standard deviation),
  H (t_0 + T_0) = 1.026, rms 0.0019 in z, every star's z within 0.007 of the
  exact form's at its tau; the model's kinematics alone, from one point,
  give the coasting universe and nothing else. The clocks scatter it (rms
  0.021 and 0.014, k of 0 to 0.068 per star per window, outside the 0.05
  bracket in both) and in the early windows drive q to the grid's edge
  (-0.95 at t_0 = 150 with the scalar clock): a bursty count, not a bend.
- **The gravity and double crowds** (expected q +0.04 .. +0.44 and +0.30 ..
  +0.89, decelerating): on the GameBoard EVERY star's momentum fell, by 14
  to 58 % (`gravity`) and by 27 to 99 % (`double`), the inner stars of the
  x line the most, within 10 % of the derivation with the reader's Doppler
  factor dropped (found after the runs, item 1 above) and outside the
  pinned bracket in `gravity` (which expected some inner stars to gain). At
  the detector the deceleration is not read as a deceleration: `gravity`
  reads q = -0.76, -0.22 and +1.19 under the three clocks (all outside),
  `double` +1.50, +0.54 and -0.11 (one inside), the same world swinging
  from +0.53 to -0.76 between the middle and the late window
  (`gravity_none`), with an rms in z of 0.03 to 0.15, ten to eighty times
  the coasting control's. The cause is item 2 above, read in the per-star
  table: a decelerated star stalls for 17 to 42 intervals and then bursts
  (`s_px1` 3 Links, `s_py1` 4 Links on consecutive intervals), so its light
  in a window carries the Doppler of a jerky motion; `s_px1`, whose
  momentum fell to 0.42 of its start, reads z = 0.170 (three times its
  declared 0.057) because the late window caught its burst, while `s_px2`
  (0.45 left) reads 0.082 at a declared 0.172 because the window caught its
  stall. The three lines' different crowds add to the scatter.
- **The Doppler part alone** (the clock removed; not pinned): the same
  swings (`gravity` -0.64, +0.39, +1.50), so the clocks are not the cause
  of the gravity worlds' scatter; the step rule is.
- **The ordering** (expected coasting < gravity < double): outside under
  every clock.
- **The bend of the age clock** (reported): in the coasting crowd
  z_age - z_scalar per star within +- 0.07, the two bursty counts; the q of
  the pair -0.10 against -0.09 in the late window; in the pushing crowds the
  pair's q differ by 1.4 and 0.6, the step rule's scatter under each clock.
- **What is observed today** (expected not the nearest in every world): the
  nearest of the three forms in `coasting_scalar` (by the clocks' scatter,
  the coasting control `coasting_none` reading q = 0 nearest), `gravity_none`
  and `gravity_scalar` (by the stalls and bursts, every star decelerating on
  the GameBoard): outside in three worlds, not the nearest in six. As in
  series G, the detector shows the accelerating form's signature where
  nothing accelerates, and again from what the detector cannot see, here
  the step rule.
- Host cost: 36 to 39 s per run of 400 intervals (24 stars, about 12 000
  rows in flight on 301^3); the tool 15 s; the nine runs 5 minutes on three
  cores.

## The re-run under the record click (the owner's rule: through the click and the quantum)

The physicist's design, written after the first registration above and
before this re-run, is
[docs/designs/hubble_stars/DESIGN.md](../../../docs/designs/hubble_stars/DESIGN.md)
(its section 2.4 binds the reading). The nine worlds were written again by
`make_worlds.py --record` under the world key `amplitude` (`record/<world>.json`,
the detector reading `sum`, the model ids `rays-hubble-stars-record-<crowd>-<clock>-space-v1`;
not shipped until the key lands on main, since the base engine refuses it)
and run on the branch `claude/amplitude-impl` at commit `62369cb8` with its
`src` on `PYTHONPATH`:

```bash
PYTHONPATH=src python examples/events/hubble_stars/make_worlds.py --record
PYTHONPATH=<the branch's src> python tools/run_series.py --jobs 3 --out artifacts/hubble_stars_record examples/events/hubble_stars/record/*.json
PYTHONPATH=<the branch's src> python tools/hubble_stars_readings.py artifacts
```

Under the key every unit of a star's light is born as one record of one row
(the lamp's rate [1, 1]), the detector at the centre reads the record's
scope, and the tool takes every number from the `gather` lines, one click
per record (the record's birth phase `u` and the interval it `arrived`; the
click's `age`); the branch's own `tools/amplitude_path.py --check` replays
each run's register to its world's list (checked on `coasting_none`,
`gravity_none`, `double_age`: 7178, 6906 and 6879 gathers, all at `centre`,
the replay equal to `run.json`'s world). The worlds declare no `meeting`,
so the branch's limit on the shared birth phase (record 97) does not touch
them. Every run completed in 38 to 44 s with the books balanced, the
identity `amplitude-v1` on the record.

| World | q from the `record` lines (the first registration) | q from the `gather` lines (the record click) | H (t_0 + T_0) | rms in z | largest difference in z per star between the two readings | gathers per interval per star, mean |
| --- | --- | --- | --- | --- | --- | --- |
| `coasting_none` | -0.108 | -0.108 | 1.026 | 0.0019 | 0 | 0.794 |
| `coasting_scalar` | -0.105 | -0.105 | 1.070 | 0.0213 | 0 | 0.785 |
| `coasting_age` | -0.092 | -0.092 | 1.048 | 0.0136 | 0 | 0.788 |
| `gravity_none` | -0.760 | -0.760 | 1.034 | 0.0479 | 0 | 0.812 |
| `gravity_scalar` | -0.220 | -0.220 | 0.956 | 0.0417 | 0 | 0.812 |
| `gravity_age` | +1.192 | +1.192 | 0.818 | 0.0291 | 0 | 0.815 |
| `double_none` | +1.500 | +1.500 | 0.664 | 0.0839 | 0 | 0.864 |
| `double_scalar` | +0.539 | +0.539 | 0.813 | 0.0992 | 0 | 0.837 |
| `double_age` | -0.108 | -0.108 | 1.072 | 0.1525 | 0 | 0.814 |

The world's list of clicks is the first registration's click by click (the
clicks at the centre and the stars' steps compared line by line on
`coasting_none` and `coasting_scalar`: 7178 and 7126 clicks, equal), so
every reading agrees to the last digit: the reading's formula 648 of 648,
the luminosity 631 of 648, 34 pinned readings inside and 29 outside, the
same ones. The lattice is unchanged under the key and a record of one row
cancels with nothing; the record click adds to this series the one thing
the owner asked for, that its numbers are the world's rows and nothing
else. When the one click lands on main the `record/` worlds become the
shipped ones and the numbers are compared again.

## Verdict

The detector reads, of stars thrown from one point without gravity, the
coasting universe exactly: the Hubble law with H (t_0 + T_0) = 1.03 and
q = -0.11 +- 0.07, the Milne form to the grain, under the clock-free
control; the clocks of this law scatter it by their bursty counts but do
not bend it. With the model's own gravity on, every star's momentum
decelerates on the GameBoard (by 14 to 58 %, doubled 27 to 99 %, within
10 % of the derivation once the law's reading rule is used: a body's own
motion does not Doppler what it reads), and nothing in the law pushes any
star outward: the model has NO term that gives q < 0. But the detector
cannot read that deceleration as a q, because the step rule turns a
smoothly falling momentum into stalls of tens of intervals and bursts at
one Link per interval, so the light of a decelerating star carries the
Doppler of a jerky motion, the diagram scatters by 0.03 to 0.15 in z, and
the fitted q swings between -0.76 and +1.50 with the world and the window;
three of the nine worlds name the accelerating form q = -0.55 the nearest
while every momentum in them falls. To the owner's question the honest
answer is: in this model, on this engine, the Hubble diagram of gravitating
stars is not yet readable; what is readable is that the kinematics give
q = 0 and the gravity gives a deceleration in the momenta (q about +0.9 in
the derivation) and never an acceleration, so nothing here removes dark
energy and nothing here mimics it either, once the artefacts of the reading
(the clocks' bursts, series G's initial offsets, and now the step rule) are
named. What this reading cannot decide: the luminosity distance (a beam does
not dilute), the three-dimensional gravity of a crowd (the beams are lines),
and the motion of a decelerating body (the step rule). Nothing was tuned;
the 29 readings outside are registered as read.

## The register entry, drafted (not registered until the model owner says so)

### G2, the Hubble diagram with stars behind the detector (2026-09-20)

- **Confronts.** The model owner's question (2026-09-20): "Can you run on
  a separate machine a test of whether dark energy is needed? What comes
  out of an experiment in our model? A star has to be placed there."
  Twenty-four stars of the catalog's kind (one measured event holding a
  mass and shining as a lamp, E = h f) thrown from a centre with a
  Hubble-flow initial condition, the model's own gravity between them (the
  universal column, the rows on the axes), a detector of one Node at the
  centre reading `wave` with `reads: "age"`; per star the redshift from the
  pointer's turn, the distance from the arrivals' ages, the luminosity from
  the click rate; the deceleration q by a two-parameter fit (H and q free)
  and the three exact forms with H free; three crowds (the coupling off,
  on, doubled) and three clocks (none, scalar, age). Series G's lesson
  applied: one point, H free, the criterion validated on the exact form and
  the grain's effect on q measured before the brackets were set.
- **Model prediction, pinned before the runs
  ([the derivation](#the-derivation-before-the-runs),
  `expectations.json`).** The coasting crowd the exact Milne form, q within
  +- 0.25 and H (t_0 + T_0) = 1 within 10 %; the gravity crowd q = +0.25
  (+0.04 .. +0.44) and the double crowd q = +0.59 (+0.30 .. +0.89) by the
  continuum derivation with the acoustic Doppler on the emitter and the
  reader, |p(end)| / p(0) 0.67 .. 1.11 and 0.28 .. 1.27; the reading's
  formula within 2 %; the luminosity 1 / (1 + z) within 5 %; k within 0 ..
  0.05; the ordering coasting < gravity < double; q = -0.55 not the nearest
  in any world.
- **Features.** The held content (a lamp holding a free family, the first
  world to place the catalog's star as one event); the lamp's release with
  its clock phase and its cost; the push of the mass rows on the stars
  through the detector; `pass` for the other stars' light; `wave` on a set
  of one Node with the age moment on the click record; the clocks (the
  presence, the age moment, none).
- **Run.** `examples/events/hubble_stars/` (nine worlds by `make_worlds.py`,
  `<crowd>_<clock>`, the model ids `rays-hubble-stars-<crowd>-<clock>-space-v1`);
  `tools/run_series.py --jobs 3`; `tools/hubble_stars_readings.py`;
  `tests/test_hubble_stars_readings.py`.
- **Result (2026-09-20, measured against expected).** Fingerprint
  `b4d074f2b762e58d15037a46b614e89609a48bcee2211eaf471af16e3d4923d1`,
  Python 3.14.0rc2, numpy 2.5.3, headless; every run completed in 36 to
  39 s with the books balanced at every tick; the reading's formula 648 of
  648 inside, the luminosity 631 of 648 inside, 34 pinned readings inside
  and 29 outside, none moved (the table above). The coasting crowd: q =
  -0.11, H (t_0 + T_0) = 1.026, rms 0.0019 under the clock-free control
  (inside), inside under the scalar and age clocks with k scattering 0 to
  0.068 per window (outside its bracket). The gravity crowd: every momentum
  down by 14 to 58 % on the GameBoard, the detector's q -0.76, -0.22, +1.19
  under the three clocks (outside), rms 0.03 to 0.05; the double crowd:
  momenta down by 27 to 99 %, q +1.50, +0.54, -0.11 (one inside); the
  ordering outside under every clock; q = -0.55 the nearest of the three
  in three worlds (outside). Re-run under the record click (`amplitude-v1`,
  the branch `claude/amplitude-impl` at `62369cb8`, every number from the
  gather lines): the same list of clicks and the same readings to the last
  digit; the physicist's design `docs/designs/hubble_stars/DESIGN.md`.
- **Verdict.** The kinematics of the law give the coasting universe exactly
  from one point (Milne, q = 0 to the grain); the law's gravity decelerates
  every star's momentum and pushes none outward, so nothing in the law
  gives q < 0; but the deceleration is not readable at the detector,
  because the step rule stalls and bursts under a changing momentum and the
  light carries the Doppler of that jerky motion. Nothing here removes dark
  energy and nothing mimics it once the reading's artefacts are named. What
  the law lacked, registered: a body's own motion does not Doppler what it
  reads (measured on a bar: 1.000 row per interval at rest, receding at
  0.45 or approaching at 0.30); the step rule's count `floor(age |p| / D)`
  read at the current momentum (stalls of up to 85 intervals, bursts of up
  to 12 Links on consecutive intervals); the clocks' bursty counts; the
  outward rows taken home; the gravity of a line; no luminosity distance.
  Nothing was tuned.
