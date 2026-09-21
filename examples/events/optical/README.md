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

**What the run decides, in the order of the chief physicist's reading
(2026-09-21, record 483; the rule and the pins unchanged, no second run).**

1. **The wall's factor is read as Shapiro's** (DETECTOR): the delays'
   ratios f = 2 over f = 1 are 2.03 (`mass`) and 2.07 (`near`), inside the
   pinned 2.00 +- 0.25; the time part and the space part of the index
   1 + (1 + gamma) k in one wall (verb 1).
2. **The shifts are inside 0.5 pixel in three of the four worlds**
   (DETECTOR); `near` at f = 1 misses by 0.07 with the beam's width at
   b = 3 as the cause: the pin is one row on the lamp's line at b, while
   the beam's five directions pass the mass at b + (0, +-1.08, +-2.17)
   Links, and at b = 3 the inner rows at 0.83 and 1.92 Links turn 11 to
   18 degrees and pull the centroid.
3. **The shifts' ratio is not read at this fan** (DETECTOR 2.37 for
   `mass`, 1.56 for `near`): the fan's teeth near the heading are 0, 2.39
   and 4.76 degrees (the beam's own (24, +-1, 0) and (12, +-1, 0)), then
   11.31, 14.04 and 18.43, and the label steps at the bisectors 1.19, 3.58
   and 8.04 degrees; the pinned angles 4.25 and 8.48 degrees at b = 6 sit
   beside the bisectors, so `mass` at f = 1 is a mixture of rows ending at
   2.39 and 4.76 degrees (read -1.607 pixels) and at f = 2 of rows at 4.76
   and 11.31 (read -3.81): the ratio 2.37 is the comb's, right and not a
   bug. A fact of the pin as written: the ratio's bracket 0.25 was never
   derivable from the shifts' brackets (+-0.5 pixel each propagates to
   +-0.58 for `mass` and +-0.46 for `near` in quadrature), and 2.37 and
   1.56 lie inside the propagated brackets; the pin stays as written and
   refuted at 0.25, both said here.
4. **The `near` shift at f = 2 is a survivors' reading**: the 398 clicks
   the mass took are the inner rows, the survivors' centroid the outer
   beam's, so the near ratio 1.56 is the capture at f = 2 over the width at
   f = 1, not the comb.

The mechanism behind item 3, as the physicist read it: the rule as built
conserves **P** exactly and lets the position's error grow with the Links
walked (up to 1.5 pixels at the screen in the tooth between 4.76 and
11.31 degrees); the law's own generic form is the flight's, an accumulator
that bounds the position's error and acts when it crosses (the label's
Bresenham on the line of **P**), a change to verb 3 under this identity
that is the model owner's decision on his return, not this run's; a denser
fan is not the answer (the error still grows with the Links, at eight times
the host cost).

**The bounded diagnostic** (the physicist's, record 483; GAMEBOARD, never a
detector reading; `tools/optical_readings.py` on the runs' `state.json`,
the light rows at x >= 40 in the final state, **P** = Q d content **u**_D +
**W** off the row's label and its `push`): the mean transverse angle of
**P** about +x, negative toward the mass, `mass` -4.181 degrees at f = 1
and -8.680 at f = 2 (the pinned angles 4.25 and 8.48), `near` -6.854 and
-11.955 (99 rows at f = 2 for 122 at f = 1, the survivors); the ratios
2.076 (`mass`) and 1.744 (`near`), the arithmetic of verb 2 read back to
itself (2.00 by construction; `near`'s 1.744 the survivors' selection),
saying nothing about where the light arrives; per row the angle of **P**
against the label's, the mean +0.55 / -0.29 degrees (`mass`) and +0.57 /
+0.08 (`near`), the largest 3.0 to 4.2 degrees: the position's error the
comb leaves on a row.
