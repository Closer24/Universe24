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

The key reads the crowd twice, both at the row's own Node and less its
own number (the physics-rule review of 408cf719, record 494, S3): the
wall's age moment A before step 1, one interval retarded, and the turn's
flow **V** after the walk and the collision, the interval's own arrivals,
the crossing rule's set. The row's flight residue crosses a turn as the
time of its last Link, s' = (s x S_new) // S_old with S the Manhattan
length (the chief physicist's word, record 496), exact from a heading
(every first turn in these worlds); between two off-heading directions
the remainder under one unit of the accumulator, 1 / (2 Q d S_new) of an
interval (about 4 x 10^-8 here), is dropped: the one place the flight's
time is not exact, bounded by one unit per turn (whether that remainder
is carried at the price of a denominator per row is the model owner's
footnote on his return, not a blocker). The count at the new wall is
capped at one Link by the primitive's `at_most` with the surplus kept.

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
the key) and the shipped worlds to the generator and the register. The
key is refused at load beside the key `massive_rows`: the composed flight
of massive rows under the optical key is not reviewed (the physics-rule
review of f4138855, record 510); a world declares one of the two.

## Measured (2026-09-21, the first run on branch optical-v1, after the pins above; the re-read after the review's M1 below)

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

## Re-read after M1 of the physics-rule review (2026-09-21, the fixed head)

The review of 408cf719 (docs/designs/optical_v1/REVIEW_408CF719.md,
record 494) found the junction of verb 1 and verb 3 undeclared: the walk
capped its count after the primitive and kept the residue of the uncapped
count, and the turn carried the residue in the old direction's units. The
fixed head caps the count by the primitive's own `at_most` with the surplus
kept and rescales the residue at a turn as the time of the last Link,
s' = (s x S_new) // S_old (the chief physicist's word, record 496;
`tests/test_optical.py` (g) and (h)). The six worlds run again on it
(`tools/run_series.py --jobs 2`, 400 intervals) and read by the same tools;
the two controls byte identical to the first run (no crowd, no turn; the
state 96d9aa366dce), the four mass worlds moved. DETECTOR, the first run's
value beside each new one as "was":

| World | f | clicks in the window (control 1455) | centroid y, shift | width rms y, delta | mean age, delay | count ratio | light the mass took | pinned shift / delay | inside |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `mass_g0` | 1 | 1398 (was 1396) | 24.378, -1.622 (was -1.607) | 3.330, +0.502 (was +0.514) | 92.37, +2.97 (was +2.89) | 0.9608 (was 0.9595) | 0 (was 0) | -1.93 / 2.68 | yes / yes |
| `mass_g1` | 2 | 1389 (was 1385) | 22.195, -3.805 (was -3.812) | 3.665, +0.836 (was +0.833) | 95.28, +5.88 (was +5.87) | 0.9546 (was 0.9519) | 0 (was 0) | -3.86 / 5.36 | yes / yes |
| `near_g0` | 1 | 1455 (was 1456) | 20.000, -3.000 (was -2.992) | 4.195, +1.367 (was +1.371) | 91.80, +2.40 (was +2.40) | 1.0000 (was 1.0007) | 0 (was 0) | -2.42 / 2.17 | no (by 0.08; was by 0.07) / yes |
| `near_g1` | 2 | 1001 (was 1122) | 19.726, -3.274 (was -4.654) | 4.467, +1.638 (was +2.326) | 93.91, +4.51 (was +4.97) | 0.6880 (was 0.7711) | 547 (was 398) | -4.83 / 4.34 | no (by 1.06; was yes) / yes |

The ratios f = 2 over f = 1: the delays 1.98 (`mass`, was 2.03) and 1.88
(`near`, was 2.07), both inside the pinned 2.00 +- 0.25; the shifts 2.35
(`mass`, was 2.37) and 1.09 (`near`, was 1.56), outside. The centroid in z
20.000 in every world, as before.

