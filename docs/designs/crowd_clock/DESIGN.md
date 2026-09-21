# Series U, a lamp inside a crowd: the design, with the expectation pinned before any run

The G2 experimenter, 2026-09-21, on the model owner's word after the
two-stars run ([series O](../two_stars/DESIGN.md)). The owner (in
conversation, translated): "this says something; it could explain something
about distant galaxies and why they look as if at high speed", and then
"check it yourself and report to the Boss". This document is the check's
design: what the law as built says a distant crowd's lamp reads, pinned
before any run, the worlds that test it, what would refute it and what the
run cannot decide. Section 7 is written after the run. Nothing here is
registered in [docs/EXPERIMENTS.md](../../EXPERIMENTS.md); the register
entry is drafted in the folder's
[README](../../../examples/events/crowd_clock/README.md) for the owner's
word.

Sources: [BEAM_LAW](../../BEAM_LAW.md) step 4 (the clock: after each
self-creation a body owes `by_drive(acc, k n, d)` intervals, k the presence
at its Node, n / d the world's `suspension`) and note 41 (the fraction-free
count); the crossing rule (note 48: a body and a row meet at the crossing of
their world lines; the Doppler 1 + v / c is a count); the step drive
(note 17 as amended: a body steps only at a self-creation); series O's
readings (the lab at rest reads a receding lamp at 1 + v / c, without gamma).

## 1. The question, on the board

A detector at rest reads a lamp's light as a count of births per interval.
Two things slow that count under the law as built:

- **The lamp's motion.** A lamp receding at v births one record per
  interval of its own clock, and the reader meets them at the crossing of
  world lines: 1 + z = 1 + v / c ([series O](../two_stars/DESIGN.md)
  section 3, read 1.200 for 0.2 c). With v < c this never passes z = 1.
- **The lamp's crowd.** After each self-creation the lamp's clock owes
  k n / d intervals, k the presence of other numbers' rows at its Node. In a
  crowd (a "galaxy": the gravity rows of everything around it crossing its
  Node every interval) the lamp births once per 1 + k intervals, so its
  count at any reader is slowed by 1 + k, motion or none. Nothing bounds k:
  a heavy enough crowd gives z = 1, 2, 10.

The law's reading of a distant crowd's lamp is therefore the product

    1 + z = (1 + k)(1 + v / c),

a Doppler by the speed and a slowing by the crowd. Nature reads a galaxy's
z by expansion (1 + z = a_now / a_then) with the same z appearing as a
"speed" when read as Doppler; the owner's remark is that the law as built
has a second term that is not a speed. The check is whether the law does
what section 1 says: whether the crowd's k reaches 1 and beyond, whether
the light escapes the crowd at the slowed rate (a slow clock, not a lost
light), and how z splits between the two factors when the crowd moves.

One more consequence follows from the same step 4 and is pinned here: a
body that waits neither releases nor steps (the step drive counts Links
only at a self-creation). A lamp slowed by 1 + k inside a crowd moving at
v moves at v / (1 + k). Its crowd, if nothing slows it alike, moves at v:
the lamp falls behind. In the worlds below the crowd's two sources are not
crossed by anything and do not slow; the lamp lags k v t / (1 + k) Links
after t intervals and, once past the fan's reach, is out of its crowd and
recovers. A crowd carries a slow clock only when the crowd is slowed alike
(as every star of a galaxy is, in the crowd of all the others).

## 2. The worlds

`examples/events/crowd_clock/make_worlds.py` writes eight worlds on a bar
of 121 x 9 x 9 Nodes (open), `ticks` 500, `suspension` [1, 2^16],
`release` [1, 2^16], `width` 2^20, N = 64.

- **The lamp** `s_px1` (series G2's light family), 8192 units (amended
  after the first run to 2^20 units, section 7: a lamp's wheel turns by its
  content over K and the first run read the lamp's own spending as a k of
  0.03 to 0.04 by the second window), a lamp of one
  unit per self-creation on one direction (+x to the detector when still,
  -x when moving away from it), the birth wheel [1, 64]; its table lets the
  crowd's rows pass (`mass: pass`), so the coupling is off and only the
  clock counts them.
- **The crowd**: two bodies of the free family `mass` three Links from the
  lamp on +y and +z, each releasing F units per interval on every direction
  of a fan of nine toward the lamp's line, (dx, -3, 0) and (dx, 0, -3) for
  dx = -4 .. 4 in primitive form (a free family's release is not consumed;
  every direction carries the whole F). The heading's rows cross the lamp's
  Node; the oblique ones cross the lamp's line one to four Links along x on
  either side, so the fan covers a lamp up to four Links behind its crowd.
