# The orbit series D under the law of the ray, on the plane

Six worlds of one base, written by `make_worlds.py`; the register entry is
[D, the orbit under the law of the ray, on the plane (2026-09-19)](../../../docs/EXPERIMENTS.md#d-the-orbit-under-the-law-of-the-ray-on-the-plane-2026-09-19)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
question: with the width of the push (the model owner's D1 of 2026-09-19,
the world key `width`, [RAY_LAW section 3](../../../docs/RAY_LAW.md#3-the-nodes-interval-nature_beam)
step 5), does a light free probe close an orbit about a heavy fixed source
under the measured push law, and how does its period scale with the radius?
A research run, made once, never a test; the derivation and the
expectations below were written before the runs; a reading outside its
expectation is reported with its numbers, never moved.

## The base

The plane of the coupling series: a board of 121 x 121 x 1 Nodes with the
z axis periodic (`"boundary": {"z": "periodic"}`), the centre c = (60, 60,
0), `"law": "rays"`, K 2^22, N 64, one free family `m` of charge 0 without
a phase circle (`"phase": false`), `suspension` 0 (the clock's count is not
read: the push law alone moves the probe), `width` S in 1, 8, 32. The
source is a fixed measured event of content M = 2^10 at c releasing on a
ballistic fan: every primitive in-plane direction (a, b, 0) with 0 < a^2 +
b^2 <= 8^2, 120 directions (116 declared in the world's table beyond the
four in-plane headings), uniform in angle to the grain of the lattice (the
primitive vectors of a square are twice as dense on the diagonals as on the
axes, a disk's are not). At `release` [1, 2^10 x 10] the source's clock
gives `by_clock(age, 2^10, 2^10 x 10)` = 1 ray per direction at the ages
10, 20, ...: one shell of 120 rays every 10 intervals, so the net emission
into the plane is q = 12 units per interval, exact in the mean, in bursts.
The probe is a free measured event of content m = 1 at (60 + r, 60, 0),
r = 12 or 24, with the default table (`read`: the push taken, the rays go
on) and the tangential momentum [0, p, 0] of the derivation below; its own
release (one ray per direction at the age 10240) never comes within a run
of 4000 intervals. The probe reads nothing of its own number; the source is
`fixed` and takes the probe's push into its momentum without stepping.

## The derivation of p, before the runs

The push per interval on a free measured event of content m is -m times
the net arrival flow of the other number at its Node (the one reading; the
`read` rule). Series C measured on this plane the flow through the ring at
radius r as flow x 2 pi r / q = 1.00 +- 0.10 in the ring mean (0.785 to
1.122 at r = 4 to 40; the mean 1.0075 over r >= 5;
[C under the law of the ray](../../../docs/EXPERIMENTS.md#c-the-couplings-under-the-law-of-the-ray-on-the-plane-2026-09-19),
item 5), Gauss's flux through the square 1.0000 q: a ballistic stream on
the plane falls as 1 / r. So the mean inward push per interval at r is

    F = m x q x C / (2 pi r),  C = 1 (taken; series C: 1.00 +- 0.10).

With the width S the probe steps on an axis whose momentum component is p
once per (S m + p) / p self-creations, the speed v = p / (S m + p) per axis
(every interval is a self-creation at `suspension` 0). A circular orbit
turns the momentum vector of magnitude p at the rate v / r per interval,
so it needs |dp/dt| = p v / r = F:

    p v = p^2 / (S m + p) = m q C / (2 pi),

independent of r: on the plane a 1 / r force gives the same speed at
every radius (a flat rotation curve) and T = 2 pi r / v proportional to r,
so T(24)^2 / T(12)^2 = (24 / 12)^2 = 4, the exponent k = 2 (Kepler's k = 3
of the 1 / r^2 force in space would give 8). With n = p / m (the
equivalence: the push per unit of flow is m, so n counts the units of flow
taken and the speed n / (S + n) does not depend on m) and A = q C /
(2 pi) = 12 / 6.2832 = 1.9099:

    n = (A + sqrt(A^2 + 4 S A)) / 2.

| S | n | p (the nearest whole) | v = p / (S + p) per axis | T(12) = 2 pi 12 / v | T(24) |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.635 | 3 | 0.750 | 101 | 201 |
| 8 | 4.979 | 5 | 0.385 | 196 | 392 |
| 32 | 8.831 | 9 | 0.220 | 343 | 687 |

What the derivation leaves to the run, each expected to show in the
readings:

- **The push's grain.** The momentum changes by whole units of m per
  arriving unit of flow, along the arrival Port's heading (+-x or +-y, not
  the radial direction): a momentum of p = n m points on one of the lattice
  vectors of length about n, so the orbit is a polygon. The field is
  bursty: one shell every 10 intervals brings to a Node at r about 120 x
  1.27 / (2 pi r) units (the lines through the Node: about 2 at r = 12,
  about 1 at r = 24), so the momentum turns by about 2 / n rad per shell
  at r = 12 (13 degrees at S = 32, 24 at S = 8, 40 at S = 1) and half that
  at r = 24, with 2 pi n units per orbit in all (57 at S = 32, from 34
  shells over T(12) = 343). At S = 1 the derived p = 3 is three grains and
  v = 0.75 per axis is faster than the rays (1 / sqrt 3 = 0.577): no
  closed orbit is expected at S = 1; the run shows what the push law does
  with it.
- **The field's granularity.** The fan's lines separate as r grows: near
  the axes the widest gap of the disk fan is between (1, 0) and (8, 1),
  7.1 degrees, 1.5 Links of arc at r = 12 and 3 at r = 24, so from r of
  about 16 on some ring Nodes lie on no line and the probe coasts across
  them; the kicks are where the lines are.
- **The flight's anisotropy.** The speed n / (S + n) is per axis: at
  45 degrees the components n / sqrt 2 give a Euclidean speed of n / (S +
  n / sqrt 2), faster than on the axes by (S + n) / (S + n / sqrt 2) (1.05
  at S = 32, 1.09 at S = 8, 1.17 at S = 1); and a step is at most one Link
  per interval, x before y, so a y step that falls in an interval with an x
  step is lost, nothing carried (rare at S = 32, about v_x v_y of the
  intervals; at S = 1 with equal components every y step is lost).

## The criteria, pinned before the runs

- A record check (fails the tool): every run completed, the books balanced
  at every tick.
- **Closed orbit**: read from the probe's `step` records, the angle about
  c unwrapped; at the first tick at which it reaches 2 pi, the probe is
  within one Link of its start on each axis (max(|dx|, |dy|) <= 1) and the
  y component of its momentum has the initial sign (+). Expected: closed
  at S = 32 at both radii and at S = 8 at both radii, within the grain
  above; not closed at S = 1.
- **The period T**: that tick; expected T(12) and T(24) of the table within
  +- 15 % (C = 1.00 +- 0.10 and the anisotropy of the speed).
- **The mean radius** over the first orbit: r +- 1 (the polygon's
  eccentricity from the whole p).
- **The drift per orbit**: the radius at the closing tick less the radius
  at the previous closing (the initial radius for the first): |drift| <= 1
  Link per orbit, the later orbits closing as the first.
- **The ratio** T(24)^2 / T(12)^2 = 4 +- 15 % (k = 2, the plane); 8 would
  be Kepler's k = 3.
- **The push read**: the mean inward push per interval over the run
  divided by m q / (2 pi r_mean) gives C; expected 1.00 +- 0.15.

## The worlds

| World | S | r | p | Intervals |
| --- | --- | --- | --- | --- |
| `s1_r12`, `s1_r24` | 1 | 12, 24 | 3 | 4000 |
| `s8_r12`, `s8_r24` | 8 | 12, 24 | 5 | 4000 |
| `s32_r12`, `s32_r24` | 32 | 12, 24 | 9 | 4000 |

Run them in parallel and read the records:

```bash
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/orbit examples/events/orbit/s*.json
PYTHONPATH=src python tools/orbit_readings.py artifacts/orbit
```

`tools/orbit_readings.py` prints the record checks, the table of the
readings (closed, T, the mean radius, the drift per orbit, the turns made,
the least and greatest radius, the reads, the units taken, C measured, how
the run ended) and the period ratios per width.

## The readings (2026-09-19)

Source fingerprint
`587cbf4852a7fafddc07b2ab35a6a530ed27607ea1aaaec8b17d89933e66d788`
(the worktree of `claude/universe24-new-3ytqde` at the D1 commit), Python
3.14, headless, four cores; every run completed in 5.5 to 6.4 s with the
books balanced at every tick; `tools/orbit_readings.py`: 12 record checks
passed, 0 failed, exit 0. The register entry marks every reading measured
against expected; the short of it:

| World | S | r | p | Closed | T (expected) | Mean radius | Drift per orbit | Reads / units | C on the first orbit | End |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `s1_r12` | 1 | 12 | 3 | no turn | - (101) | - | - | 0 / 0 | - | escaped through face:+y at tick 82 |
| `s1_r24` | 1 | 24 | 3 | no turn | - (201) | - | - | 0 / 0 | - | escaped through face:+y at tick 82 |
| `s8_r12` | 8 | 12 | 5 | no turn | - (196) | - | - | 18 / 66 | 0.49 (run) | beside the source, then escaped through face:+x at tick 275 |
| `s8_r24` | 8 | 24 | 5 | no | 825 (392) | 45.01 | +33.01 | 44 / 44 | 0.87 | escaped through face:+y at tick 978 |
| `s32_r12` | 32 | 12 | 9 | yes | 346 (343) | 13.83 | -1.00, +1.04, +16.96 | 217 / 296 | 1.13 | escaped through face:-y at tick 2396 |
| `s32_r24` | 32 | 24 | 9 | no | 541 (687) | 20.31 | -13.00, -5.00, +9.03 | 142 / 245 | 1.12 | escaped through face:+x at tick 1295 |

T(24)^2 / T(12)^2 at S = 32: 2.44 against 4 (k = 2) and Kepler's 8. One
orbit closes by the criterion (S = 32, r = 12: the turn in 346 intervals,
the return one Link off on x) and it is an eccentric loop (the radius at
eighths of the turn 12.0, 15.0, 18.8, 19.1, 18.4, 14.8, 10.0, 4.0, 11.0)
whose later turns wander and escape; the S = 1 probes outrun the field
(zero reads); the S = 8 probes spiral in or swing out; the r = 24 probe at
S = 32 falls inward. The mean push reads as derived (C 1.1 on the first
turns); the grain of the push, the bursts of the field, the empty source
at the start (no push for the first 31 intervals at r = 12) and the
flight's anisotropy break the orbit. `tests/test_orbit_world.py` pins the
one closing (the probe of `s32_r12` at (71, 60, 0) after 346 intervals).