Against the physicist's four items above: (1) the delays' ratios stay
inside the bracket, the wall's factor still read as Shapiro's; (2) the
shifts are inside 0.5 pixel in two of the four worlds, not three: `mass`
at both f as before, `near` at f = 1 outside by 0.08 (was 0.07, the beam's
width at b = 3 as before), and `near` at f = 2 now outside by 1.06 pixel
(was inside by 0.18); (3) the shifts' ratio stays unread at this fan
(`mass` 2.35, the comb's; `near` 1.09, the survivors'); (4) `near` at
f = 2 is the survivors' reading more than before: the mass takes 547 of
the beam's clicks (was 398), the survivors the outer beam, its centroid
less deflected. The four `mass` readings and `near` at f = 1 moved by
hundredths, as the reviewer's counterexample tree had them (his residue
scaled by T_new / T_old: -1.622 / -3.806 and -3.000 / -4.408 pixels, the
delays 2.96 / 6.04 and 2.60 / 5.15); `near` at f = 2 moved by more than a
pixel under the physicist's rule, S_new / S_old, which differs from the
T ratio by 3.3 per cent in the plane's near fan, where every turn of this
world happens ((1, 0, 0) to (24, +-1, 0): T / S 110 against 106.5; a
heading-to-diagonal turn's 1.72 is a diagonal's, not this world's). The
cause of the pixel's move is the capture threshold, not a sensitivity of
the deflection to the residue rule (the chief physicist, record 505;
DETECTOR): the mass takes 547 clicks, 94 per cent of the two inner
directions' 582, against 415, 1.4 directions, under the T ratio; the
pixel's move is a capture count. No pin was changed and no second rule
entered; the reading is recorded as it is.

The bounded diagnostic re-read (GAMEBOARD, `tools/optical_readings.py`,
the first run's value as "was"): the mean transverse angle of **P**
`mass` -4.203 / -8.976 degrees (was -4.181 / -8.680; the ratio 2.136, was
2.076), `near` -6.993 / -8.277 (was -6.854 / -11.955; the ratio 1.184,
was 1.744; 80 rows at f = 2 for 122 at f = 1, was 99 for 122); per row
the angle of **P** against the label's, the mean +0.53 / -0.52 degrees
(`mass`, was +0.55 / -0.29) and +0.48 / -0.35 (`near`, was +0.57 /
+0.08), the largest 1.7 to 3.6 degrees (was 3.0 to 4.2).

## Re-read under verb 3's form by Bresenham with the momentum's pace (2026-09-22, branch optical-v1-bresenham)

The model owner's GO (record 536): verb 3's label follows the line of
**P** by Bresenham (the error accumulator `cross`, the label chosen among
D and its fan neighbours by the next Link's |**c** + **h** x **P**|^2);
the chief physicist's word on the build's first reading (DERIVED): a
pushed row's pace is its momentum's, the pair (S_1(P), T(P)) of the
primitive **P** in the wall and the residue rescaled by S_1(P') / S_1(P)
at every push. The one truncation of the flight's time is now per push
rather than per turn: the sub-unit remainder of that rescale, under
1 / (2 Q d S_1(P)) of an interval (about 10^-13 here), dropped; whether
it is carried at the price of a denominator per row stays the model
owner's footnote. The six worlds run on the head (`tools/run_series.py
--jobs 2`, 400 intervals), read by the same tools; the two controls byte
identical to the first run (no crowd, no push), the four mass worlds
moved. DETECTOR, the M1 re-read's value beside each new one as "was":

| World | f | clicks in the window (control 1455) | centroid y, shift | width rms y, delta | mean age, delay | count ratio | light the mass took | pinned shift / delay | inside |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `mass_g0` | 1 | 1347 (was 1398) | 24.007, -1.993 (was -1.622) | 2.839, +0.010 (was +0.502) | 92.35, +2.95 (was +2.97) | 0.9258 (was 0.9608) | 0 (was 0) | -1.93 / 2.68 | yes / yes |
| `mass_g1` | 2 | 1394 (was 1389) | 22.011, -3.989 (was -3.805) | 2.848, +0.020 (was +0.836) | 94.50, +5.10 (was +5.88) | 0.9581 (was 0.9546) | 0 (was 0) | -3.86 / 5.36 | yes / yes |
| `near_g0` | 1 | 1453 (was 1455) | 20.392, -2.608 (was -3.000) | 4.124, +1.296 (was +1.367) | 92.39, +2.99 (was +2.40) | 0.9986 (was 1.0000) | 0 (was 0) | -2.42 / 2.17 | yes (by 0.19; was no) / yes |
| `near_g1` | 2 | 1452 (was 1001) | 16.588, -6.412 (was -3.274) | 5.677, +2.848 (was +1.638) | 95.60, +6.20 (was +4.51) | 0.9979 (was 0.6880) | 0 (was 547) | -4.83 / 4.34 | no (by 1.08) / no (by 0.86) |

The ratios f = 2 over f = 1: the shifts 2.00 (`mass`, 3.989 / 1.993 =
2.0015, was 2.35: the law's 2.00 within 0.25, read for the first time)
and 2.46 (`near`, was 1.09), the delays 1.73 (`mass`, 5.10 / 2.95, was
1.98; outside 2.00 +- 0.25 by 0.02) and 2.07 (`near`, was 1.88). The
centroid in z 20.000 in every world; the mass takes no light in any of
the four (was 547 in `near` at f = 2): the rows along **P**'s line pass
it, and `near` at f = 2 reads the whole beam, no longer a survivors'
reading. What the re-read decides, in the physicist's order: (1) the
wall's factor as Shapiro's, the mass delays 2.95 / 5.10 inside the pins
2.68 / 5.36 +- 1, `near`'s 2.99 inside 2.17 +- 1 and 6.20 outside
4.34 +- 1 by 0.86; the mass delays' ratio 1.73 leaves 2.00 +- 0.25 by
0.02, the reading that decides, recorded as it is; (2) the shifts inside
0.5 pixel in three of four, `near` at f = 1 now inside (was outside by
0.08) and `near` at f = 2 outside by 1.08 (the beam bent more than the
one-line pin at b = 3); (3) the shifts' ratio read at this fan: `mass`
2.00, the comb gone; `near` 2.46 (the beam's width at b = 3). No pin was
changed; a pin the run does not meet is reported with the engine's
number. The head before the physicist's word (c0e8187, the label's pace
on **P**'s line) read the mass shifts -1.794 / -3.966 (2.21) and the
delays -1