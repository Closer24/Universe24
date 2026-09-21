# optical-v1's pin worlds: light beside a mass under the key `optical`

The generic `optical-v1` (the model owner's "go" of 2026-09-21, record 303,
"clearly, in the generic form", records 421 to 428; the design
[docs/designs/one_wall/NOTE.md](../../../docs/designs/one_wall/NOTE.md) at
12423748 with REVIEW_3's four
must-fixes (docs/designs/optical_v1/REVIEW_3.md on branch claude/optical-v1-review-3) and the physicist's fifth), built on branch `optical-v1` on
2026-09-21: series K's `mass` (M = 2^16, b = 6) and `near` (2^16, b = 3)
at the suspension pair [1, 16384], the mass sixteen times series K's,
under `optical: gamma` at gamma = 0 (f = 1 + gamma = 1, the six verbs' own
number, Newton's half) and gamma = 1 (f = 2, nature's PPN gamma), with the
control (no mass) at each gamma for the readings tool. The worlds are
written by `make_worlds.py` from series K's generator (the one copy of the
fan, the beam and the screen), the pins before any run in
`expectations.json` (the one-wall note's section 6, from the lattice's
lines), the readings by `tools/lensing_readings.py` against each folder's
control.

| World | gamma | f | M | b | pinned shift, pixels (DETECTOR) | pinned delay, intervals (DETECTOR) |
| --- | --- | --- | --- | --- | --- | --- |
| `control_g0.json`, `control_g1.json` | 0, 1 | 1, 2 | - | - | 0 | 0 |
| `mass_g0.json` | 0 | 1 | 2^16 | 6 | -1.93 +- 0.5 | 2.68 +- 1 |
| `mass_g1.json` | 1 | 2 | 2^16 | 6 | -3.86 +- 0.5 | 5.36 +- 1 |
| `near_g0.json` | 0 | 1 | 2^16 | 3 | -2.42 +- 0.5 | 2.17 +- 1 |
| `near_g1.json` | 1 | 2 | 2^16 | 3 | -4.83 +- 0.5 | 4.34 +- 1 |

The number the run reads: the ratio of the two shifts (f = 2 over f = 1),
2.00 within 0.25.

## Run and read

```bash
python examples/events/optical/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/optical_g0 examples/events/optical/control_g0.json examples/events/optical/mass_g0.json examples/events/optical/near_g0.json
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/optical_g1 examples/events/optical/control_g1.json examples/events/optical/mass_g1.json examples/events/optical/near_g1.json
PYTHONPATH=src python tools/lensing_readings.py artifacts/optical_g0 --no-replay
PYTHONPATH=src python tools/lensing_readings.py artifacts/optical_g1 --no-replay
```

`tests/test_optical.py` pins the rule (the wall, the push and the turn,
the conservation of the momentum, the refusals, the byte identity without
the key) and the shipped worlds to the generator and the register.

## Measured (2026-09-21, one run on branch optical-v1, after the pins above)

DETECTOR, the screen's late window, each world against its folder's
control (the tool's own verdict columns compare with series K's pins and
are not this entry's):

| World | f | clicks in the window (control 1455) | centroid y, shift | width rms y, delta | mean age, delay | count ratio | light the mass took | pinned shift / delay | inside |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `mass_g0` | 1 | 1396 | 24.393, -1.607 | 3.343, +0.514 | 92.29, +2.89 | 0.9595 | 0 | -1.93 / 2.68 | yes / yes |
| `mass_g1` | 2 | 1385 | 22.188, -3.812 | 3.662, +0.833 | 95.27, +5.87 | 0.9519 | 0 | -3.86 / 5.36 | yes / yes |
| `near_g0` | 1 | 1456 | 20.008, -2.992 | 4.199, +1.371 | 91.80, +2.40 | 1.0007 | 0 | -2.42 / 2.17 | no (by 0.07) / yes |
| `near_g1` | 2 | 1122 | 18.346, -4.654 | 5.154, +2.326 | 94.37, +4.97 | 0.7711 | 398 | -4.83 / 4.34 | yes / yes |

The ratios f = 2 over f = 1: the delays 2.03 (`mass`) and 2.07 (`near`),
inside the pinned 2.00 +- 0.25; the shifts 2.37 (`mass`) and 1.56
(`near`), outside. The centroid in z 20.000 in every world (no deflection
off the mass's plane); the crowd at b (GAMEBOARD, the tool's replay of the
world): the presence 17.63 rays per Node and the age moment 181.8 at b = 6,
70.51 and 363.6 at b = 3.

**What the run decides.**

1. **The wall's coefficient is read as Shapiro's factor.** The delay
   doubles from f = 1 to f = 2 at both impact parameters (2.03, 2.07),
   the time part and the space part of the index 1 + (1 + gamma) k in one
   wall (verb 1).
2. **The turn bends the beam toward the mass at every f**, by 1.6 to 4.7
   pixels, the pins met to 0.5 pixel in three of the four worlds and
   missed by 0.07 in `near` at f = 1; at f = 2 the near beam is bent into
   the mass (398 clicks taken, the count ratio 0.77).
3. **The shift's factor is not read to 0.25 at this fan**: 2.37 and 1.56
   for the pinned 2.00. A single row turns whole fan steps when its whole
   momentum crosses a bisector (verb 3, the note's form, no dither), and
   the centroid of a beam of five directions moves in the fan's comb (the
   light-bending note's section 4): the grain of the reading is the fan's.
   Whether the fan is the design's to widen (the note's second pin at a
   denser fan) or the turn's to dither (the earlier design's wheel) is a
   question for the physicist through the Boss, not this run's.
