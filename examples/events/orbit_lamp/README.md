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
+ r, 60, 0) with the tangential momentum p = n Q M_total, n = 10 (the
orbit register's lamp worlds: the circular condition n x pace(n) = q L C /
(2 pi) under the directional drive, form B, the real root 9.63 at S = 32,
the nearest whole 10). What changes, and nothing else:

- **The probe** is a body of a paid family of its own, `probe` (`quantum`
  1, the default phase circle), of `amount` R = 2^12, the lamp's
  reservoir, holding the free mass `held` {"m": 2^20} the fan pushes
  (`table` {"m": "read"}); M_total = R + M_held, the reservoir 0.4 % of
  it; K = M_held so that the turn is 1 at every self-creation and never 0
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
| `r12` | M, the fan | 12 | 2^20 | 2^20 | 640 x (2^12 + 2^20) = 673 720 320 | 4000 |
| `r24` | the same | 24 | 2^20 | 2^20 | the same | 4000 |
| `r24_4m` | the same | 24 | 2^22 | 2^22 | 640 x (2^12 + 2^22) = 2 687 176 320 | 4000 |
| `r12_control` | none | 12 | 2^20 | 2^20 | as `r12` | 4000 |
| `r24_control` | none | 24 | 2^20 | 2^20 | as `r24` | 4000 |

## The pins, written before the runs (`expectations.json`)

From DERIVATIONS_BEAM 3.3 on the plane (the 1 / r force, a flat rotation
curve: v the same at every r, T proportional to r) at the declared n = 10
under the directional drive's pace 64 n / (64 S + 110 n) = 0.2033 Links
per interval:

- **The period** T = 2 pi r / v: 371 at r = 12 and 742 at r = 24, each
  within the continuum map's own margin of 9 percent (338 to 404; 675 to
  809; the orbit register's lamp_orbits_map integrates 392 and 784 inside
  them). DETECTOR: the recurrence of the clicks' x, the mean spacing of
  successive crossings of the centre column in one direction, each
  crossing interpolated between the two births that bracket it.
- **The ratio** T(24) / T(12) = 2.00 +- 0.18; k = 2 on the plane (space's
  k = 3 would give 2.83).
- **The second difference** of the clicks' x against t at the lag h of a
  quarter period (96 and 184 intervals): x(t + h) - 2 x(t) + x(t - h) =
  -4 sin^2(omega h / 2) (x(t) - c_x), so omega^2 = (2 pi / T)^2 = 2.87e-4
  and 7.18e-5 per interval^2 (the brackets from T's), the acceleration a =
  omega^2 r = v^2 / r = 3.44e-3 and 1.72e-3 Links per interval^2, the
  ratio 2.00 (3.3's small-n limit q L C / (2 pi r S), with v = n / S, is
  4.97e-3 and 2.49e-3, the ratio 2.00 again; at n = 10 under the cap the
  pace is 0.65 of the limit's).
- **The amplitude** of the clicks' x, (max - min) / 2: r - 1 to r + 2 (the
  rosette's extents of the map).
- **The equivalence**: `r24_4m` reads T within one birth interval (8) of
  `r24`'s and the same x on every common birth tick within one Node.
- **The controls**: every click at x = 60 + r; the probe leaves through the
  face +y near the tick 60 / v = 295 (+- 6).
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

## The readings (2026-09-22, measured against expected)

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