- **The detector**, fixed, off the crowd's lines, measuring `s_px1` with
  `reads: "age"`: at x = 110 for the still lamp at x = 10 (a flight of 100
  Links, 172 intervals), at x = 3 for the moving lamp thrown from x = 40
  toward +x at 0.2 c (a flight of 37 Links and growing).

| World | F per source per interval | pinned k | lamp | model id |
| --- | --- | --- | --- | --- |
| `still_005.json` | 82 | 0.005 | at rest | `rays-crowd-clock-still-005-v1` |
| `still_08.json` | 1311 | 0.08 | at rest | `rays-crowd-clock-still-08-v1` |
| `still_3.json` | 4915 | 0.3 | at rest | `rays-crowd-clock-still-3-v1` |
| `still_1.json` | 16384 | 1 | at rest | `rays-crowd-clock-still-1-v1` |
| `still_2.json` | 32768 | 2 | at rest | `rays-crowd-clock-still-2-v1` |
| `moving_08.json` | 1311 | 0.08 | 0.2 c with its crowd, away from the detector | `rays-crowd-clock-moving-08-v1` |
| `moving_3.json` | 4915 | 0.3 | the same | `rays-crowd-clock-moving-3-v1` |
| `moving_1.json` | 16384 | 1 | the same | `rays-crowd-clock-moving-1-v1` |

## 3. What the run reads, pinned before it

**The probe.** Before the design a probe of two heading sources of F = 64 on
the engine as merged (main 119fd9b) read the presence 256 = 4 F at the Node
between them: two sources, each unit at the Node for two intervals on
average (a row at c = 0.58 Links per interval, "outside and here" in the
one moment table). A second probe of this folder's `moving_3` for 200
intervals read the lamp two Links behind its crowd at half the heading's
presence. Both probes are calibration, not readings; the numbers below are
derived from them and from the law, and the run decides.

**(a) The still lamp's clock.** Presence at the lamp's Node = 2 x 2 x F;
k = 4 F / 2^16: 0.005, 0.08, 0.3, 1, 2 for the five still worlds. The
lamp births once per 1 + k intervals (k read from the birth ticks within
20 % of the pin or within 0.02); in the world `still_1` it waits one
interval in two, in `still_2` two in three.

**(b) The detector reads the clock.** The slope of the birth ordinal against
the click's tick is 1 / (1 + z) with 1 + z = 1 + k: 1.005, 1.08, 1.3, 2.0,
3.0 (within 0.02 or within the k bracket); the click rate is 1 / (1 + k)
per interval; the age read at every click is the flight, 172 intervals.
z = 1 and z = 2 are read from a lamp at rest.

**(c) The light escapes.** Every birth reaches the detector: the count of
clicks equals the count of births one flight earlier (the crowd slows the
clock; it takes nothing from the light, the rows `pass`).

