# Series X: the directional drive of a body (`drive-b-v1`)

The six worlds of series X, written by `make_worlds.py` with their
expectations before the runs (`expectations.json`); the register entry is
[X, the directional drive (2026-09-22)](../../../docs/EXPERIMENTS.md#x-the-directional-drive-2026-09-22)
and the evidence is in [validation](../../../docs/VALIDATION.md). The model
owner's approval of form B (2026-09-22, record 652 of the log of
2026-09-20, translated: "Form B is approved, go on it"), the design
[docs/designs/drive_b/DESIGN.md](../../../docs/designs/drive_b/DESIGN.md)
(form B in the integer form (c) of
[light_speed/FORM.md 3.1](../../../docs/designs/light_speed/FORM.md#31-amended-after-the-physics-rule-review-of-the-build-m1-the-residue-across-lines-and-the-correction),
the physics-rule reviewer's ADMISSIBLE WITH CORRECTIONS folded in). A
research run, made once, never a test; every expectation below was written
before the run; a reading outside its expectation is reported with its
numbers, never moved. Every number is one of two kinds
([the register](../../../docs/EXPERIMENTS.md), "Two kinds of readings"): a
DETECTOR reading (the body's click on a face of the open box: its tick, the
face, the Node it left from) or a GAMEBOARD reading (the `step` lines'
Nodes against the line of the momentum, the `drive` accumulators, the
Links before the escape, `fast_steps`: the host's view, a diagnostic). The
readings tool is `tools/drive_b_readings.py`, every line labelled by its
kind.

## Since 2026-09-22 the law's drive (the model owner, record 972)

On the owner's word of the same day (record 972 of the log of 2026-09-20,
"definitely type B should be the default"; the design
[docs/designs/drive_b/DEFAULT.md](../../../docs/designs/drive_b/DEFAULT.md))
the rule below is the law's drive of a body with nothing declared (BEAM_LAW
note 17 as amended) and the key `drive_b` is deleted: `axis_b`, `plane_b`
and `cube_b` declare nothing, and the controls `axis_main`, `plane_main` and
`cube_main` declare `per_axis_drive`, the per-axis drive of history
(`per-axis-drive-v1`), so that every pin below stands as registered; the
record carries `drive`, "line" or "per_axis". The section below is the
record of the build, its "under the key" read as "under the law" from that
day; the run blocks of `expectations.json` are the registered runs', whose
digests the flip does not touch (the state, the books and the events are the
same integers).

## What was built (the engine, under the world key alone)

The world key `drive_b` (`true`; absent or `false` by default; any other
type refused at load), the identity `drive-b-v1` under the record's
`hypotheses` and `drive_b: true` in `run.json` under the key alone. Under
it, for every free body at a self-creation:

- the three drive accumulators of the body's record (the rows the counts
  table already has, `drive` on the `step` line and in `state.json`) gain
  `p_a Q` each, Q = 64 the label's scale, checked against the integer bound
  before every addition;
- the ONE wall is `W = Q^2 S M + |p|_1 T_h` (`world.drive_wall`; M the
  content, S the world's `width`, `T_h = isqrt(3 Q^2) = 110` the flight
  table's heading resolution formed at load, `world.T_HEADING`; the two
  products tested by division before they are formed, a wall past the
  bound refusing the run naming the rule); under `covariant_readings` the
  cap term is keyed off and the wall is `Q^2 S M` (the pace per
  self-creation `p_a / (Q S M)` on every axis, `|p|_2 / E'` per lattice
  interval with the gate);
