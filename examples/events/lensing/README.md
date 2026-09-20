# Series K: light beside a mass, under the Beam Law, in space

Four worlds of one base, written by `make_worlds.py`; the register entry is
[K, light beside a mass (2026-09-20)](../../../docs/EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20)
and the evidence is in [validation](../../../docs/VALIDATION.md). The model
owner's go of 2026-09-20 on the law's own predictions ([Highlights 5.4](../../../docs/HIGHLIGHTS.md#54-the-detector),
"go on everything; just make sure again that it is good and generic":
"the two runs on the law's own predictions, light beside a mass (series K)
and the single-click build-up of fringes (A10 at a low rate)"), on the
physicist's list of what the law predicts beyond what it was built to
reproduce, entry 2: "Light is not bent by a mass, and not delayed. The
rule: a ray in transit is moved by the flight table alone and turned only
by the collision, which acts among the single units of one number and
content on the six headings at a Node of free space and never on a fan
ray; the crowd of a mass (its free rays) pushes a measured event (the one
reading set, the push) and nothing in flight; no rule of the GameBoard
reads the crowd for a ray's step. Disagrees, plainly: the law predicts
zero deflection and zero delay for light of another number passing any
mass." The derivation says the law disagrees with nature; the run decides,
and the derivation may be wrong. A research run under the
[experimenter skill](../../../skills/experimenter/SKILL.md), made once,
never a test; the design, the derivation and the expectations below were
written before the runs; a reading outside its bracket is reported with
its numbers, never moved. Every number is labelled a **detector reading**
(the record of a detector's set or of a measured event: the only kind
reality has) or a **GameBoard reading** (the host's view of the GameBoard:
the rays in flight, the meetings, the picture and the checks, never the
measurement).

## The GameBoard

An open box of 57 x 41 x 41 Nodes, the centre c = (28, 20, 20), `"law":
"beam"`, K 2^30, N 64, `release` [1, 2^12], `suspension` 0, 400 intervals.

- **The lamp**: a fixed measured event of the paid family `light` at
  (2, 20 + b, 20), content 8 K + 1 400 000 (the turn 8 steps of 64 per
  self-creation, so a release at tick t carries the phase 8 t mod 64 and
  the wavelength is lambda = c x period = 8 x 32 / 55 = 4.65 Links, c the
  speed on a heading read off the flight table, 32 Links per 55
  intervals), releasing one unit per self-creation on each of five
  directions, the heading (1, 0, 0) toward the screen and the four
  in-plane directions (24, +-1, 0) and (12, +-1, 0) within 5 degrees of
  it: a narrow beam, five rays per interval, whose arrival on the screen
  52 Links away spans nine pixels (the offsets 0, +-2 and +-4 in y, off
  the flight table's digital lines). Its entry for the mass's family is
  `pass`.
- **The mass**: a fixed measured event of the free, phase-less family `m`
  (`quantum` 0, `charge` 0, `"phase": false`) of content M at c,
  releasing on the full fan of the 290 primitive directions (a, b, c)
  with 0 < |a| + |b| + |c| <= 6, series E's form: at `release` [1, 2^12]
  it releases `by_clock(age, M, 2^12)` rays per direction per
  self-creation, one for M = 2^12 (q = 290 rays per interval) and two for
  M = 2^13 (q = 580). Its table is the default (its own rays come home;
  a ray of `light` would click); its crowd escapes through the six open
  faces, the GameBoard's face detectors.
- **The screen**: the plane x = 54 of 1681 fixed measured events of the
  paid family `wall`, each declared as the one-Node detector
  `screen_<y>_<z>` reading `wave` (the coherent pointer's square per
  interval, cumulative) with the entry `{"rule": "measure", "reads":
  "age"}` for `light`, so that every click record carries the age moment
  of its group, amount x age summed over the rays of one number met in
  one interval (the flight time, Shapiro's reading), and `pass` for `m`
  (the mass's rays cross the screen unread: nothing is pushed, no record
  is written).
- **No clock is slowed**: `suspension` 0 in every world, so the lamp's
  clock beside the mass's crowd is not slowed and the phase rate at the
  screen is the lamp's own turn unless the flight changes it; the
  emitter's redshift beside a mass is series E's reading
  ([E](../../../docs/EXPERIMENTS.md#e-the-clocks-redshift-in-space-under-the-age-reading-2026-09-20)),
  not this run's, which reads the flight alone.

| World | The mass | b | What it asks |
| --- | --- | --- | --- |
| `control` | none | 6 | the beam alone: the centroid, the ages, the count, the phase rate |
| `mass` | M = 2^12, one ray per direction per interval | 6 | the same beside the mass |
| `heavy` | M = 2^13, two rays per direction per interval | 6 | twice the crowd |
| `near` | M = 2^12 | 3 | half the impact distance |

## The derivation, before the runs

**What the collision table does to a beam crossing a radial fan.** The
collision (BEAM_LAW section 3 step 3, section 4; `nature_beam.collide`)
acts per family's store, and within a store per (Node, number, content)
class: only the single units of ONE number and content on the six
headings at a Node of free space are put into the eight slots. The beam's
rays are of the paid family `light` with the lamp's number; the mass's
rays are of the free family `m` with the mass's number, in another store.
A ray of the beam and a ray of the mass therefore never enter one slot
state, whatever their directions: the table is never applied between
them, and the mean deflection of a beam ray meeting a radial ray is
exactly 0, not by symmetry but because the rule does not act. Were the
two of one family and number (which no world can declare: a lamp's rays
are paid, a mass's free), the geometry would still give nothing: the
mass's fan rays are spectators (not headings), its heading (0, 1, 0)
crosses the beam's line at one Node in the pattern "+x +y", a class of
one, fixed; only a head-on pair "+x -x" moves (it parks and leaves on
+-z), and the mass sends no -x ray along the beam's line. Within the
beam's own store, its rays of one number and content on (1, 0, 0) that
share a Node are a crowd in the +x slot (a wall the table never moves)
and its fan rays are spectators: no collision either.

**What else could act.** Nothing: the flight table moves a ray by its
direction and age alone (step 1), the readings are read-only (step 2),
the tables act at measured events (step 4) and the beam's line passes no
measured event but the screen (in `near` the (12, -1, 0) ray's digital
line passes one Node above the mass at x = 28: the beam clears the mass
in every world, so the mass takes no light), and the clocks are not
slowed. So the law derives, for every M and b:

- the centroid of the arrival on the screen at the beam's axis, the
  lamp's y and z: **a deflection of 0**;
- every ray's age at its click the flight table's, 89 intervals on
  (1, 0, 0) and (12, +-1, 0) and 90 on (24, +-1, 0) from x = 2 to x = 54
  (the least age at which the digital line reaches the screen): **a delay
  of 0**, the first click at tick 90;
- the count the control's, 5 per interval, none on the faces, none taken
  by the mass; the phase rate the lamp's turn, 8 steps per interval.

**The brackets, pinned.** The deflection of the centroid (the offset of
the count-weighted centroid from the beam's axis, against the control's
offset) within +-0.5 pixel in y and in z (half the grain of a one-Node
pixel; a deflection toward the mass is negative in y); the count-weighted
mean age of the arrivals within +-1 interval of the control's; the count
in the window within 1 % of the control's; the phase rate within +-0.05
step per interval of the turn 8. A run is read over the window [110, 400]
(every direction of the beam has arrived by tick 90; the mass's front
reached the far faces by tick 50).

**What nature shows, scaled to the world.** Nature bends light by the
angle 4 G M / (b c^2) toward the mass (1.75 arcseconds at the Sun's limb,
where G M / (b c^2) = 2.1 x 10^-6; Eddington 1919, VLBI to 10^-4 of it)
and delays it by (2 G M / c^3) ln(4 x_1 x_2 / b^2) (Shapiro; Cassini 2003).
The law's dimensionless equivalent of G M / (b c^2) is the potential a
clock reads at b, series E's age moment: by series E's form the mass's
crowd at the beam is the shell mean of the presence, q x dwell / (4 pi
b^2) rays per Node (dwell = 55 / 32 intervals per Link on a heading), and
the age moment per Node is that presence times the age of a ray at b,
b / c; a clock beside the beam at `suspension` [1, 1] would count it
per self-creation (k_a; series E measured k_a x r = 36 at [1, 2] for this
mass). The numbers:

| World | presence at b (rays per Node) | age moment per Node, k_a at [1, 1] | nature's deflection 4 k_a (radians) | nature's capture radius 2 k_a b (Links) |
| --- | --- | --- | --- | --- |
| `mass` (M = 2^12, b = 6) | 1.10 | 11.4 | 46 | 137 |
| `heavy` (M = 2^13, b = 6) | 2.20 | 22.7 | 91 | 273 |
| `near` (M = 2^12, b = 3) | 4.41 | 22.7 | 91 | 137 |

By nature's measure this crowd is not a weak field: the beam passes far
inside the radius 2 G M / c^2 at which nature captures light, so nature's
prediction here is not a small angle but the beam's capture; the
weak-field angle, if it applied, would move the arrival by dozens of
pixels toward the mass and grow with M / b. The law predicts 0 at every M
and b. A weak crowd (a smaller release) would put nature's angle at a few
pixels, still far outside the bracket; the dense crowd is kept because it
is the sharper test of a coupling: the beam's Nodes each hold about one
ray of the crowd per interval (the GameBoard's meetings), so any rule
that let a ray in flight read the crowd would show on this screen.

## The readings (2026-09-20, measured against expected)

Source fingerprint
`a1b2a949ccda2194537ecae4c6ff7380642f8f7d7877c01ab0e1649ba51c5d4b` (the
worktree of `claude/universe24-new-3ytqde` at the tip `9fc895a2`, the
Beam Law `beam-v1`), Python 3.14.0rc2, numpy 2.5.3, headless, four cores,
`tools/run_series.py --jobs 4`; every run completed (6.5, 9.1, 9.9, 9.1 s
for `control`, `mass`, `heavy`, `near`) with the books balanced at every
tick; `tools/lensing_readings.py`: 0 record checks failed, 16 readings
inside, 0 outside, none moved.

DETECTOR readings, the window [110, 400] (the deflection is the centroid's
offset from the beam's own axis against the control's; the delta of the
width and of the mean age against the control):

| World | M | b | crowd at b: presence, age moment | clicks | centroid y (deflection) | centroid z (deflection) | width rms y | mean age (delta) | first click | count ratio | phase rate (delta vs 8) | light on the faces | light the mass took | verdicts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `control` | - | 6 | 0, 0 | 1455 | 26.000 (-) | 20.000 (-) | 2.828 | 89.40 (-) | 90 | - | 8.000 (0.000) | 0 | 0 | phase rate inside |
| `mass` | 2^12 | 6 | 1.10, 11.4 | 1455 | 26.000 (0.000) | 20.000 (0.000) | 2.828 (0.000) | 89.40 (0.00) | 90 | 1.0000 | 8.000 (0.000) | 0 | 0 | centroid y, centroid z, delay, count, phase rate: inside |
| `heavy` | 2^13 | 6 | 2.20, 22.7 | 1455 | 26.000 (0.000) | 20.000 (0.000) | 2.828 (0.000) | 89.40 (0.00) | 90 | 1.0000 | 8.000 (0.000) | 0 | 0 | all five inside |
| `near` | 2^12 | 3 | 4.41, 22.7 | 1455 | 23.000 (0.000) | 20.000 (0.000) | 2.828 (0.000) | 89.40 (0.00) | 90 | 1.0000 | 8.000 (0.000) | 0 | 0 | all five inside |

- **The deflection** (expected 0 within 0.5 pixel; nature 46 to 91
  radians toward the mass, or the capture): measured 0.000 in y and in z
  in every world, the centroid on the beam's axis (y = 26 for b = 6, 23
  for b = 3; z = 20) to the last digit, the width 2.828 pixels the same.
  Inside. Nature's value outside.
- **The delay** (expected 0 within 1 interval; nature hundreds of
  intervals): the mean age 89.40 intervals in every world (the five
  directions' 89, 89, 89, 90, 90), the first click at tick 90, the delta
  0.00. Inside.
- **The count** (expected the control's): 1455 clicks in the window in
  every world, the ratio 1.0000; no light on any face, none taken by the
  mass. Inside.
- **The phase rate** (expected the turn 8): 8.000 steps per interval in
  every world, the delta 0.000: no redshift of the light in flight
  (the clocks were not slowed by design). Inside.
- The screen's record and count in the three mass worlds are the
  control's pixel by pixel: the light's part of the record is identical
  with and without the mass (the runs' audit digests of `mass` and `near`
  are equal to each other, `2c7d0cdc329e`, since the same amounts flow in
  both).

GAMEBOARD readings (the world replayed through `NatureBeamSimulation`):
the beam's rows in flight 447 at most in every world, none at rest, none
on a direction outside the lamp's five (no ray was turned by a collision
anywhere); the crowd's rows in flight 13618 at most (`mass`, `near`) and
the Nodes holding a ray of the beam and a ray of the crowd in the same
interval 162 per interval on average over the window in `mass` and
`heavy` (156 in `near`): the beam crossed the crowd at about one third of
its Nodes every interval and met it nowhere, as derived.

## Verdict

In this law light is neither bent nor delayed beside a mass, exactly:
the deflection 0.000 pixel, the delay 0.00 interval, the count and the
phase rate the control's, at a crowd where nature would capture the beam
and at twice that crowd and at half the impact distance, the beam's
Nodes each holding a ray of the crowd at every interval. The derivation
held, and the physicist's entry 2 is registered as measured: a plain
disagreement with nature (1.75 arcseconds at the Sun's limb, the Shapiro
delay, lensing). Nothing was tuned. What the law lacked: a rule by which
a ray in transit reads the crowd at the Node it enters (a wait per whole
unit of presence, or a turn of its direction by the flow), which the Beam
Law removed on 2026-09-19 to keep the flight a bijection blind to the
crowd; the collision, the one rule that turns a ray, acts within one
family and number only, so the crowd of a mass cannot reach a ray of
light through it either. Giving a ray a reading is the model owner's
decision, not a parameter.

## The same worlds under the meeting (2026-09-20)

The model owner's decision of the same day ([Highlights 5.4](../../../docs/HIGHLIGHTS.md#54-the-detector),
"DECIDED: the meeting, M-R: an event in transit reads the crowd as a body
does, a report, not a balance"; [BEAM_LAW section 3 step 3 and note 34](../../../docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam);
the identity `meeting-v1`) gives a paid unit in transit a reading: at
every Node of free space, after the collision, it reads the free units of
every number but its own (the one reading set, the vector moment V with
the labels as weights), the column sum of its family against theirs
(gravity: -1) and turns toward t = -V by one grain step of the direction
table per 64 crowd units met, the count kept on its phase register; the
crowd is untouched. `make_worlds.py` writes the four worlds again under
the key (`control_meeting.json`, `mass_meeting.json`, `heavy_meeting.json`,
`near_meeting.json`, the model ids `beam-lensing-<name>-meeting-v1`) and
a fifth, `lens_meeting.json`: two lamps at y = 26 and y = 14 (+-b = 6)
on a box of 105 x 41 x 41 with the mass at x = 28 and the screen at x =
102, 600 intervals, so that the two beams, each turned toward the mass,
cross past it. The register entry is
[K under the meeting (2026-09-20)](../../../docs/EXPERIMENTS.md#k-under-the-meeting-2026-09-20).

**The expectation, written before the runs** (the design's offline
flight of the beam beside the replayed crowd, `scratchpad/meeting/k_deflection.py`;
the brackets fixed in `tools/lensing_readings.py`): `mass` the centroid
-3.0 +- 0.5 pixels toward the mass, 0 +- 0.5 in z, the width about 6.0,
the mean age about 90.4 (+- 1), the count ratio 0.996 (+- 0.05), no ray
on the faces; `heavy` -4.3 with 209 rays on the faces (+- a quarter);
`near` -2.6 with 136; the phase offset of the arrivals (the click's phase
less the lamp's phase at the ray's birth, the crowd met modulo 64) about
55 steps in `mass` and `near` and 24 in `heavy` (+- 8); the phase rate 8
(+- 0.05); the control unchanged byte for byte; the lens world's crossing
about 70 Links past the mass, a grain of the fan, no bracket.

**The readings (2026-09-20, measured against expected).** Source
fingerprint `dc1cce964db367167732b1727d9dc8d2fcf73a27bf13e33a1822cc5a84fff1a3`
(the worktree of `claude/universe24-new-3ytqde` from the tip `329c5660`
with the meeting's commits), Python 3.14.0rc2, numpy 2.5.3, headless,
`tools/run_series.py --jobs 2` under the load of the register's replay;
every run completed with the books balanced at every tick; 0 record
checks failed, 14 readings inside, 9 outside, none moved.

| World | M | b | clicks | centroid y shift (expected) | z | width rms y | mean age (expected) | count ratio (expected) | light on the faces (expected) | light the mass took | phase offset (expected), resultant | phase rate | verdicts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `control` | - | 6 | 1455 | 26.000 (0) | 20.000 | 2.828 | 89.40 (89.40) | - | 0 (0) | 0 | 0.0 (0), 1.00 | 8.000 | inside |
| `mass` | 2^12 | 6 | 1350 | -1.790 (-3.0) | 0.000 | 3.907 | 89.90 (90.43) | 0.928 (0.996) | 0 (0) | 122 | 19.7 (55), 0.09 | 8.191 | centroid y, count, offset, rate outside; z, delay, faces inside |
| `heavy` | 2^13 | 6 | 1242 | -4.359 (-4.3) | 0.000 | 5.277 | 90.64 (90.64) | 0.854 (0.858) | 210 (209) | 1 | 34.3 (24), 0.21 | 7.101 | centroid y, z, delay, count, faces inside; offset, rate outside |
| `near` | 2^12 | 3 | 1237 | -2.301 (-2.6) | 0.000 | 4.470 | 89.71 (89.72) | 0.850 (0.901) | 77 (136) | 169 | 62.3 (55), 0.31 | 11.273 | centroid y, z, delay, offset inside; count, faces, rate outside |
| `lens` | 2^12 | +-6 | 3958 | -6.255 and +6.255 per lamp; the crossing 71.0 Links (about 70) | - | - | 173.89 | - | 2 | 394 | 56.3, 0.58 | 6.364 | a grain, no bracket |

The sign toward the mass in every world; the form reproduced at twice
the mass almost integer by integer (-4.36, 210 on the faces, the age
90.64) and at half the impact distance within the bracket; the ages the
bent path's, no delay in time; the phase offset sharp per pixel (the
resultant 0.9 to 1.0 at the lit pixels of `mass` and `near`) and tens of
steps apart between pixels, so the screen-wide mean is not one number
(the expectation was the mean over rays); the phase rate's three readings
outside are the estimator's (a pixel's pointer mixes rays of different
offsets), not a redshift. What the offline flight lacked: the mass is a
measured event that measures the light reaching it, so the most turned
rays click on it (122 in `mass`, 169 in `near`, 1 in `heavy`) and the
centroid at (2^12, 6) reads -1.79 where -3.0 was expected. GAMEBOARD: the
meetings 165, 191, 167 and 414 Nodes per interval; the books' `turned`
line of `light` (-8016, -85088, 0), (-142936, -215752, 0), (-102000,
-112152, 0) and (-32448, 0, 0); the lens world's mean lines closest 58
Links past the mass. `control_meeting`'s `events.jsonl` is byte-identical
to the control's.

Run the worlds:

```bash
python examples/events/lensing/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/lensing examples/events/lensing/control.json examples/events/lensing/mass.json examples/events/lensing/heavy.json examples/events/lensing/near.json
PYTHONPATH=src python tools/lensing_readings.py artifacts/lensing
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/lensing_meeting examples/events/lensing/control_meeting.json examples/events/lensing/mass_meeting.json examples/events/lensing/heavy_meeting.json examples/events/lensing/near_meeting.json examples/events/lensing/lens_meeting.json
PYTHONPATH=src python tools/lensing_readings.py artifacts/lensing_meeting
```

`tools/lensing_readings.py` prints the record checks, the DETECTOR tables
above (the worlds without the key against the derivation, the worlds
under the key against the offline flight) and the GAMEBOARD replay of
every world (`--no-replay` skips it).