**(d) The moving crowd.** In `moving_08` (k = 0.08) the lamp stays inside
its fan through the run (the exit no earlier than tick 464) and the
detector reads 1 + z between 1.224 and 1.296 in both windows,
(1 + k)(1 + 0.2) with k between k / 4 and k: above the Doppler 1.200 of a
lamp alone at 0.2 c, the excess the clock's. In `moving_1` (k = 1) the lamp
falls behind its crowd (its speed v / (1 + k) against the crowd's v) and
leaves the fan between ticks 69 and 172; the detector's second window
(250 to 400, seeing the lamp 64 intervals earlier) reads 1.200, the Doppler
alone, and its first window reads more, between 1.200 and 2.400. In
`moving_3` (k = 0.3) the exit comes between ticks 149 and 493 and the read
1 + z falls from the first window to the second, both between 1.200 and
1.560. In every moving world the lag of the lamp behind its crowd grows
while it is inside the fan and is constant once outside.

**(e) The split.** For a lamp inside its crowd 1 + z = (1 + k)(1 + v / c)
to the precision of (b): the clock's factor and the Doppler multiply; the
detector cannot tell the two apart from one reading of 1 + z (it reads the
age too, but the age is the flight, not the clock).

## 4. What would refute the reading

- The still lamp's k off the pin by more than 20 % and 0.02 at any rung, or
  not linear in F: the presence is not 4 F, and the probe's calibration was
  wrong or the count is not of rows at the Node.
- The detector's 1 + z different from 1 + k: the crowd changes the light,
  not (only) the clock.
- Clicks fewer than the births one flight earlier: the light does not
  escape, and the crowd is a loss, not a slowing.
- A moving lamp that keeps up with its crowd while its clock is slowed: a
  body steps while waiting, against the step drive as written.
- `moving_08` reading 1.200 in both windows: the clock's factor does not
  multiply the Doppler at the detector.

## 5. What the run cannot decide, and what it is for

The worlds pin the law's arithmetic, not nature's. The run cannot say
whether a galaxy's redshift is a slowed clock; it says what the law as
built makes of a crowd: how heavy a crowd gives k = 1 (F = 16384 units per
source per interval here, against the G2 star's release 2^22 / 2^16 = 64
per interval, so a crowd of about 500 such stars' rows through one Node),
that the count is unbounded, that the light escapes, and that a slowed clock
and its unslowed crowd part ways. It is for the Boss's and the owner's
question whether the law's clock term is a candidate for what nature reads
as z, and for the lorentz-v1 request (a moving body reads the Nodes it
passes) that the two-stars run raised: there the reader's clock, here the
source's.

## 6. The run, when ordered

    PYTHONPATH=src python examples/events/crowd_clock/make_worlds.py
    PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/crowd_clock examples/events/crowd_clock/still_005.json examples/events/crowd_clock/still_08.json examples/events/crowd_clock/still_3.json examples/events/crowd_clock/still_1.json examples/events/crowd_clock/still_2.json examples/events/crowd_clock/moving_08.json examples/events/crowd_clock/moving_3.json examples/events/crowd_clock/moving_1.json

The readings are the lamp's `birth` lines (its clock), the detector's
`click` lines (the birth ordinal `record & 0xFFFFFFFF` against the tick,
the `age`), and the `step` lines of the lamp and its two sources (the lag).
`tests/test_crowd_clock.py` pins the shipped worlds to the generator, the
presence 4 F after the rows arrive, and the algebra of section 1.

## 7. Measured (2026-09-21, two runs on main 119fd9b, after the pins above)

The runs are `tools/run_series.py --jobs 3` over the eight worlds (about two
seconds each, the books balanced, 500 intervals); the readings are the
lamp's `birth` lines, the detector's `click` lines (the birth ordinal
against the tick) and the `step` lines of the lamp and its sources, read by
the experimenter's script in windows of 150 intervals (the lamp's clock in
the intervals whose light the window sees, one flight earlier).

**The first run, the lamp of 8192 units.** Every reading of the first
window inside the pins: the still lamp's 1 + z at the detector 1.009, 1.089,
1.304, 2.000, 3.000 for the pinned 1.005, 1.08, 1.3, 2, 3; `moving_08`
1.293 (pinned 1.224 to 1.296), `moving_3` 1.419, `moving_1` 1.854; the
exits at ticks 198 (`moving_3`, pinned 149 to 493) and 86 (`moving_1`,
pinned 69 to 172), none in `moving_08` (pinned none before 464). The second
window outside at six rungs: the lamp's k read from its births rose by 0.03
to 0.04 between the windows at every rung below 2 (`still_005` 0.007 to
0.042, `still_1` 1.000 to 1.027), and the detector's 1 + z with it (1.0375,
1.112, 1.330, 2.041 for the pinned 1.005, 1.08, 1.3, 2). The cause is not
the crowd: the lamp's births per 50 intervals fell from 50 to 47 in
`still_005` with two waits in the whole run. It is the lamp's own spending,
known from the register (a lamp's wheel turns by its content over K, and
the content falls by one unit per birth): 8192 - 483 units by the end, a
wheel 6 % slow. The design did not foresee it; the worlds were amended to a
reservoir of 2^20 units (a spending of 0.05 %) and run again. Nothing else
changed.

**The second run, the lamp of 2^20 units.** Every one of the 32 readings
inside the pins (the k read from the lamp's births within its bracket or
within 0.02; the detector's 1 + z within its bracket or within 0.02; the
exits within their brackets; the light escaping whole):