- the axis furthest over the wall makes the Link toward the accumulator's
  sign, the lowest axis on a tie, and loses W with that sign; the others
  keep their overflow for the following self-creations
  (`core.integer.by_line`, the rows' own argmax carry): the Bresenham line
  of the momentum, one Link per interval at most, no coincident fire lost,
  no direction read, no root at run time. A component of 0 leaves its
  accumulator as it is and never steps; **p** = 0 never steps; a reversal
  cancels first (the signed accumulator); a refused step at a contact pays
  W and does not move the body; the escape clicks on the face.
- the one-axis refusals of `covariant_readings` (at load and at the frame)
  are lifted when the world declares `drive_b`; the domain `|p|_1 <= Q S M`
  stays.

With the key absent the per-axis drive of BEAM_LAW note 17 runs as it did,
byte for byte (the gate set's digests, `tests/test_drive_b.py` (a)).

## The worlds

Each an open box of 41 x 41 x 41 (`"law": "beam"`, K 2^20, N 64, `release`
[1, 2^20] so no row is born within the run, `suspension` 0, `width` 1, 200
intervals), one free body of the shipped family `probe` (content 64: Q S M = 4096,
Q^2 S M = 262144) at the centre (20, 20, 20), the six open faces the
detectors; `|p|_1 = 6000` on all three momenta, so the wall under the key
is one number, W = 262144 + 660000 = 922144.

| World | **p** | The key | The pace (HOST, Links per interval) |
| --- | --- | --- | --- |
| `axis_b` | (6000, 0, 0) | `drive_b` true | per axis 0.4164; Euclidean 0.4164 (today's rule 0.5943, above the rows' 0.5818) |
| `plane_b` | (3000, 3000, 0) | true | per axis 0.2082; Manhattan 0.4164, Euclidean 0.2945 |
| `cube_b` | (2000, 2000, 2000) | true | per axis 0.1388; Manhattan 0.4164, Euclidean 0.2404 |
| `axis_main`, `plane_main`, `cube_main` | the same | absent | the per-axis drive: 0.5943; 0.4228 per axis with every y fire lost; 0.3281 per axis with every y and z fire lost |

## The expectations, pinned before the runs (`expectations.json`)

Derived by the generator from the rule's own integers (the host's replay of
`by_line` from the centre, and of `step_axis` with the lost fire for the
controls; the same integers as `docs/designs/drive_b/drive_b_map.py` (A)):

| World | Reading | Kind | The pin |
| --- | --- | --- | --- |
| `axis_b` | the click on a face | DETECTOR | tick 51 +- 1, face:+x, from (40, 20, 20) (the 21st x Link at ceil(21 W / (6000 Q)) = 51) |
| `plane_b` | the click | DETECTOR | tick 101 +- 1, face:+x, from (40, 40, 20) (ceil(21 W / (3000 Q)) = 101; x wins every tie, y trails by one Link) |
| `cube_b` | the click | DETECTOR | tick 152 +- 1, face:+x, from (40, 40, 40) (ceil(21 W / (2000 Q)) = 152) |
| `axis_main`, `plane_main`, `cube_main` | the click | DETECTOR | tick 36, 50, 65 (+- 1), face:+x, from (40, 20, 20): y and z never moved (21 and 42 coincident fires lost) |
| every world under the key | the Links before the escape | GAMEBOARD | (20, 0, 0), (20, 20, 0), (20, 20, 20) |
| every world under the key | every `step` line's Node against the line of **p** | GAMEBOARD | within one Link (the replay's 0, 0.707, 0.816) |
| every world under the key | the largest `drive` on a `step` line | GAMEBOARD | below 3 W = 2766432 (proved, DESIGN.md section 4); the replay's 381280, 1111424, 1175424, below W + 2 max |p_a| Q |
| `axis_b` | `fast_steps` | GAMEBOARD | 0 |

The tolerance of one interval on the tick covers the engine's numbering of
its first advance alone; the face, the Node and the Links are exact.

## What was measured (2026-09-22)

`tools/drive_b_readings.py` on the six runs (`tools/run_series.py --jobs
3`, 200 intervals each; the head `fcaf6f194e62...` of `run.json`'s
`source_sha256`; Python 3.14.0rc2, numpy 2.5.3, headless; 0.10 to 0.11 s
per world, 43 MB peak; every run completed with the books balanced at
every tick): 0 record checks failed, 19 readings inside, 0 outside, nothing
moved.

| World | Reading | Kind | Measured | Verdict |
| --- | --- | --- | --- | --- |
| `axis_b` | the click | DETECTOR | tick 51 on face:+x from (40, 20, 20), the momentum (6000, 0, 0) | inside (the pin 51 +- 1, the Node exact) |
| | the Links before the escape; the line; the accumulators; `fast_steps` | GAMEBOARD | (20, 0, 0); 0.000 Link off the line; the largest drive 381280; 0 | inside |
| `plane_b` | the click | DETECTOR | tick 101 on face:+x from (40, 40, 20) | inside (101 +- 1, the Node exact) |
| | the Links; the line; the accumulators | GAMEBOARD | (20, 20, 0); 0.707 Link; 1111424 (below 3 W and below 1306144); `fast_steps` 20 reported | inside |
| `cube_b` | the click | DETECTOR | tick 152 on face:+x from (40, 40, 40) | inside (152 +- 1, the Node exact) |
| | the Links; the line; the accumulators | GAMEBOARD | (20, 20, 20); 0.816 Link; 1175424 (below 1178144); `fast_steps` 40 reported | inside |
| `axis_main` | the click | DETECTOR | tick 36 from (40, 20, 20) | inside (the control: today's rule, 0.594 Links per interval) |
| `plane_main` | the click | DETECTOR | tick 50 from (40, 20, 20), y never moved | inside (the control: 21 fires lost) |
| `cube_main` | the click | DETECTOR | tick 65 from (40, 20, 20), y and z never moved | inside (the control: 42 fires lost) |

What the run establishes: on the engine as built a body under the key walks
the digital line of its momentum at the pace the wall gives it on every
direction, and no coincident fire is lost (the plane body reaches the face
at (40, 40, 20) where the control reaches it at (40, 20, 20)); with the key
absent the record is the per-axis drive's to the byte. It establishes no
physical law: the cap off the headings is the Manhattan-isotropic 64 / 110,
and the choice between this pace and the rows' triple under the law alone
is the chief physicist's and the owner's (DESIGN.md section 7).
