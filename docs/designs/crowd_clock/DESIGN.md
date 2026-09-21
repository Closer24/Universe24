# Series P, a lamp inside a crowd: the design, with the expectation pinned before any run

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

- **The lamp** `s_px1` (series G2's light family), 8192 units, a lamp of one
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
