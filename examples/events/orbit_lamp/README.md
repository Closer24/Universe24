# Series D3, Newton after a detector: the orbit read by a lamp on the probe

Five worlds of one base, written by `make_worlds.py` with their
expectations before the runs (`expectations.json`); the register entry is
[D3, Newton after a detector (2026-09-22)](../../../docs/EXPERIMENTS.md#d3-newton-after-a-detector-2026-09-22).
The chief physicist's design (records 574 and 594 of
[the log](../../../docs/LOG_2026-09-20.md)) on the owner's word (record
581, "build them"; 01:09Z on the deviation below, "Build"): series C read
Newton's push off the probe's own register, a GameBoard reading; what a
detector can read of a body that falls or orbits is where its light comes
from and when, so the probe of series D carries a lamp and a line of
one-Node detectors reads the lamp's rows. Every number here is labelled
DETECTOR (the clicks' x, tick and age) or GAMEBOARD (a diagnostic, never
pinned); the pins were written before any run; a reading outside its pin
is registered with its cause and never moved.

## The six lines

1. **The information.** The lamp on the probe releases one row toward +y
   and one toward -y every 8 intervals, each carrying one unit of the
   probe's own paid content; the row toward -y walks the heading -y at c =
   32 / 55 Links per interval, keeping its x, to the detector line at y =
   20, where the wall's `measure` entry with `reads: "age"` clicks it with
   its age; the row toward +y is lost to the face +y; the fan's rays cross
   the line unread (`pass`). What is kept: x at the birth and the birth's
   tick (the click's tick less its age). What is lost: the probe's y, its
   momentum, its store (the reading never touches them).
2. **The generic solution.** One primitive, for every family alike: a
   paid family's lamp spends its own content and births records on its
   declared directions; a wall's `measure` entry clicks a row with the age
   moment; the push on a body is the one bilinear form on the arriving
   labels, scaled by its whole content, and the step divides by that
   content (the equivalence). No rule, no key, no identity added.
3. **Why it will work.** The orbit sweeps every line of the fan once per
   turn, so its mean push per turn is the ring mean q L C / (2 pi r), the
   1 / r force of DERIVATIONS 3.3 (a resting Node reads one line or none,
   DERIVATIONS 3.2), and the clicks' x(t) turns with the orbit: its
   recurrence is the period, its lagged second difference the angular
   rate squared. The reading that shows it: T proportional to r, the
   ratio 2.00. The reading that refutes it: the ratio outside 2.00 +-
   0.18, a period outside its bracket, or the 4 M_held world off the same
   clicks.
4. **Why do this at all.** The first Newton reading by a click, the one
   NATURE's inverse-square row can carry; G's place and the equivalence
   principle without the board. Without it series C's Newton stays a
   GameBoard diagnostic and the paper's table has no detector reading of
   the 1 / r force.
5. **The Highlights.** Kept: 281 (only a detector's reading is a
   measurement), 562, 564 (a GameBoard reading is a diagnostic, never
   pinned or compared with nature), 569 (every external entity a detector
   or an emitter; an emitter is also a detector at its own Node), the pin
   first, the fraction-free law. Nothing proposed to change.
6. **The implementation.** The generator here (five worlds, the pins), the
   tool `tools/orbit_lamp_readings.py` (the click lines only), the test
   `tests/test_orbit_lamp_readings.py`, this README, the register entry,
   the index row; no engine change; danger none (a new folder, a new tool,
   a new test); host time 14 s per world with the source, 7 s without
   (GAMEBOARD).

## The base and what changes from series D

The plane of series D ([orbit/](../orbit/README.md)): 121 x 121 x 1 Nodes,
the z axis periodic, the centre c = (60, 60, 0), `suspension` 0, `width` S
= 32, N 64, the source a fixed measured event of the free phase-less family
`m` at c releasing one ray per direction every 10 intervals on the uniform
fan of the 120 primitive in-plane directions with a^2 + b^2 <= 64 (q = 12
units per interval, L = 1.0000 the fan's mean |u_d| / Q), the probe at (60
+ r, 60, 0) with the tangential momentum p = n Q M_total of the circular
orbit. The shipped worlds (the re-run of 2026-09-22 on the owner's word of
01:42Z) declare n = 9, the circle under the per-axis drive the engine runs
(BEAM_LAW note 17: the pace n / (S + n) per axis, n^2 / (S + n) = q L C /
(2 pi), the real root 8.83 at S = 32, the whole 9, series D's own p = 576
per unit of content). The first run declared n = 10, the circle under the
directional drive (form B, note 49, which the engine does not run: the
real root 9.63, the whole 10, the orbit register's lamp worlds); its rows
stay below as history with their cause. What changes from series D, and
nothing else:

- **The probe** is a body of a paid family of its own, `probe` (`quantum`
  1, the default phase circle), of `amount` R = 2^12, the lamp's
  reservoir, holding the free mass `held` {"m": 2^20} the fan pushes (the
  keys' own rule for `m`, `read`, not written out); M_total = R + M_held,
  the reservoir 0.4 % of it; K = M_held so that the turn is 1 at every
  self-creation and never 0
  (a turn of 0 skips the birth). The deviation of 00:56Z: the design's
  `amount` 1 silences the lamp (the birth gate `held // (cost x quanta)
  >= 1` with the cost 1 and 2 quanta per birth), settled by the chief
  physicist's word of 01:09Z as proposed.
- **The lamp**: `rate` [1, 8], `wheel` [1, N], `directions` [[0, 1, 0],
  [0, -1, 0]]: two rows per birth in opposite directions, the recoil
  cancelling exactly by the pair. The probe's `directions` (the directions
  it re-emits a row of its own taken home on) are the same pair; the
  default six headings put a homed row on +-z, which on a plane of one
  Node in z comes home again at once.
- **The detector line** at y = 20: 121 measured events of the paid family
  `wall`, each the one-Node detector `line_<x>` reading `wave` at the
  threshold 1, the entry for `probe` {"rule": "measure", "reads": "age"},
  for `m` `pass`; the source's entry for `probe` `pass`.
- **The source's content** M = 2^32 at `release` [1, 2^32 x 10]: the same
  one ray per direction every 10 intervals as series D's 2^10 at [1, 2^10
  x 10], the denominator scaled so that the probe's held mass, which the
  same key would release on the body's directions at `by_clock(age,
  M_held, d)`, releases nothing within the run (its first ray at the age
  40960; 10240 in the 4 M_held world).

| World | The source | r | `held` m | K | p (label units) | Intervals |
| --- | --- | --- | --- | --- | --- | --- |
| `r12` | M, the fan | 12 | 2^20 | 2^20 | 576 x (2^12 + 2^20) = 606 348 288 (the first run 640 x, n = 10) | 4000 |
| `r24` | the same | 24 | 2^20 | 2^20 | the same | 4000 |
| `r24_4m` | the same | 24 | 2^22 | 2^22 | 576 x (2^12 + 2^22) = 2 418 458 624 | 4000 |
| `r12_control` | none | 12 | 2^20 | 2^20 | as `r12` | 4000 |
| `r24_control` | none | 24 | 2^20 | 2^20 | as `r24` | 4000 |

## The pins, written before the runs (`expectations.json`)

From DERIVATIONS_BEAM 3.3 on the plane (the 1 / r force, a flat rotation
curve: v the same at every r, T proportional to r) at the declared n = 9
under the per-axis drive's pace n / (S + n) = 9 / 41 = 0.2195 Links per
interval (the shipped register; the first run's pins at n = 10 under the
directional drive's 0.2033, T = 371 and 742 with the same brackets, the
escape at 60 steps, are reproduced by `expectations(10, "directional")`
and stand in the history block below):

- **The period** T = 2 pi r / v: 343 at r = 12 and 687 at r = 24 (series
  D's own table), each within the continuum map's own margin of 9 percent
  (313 to 374; 625 to 749). DETECTOR: the recurrence of the clicks' x, the
  mean spacing of successive crossings of the centre column in one
  direction, each crossing interpolated between the two births that
  bracket it.
- **The ratio** T(24) / T(12) = 2.00 +- 0.18; k = 2 on the plane (space's
  k = 3 would give 2.83).
- **The second difference** of the clicks' x against t at the lag h of a
  quarter period (88 and 168 intervals): x(t + h) - 2 x(t) + x(t - h) =
  -4 sin^2(omega h / 2) (x(t) - c_x), so omega^2 = (2 pi / T)^2 = 3.35e-4
  and 8.37e-5 per interval^2 (the brackets from T's), the acceleration a =
  omega^2 r = v^2 / r = 4.02e-3 and 2.01e-3 Links per interval^2, the
  ratio 2.00 (3.3's small-n limit q L C / (2 pi r S), with v = n / S, is
  4.97e-3 and 2.49e-3, the ratio 2.00 again; at n = 9 the pace 9 / 41 is
  0.78 of the limit's 9 / 32).
- **The amplitude** of the clicks' x, (max - min) / 2: r - 1 to r + 2 (the
  near-circular loop of the whole 9 above 8.83).
- **The equivalence**: `r24_4m` reads T within one birth interval (8) of
  `r24`'s and the same x on every common birth tick within one Node.
- **The controls**: every click at x = 60 + r; the probe leaves through the
  face +y at its 61st step (from y = 60 to 121), 61 / v = 278 (+- 6).
- **Read beside the pins, not pinned**: the radius at every birth from the
  clicks alone, x the column and y the line's y plus the Links the row
  walked by its age off the flight table (the tool's `links_of`): its
  least, greatest and mean over the run, the loop's shape.
- **Refuted if** the ratio leaves 2.00 +- 0.18, a period or omega^2 leaves
  its bracket, or the two held masses' periods differ beyond one birth
  interval. A record check (completed, the books balanced at every tick)
  fails the tool.

Run and read:

```bash
PYTHONPATH=src python examples/events/orbit_lamp/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/orbit_lamp examples/events/orbit_lamp/r*.json
PYTHONPATH=src python tools/orbit_lamp_readings.py artifacts/orbit_lamp
```

## The first run at n = 10 (2026-09-22, history: measured against its pins, the cause named, none moved)

The rows of the first run, at the declared n = 10 under the directional
drive's pins (T = 371 and 742, the escape 295), kept as registered; the
re-run at n = 9 on the owner's word of 01:42Z follows in the next section.

Source fingerprint `5a5b79ef438c1c6c` (the checkout of
`newton-after-detector` off `origin/main` at `fa2cb6d`, package 0.3.1),
Python 3.14.0rc2, numpy 2.5.3, headless, four cores, `tools/run_series.py
--jobs 4`; every run completed at 4000 intervals (14.0, 14.2, 13.5, 6.7,
7.0 s for `r12`, `r24`, `r24_4m`, `r12_control`, `r24_control`) with the
books balanced at every tick; the digests (state, audit, events):
`7aa490bef500`, `440b994b82fe`, `48e096ef364f` (`r12`); `f6578cc73a0e`,
`11d80c9ec029`, `494337f52bcc` (`r24`); `330741539a62`, `c082e13c5f93`,
`75b4a7dfa20e` (`r24_4m`); `85f0b01726ac`, `1f207245cd75`,
`072fd725e929` (`r12_control`); `3add671fad16`, `1f207245cd75`,
`beff00cf66eb` (`r24_control`). `tools/orbit_lamp_readings.py`: 0 record
checks failed, 3 readings inside, 13 outside, none moved.

DETECTOR readings (the line's clicks: x, tick, age):

| World | Clicks | x from .. to | Amplitude (expected) | Crossings down, up | T (expected) | omega^2 (expected) | a = omega^2 x amplitude | The probe's escape (a face click) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r12` | 222 | 28 .. 119 | 45.5 (11 .. 14): outside | 3, 3; the spacings 565 .. 832 | 697 (338 .. 404): outside | 6.42e-5 (2.42e-4 .. 3.47e-4): outside | 2.92e-3 | `face:+x` at the tick 1940 |
| `r24` | 91 | 37 .. 120 | 41.5 (23 .. 26): outside | 2, no spacing | none: outside | 1.21e-4 (6.04e-5 .. 8.67e-5): outside | 5.04e-3 | `face:+x` at the tick 780 |
| `r24_4m` | 91 | 37 .. 120 | 41.5 (23 .. 26): outside | 2, no spacing | none: outside | 1.21e-4: outside | 5.04e-3 | `face:+x` at the tick 780 |
| `r12_control` | 32 | 72 .. 72 | 0 | - | - | - | - | `face:+y` at the tick 257 (289 .. 301): outside; every click at x = 72: inside |
| `r24_control` | 32 | 84 .. 84 | 0 | - | - | - | - | `face:+y` at the tick 257 (289 .. 301): outside; every click at x = 84: inside |

