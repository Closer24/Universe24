# The orbit series D under the Beam Law, on the plane

Six worlds of one base, written by `make_worlds.py`; the register entry is
[D, the orbit under the Beam Law, on the plane (2026-09-19)](../../../docs/EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
question: with the width of the push (the model owner's D1 of 2026-09-19,
the world key `width`, [BEAM_LAW section 3](../../../docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
step 5), does a light free probe close an orbit about a heavy fixed source
under the measured push law, and how does its period scale with the radius?
A research run, made once, never a test; the derivation and the
expectations below were written before the runs; a reading outside its
expectation is reported with its numbers, never moved.

## The base

The plane of the coupling series: a GameBoard of 121 x 121 x 1 Nodes with the
z axis periodic (`"boundary": {"z": "periodic"}`), the centre c = (60, 60,
0), `"law": "beam"`, K 2^22, N 64, one free family `m` of charge 0 without
a phase circle (`"phase": false`), `suspension` 0 (the clock's count is not
read: the push law alone moves the probe), `width` S in 1, 8, 32. The
source is a fixed measured event of content M = 2^10 at c releasing on a
ballistic fan: every primitive in-plane direction (a, b, 0) with 0 < a^2 +
b^2 <= 8^2, 120 directions (116 declared in the world's table beyond the
four in-plane headings), uniform in angle to the grain of the GameBoard (the
primitive vectors of a square are twice as dense on the diagonals as on the
axes, a disk's are not). At `release` [1, 2^10 x 10] the source's clock
gives `by_clock(age, 2^10, 2^10 x 10)` = 1 ray per direction at the ages
10, 20, ...: one shell of 120 rays every 10 intervals, so the net emission
into the plane is q = 12 units per interval, exact in the mean, in bursts.
The probe is a free measured event of content m = 1 at (60 + r, 60, 0),
r = 12 or 24, with the default table (`read`: the push taken, the rays go
on) and the tangential momentum [0, p, 0] of the derivation below (in
label units since 2026-09-19: 64 per unit of the probe's content); its own
release (one ray per direction at the age 10240) never comes within a run
of 4000 intervals. The probe reads nothing of its own number; the source is
`fixed` and takes the probe's push into its momentum without stepping.

## The derivation of p, before the runs

The push per interval on a free measured event of content m is the one
form of the law over the rays arriving at its Node ([BEAM_LAW section 3](../../../docs/BEAM_LAW.md#3-the-nodes-interval-nature_beam)
step 4): for an uncharged free source's rays, -m times their label
moment, the sum of amount x u_d over the arriving rays ([BEAM_LAW section
2](../../../docs/BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file):
the momentum of a ray is its label, since 2026-09-19 along the unit
vector u_d of its direction at the flight table's scale Q = 64, the
integer vector nearest Q D / |D|). A ray of any direction therefore
pushes Q units of momentum per unit of amount within 1.35 %, along its
own line (radial from the source within 0.8 degrees): a line crossing the
probe's ring delivers Q per ray, so the inward label flux through a ring
of radius r is Q x q x L per interval with L the fan's mean |u_d| / Q
(1.0000 over the 120 directions of this fan, 0.994 .. 1.009 per
direction; exactly 1 on the six headings of series C, whose flow x 2 pi r
/ q = 1.00 +- 0.10 in the ring mean with the flow read in units of Q,
Gauss's flux through the square 1.0000 q: a ballistic stream on the plane
falls as 1 / r). In units of one free unit's label, Q x m, the mean
inward push per interval at r is

    F = m x q x L x C / (2 pi r),  L = 1.0000 (the fan's mean |u_d| / Q),  C = 1 (taken; series C: 1.00 +- 0.10).

With the width S the probe steps on an axis whose momentum component is p
(label units) once per (Q S m + p) / p self-creations, the speed v = n /
(S + n) per axis with n = p / (Q m) (every interval is a self-creation at
`suspension` 0). A circular orbit turns the momentum vector of magnitude
p at the rate v / r per interval, so it needs |dp/dt| = p v / r = Q F:

    n v = n^2 / (S + n) = q L C / (2 pi),

independent of r: on the plane a 1 / r force gives the same speed at
every radius (a flat rotation curve) and T = 2 pi r / v proportional to r,
so T(24)^2 / T(12)^2 = (24 / 12)^2 = 4, the exponent k = 2 (Kepler's k = 3
of the 1 / r^2 force in space would give 8). With n in units of the
probe's content (the equivalence: the push per unit of label is m, so n
counts the labels taken and the speed n / (S + n) does not depend on m)
and A = q L C / (2 pi) = 12 / 6.2832 = 1.910:

    n = (A + sqrt(A^2 + 4 S A)) / 2,  the declared momentum p = 64 n.

| S | n | p (the nearest whole; label units) | v = n / (S + n) per axis | T(12) = 2 pi 12 / v | T(24) | Against the rays' 1 / sqrt 3 = 0.577 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2.635 | 3; 192 | 0.750 | 101 | 201 | faster: no closed orbit expected |
| 8 | 4.979 | 5; 320 | 0.385 | 196 | 392 | slower, marginal: a kick of 64 on 320 turns 11.5 degrees per ray (the first registration at this grain did not close) |
| 32 | 8.831 | 9; 576 | 0.220 | 343 | 687 | slower: closed expected within the grain, 6.4 degrees per ray |

The first registration (the D1 engine, the push the unit Link of a ray's
last step, L = 1, p = 3, 5, 9) and the second (the one push form with the
label along the integer direction D, L = 5.194 the fan's mean |D|, p =
11, 15, 23) are history in the register entry and in git at the D1 and
the one-form commits. What the derivation leaves to the run, each
expected to show in the readings:

- **The push's grain.** The momentum changes by the whole label of each
  arriving ray, 64 label units along the ray's own line, several rays at
  once when a shell passes; a momentum of 576 turns by 6.4 degrees per
  ray, so the orbit is a polygon with kicks along the fan's lines, radial
  within 0.8 degrees.
- **The field's granularity.** As before: the fan's lines separate as r
  grows (from r of about 16 on some ring Nodes lie on no line).
- **The flight's anisotropy.** As before: the speed n / (S + n) is per
  axis, a step at most one Link per interval, x before y.
- **The speed at S = 1.** The derived v exceeds the rays' speed, so the
  probe is expected to outrun the field, as the S = 1 probes did in the
  earlier registrations; at S = 8 the derived v is below the rays' for
  the first time.

## The criteria, pinned before the runs

- A record check (fails the tool): every run completed, the books balanced
  at every tick.
- **Closed orbit**: read from the probe's `step` records, the angle about
  c unwrapped; at the first tick at which it reaches 2 pi, the probe is
  within one Link of its start on each axis (max(|dx|, |dy|) <= 1) and the
  y component of its momentum has the initial sign (+). Expected: closed
  at S = 32 at both radii, within the grain above; not closed at S = 1 or
  S = 8.
- **The period T**: that tick; expected T(12) and T(24) of the table within
  +- 15 % (C = 1.00 +- 0.10 and the anisotropy of the speed).
- **The mean radius** over the first orbit: r +- 1 (the polygon's
  eccentricity from the whole p).
- **The drift per orbit**: the radius at the closing tick less the radius
  at the previous closing (the initial radius for the first): |drift| <= 1
  Link per orbit, the later orbits closing as the first.
- **The ratio** T(24)^2 / T(12)^2 = 4 +- 15 % (k = 2, the plane); 8 would
  be Kepler's k = 3.
- **The push read**: the mean inward push per interval over the orbit
  divided by m q L / (2 pi r_mean) gives C; expected 1.00 +- 0.15.

## The worlds

| World | S | r | p (label units; units of m) | Intervals |
| --- | --- | --- | --- | --- |
| `s1_r12`, `s1_r24` | 1 | 12, 24 | 192; 3 | 4000 |
| `s8_r12`, `s8_r24` | 8 | 12, 24 | 320; 5 | 4000 |
| `s32_r12`, `s32_r24` | 32 | 12, 24 | 576; 9 | 4000 |

Run them in parallel and read the records:

```bash
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/orbit examples/events/orbit/s*.json
PYTHONPATH=src python tools/click_readings/orbit.py artifacts/orbit
```

`tools/click_readings/orbit.py` prints the record checks, the table of the
readings (closed, T, the mean radius, the drift per orbit, the turns made,
the least and greatest radius, the reads, the units taken, C measured
against m q L / (2 pi r), how the run ended) and the period ratios per
width.

## The lamp worlds `s32_r24_lamp` and `s32_r12_lamp` (2026-09-21, written before any run)

The two worlds [DERIVATIONS_BEAM 21.5](../../../docs/DERIVATIONS_BEAM.md#215-the-standard-and-the-new-rows-under-it)
row 58 (Kepler's three laws) named "to be written", on the Boss's order
after the model owner's record 333: series D's S = 32 worlds with one
change so that a detector reads the orbit, under the directional drive
(form B, [light_speed/FORM.md section 3](../../../docs/designs/light_speed/FORM.md#3-the-vector-form-that-inserts-c-into-the-bodies-one-flight-primitive-for-rows-and-bodies);
BEAM_LAW note 49). Written by the generator; every number below is printed
by the host map [lamp_orbits_map.py](../../../docs/designs/derivations_beam/lamp_orbits_map.py)
with its output [lamp_orbits_map.out](../../../docs/designs/derivations_beam/lamp_orbits_map.out),
whose one source of the fan, the emission, the momentum and the pace is
this generator. Every number is a GAMEBOARD reading of the design (derived
before the run) unless labelled the detector's expected reading; no run
(the runs by an experimenter on the Boss's order).

**What the two worlds declare** (the model ids
`rays-orbit-s32-r<r>-lamp-plane-v1`; everything not named here is
`s32_r<r>`'s). The probe is a body of the shipped free family `probe`
(charge 0, no phase circle: the same push as `m`, gravity alone) of
content 2^10, so that at the world's one `release` [1, 2^10 x 10] it
releases one row per direction of the same fan of 120 every 10 intervals,
as the source does (a probe of content 1 releases at the age 10240, beyond
the run; the dynamics per unit of content do not depend on the content:
the push per ray is one unit of n whatever m, and the pace reads n alone);
the source's table measures the probe's family (`{"probe": "measure"}`:
the probe's rows that reach the source's Node click there), and a
detector `source` of that one Node reads the count (`beam`, the family
having no phase circle). The momentum is the circular-orbit momentum
under the directional drive: the pace on a heading is `n Q / (Q S + n
T_D) = 64 n / (64 S + 110 n)` per unit of content in place of `n / (S +
n)`, so the circular condition `n v = A = q L C / (2 pi) = 1.910` reads
`64 n^2 = A (64 S + 110 n)`, n = 9.629 at S = 32, the nearest whole 10:
640 label units per unit of content (today's rule gave 9, 576), 655360
for the probe of content 2^10. The pace at n = 10 is 0.2033 Links per
interval (beta = 0.349 of the rows' 0.582; the kept 576 would give
0.1896); the kick of one ray is 64 on 640, 5.7 degrees.

| World | r | p (label units; per unit of content) | the pace | the analytic circle's T = 2 pi r / v | Intervals |
| --- | --- | --- | --- | --- | --- |
| `s32_r12_lamp` | 12 | 655360; 640 | 0.2033 | 371 | 4000 |
| `s32_r24_lamp` | 24 | 655360; 640 | 0.2033 | 742 | 4000 |

**The pins, restated from row 58 for these worlds.** The map integrates
the law's continuum limit on the plane with the declared n = 10 (the
smooth `1 / r` push of the fan's mean, the directional drive's pace, one
step per interval, the source unpushed): the whole n above the circle's
9.629 makes a near-circular rosette, not a circle.

- **The period T** (GAMEBOARD; the DETECTOR reading is the recurrence of
  the clicks' arrival direction through 2 pi): `s32_r24_lamp` 784
  intervals (the analytic 742 at n = 10; 21.5 wrote 795 at the kept 576),
  within the continuum's own margin of 9 percent that
  [12b.2](../../../docs/DERIVATIONS_BEAM.md#12b2-the-orbit-as-the-bond-the-registered-orbit-thrown)
  carries for the burst field and the fan's grain: 714 to 855;
  `s32_r12_lamp` 392 (371 analytic): 357 to 428.
- **The mean radius** (GAMEBOARD; DETECTOR: the clicks' ages, `r = age x
  c` per direction, the flight 24 Links x 110 / 64 = 41 intervals on a
  heading at r = 24, 21 at r = 12): 24.8 +- 1 (the extents 24.0 to 25.9)
  and 12.4 +- 1 (12.0 to 13.0).
- **The precession per radial period**, the angle between successive
  closest approaches less 360 degrees (GAMEBOARD; DETECTOR: the direction
  of the ages' minimum): -81 +- 15 degrees at both radii, the radial
  period 614 at r = 24 and 307 at r = 12. Row 58's -105 +- 15 is the
  plane's `1 / r` force under a Newtonian pace (the apsidal angle `pi /
  sqrt 2 = 127.3` degrees), which the map reproduces (-105.5); under the
  cap the pace grows more slowly than the momentum (the local exponent
  `d ln v / d ln n = 0.65` at n = 10, beta = 0.35; today's per-axis rule
  0.78 at n = 9, giving -90.5), the radial oscillation is faster against
  the turning and the apsidal angle is 139.7 degrees: the restatement is
  form B's, not the fan's. It holds for the near-circular loop these
  momenta make; a loop widened to eccentricity by the kicks reads its
  own precession (the registered `s32_r24` at the kept 576 under form B:
  a rosette from r = 10.6 to 67.5, -109.5 and -118.2 degrees), which the
  map does not pin.
- **The exponent**: `T(24) / T(12) = 2.00 +- 0.15` (the integrated 2.00;
  the plane's exponent 1; space's `3 / 2` would give 2.83).
- **The clicks** (the detector's expected readings): the probe's ray
  toward the source exists only where the probe's Node lies on a fan line
  through the source (its reduced direction within the fan's `|D| <= 8`),
  28 of the 68 ring Nodes at r = 12 and 16 of the 144 at r = 24; one shell
  every 10 intervals, so about 15 clicks per orbit of 37 shells at r = 12
  and about 8 per orbit of 74 at r = 24; each click's arrival direction is
  the probe's direction from the source reversed and its age the flight,
  so the clicks' directions turn through 2 pi in T and the ages' minimum
  points to the closest approach. Whether the count reading `beam` at a
  `measure` entry of a phase-less family records every arrival as a
  click is what the experimenter reads on the first shells; the `click`
  lines of `events.jsonl` carry the same rows either way.

**What refutes** (row 58's last column, for these worlds): a period
outside its bracket (form B's first-order slowing of the cap); a ratio
at 2.83 (space's exponent on the plane) or outside 2.00 +- 0.15; a
precession outside -81 +- 15 degrees (-105 would be the Newtonian
pace's, 0 a closed ellipse of the `1 / r^2` force and not the plane's
`1 / r`); a closed return within one Link is a circle's criterion and is
not expected. A record check as above (completed, the books balanced at
every tick); every reading registered inside or outside its pin and
never moved.

## The readings (2026-09-19, under the label along the unit vector)

Source fingerprint `0eaa589ab51cdc0a12a863cd23e535e1e8ac052e8b4f3f8facf30ef05a323c5a` (the worktree of
`claude/universe24-new-3ytqde` on the label commit), Python 3.14,
headless, four cores; the six worlds regenerated; every run completed in
3.9 to 6.1 s with the books balanced at every tick;
`tools/click_readings/orbit.py`: 12 record checks passed, 0 failed, exit 0.
The register entry marks every reading measured against expected; the
short of it (p in label units; C on the first turn):

| World | S | r | p | Closed (expected) | T (expected) | Mean radius | Drift per orbit | Turns | Reads / units | C | End |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `s1_r12` | 1 | 12 | 192 | no turn (no) | - (101) | - | - | 0.22 | 0 / 0 | - | escaped through face:+y at tick 82 |
| `s1_r24` | 1 | 24 | 192 | no turn (no) | - (201) | - | - | 0.19 | 0 / 0 | - | escaped through face:+y at tick 82 |
| `s8_r12` | 8 | 12 | 320 | no: the return (+5, 0) (no) | 198 (196) | 15.20 | +5.00 | 1.03 | 24 / 3783 | 1.54 | escaped through face:+x at tick 271 |
| `s8_r24` | 8 | 24 | 320 | no turn (no) | - (392) | - | - | 0.93 | 25 / 2425 | 0.25 (the run) | escaped through face:+x at tick 449 |
| `s32_r12` | 32 | 12 | 576 | no: the return (-4, 0) (yes) | 289 (343) | 11.25 | -4, -2, +3, +5, -6, +9, -15 | 6.74 | 307 / 49121 | 1.32 | escaped through face:-y at tick 2891 |
| `s32_r24` | 32 | 24 | 576 | no: the return (-13, 0) (yes) | 829 (687) | 28.27 | -13.00 | 1.46 | 77 / 8052 | 1.27 | escaped through face:-x at tick 1054 |

(superseded for the pushed worlds by the re-read below, 2026-09-20)
No orbit closes by the criterion (a return within one Link with the
heading kept). The S = 1 probes outrun the field; the S = 8 probe at
r = 12 makes one turn in 198 intervals (the derived 196) and leaves; the
S = 32 probe at r = 12, expected to close, is bound for 2891 intervals
and seven precessing turns (289, 189, 216, 333, 336, 328, 962 intervals;
the mean radius 11.25 on the first, within 12 +- 1; C 1.3 to 1.5) where
the second registration escaped after one turn at tick 470; the S = 32
probe at r = 24 turns once in 829 (687 derived) and falls in. The kick
per ray is now 64 label units along the ray's own line, radial within
0.8 degrees; what remains is the field's burst (one shell per 10
intervals) and the GameBoard granularity of the fan's lines. The two
earlier registrations (p = 3, 5, 9 under the D1 engine; p = 11, 15, 23
under the label along D) are history in the register entry and in git.

Under the contact through the table (2026-09-20) `s8_r12` alone
changes: at tick 174 the probe beside the source hands 251 of its y
momentum to it, the angle then reaches 1.00 turn without closing and
the probe leaves through face:+x at tick 260; the five other worlds are
byte-identical ([validation](../../../docs/VALIDATION.md#the-columns-the-lifetime-the-held-content-and-the-contact-through-the-table-the-66-example-worlds-compared---2026-09-20)).

## The readings (2026-09-19, the night; under the one push form; history)

Source fingerprint
`cc7815756f50640ad10582af461cf58267c424eb8182177e580d0b5eedbd4769`
(the worktree of `claude/universe24-new-3ytqde` on the one-form commits),
Python 3.14, headless, four cores; every run completed in 5.7 to 6.5 s
with the books balanced at every tick; `tools/click_readings/orbit.py`: 12
record checks passed, 0 failed, exit 0. The register entry marks every
reading measured against expected; the short of it:

| World | S | r | p | Closed (expected) | T (expected) | Mean radius | Drift per orbit | Reads / units | C on the first orbit | End |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `s1_r12` | 1 | 12 | 11 | no turn (no) | - (82) | - | - | 0 / 0 | - | escaped through face:+y at tick 67 |
| `s1_r24` | 1 | 24 | 11 | no turn (no) | - (165) | - | - | 0 / 0 | - | escaped through face:+y at tick 67 |
| `s8_r12` | 8 | 12 | 15 | no turn (no) | - (116) | - | - | 0 / 0 | - | escaped through face:+y at tick 94 |
| `s8_r24` | 8 | 24 | 15 | no turn (no) | - (231) | - | - | 0 / 0 | - | escaped through face:+y at tick 94 |
| `s32_r12` | 32 | 12 | 23 | no: the return (-2, 0) (yes) | 229 (180) | 17.30 | -2.00 | 38 / 404 | 1.43 | escaped through face:-x at tick 470 |
| `s32_r24` | 32 | 24 | 23 | no turn (yes) | - (361) | - | - | 28 / 221 | 0.30 (the run) | escaped through face:+x at tick 415 |

No orbit closes at any width: the S = 1 and S = 8 probes outrun the
field (zero reads); the S = 32 probe at r = 12 makes one eccentric turn
(the radius at eighths 12.0, 16.3, 25.5, 26.0, 22.0, 19.7, 13.9, 6.7,
10.0) in 229 intervals, returns two Links off and escapes; the S = 32
probe at r = 24 falls in to the Node beside the source and escapes. The
finding for the model owner: the magnitude of a fan ray's label grows
with the integer length |D| of its direction, the law as designed and an
open question ([BEAM_LAW section 10](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
note 21). The first registration (p = 3, 5, 9 under the engine of the D1
commit, fingerprint `587cbf48...`, one eccentric closing at S = 32, r =
12) is kept as history in the register entry.

## Re-read under the step drive (2026-09-20)

The S = 1 probes read the same (no push); the four others move differently
under the step drive (a body's count of Links is the whole part of the
distance its momentum has driven): `s8_r12` closes one turn (T 226,
return +7, C 1.65) and leaves at tick 571; `s8_r24` reverses and leaves
at 495; `s32_r12` closes two turns (T 474, 236) and leaves at 1568;
`s32_r24` closes by the criterion (the return (-1, +1), heading kept, T
623 against the derived 687, the mean radius 23.63) and again in 464
before leaving at 1849; T(24)^2 / T(12)^2 = 1.73 against 4. The register
entry has every number ([migration](../../../docs/MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).

## Re-read under the signed drive (2026-09-20)

The S = 1 probes read the same; the four others move differently under
the signed drive (record 126: the drive is the signed distance the
momentum has driven, a reversal first cancelling what was driven the
other way): no orbit closes by the criterion (the S = 32 probe at r = 24
returns 9 Links off at T 701, its closed return (-1, +1) under the
unsigned drive having been the reversal defect's kick back), but that
probe is bound for the whole run of 4000 intervals (four turns of 701 to
880, the mean radius 26 to 36) and T(24)^2 / T(12)^2 from the first turns
701 and 363 reads 3.73 against the expected 4; `s8_r12` closes the angle
five times and leaves at 917, `s32_r12` three times and leaves at 2004,
`s8_r24` does not turn. The register entry has every number and the
verdict re-read ([migration](../../../docs/MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).

## Re-read under the crossing rule (2026-09-21)

The section above describes the tree before the crossing rule (the step
before the law: a row and a body met once,
[migration](../../../docs/MIGRATION.md#the-crossing-rule-on-2026-09-21-the-step-before-the-law-a-row-and-a-body-met-once-the-key-doppler-and-the-grain-deleted)).
Under it the S = 32 probes move again, the worlds unchanged: `s32_r12`
closes the angle once (T 525, the return (-11, 0), heading kept, the mean
radius 17.90, C 1.87) and leaves through face:-x at 932 (three closings
and the exit at 2004 before); `s32_r24` closes the angle once (T 932, the
return (+8, 0), the mean radius 34.16, C 1.29) and leaves through face:-x
at 1239 (bound for the whole run before); T(24)^2 / T(12)^2 = 3.15
against 4 (3.73 before); no orbit closes by the criterion. T, the returns,
the radii and C are GameBoard readings (the probe's `step` and `read`
records); the exits are the face detectors' clicks. Measured once by the
auditor at main e42c49e5 and read the same by the tool on this tree;
nothing pinned, no pin moved. The register entry has the numbers
([EXPERIMENTS, D](../../../docs/EXPERIMENTS.md)).
