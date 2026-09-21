# Series G: the Hubble diagram behind the detector, under the Beam Law, in space

Four worlds of one base, written by `make_worlds.py`; the register entry is
[G, the Hubble diagram behind the detector (2026-09-20)](../../../docs/EXPERIMENTS.md#g-the-hubble-diagram-behind-the-detector-2026-09-20)
and the evidence is in [validation](../../../docs/VALIDATION.md). The model
owner's question (2026-09-20, [Highlights 5.4](../../../docs/HIGHLIGHTS.md#54-the-detector),
"DECIDED: series G"): "let it check whether what is observed today is also
seen in our detector." Sources thrown from a centre with a spread of
momenta, each a family of its own, each releasing rays with its phase; a
detector at the centre reads, per source, the redshift (the rate at which
the pointer of its record turns against the emitter's own rate) and the
distance (the age of the arriving rays, the flight time); the curve of
redshift against distance is compared in shape with what is observed today
(the linear law near, and far the supernova curve of an accelerating
recession, the deceleration parameter q about -0.55) and with the two
curves the law can give, a coasting recession (the Milne form, q = 0) and a
decelerating one (the push of the crowd, q > 0). A research run under the
[experimenter skill](../../../skills/experimenter/SKILL.md), made once,
never a test; the design, the derivation and the expectations below were
written before the runs; a reading outside its expectation is reported with
its numbers, never moved. Every number is labelled a **detector reading**
(the record of the detector's set or of a measured event: the only kind
reality has) or a **GameBoard reading** (the host's view of the GameBoard: a
source's position, its steps, its momentum, the books; the picture and the
checks, never the measurement).

## The throw

An open cube of 301^3 Nodes, the centre c = (150, 150, 150), `"law":
"beam"`, N 64, 400 intervals, `width` S = 2^20, `release` [1, 64].

- **The sources.** Twenty-four free measured events, each a free family of
  its own (`px1` .. `mz4`: the axis and the rank), thrown from the centre
  along the six axes: on every axis a chain of four sources of ranks
  i = 1 .. 4 at the initial distances r_0 = 1 + 2 i = 3, 5, 7, 9 Links, the
  faster the farther, so that no source overtakes another (a step onto an
  occupied Node is refused and its momentum is kept, [Highlights 5.4](../../../docs/HIGHLIGHTS.md#54-the-detector),
  the contact defect). A source of content M with the momentum p along its
  axis steps one Link per (Q S M + p) / p self-creations ([BEAM_LAW section 3](../../../docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
  step 5, Q = 64): its speed is v = p / (Q S M + p) Links per interval.
  The speed ladder: v = c x V(axis) x (2 i - 1) / 7 with V = 0.6, 0.55,
  0.5, 0.45, 0.4, 0.35 on +x, -x, +y, -y, +z, -z, twenty-four speeds from
  0.05 c to 0.6 c, c the ray's speed on a heading **read off the flight
  table** (`nature_beam.flight_table`: 32 Links per period of 55
  intervals, c = 0.58182 per interval; the momenta are in the table
  `make_worlds.py` prints). Every source releases at every self-creation
  one row of F rays on the heading toward the centre alone (`by_clock(age,
  M, 64)` = M / 64 per direction per self-creation): the carrier of the
  phase.
- **The phase.** A free family's release stamps the clock's phase on every
  ray born ([BEAM_LAW section 3](../../../docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
  step 5), and with `phase_per_link` 0 the phase is not turned in flight:
  the ray carries the emitter's phase at birth to the detector, and the
  click record shows it (the choice: free families, matter; a paid family
  would need a lamp that spends its content and pushes readers by its
  label). The emitter's clock turns ONE step of the circle per
  self-creation (`by_clock(age, M, K)` with K = M): the rate the redshift
  is read against.
- **The detector.** One measured event of the paid family `detector` (it
  releases nothing) at the centre declared as the detector `centre` of one
  Node reading `wave` (a set of one Node with one record: the sources aim
  exactly at it along the axes); its table entry for every source family
  is `{"rule": "measure", "reads": "age"}`, so the click record of every
  arriving row carries `reading` = the age moment of the row, amount x
  age (the flight time), and the `record` line of the interval carries
  the pointer and its phase; the family names the source. No second
  detector: the plain count is the number of click lines.
- **The mass inside.** Six fixed free measured events of the phase-less
  family `mass` at one Link from the centre on the six axes, inside every
  chain, each releasing on the outward heading of its axis alone: the
  crowd's mass inside every source, whose row pulls every source of the
  chain inward (kappa = -M_A: a free ray pushes its reader toward its
  emitter). On a line a beam does not dilute (series C: the count on an
  axis is constant with r), so the pull is the same at every rank; the
  inward rows of the 4 - i sources ahead of rank i pull it outward by
  (4 - i) F per interval, so the net pull on rank i is M_in - (4 - i) F
  per interval, M_in the mass's rows per interval: with M_in = 4 F it is
  i x F inward, the one-dimensional analogue of the mass inside the
  sphere, growing with the rank as the mass inside grows with the
  distance. The masses' table entry for every source family is `pass`
  (their clocks count the rows all the same).

## Two crowds, two clocks: the four worlds

The push a passing row gives a reader is one own-label unit per unit of
amount whatever the reader's content (kappa = -M_A, the equivalence
principle: `Delta n = amount` in units of Q M_A, [BEAM_LAW section 3](../../../docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
step 4), and the speed changes by (1 - v)^2 x amount / S per row. What
"light" and "heavy" mean here is therefore the number of rays a source
releases, M / 64 per row, at the one width S = 2^20.

| World | Crowd | The sources' content M (= K) | Rows | The masses' content | The clocks count | `suspension` |
| --- | --- | --- | --- | --- | --- | --- |
| `coasting_scalar` | coasting | 64 | F = 1 | 1 (one ray per 64 self-creations, a residual) | the presence | [1, 2^12] |
| `coasting_age` | coasting | 64 | F = 1 | 1 | the age moment (`reads: "age"`) | [1, 2^19] |
| `pushing_scalar` | pushing | 1024 | F = 16 | 4096 (64 per self-creation) | the presence | [1, 2^12] |
| `pushing_age` | pushing | 1024 | F = 16 | 4096 | the age moment | [1, 2^19] |

The speeds are the same in every world (p x F at M x F). The clocks
(series E's pair): every measured event's clock owes `by_clock(age,
counted, d)` intervals after each self-creation, `counted` the presence of
the rays of other numbers at its Node in the `scalar` worlds and their age
moment `sum amount x age` in the `age` worlds (every source's table entry
for every other family `{"rule": "read", "reads": "age"}`, every mass's
`{"rule": "pass", "reads": "age"}`): the emitter's clock beside the
crowd's rays. The detector's entries read `age` in every world (the
distance needs the age on the arrival record); its own clock paces nothing
(it releases nothing) and is reported.

## The first throw, and what it taught (before the registered runs)

The design as first written (in git before the registered worlds) released
a second row from every source away from the centre, as its field on the
sources behind it, and made the detector's measured event the centre's mass
(a free family releasing on the six headings). A run of forty intervals and
one of four hundred showed two things of the law, both registered here as
findings and neither changed:

- **A source that steps into the Node of the row it has just released
  takes it home.** The row is born at the source's Node in step 5 of the
  interval and the source steps in the same interval (`_move` after
  `nature_beam`); at the next interval the row walks one Link and arrives
  at the source's new Node, an own-number arrival, which the law takes home
  and creates again at the next self-creation on the source's declared
  directions with its arriving phase (`apportion_whole` over the two
  headings: half the returned rows went inward with a stale phase, half
  out again). A fast source (v = 0.35 Links per interval) recycled a third
  of its outward rows; the detector saw pairs of rows of one source in one
  interval with phases one step apart, and the group's age moment on both
  click records. The registered throw releases inward only.
- **The clock of a measured event that reads `age` beside every arrival
  runs slow.** The detector's entries read `age` in every world (the
  distance needs it), so its clock counted the age moment of every
  arriving row over the `scalar` worlds' denominator 2^12: at the centre,
  where every source's rows arrive, the count reached 0.25 (coasting) and
  2.4 (pushing) per self-creation, and as the centre was also the mass
  inside its release fell to 0.80 and 0.29 of the design, which reversed
  the pull on the inner sources. The registered throw separates the two:
  the detector is a paid family releasing nothing and the masses inside
  are six events at one Link, off the arrivals' end.

## The derivation, before the runs

**The redshift.** The emitter turns rho = 1 step per self-creation and
releases a row at every self-creation; consecutive rows leave from
positions that differ by the Links the source stepped between them, and
each Link costs 1 / c = 55 / 32 intervals of flight on a heading. Over a
window the arrivals' pointer turns Delta Phi steps in Delta t detector
intervals, so the reading

    1 + z = rho / (Delta Phi / Delta t) = Delta t / Delta Phi = (1 + k) (1 + v / c),

k the clock's owed count per self-creation (the emitter's rate 1 / (1 + k))
and v the source's speed at emission: the acoustic Doppler of a source
receding through the GameBoard at v from a detector at rest in it, times the
emitter's clock. There is no time dilation in the law (a clock's rate does
not depend on its motion) and no cosmological stretch (a ray's phase per
Link is fixed): the redshift is the Doppler of the throw and the clocks'
rates, nothing else.

**The distance.** A row clicked at the age tau crossed m(tau) Links on its
heading (the flight table, `manhattan_steps`; m(tau) = (128 tau + 110) //
220 on a heading), the distance of the source when the row left, d = m(tau)
Links; tau is the light-travel time. Both are read from the click record.

**The coasting throw is the Milne form.** A source of constant speed v
that left the centre at t = 0 is at d = v t_e when its light leaves at t_e
and is observed at t_0 = t_e + tau with tau = d / c: d = v t_0 / (1 +
v / c), and 1 + z = 1 + v / c = (t_e + tau) / t_e = t_0 / t_e. In the
light-travel time,

    z(tau) = H tau / (1 - H tau),  H = 1 / t_0,

the Milne form (a coasting recession, a proportional to t, q = 0) with
the Hubble time equal to the age of the throw: **H t_0 = 1**. Near, z = H
tau + O((H tau)^2), the linear Hubble law by itself; far, the Milne
curvature (1 + q / 2) H^2 tau^2 with q = 0. A source thrown from r_0 rather
than from the centre reads the same z = v / c at tau = (r_0 + v t_0) / (c +
v), the Milne form shifted by r_0 / c in tau, 5 to 15 intervals here: the
throw's own coasting form, which the tool prints beside the reading.

**The three forms compared.** With H fitted on the near part (z <= 0.2 by
the linear law through the origin) the far part is compared with the three
exact forms in the light-travel time, all equal to H tau + (1 + q / 2) (H
tau)^2 to second order:

- q = 0, the coasting form (Milne, a proportional to t): 1 + z = 1 / (1 - H tau);
- q = +0.5, the decelerating form (Einstein-de Sitter, a proportional to t^(2/3)): 1 + z = (1 - 1.5 H tau)^(-2/3);
- q = -0.55, the accelerating form observed today (flat, Omega_m = 0.3,
  Omega_Lambda = 0.7, q_0 = Omega_m / 2 - Omega_Lambda): 1 + z = [sinh A /
  sinh(A - 1.5 sqrt(Omega_Lambda) H tau)]^(2/3), A = asinh(sqrt(Omega_Lambda
  / Omega_m)) = 1.2099, H t_0 = 0.964.

In the light-travel time an accelerating universe expanded less in the
past, so its z at a given tau lies below the coasting form's and a
decelerating one's above it. The tool reports, per run and per window, the
rms of z against each form over the far part (z > 0.2) at the near fit's
H, the best H of each form over all sources with its rms, and the
effective q of a free quadratic fit z = a tau + b tau^2, q_eff = 2 (b /
a^2 - 1).

**The pushing throw decelerates.** The net pull on rank i is i F units per
interval inward (Doppler factors on the arrival rates aside), so a source
loses i F t (1 - v)^2 / S of its speed by the interval t: with F = 16,
S = 2^20 and t = 400 the fraction u lost is i F t (1 - v)^2 / (S v): 0.06
to 0.32 on the +x chain (V = 0.6, the inner ranks losing the larger
fraction) and 0.1 to 0.5 on the -z chain (V = 0.35). For a self-similar
deceleration by the fraction u at t_0 the diagram reads H t_0 = (1 - u) /
(1 - u / 2) < 1 and the quadratic coefficient (2 - 2 u + u^2) / (2 (1 -
u)^2), an effective q of 0.1 at u = 0.05 and 0.56 at u = 0.2: the far part
above the Milne form of the near fit (q > 0), the nearest of the three
forms q = 0 or q = +0.5 by the size of the deceleration reached, and the
accelerating form the farthest of the three. Nothing in the law gives
q < 0: a free ray pushes its reader toward its emitter.

**The clocks.** The presence at a source in the pushing crowd is about
1.7 x (64 + (4 - i) x 16) rays, k of about 0.05 at rank 1 and 0.03 at rank
4 in the `scalar` world, a factor 1 + k on 1 + z that reddens the inner
sources more; in the `age` world the age moment grows with the rank and
with the age of the crowd (the mass's rays at rank i are r_i x 55 / 32
old), k of about 0.02 at rank 1 and 0.05 at rank 4 near the end of the
run, so the age clock reddens the outer sources more: the bend, expected
upward at large d (an apparent acceleration of the clocks, not of the
throw), reported as measured either way. In the coasting crowd both k are
below 0.002, negligible. Read against the detector's own clock (its
self-creations, not the intervals), 1 + z is multiplied by its rate: the
tool prints both.

## The criteria, pinned before the runs

- A record check (fails the tool): every run completed, the books balanced
  at every tick.
- **The windows**: the record read over [100, 200), [200, 300) and the
  late window [300, 400), t_0 the window's centre; every source with at
  least ten `record` lines in the window is a point of the diagram; the
  late window is the registered reading.
- **The reading's formula** (every world, every source, every window):
  1 + z read from the pointer's turn against (1 + k) (1 + v / c) with k
  and v read from the same record (the emission ticks tick - age and the
  emission distances m(age)): within 2 %.
- **The linear law** (the coasting worlds): H fitted through the origin on
  z <= 0.2; H t_0 = 1 within 10 %.
- **The coasting form** (the coasting worlds): of the three forms at the
  near fit's H the least rms over the far part is q = 0, and that rms is
  below 0.02 in z.
- **The decelerating form** (the pushing worlds): H t_0 < 1; q_eff > 0; the
  accelerating form q = -0.55 has the largest rms of the three.
- **The bend of the age clock** (each pair): z_age - z_scalar per source,
  reported as measured, no bracket.
- **What is observed today** (every world): whether the far part resembles
  the accelerating form q = -0.55 best of the three. Expected: outside in
  every run; the answer to the owner's question is registered as read.

## Run and read

```bash
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/hubble examples/events/hubble/coasting_scalar.json examples/events/hubble/coasting_age.json examples/events/hubble/pushing_scalar.json examples/events/hubble/pushing_age.json
PYTHONPATH=src python tools/hubble_readings.py artifacts/hubble
```

`tools/hubble_readings.py` reads the engine's own record (`events.jsonl`,
`run.json`, `initialization.json`) and the flight table through the
engine's own function, replays the world through the API for the clocks'
counts, the positions and the momenta at the windows' ends (GameBoard
readings, the check columns; `--no-replay` skips it), and prints the
record checks, the table per source (v / c declared and the throw's own
form, z, k, v / c and tau, d from the record; the steps, the replay's k
and v and the momentum left), the Hubble diagram per window as a table,
the fits and the verdicts, then the late half [200, 400) as one window
and the Doppler part of the reading alone (the emitter's clock removed),
both printed after the runs and not pinned; `--png DIR` writes the
diagrams with matplotlib (the repository gets the numbers);
`--from-one-point` (the physicist's review, 2026-09-20) fits every window
again with each tau reduced by (r_0 / c) / (1 + z), the exact equivalent of
a coasting throw from the centre, and prints what the near fit itself reads
off an exact coasting form at the window's taus (H t_0 = 1.10 to 1.15 here:
the criterion "the nearest at the near fit's H" names q = -0.55 for a
coasting form too; the register entry's follow-up bullet).
`tests/test_hubble_readings.py` pins the tool to the engine on a bar of
61 Nodes. The runs take about 40 s each (the 301^3 GameBoard's per-interval
host cost, not the rays: about 6 000 rows in flight).

## What the law lacks for this experiment (found while designing it)

- A throw off the axes is not straight: a measured event steps one axis
  per interval, x before y before z, and a step that coincides with an
  earlier axis's step is lost ([BEAM_LAW section 10](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
  note 17), so a diagonal momentum moves along x alone when its components
  are equal; the sources are thrown along the six axes only.
- A crowd of point sources has no three-dimensional gravity to read: a
  source's field is its rows on its declared directions, a beam per
  direction that never dilutes (Gauss on a line), and a fan's lines miss
  every Node not on them (series E: a probe reads its line's beam or
  nothing), so the crowd's push on a chain is one-dimensional and constant
  per row; the mass of the crowd inside a source is stood in for by the
  masses at one Link.
- A source stepping into the Node of the row it has just released takes
  the row home and re-emits it with its stale phase (the first throw
  above): a moving source cannot release along its own motion without
  recycling part of its field.
- The emitter's clock is counted by the crowd's rays at its Node and the
  detector's by every arrival: the reading's factor (1 + k) is the
  model's, not the throw's; the tool prints the redshift per interval (as
  defined), against the detector's own clock, and the Doppler part alone.
- The step rule reads the whole part off the clock at the current
  momentum: under a changing momentum the crossings of the whole part
  cluster (double steps, long gaps), so a source's speed over a hundred
  intervals scatters by a few per cent about its momentum's (the pushing
  crowd's `v / c (record)` against `p(t) / p(0)`).

## The readings (2026-09-20, measured against expected)

Source fingerprint
`5a93868357b564b3c0448e04db424eaf3acb1617e1ab1a448a42989e88481776` (the
worktree of `claude/universe24-new-3ytqde` at the merge of the charge per
unit of content, `b9a0e6c6`, with the worlds and the tool of this series),
Python 3.14.0rc2, numpy 2.5.3, headless, four cores, `--jobs 4`; every run
completed in 36 to 37 s with the books balanced at every tick; the tool: 0
record checks failed, the reading's formula 288 of 288 inside 2 %, 22
pinned readings inside and 26 outside, registered, none moved (the counts
below).

**The late window [300, 400), t_0 = 350.** Detector readings: z from the
pointer's turn, tau the mean age of the arrivals, k the emitter's clock
from the record's emission ticks. GameBoard readings: v / c declared, the
momentum left p(t) / p(0) at t = 400 from the replay.

| source | v / c declared | coasting: z, tau | coasting p(t) / p(0) | pushing scalar: z, k, tau | pushing age: z, k, tau | pushing p(t) / p(0) |
| --- | --- | --- | --- | --- | --- | --- |
| mz1 | 0.050 | 0.0496, 20.7 | 1.030 | 0.119, 0.063, 16.2 | 0.092, 0.012, 21.6 | 0.683 |
| pz1 | 0.057 | 0.0606, 22.9 | 1.025 | 0.101, 0.052, 20.6 | 0.061, 0.026, 18.5 | 0.708 |
| my1 | 0.064 | 0.0611, 24.9 | 1.022 | 0.054, 0.017, 23.5 | 0.036, 0.000, 23.7 | 0.735 |
| py1 | 0.071 | 0.0818, 27.2 | 1.019 | 0.135, 0.068, 24.3 | 0.046, 0.013, 24.1 | 0.751 |
| mx1 | 0.079 | 0.0812, 29.4 | 1.017 | 0.121, 0.064, 27.2 | 0.062, 0.000, 27.8 | 0.773 |
| px1 | 0.086 | 0.0866, 31.5 | 1.015 | 0.086, 0.023, 26.4 | 0.167, 0.053, 29.6 | 0.786 |
| mz2 | 0.150 | 0.1499, 52.0 | 1.006 | 0.149, 0.016, 51.0 | 0.148, 0.006, 47.8 | 0.849 |
| pz2 | 0.171 | 0.1774, 56.0 | 1.005 | 0.252, 0.037, 56.4 | 0.190, 0.017, 55.0 | 0.868 |
| my2 | 0.193 | 0.1908, 62.7 | 1.004 | 0.230, 0.043, 61.6 | 0.207, 0.018, 59.1 | 0.882 |
| py2 | 0.214 | 0.2108, 67.7 | 1.004 | 0.213, 0.030, 65.2 | 0.197, 0.015, 65.2 | 0.893 |
| mx2 | 0.236 | 0.2374, 72.5 | 1.003 | 0.248, 0.028, 68.1 | 0.239, 0.000, 71.0 | 0.904 |
| px2 | 0.257 | 0.2596, 77.3 | 1.003 | 0.309, 0.039, 75.7 | 0.236, 0.010, 73.3 | 0.911 |
| mz3 | 0.250 | 0.2496, 78.3 | 1.002 | 0.256, 0.022, 75.9 | 0.259, 0.000, 75.7 | 0.889 |
| pz3 | 0.286 | 0.2854, 85.7 | 1.001 | 0.273, 0.019, 81.0 | 0.268, 0.016, 83.6 | 0.904 |
| my3 | 0.321 | 0.3195, 93.1 | 1.001 | 0.366, 0.045, 92.3 | 0.295, 0.000, 92.1 | 0.917 |
| py3 | 0.357 | 0.3581, 99.6 | 1.001 | 0.359, 0.035, 96.8 | 0.404, 0.041, 97.9 | 0.926 |
| mz4 | 0.350 | 0.3468, 101.0 | 1.000 | 0.352, 0.032, 97.7 | 0.339, 0.020, 98.5 | 0.911 |
| mx3 | 0.393 | 0.3953, 106.1 | 1.001 | 0.424, 0.018, 104.1 | 0.416, 0.046, 103.9 | 0.934 |
| pz4 | 0.400 | 0.3984, 109.8 | 1.000 | 0.387, 0.015, 105.7 | 0.411, 0.015, 106.7 | 0.925 |
| px3 | 0.429 | 0.4296, 112.0 | 1.001 | 0.448, 0.022, 107.7 | 0.425, 0.020, 109.7 | 0.942 |
| my4 | 0.450 | 0.4530, 117.8 | 1.000 | 0.451, 0.008, 114.5 | 0.501, 0.054, 114.6 | 0.936 |
| py4 | 0.500 | 0.4987, 125.8 | 1.000 | 0.478, 0.004, 122.7 | 0.513, 0.016, 122.6 | 0.944 |
| mx4 | 0.550 | 0.5482, 132.8 | 1.000 | 0.571, 0.034, 130.7 | 0.556, 0.000, 132.3 | 0.952 |
| px4 | 0.600 | 0.6001, 139.7 | 1.000 | 0.604, 0.019, 137.9 | 0.619, 0.036, 137.1 | 0.958 |

The coasting worlds read alike to the last digit (their clocks counted
nothing: k = 0 at every source). The fits per window (detector readings):

| World | Window | H t_0 (near fit; Milne 1) | rms far: q = +0.5 / 0 / -0.55 at the near H | best-H rms: +0.5 / 0 / -0.55 | q_eff | Nearest of the three |
| --- | --- | --- | --- | --- | --- | --- |
| coasting (both) | [100, 200) | 0.875 outside | 0.087 / 0.026 / 0.029 | 0.011 / 0.016 / 0.020 | 9.5 | q = 0 inside |
| coasting (both) | [200, 300) | 0.949 inside | 0.103 / 0.033 / 0.018 | 0.008 / 0.011 / 0.015 | 6.1 | q = -0.55 outside |
| coasting (both) | [300, 400) | 1.029 inside | 0.153 / 0.066 / 0.021 | 0.007 / 0.008 / 0.012 | 4.6 | q = -0.55 outside |
| pushing scalar | [100, 200) | 1.079 outside | 0.266 / 0.130 / 0.069 | 0.030 / 0.027 / 0.026 | 1.1 inside | q = -0.55 outside |
| pushing scalar | [200, 300) | 1.072 outside | 0.193 / 0.088 / 0.037 | 0.029 / 0.025 / 0.024 | 0.5 inside | q = -0.55 outside |
| pushing scalar | [300, 400) | 1.292 outside | 0.432 / 0.223 / 0.142 | 0.037 / 0.032 / 0.030 | -0.55 outside | q = -0.55 outside |
| pushing age | [100, 200) | 0.912 inside | 0.113 / 0.042 / 0.025 | 0.017 / 0.020 / 0.023 | 7.5 inside | q = -0.55 outside |
| pushing age | [200, 300) | 1.017 outside | 0.152 / 0.066 / 0.029 | 0.022 / 0.021 / 0.023 | 4.5 inside | q = -0.55 outside |
| pushing age | [300, 400) | 1.120 outside | 0.219 / 0.106 / 0.052 | 0.028 / 0.027 / 0.029 | 3.7 inside | q = -0.55 outside |

- **The reading's formula** (expected within 2 %): 288 of 288 inside, the
  ratio (1 + z) / ((1 + k)(1 + v / c)) from 0.992 to 1.008: the redshift
  the detector reads is the Doppler of the throw times the emitter's clock,
  exactly as derived, and the coasting worlds read z = v / c declared to an
  rms of 0.003 (the digital step's grain) and tau to 1.3 intervals of the
  throw's own form (r_0 + v t_0) / (c + v).
- **The linear law** (expected H t_0 = 1 within 10 %, the coasting worlds):
  0.875, 0.949, 1.029 at t_0 = 150, 250, 350; outside, inside, inside: the
  Hubble time is the age of the throw once the initial distances (3 to 9
  Links, 5 to 15 intervals of tau) are small against it.
- **The coasting form** (expected q = 0 the nearest at the near H with rms
  below 0.02): inside at t_0 = 150 (0.026, the rms outside), outside at
  250 and 350, where q = -0.55 is the nearest (0.018, 0.021 against 0.033,
  0.066 for q = 0). The cause is in the table: every source reads exactly
  the Milne form shifted by its own r_0 / c, and the far sources' r_0 is
  three times the near ones', so at the near fit's H the far part lies
  below the coasting form, which is the accelerating form's signature. With
  H free per form the three fit within 0.005 of one another (0.007, 0.008,
  0.012): the shape does not tell them apart at this precision, and the
  throw's own form fits with no free parameter.
- **The decelerating form** (expected H t_0 < 1, q_eff > 0, the
  accelerating form the farthest): on the GameBoard every pushing source
  decelerated, p(t) / p(0) = 0.68 to 0.79 at rank 1, 0.85 to 0.91 at rank
  2, 0.89 to 0.94 at rank 3 and 0.91 to 0.96 at rank 4 (the inner ranks
  losing the larger fraction, as derived), and its Doppler part fell with
  it (v / c from the record 0.04 to 0.58 against 0.05 to 0.60 declared).
  The detector's curve nevertheless reads H t_0 > 1 in five of six windows
  (1.07 to 1.29 with the scalar clocks, 0.91 to 1.12 with the age clocks),
  q_eff > 0 in five of six (-0.55 in the scalar late window), and the
  accelerating form the NEAREST of the three in all six (0.025 to 0.142
  against 0.042 to 0.223 for q = 0): outside on every count but q_eff. The
  cause is the emitters' clocks: the inner ranks sit in the thickest part
  of the crowd's rays (the mass's row and the three rows of the sources
  ahead) and their clocks run slowest, k = 0.02 to 0.07 against 0.004 to
  0.035 at rank 4 with the scalar clock, which reddens the near part,
  inflates the near fit's H and leaves the far part below the coasting
  form at that H. With H free per form the three fit within 0.004 of one
  another in every pushing window. The Doppler part alone (z_D = v / c
  from the record's emission ticks and distances, the emitter's clock
  removed; printed after the runs, not pinned) reads the deceleration:
  H t_0 = 0.80, 0.92, 0.92 (scalar) and 0.85, 0.90, 0.99 (age) at t_0 =
  150, 250, 350, below 1 in all six windows, and the nearest form q =
  +0.5 or q = 0 in four of the six (q = -0.55 in the scalar middle and the
  age late window).
- **The bend of the age clock** (reported, no bracket): in the coasting
  crowd zero at every source (no clock counted); in the pushing crowd
  z_age - z_scalar from -0.089 to +0.081 in the late window, negative at
  four of the six rank-1 sources and at three of the six rank-4 sources,
  no monotone bend: the age clock's k (0 to 0.054) is smaller and more
  even over the ranks than the scalar's (0.004 to 0.068), and the
  differences are within the grain of the step rule (about 0.03 in z per
  window).
- **What is observed today** (expected outside in every run): the
  accelerating form q = -0.55 is the nearest of the three at the near
  fit's H in ten of the twelve windows (all but the coasting first window),
  inside the bracket of "resembles" and outside the expectation: the
  detector's curve does resemble the curve observed today, in the coasting
  throw by the throw's initial distances and in the pushing throw by the
  crowd's clocks, while on the GameBoard nothing accelerates.
- Host cost: 36 to 37 s per run of 400 intervals (about 6 000 rows in
  flight, 31 measured events; the 301^3 GameBoard's per-interval arrays); the
  tool with the replay 3 minutes.

## Verdict

The detector reads the linear Hubble law by itself: z = v / c to 0.003 for
every source and H t_0 = 1.03 at t_0 = 350 in the coasting throw, the
Hubble time the age of the throw. At large distance the detector's curve
falls below the coasting form of its own near fit in every run, and of the
three forms the one observed today, q = -0.55, is the nearest in ten of
twelve windows; but this is not an acceleration: on the GameBoard the
coasting sources coast (their momenta within 3 %) and the pushing sources
decelerate (their momenta fall by 4 to 32 %). The resemblance comes from
what the detector cannot see, the throw's initial distances (an exact,
parameter-free coasting form fits the coasting reading) and the emitters'
clocks in the crowd (the near ones slowest), and with H fitted per form
the three forms agree within 0.005 in z, so the shape at this precision
does not tell q = +0.5 from 0 from -0.55. The age clock bends nothing
beyond the grain. Nothing was tuned; the five findings for the law are the
section above.

## Re-read under the step drive (2026-09-20)

Every source is a lamp whose recoil changes its momentum at every
self-creation, so the four worlds move differently under the step drive
(a body's count of Links is the whole part of the distance its momentum
has driven), by little: the near fit's H t_0 in the three windows and the
late one reads 0.877, 0.969, 1.017, 0.996 in the coasting worlds (0.875,
0.949, 1.029, 0.985 registered), 1.144 to 1.305 in `pushing_scalar` and
0.866 to 1.057 in `pushing_age`; q = -0.55 is the nearest of the three
forms in 8 of the 12 windows (10 of 12), `pushing_age` reading q = 0 the
nearest in its first two; 309 readings inside and 27 outside (310 and
26). The verdict stands as read. The register entry has every number
([migration](../../../docs/MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).

## Re-read under the fraction-free law (2026-09-20)

Under the fraction-free law ([BEAM_LAW note 41](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
the two coasting worlds are identical to the registered runs and the two
pushing worlds move by little (their clocks read a changing crowd): the
near fit's H t_0 in the three windows and the late one reads 1.176,
1.302, 1.324, 1.301 in `pushing_scalar` (1.144, 1.182, 1.305, 1.292 under
the signed drive) and 0.848, 1.018, 1.086, 1.035 in `pushing_age` (0.866,
0.932, 1.057, 1.036); q = -0.55 the nearest of the three forms in 9 of
the 12 windows (8 of 12); 310 readings inside and 26 outside (309 and 27).
The verdict stands as read. The register entry has every number
([migration](../../../docs/MIGRATION.md#the-fraction-free-law-on-2026-09-20-every-count-an-accumulator-on-the-bodys-record)).

## Re-read under the directional drive (2026-09-21)

Under the directional drive ([BEAM_LAW note 49](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
the model owner's records 191 and 301) every source walks the line of
its momentum at the pace |p|_1 S_1 Q / (Q S M S_1 Q + |p|_1 T_D), the
rows' pace the cap: the declared throws on the axes, 0.05 to 0.35 of the
rows' speed under the per-axis rule, now run at the factor 1 / (1 + 0.72
v) of that (`make_worlds.py`'s `speed` reads the rate over the wall of
`drive_rate_and_wall`; the world files are unchanged), so the sources'
`step` lines over 400 intervals are 1308 for 1505 in the two coasting
worlds, 1260 for 1449 in `pushing_age` and 1244 for 1431 in
`pushing_scalar`. The four worlds re-run as registered on the branch
`directional-drive` (source fingerprint
`6a3381a556a02e8e60ecea8dfba889a2197c4fa3750e9ee4c7a7066bb3c9a5e9`,
Python 3.14, headless, one world at a time beside the base tree's
replay), 41.4, 43.9, 50.2 and 45.2 s with the books balanced at every
tick (the base tree 47.1, 41.6, 42.9, 51.5 s); `tools/hubble_readings.py`
with its replay: 8 record checks passed, 0 failed, exit 0; every world
moved against the base (the digests in the branch's VALIDATION table).

The near fit's H t_0 in the windows [100, 200), [200, 300), [300, 400)
and [200, 400) reads 0.874, 0.973, 1.032, 1.002 in the two coasting
worlds (0.877, 0.969, 1.017, 0.996 under the fraction-free law), 1.153,
1.270, 1.333, 1.319 in `pushing_scalar` (1.176, 1.302, 1.324, 1.301) and
0.861, 1.038, 1.080, 1.037 in `pushing_age` (0.848, 1.018, 1.086,
1.035); q = -0.55 is the nearest of the three forms in 12 of the 12
windows (9 of 12); 308 readings inside and 28 outside (310 and 26): the
coasting worlds' first window reads H t_0 0.874 against the pin "1
within 10 %" and q = 0 not the nearest, as before, and `pushing_scalar`
keeps H t_0 > 1 in every window. The reading's formula 288 of 288 inside
2 %. The verdict stands as read; the numbers above are this re-read's
([migration](../../../docs/MIGRATION.md#form-b-the-bodies-drive-on-the-momentums-line-2026-09-21)).