Across the worlds: the ratio T(24) / T(12) none (no period at r = 24):
outside; the equivalence on the period none: outside; the equivalence on
the clicks: 91 common birth ticks, 91 equal, the largest difference 0
Nodes: inside (the 4 M_held world reads the same x on every click, to
the Node, and leaves through the same face at the same tick). The birth
ticks of every click lie on the 8-interval grid (none read late).
GAMEBOARD, a diagnostic: homes 47 (`r12`), 13, 13, 7, 7.

**The cause, read off the controls, not a number moved.** The controls'
probe, unpushed, walks +y at the declared p and leaves through the face
+y at the tick 257: 61 steps in 257 intervals, the pace 0.238 = n / (S +
n) at n = 10, the per-axis drive of BEAM_LAW note 17 (`step_axis`) that
`main` runs, and not the directional drive's 0.2033 (form B, note 49,
which "has not landed", `engine.py`, the covariant frame's note). The
pins were written at form B's pace, as the orbit register's lamp worlds
were (a design, no run). Under the per-axis drive the circular condition
is n^2 / (S + n) = q L C / (2 pi) = 1.91, n = 8.83, the whole 9 (series
D's own p = 576 per unit of content); the declared n = 10 is 25 percent
above its circle in n v, so the probe makes the wide loop series D
registered at S = 32 (an eccentric rosette; the registered `s32_r24` at
p = 576, r from 10.6 to 67.5 in the orbit register's account): at r = 12 the loop
runs from x = 28 to 119 (r from 12 to about 59) and leaves the 121-wide
plane through the face +x after 1940 intervals, three turns of about 700;
at r = 24 it leaves after 780 intervals, before one turn. The period of
371 and 742, the ratio and omega^2 are therefore not read; what is read,
DETECTOR, stands: the clicks give x(t) one birth in every 8 intervals
with none late; the equivalence holds to the Node on every click and to
the tick on the escape (nothing of the body enters its motion); the
controls read x constant at 60 + r on every click and the pace of the
unpushed probe. What would read the pins is the same five worlds at the
per-axis drive's circle, n = 9, with T = 2 pi r (S + n) / n = 343 and
687 (series D's table) and the same brackets: one declared integer, the
chief physicist's to order; not run here (the order was this design and
nothing else).

The register entry marks every reading inside or outside as above; the
brackets are the design's and are not moved.

## The re-run at n = 9 (2026-09-22, measured against the pins of `expectations.json`)

The owner's word of 01:42Z on the first run's cause: the same five worlds
at n = 9, series D's own p = 576 per unit of content, the circle of the
per-axis drive the engine runs; the one integer changed in the generator,
the pins above committed at `fccedae` before the run.

Source fingerprint `5a5b79ef438c1c6c` (the same tree, package 0.3.1),
Python 3.14.0rc2, numpy 2.5.3, headless, four cores, `tools/run_series.py
--jobs 4`; every run completed at 4000 intervals (14.1, 14.1, 14.6, 6.3,
6.5 s for `r12`, `r24`, `r24_4m`, `r12_control`, `r24_control`) with the
books balanced at every tick; the digests (state, audit, events):
`2efe9c62ae58`, `51473f85b03e`, `96b08fae30c6` (`r12`); `36aba6039399`,
`b55f5157d83b`, `91a78c954c4e` (`r24`); `75be887c26e8`, `dd12491c6711`,
`f6a6e35e2614` (`r24_4m`); `f3e51b857359`, `b91606cc2ff5`,
`f183a351cb89` (`r12_control`); `1fe2802ea974`, `b91606cc2ff5`,
`d76f1661df10` (`r24_control`). `tools/orbit_lamp_readings.py`: 0 record
checks failed, 7 readings inside, 9 outside, none moved.

DETECTOR readings (the line's clicks: x, tick, age; the radius from x and
the age):

| World | Clicks | x from .. to | Amplitude (expected) | The radius at the births: least .. greatest, mean | Crossings down, up | T (expected) | omega^2 (expected) | a = omega^2 x amplitude | The probe's escape |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r12` | 80 | 18 .. 86 | 34 (11 .. 14): outside | 1.4 .. 73.2, 24.2 | 2, 1; one spacing | 407 (313 .. 374): outside | 1.03e-4 (2.82e-4 .. 4.04e-4): outside | 3.52e-3 | `face:+y` at the tick 698 |
| `r24` | 139 | 1 .. 103 | 51 (23 .. 26): outside | 11.0 .. 62.3, 33.7 | 2, 1; one spacing | 813 (625 .. 749): outside | 4.16e-5 (7.04e-5 .. 1.01e-4): outside | 2.12e-3 | `face:-x` at the tick 1239 |
| `r24_4m` | 139 | 1 .. 103 | 51 (23 .. 26): outside | 11.0 .. 62.3, 33.7 | 2, 1; one spacing | 813: outside | 4.16e-5: outside | 2.12e-3 | `face:-x` at the tick 1239 |
| `r12_control` | 34 | 72 .. 72 | 0 | 12.0 .. 60.2 (the probe walking +y) | - | - | - | - | `face:+y` at the tick 278 (272 .. 284): inside; every click at x = 72: inside |
| `r24_control` | 34 | 84 .. 84 | 0 | 24.0 .. 63.7 | - | - | - | - | `face:+y` at the tick 278 (272 .. 284): inside; every click at x = 84: inside |

Across the worlds: the ratio T(24) / T(12) = 813.3 / 407.3 = 1.997 (1.82
.. 2.18): inside; the equivalence on the period |T(`r24_4m`) - T(`r24`)|
= 0 (0 .. 8): inside; the equivalence on the clicks: 139 common birth
ticks, 138 equal, the largest difference 1 Node (0 .. 1): inside (the
4 M_held world leaves through the same face at the same tick). Every
birth tick lies on the 8-interval grid (none read late). GAMEBOARD, a
diagnostic: homes 15 (`r12`), 24, 24, 8, 8.

**What is read and what is not, no number moved** (the physics
reviewer's two corrections of 02:24Z folded, prose only). What D3
closes, DETECTOR: the equivalence principle after a detector (the 4
M_held world 138 of 139 clicks to the Node, the same escape tick, |dT|
= 0) and the controls' pace to the tick (the 61st step at 278 exactly;
the pin's 60-step count of the first run corrected in the derivation,
the reading not). The ratio of the two radii's recurrences, 1.997
against 2.00 inside its bracket, is consistent with the 1 / r form and
not decisive: a 1 / r force is scale-invariant (r to lambda r, t to
lambda t at the same speed), so two loops started with the same p at r
= 12 and 24 must be similar figures with T(24) / T(12) = 2 for any
eccentricity, a property no other power of r has; but the loops read are
not similar figures (the radii 1.4 to 73.2 about 24.2 against 11.0 to
62.3 about 33.7), and each period is one recurrence, one spacing between
two like crossings before the probe leaves the plane (after 698 and
1239 intervals). The scale symmetry of the 1 / r force is the claim the
ratio tests; not closed. The reading that would decide, named and not
run, not proposed: similar loops at a finer grain, or several
recurrences per radius agreeing. Not read as pinned: the periods
themselves (407 against 343 and 813 against 687, 19 percent above their
circles alike), the amplitudes and the radii, omega^2 at a quarter
period of a loop that is not a circle. Two causes, both named. The
grain of the push: the loops are the eccentric ones series D registered
at the same p = 576 (its `s32_r24`: T 829 against 687, escaped through
`face:-x` at 1054, the mean radius 28.3; its `s32_r12`: T 289, one
turn, escaped at 2891; "the grain of the push breaks the rest"): the
push comes in whole labels of 64 on p = 576 per unit of content, 6.4
degrees per ray, along the fan's lines and in shells every 10
intervals, and a probe on the axis reads the heading's line alone until
it moves off it. The per-axis drive's own anisotropy: the Euclidean pace
on a diagonal heading is sqrt 2 x (n / sqrt 2) / (S + n / sqrt 2) =
0.2346 against the axis's 0.2195, 6.9 percent faster at 45 degrees, so
no circle exists under the drive `main` runs even with a continuous
push. A circle at this grain is not what the law gives at S = 32, and
no pin is moved to say otherwise.

## The one-constant worlds (flow-link-v1, 2026-09-22): the pins before any run

The owner's decision of 2026-09-22 (record 915 of
[the log](../../../docs/LOG_2026-09-20.md), about 10:05Z): Newton's rows
go on the one constant of gravity, the hypothesis flow-link-v1 of
[the design](../../../docs/designs/flow_weight/DESIGN.md) (section 3 (c),
the pins that move; section 6, the key) and
[its algebra](../../../docs/designs/flow_weight/ALGEBRA.md) (section 5,
Newton's rows by formula), in parallel with the ring world's run. Under
the world key `flow_link` the arrival flow every reader sums carries per
arriving row the flow label nearest `Q D / S_1` in place of the unit
label, so every push is divided by its fan's mean of `S_1 / |D|`, the
Nodes per Euclidean Link of a digital line; the age moment, the wall and
the flight are untouched. The key is the Flow Link Builder's (one writer
of the code); these four worlds and their pins are series D3's side of
it, written by the generator before any run (`worlds(flow=True)`,
`expectations(flow=True)`, `expectations_flow.json`), the registered
five worlds and `expectations.json` untouched, byte for byte.

| World | The source | r | `flow_link` | `held` m | K | p (label units) | Intervals |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `r12_flow` | M, the fan | 12 | true | 2^20 | 2^20 | 512 x (2^12 + 2^20) = 538 968 064 (n = 8) | 4000 |
| `r24_flow` | the same | 24 | true | 2^20 | 2^20 | the same | 4000 |
| `r12_flow_control` | none | 12 | true | 2^20 | 2^20 | as `r12_flow` | 4000 |
| `r24_flow_control` | none | 24 | true | 2^20 | 2^20 | as `r24_flow` | 4000 |

Each is the registered `r12`, `r24` or its control with two changes and
no other: the key `flow_link: true`, and the probe's momentum at the
whole n = 8 of the circle under the key (the model ids
`rays-orbit-lamp-r12-flow-plane-v1` and so on). No equivalence world: the
equivalence carries no constant and is closed by the registered run.

**The derivation, the generator's own and not by hand.** The generator
computes on its own fan of 120 the mean of `S_1 / |D|`, `F_plane =
1.2871` (the design's number; `4 / pi = 1.2732` in the isotropic limit),
and divides its circular balance by it: `A = q L C / (2 pi) = 1.9098`
becomes `A / F_plane = 1.4838`, and `n^2 / (S + n) = A / F_plane` at S =
32 has the real root `n = 7.672`. The generator takes the nearest whole,
8, as it took 9 for the register's 8.83: the momentum is a whole count of
label units per unit of content, `p = n Q M_total`, and the register
declares the whole nearest the root. The design's `7.818` is the same
formula on the declared whole 9's balance `81 / 41 = 1.976` in place of
the real root's `1.910`; the two round to the same 8, and the design's
`384 / 768` at 7.818 are the generator's `377 / 754` at the whole 8, which
the design names in the same line. The band is the register's: the
generator's own margin on a period is the continuum map's 9 percent, the
one number, propagated to 0.18 on the ratio.

**The pins (`expectations_flow.json`), GAMEBOARD by formula until the
run; the clicks the measurement (DETECTOR); Newton's and Kepler's forms on
the comparison side only (record 817):**

- **The period** T = 2 pi r (S + n) / n at n = 8, the pace 8 / 40 =
  0.2000 Links per interval: 377.0 at r = 12 and 754.0 at r = 24, each
  within 9 percent (343 to 411; 686 to 822). DETECTOR: the recurrence of
  the clicks' x across the centre column, read as in the registered run
  (`tools/orbit_lamp_readings.py`, the same tool, the pins by
  `--expectations`).
- **The ratio** T(24) / T(12) = 2.00 +- 0.18, unchanged: the same fan at
  both radii and the weight of a line a constant of the line, not of r,
  so the factor cancels (754.0 / 377.0 = 2.000).
- **The second difference**: omega^2 = (2 pi / T)^2 = 2.78e-4 and 6.94e-5
  per interval^2 (the brackets from T's; the lag 12 and 24 births), the
  acceleration a = omega^2 r = v^2 / r = 3.33e-3 and 1.67e-3 (3.3's
  small-n limit with the constant C / F_plane = 0.777 in C's place:
  3.86e-3 and 1.93e-3), the ratio 2.00.
- **The amplitude**: r - 1 to r + 2, as registered.
- **The controls**: every click at x = 60 + r; the escape through the
  face +y at the 61st step of the pace 8 / 40, the tick 305 +- 6. A
  world without a crowd reads nothing under the key (the design's section
  3 (d)).
- **Refuted if** T leaves its band, the ratio leaves 2.00 +- 0.18, or the
  control moves under the key (a click off x = 60 + r, or the escape off
  305 +- 6). A record check (completed, the books balanced at every tick)
  fails the tool.
- **Read beside the pins, not pinned.** The registered run at n = 9 read
  its periods 19 percent above the circle's (407 and 813 against 343 and
  687) with two causes named, the grain of the push and the per-axis
  drive's anisotropy; both stand under the key, which changes the push's
  constant and nothing of its grain. The pins here are the circle's by
  the register's convention, and a reading outside its band is registered
  with its cause and never moved. The byte identity of a flow control
  with a keyless control at n = 8 is the design's by formula (section 3
  (d)) and is not run here.

**The world files.** `make_worlds.py` writes the four world files with
the key beside the registered ones; they ship in the commit that runs
them, after the key is on `main`, because the loader refuses a key it
does not know (`beam-v1: the world has unknown keys: flow_link`, the
validation gate over every shipped world) until the Flow Link Builder's
merge. The pins ship first, here. Run and read, then:

```bash
PYTHONPATH=src python examples/events/orbit_lamp/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/orbit_lamp_flow \
    examples/events/orbit_lamp/r*_flow*.json
PYTHONPATH=src python tools/orbit_lamp_readings.py artifacts/orbit_lamp_flow \
    --expectations examples/events/orbit_lamp/expectations_flow.json
```

## The run under the key (2026-09-22): measured against the pins of `expectations_flow.json`, none moved

The Boss's order of record 962 on the owner's word (Newton in the paper,
the runs in parallel with the ring's re-run): the four worlds as committed
at `485a57dc` (the key from `origin/flow-link-build` at `a3be9ba13f08`,
merged at `c52d6946`), run once, headless, and read by the clicks alone.
Source fingerprint `00fda864cf1bb868` (package 0.3.1), Python 3.14.0rc2,
numpy 2.5.3, four cores, `tools/run_series.py --jobs 4`; every run
completed at 4000 intervals (18.5, 19.3, 9.5, 9.4 s for `r12_flow`,
`r24_flow`, `r12_flow_control`, `r24_flow_control`) with the books
balanced at every tick; every run record carries `flow_link: true` (HOST:
the key is in the run); the digests (state, audit, events):
`0ea77ef65795`, `f7f1665f5440`, `68b713ddfd7b` (`r12_flow`);
`5e8c8a49508f`, `40b90c718659`, `7821c7a1a39f` (`r24_flow`);
`00f547a511a9`, `fc6e4b4f9a6b`, `aed4121a5f37` (`r12_flow_control`);
`b8005f85c902`, `fc6e4b4f9a6b`, `2c15504c6b4d` (`r24_flow_control`).
`tools/orbit_lamp_readings.py --expectations expectations_flow.json`
([run_flow.out](run_flow.out), every line by kind): 0 record checks
failed, 4 readings inside, 7 outside, none moved.

The readings by kind (the physics-rule reviewer's kinds, 2026-09-22):
DETECTOR the line's clicks (x, tick, age), the amplitude, the crossings,
T and omega^2 read off them, the escape; CONVERSION the radius at the
births (the age click turned into y by the flight table); COMPUTATION
the acceleration omega^2 x amplitude (a product of two moments) and the
ratio T(24) / T(12) (two DETECTOR periods of two records):

| World | Clicks | x from .. to | Amplitude (expected) | The radius at the births, CONVERSION: least .. greatest, mean | Crossings down, up; the spacings | T (expected) | omega^2 (expected) | a = omega^2 x amplitude, COMPUTATION | The probe's escape |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r12_flow` | 145 | 31 .. 96 | 32.5 (11 .. 14): outside | 3.2 .. 68.3, 24.3 | 2, 2; 445 .. 732 | 588.7 (343 .. 411): outside | 7.78e-5 (2.34e-4 .. 3.35e-4): outside | 2.53e-3 | `face:+y` at the tick 1208 (the detector line touched at 808) |
| `r24_flow` | 288 | 0 .. 90 | 45 (23 .. 26): outside | 17.0 .. 71.0, 37.6 | 3, 2; 789 .. 1184 | 987.3 (686 .. 822): outside | 3.11e-5 (5.85e-5 .. 8.39e-5): outside | 1.40e-3 | `face:-x` at the tick 2452 (the detector line touched at 633) |
| `r12_flow_control` | 38 | 72 .. 72 | 0 | 12.0 .. 61.2 (walking +y) | - | - | - | - | `face:+y` at the tick 305 (299 .. 311): inside; every click at x = 72: inside; the detector line never touched |
| `r24_flow_control` | 38 | 84 .. 84 | 0 | 24.0 .. 64.6 | - | - | - | - | `face:+y` at the tick 305 (299 .. 311): inside; every click at x = 84: inside; the detector line never touched |

Across the worlds: the ratio T(24) / T(12) = 987.3 / 588.7 = 1.677 (1.82
.. 2.18), COMPUTATION from two DETECTOR periods of two records: outside.
Every birth tick lies on the 8-interval grid (none read late). GAMEBOARD,
a diagnostic: homes 23 (`r12_flow`), 40, 7, 7.

**The correction of 2026-09-22 (the Newton Diagnostician's replay of the
registered events, the Boss's record 1022; the register's first record of
this run, record 966, said "none in 4000 intervals").** The probes'
own face clicks are in the registered events (`click` lines of the
probe's number on a `face:` detector): `r12_flow` ESCAPED through
`face:+y` at the tick 1208 and `r24_flow` through `face:-x` at 2452,
DETECTOR. The tool read them and printed the escape only for the
controls; it prints the escape and the contacts for every world since
this correction, and `run_flow.out` is regenerated from the same events
(the digests unchanged, no other number moved). Both probes also touched
the detector line at y = 20 once (the register's `contact` lines of the
probe's number: `r12_flow` at the tick 808 at (31, 21), `r24_flow` at 633
at (71, 21), the wall's `measure` entry taking the whole p_y component of
the probe's momentum), DETECTOR; the controls never did. So the periods
588.7 and 987.3 are the means of two and three spacings of loops that
never closed: the probes left the plane at 1208 and 2452, after 145 and
288 clicks, and each period is read from the crossings before the
escape. No pin moved, no verdict moved: FAIL as read stands.

**The paper's row, by kind, as the physics-rule reviewer wrote it
(2026-09-22):** Under flow-link-v1 (the key `flow_link`) the lamp probe
launched at the circle's whole n = 8 leaves the plane at r = 12 and 24
(DETECTOR: through `face:+y` at the tick 1208 and `face:-x` at 2452,
after touching the detector line at 808 and 633; as built the loops left
at 698 and 1239; the reviewer's row as first written said "no escape",
corrected here by the registered events) and reads the periods 588.7 and
987.3, the means of two and three spacings of loops that never closed,
against the pinned circle's 377 and 754 +- 9 percent (DETECTOR, the
recurrence of x): outside; the ratio T(24) / T(12) = 1.677 against 2.00 +- 0.18
(COMPUTATION from two DETECTOR periods): outside; the controls inside
(the escape tick 305); FAIL as read; the two loops are not similar
figures (the mean radii 24.3 and 37.6, DETECTOR), so the scale symmetry
of the 1 / r force is not tested by them, and nothing here is compared
with nature.

**The verdict by the pins as written before the run, no number moved.**
The controls INSIDE: every click at x = 60 + r and the escape at the tick
305 exactly, the 61st step of the pace 8 / 40; a world without a crowd
reads nothing under the key (the design's section 3 (d)), the controls'
two audits one digest. The periods OUTSIDE their bands, 588.7 against the
circle's 377 (56 percent above) and 987.3 against 754 (31 percent above),
and the ratio OUTSIDE its band, 1.677 against 2.00 +- 0.18: the two
readings the section above named as refuting, both read. What is refuted
is the pinned prediction, the circle's period at the whole n = 8 under
the key and the ratio 2.00 of two loops started at r = 12 and 24; the
causes, named and not moved:

- **The loops are not circles and not similar figures.** The radius at
  the births runs from 3.2 to 68.3 about 24.3 at the declared 12 and from
  17.0 to 71.0 about 37.6 at the declared 24 (the registered run as
  built, n = 9: 1.4 to 73.2 about 24.2 and 11.0 to 62.3 about 33.7); the
  mean radii's ratio is 1.55, not 2. Each period is the mean of two or
  three unequal spacings (445 to 732; 789 to 1184), the recurrence of a
  loop that never closed (the escapes at 1208 and 2452), not a circle's. The scale symmetry of the 1 / r force (T(24) /
  T(12) = 2 for similar loops, any eccentricity) is not tested by loops
  that are not similar; read beside, not pinned: T / (the mean radius) =
  24.2 and 26.3 (COMPUTATION), the periods scaling with the loops' own
  mean radii within 9 percent and not with the declared radii.
- **The whole-n grain of the launch.** At the whole 8 the launch's n^2 /
  (S + n) = 1.600 is 7.8 percent above the balance under the key (1.484,
  the root 7.672), twice the registered launch's 3.4 percent above its
  balance as built (1.976 against 1.910 at the whole 9): the probe starts
  further above its circle than the registered probe did, and the loop
  it makes is the wider for it. The momentum is a whole count of label
  units per unit of content; the register declares the whole nearest the
  root, and the nearest whole here sits on the far side of it.
- **The push's grain and the drive's anisotropy stand.** Whole labels of
  64 on p = 512 per unit of content (7.2 degrees per ray, 6.4 registered),
  along the fan's lines in shells every 10 intervals, and the per-axis
  drive's Euclidean pace 6.9 percent faster on a diagonal heading: the
  two causes the registered run named for its own periods 19 percent
  above their circles. The key changes the push's constant, not its
  grain; no circle exists on this engine at S = 32 with the key or
  without it.

What the run establishes, DETECTOR and HOST: the key is in the run (every
record's `flow_link: true`); the controls' pace to the tick at the whole
8; two loops under the key that leave the plane at 1208 and 2452 (the
registered loops as built left at 698 and 1239) after touching the
detector line at 808 and 633, with their recurrences before the escape
read. What it does not establish: the constant under the key
against the constant as built, which these worlds cannot separate from
the grain (no world as built at n = 8 was run, none ordered); the reading
that would, named and not run, not proposed: the same two worlds without
the key at the same whole 8, or a finer grain (a larger S) at both. On
flow-link-v1 itself this run decides nothing: its pins are the circle's
by the register's convention, the engine at this grain gives no circle
under the key as it gave none as built, and the hypothesis's own reading
is the ring's, stated beside this row when it comes.