| World | pinned k | k read (window 1, window 2) | 1 + z read at the detector (window 1, window 2) | pinned 1 + z | click rate | age read | light escaped | lag at the end; the exit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `still_005` | 0.005 | 0.000, 0.007 | 1.0000, 1.0064 | 1.005 | 1.000, 0.993 | 172 | 326 of 326, no ordinal missing | - |
| `still_08` | 0.08 | 0.079, 0.079 | 1.0802, 1.0800 | 1.08 | 0.927 | 172 | 304 of 304 | - |
| `still_3` | 0.3 | 0.293, 0.304 | 1.3000, 1.3000 | 1.3 | 0.767 | 172 | 253 of 253 | - |
| `still_1` | 1 | 1.000, 1.000 | 2.0000, 2.0000 | 2.0 | 0.500 | 172 | 166 of 166 | - |
| `still_2` | 2 | 2.000, 2.000 | 3.0000, 3.0000 | 3.0 | 0.333 | 172 | 112 of 112 | - |
| `moving_08` | 0.08 | 0.079, 0.064 | 1.2827, 1.2714 | 1.224 to 1.296 both | 0.773, 0.793 | 80, 104 | 344 of 344 | 4 Links; no exit (pinned none before 464) |
| `moving_3` | 0.3 | 0.240, 0.181 | 1.4152, 1.4768 | 1.2 to 1.56 both | 0.700, 0.680 | 78, 99 | 314 of 314 | 8 Links; the exit at tick 181 (pinned 149 to 493) |
| `moving_1` | 1 | 0.442, 0.007 | 1.8514, 1.2058 | 1.2 to 2.4, then 1.2 | 0.567, 0.833 | 75, 96 | 312 of 312 | 8 Links; the exit at tick 86 (pinned 69 to 172) |

The windows are 200 to 350 and 350 to 500 for the still worlds, 100 to 250
and 250 to 400 for the moving ones; the age read is the flight, 172
intervals fixed for the still lamp and growing for the receding one. The
k read in `moving_1`'s second window is out of the in-crowd bracket because
the lamp is out of its crowd, as pinned: 0.007 is one wait in 150
intervals, a residual of the fan's edge (the digital line of (-4, -3, 0)
visits three Nodes of the lamp's plane, x - 3 to x - 5, so the fan reaches
five Links, not four; the lag settles at 7 to 8 Links and creeps by the
residual). The k read of a moving lamp inside its fan is below the pin
(0.24 and 0.18 for 0.3; 0.44 for 1) because it sits behind the heading, on
the oblique directions' crossing Nodes, as the bracket allowed.

**What the runs decide.**

1. **The crowd's clock is k = 4 F / 2^16, exact to the rung and linear over
   a factor of 400 in F.** A lamp at rest inside a crowd reads z = 1 at
   F = 16384 and z = 2 at F = 32768, and the count is unbounded: the law as
   built has a redshift that is no speed.
2. **The light escapes whole.** Every birth ordinal up to the last click
   arrived, at every rung; the crowd slows the clock and takes nothing from
   the light (the rows `pass`; the coupling is off by the world's word, so
   this is the clock alone).
3. **The clock's term adds to the Doppler at the detector.** `moving_08`
   read 1.283 and 1.271 with the k read 0.079 and 0.064: between the sum
   1 + k + v / c (1.279, 1.264) and the product (1 + k)(1 + v / c) (1.295,
   1.277), inside the tolerance of both, nearer the sum. The pin (d) wrote
   the product; the lamp's speed on the GameBoard is v / (1 + k) (item 4),
   so the Doppler is by that speed and the reading is (1 + k)(1 + v /
   ((1 + k) c)) = 1 + k + v / c whether or not the crowd keeps pace. Series
   Q decides between the two forms with a comoving crowd (2.2147 read for
   the sum's 2.200 against the product's 2.400): the sum. The excess of
   0.004 to 0.007 over the sum here is series V's too (the moving lamp's
   slightly higher k).
4. **A slowed lamp cannot travel with an unslowed crowd.** It moves at
   v / (1 + k) (the step drive counts Links only at a self-creation), falls
   behind at the pinned rate, leaves the fan within the pinned bracket, and
   reads the Doppler alone thereafter (1.85 to 1.21 in `moving_1`). A
   crowd carries a slow clock only when the crowd is slowed alike, as every
   star of a galaxy is in the crowd of all the others: then the whole crowd
   moves at v / (1 + k), and the detector reads
   1 + z = (1 + k)(1 + v / ((1 + k) c)) = 1 + k + v / c, the two terms
   adding, not multiplying. The same holds for the lamp left behind: its
   own speed is v / (1 + k) too (item 3). Series V runs the comoving case.
5. **The first run's lesson.** A lamp's own spending reads as a k of the
   order of births / K; a clock experiment needs a reservoir far beyond the
   run's births, or a lamp of the fraction-free kind whose wheel does not
   spend.

**For the owner's remark.** Under the law as built a distant crowd's lamp
reads 1 + z = 1 + k with the crowd at rest, k the presence of the crowd's
rows at its Node over the suspension's wall, with no bound and no speed;
here k = 1 took a presence of 65536 = d at one Node, two sources of 16384
units per interval each, about 500 G2 stars' worth of release (64 units per
interval each) through one Node. Whether nature's z is of this kind the run
cannot say (section 5); what it says is that the law's clock term is a
candidate that reads z >= 1 from a body at rest, escapes whole and is
additive with the Doppler for a crowd slowed alike.
