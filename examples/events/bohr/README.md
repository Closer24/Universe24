# Series H: Bohr's lines behind the detector

Seven worlds of one base, written by `make_worlds.py`; the register entry is
[H, Bohr's lines behind the detector (2026-09-20)](../../../docs/EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
question, in the model owner's words (Highlights 5.4, 2026-09-20): "Bohr
should come out by itself behind the detector; what is missing on the GameBoard
by the laws?" The answer taken: the tie between a body's momentum and its
phase, placed as parameters outside the GameBoard like the age ("On Bohr, go,
and put it as parameters outside the GameBoard like the age"): the electron is
a body on a set of three Nodes (`span`, [RAY_LAW note 30](../../../docs/RAY_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(i)) and turns its phase by its momentum at every Link it steps
(`phase_by_momentum` with the world's `action`, note 30 (ii)); the rays it
releases carry that phase to the open faces of the GameBoard, the `wave`
detectors that receive what comes out of the atom (the owner: "to show
atoms I do not need a detector; a detector receives their radiation, maybe,
if it comes out"). A research run, made once, never a test; the derivation
and the expectations below were written before the runs; a reading outside
its expectation is reported with its numbers, never moved. Every number is
one of two kinds ([the register](../../../docs/EXPERIMENTS.md), "Two kinds
of readings"): a DETECTOR reading (the faces' records, the electron's own
`read` records: the only kind reality has) or a GAMEBOARD reading (the
orbit, the design: the host's view of the mechanism).

## The base

An open cube of SIDE^3 Nodes, SIDE = 2 (r + 14) + 1 for the orbit of radius
r (33 for r = 2 up to 61 for r = 16), the centre c, `"law": "rays"`, K 2^30
(the clock's own turn 0 within a run), N 64, `suspension` 0 (the push alone
moves the electron), `width` 45120 (below). Two free families: `p`, the
proton (content M_p = 1836, `charge` [1, 1], no phase circle), and `e`, the
electron (content M_e = 1836, `charge` -15, a phase circle): the push on
the electron from a proton ray of amount 1 is M_e (rho_e rho_p - 1) x
label = -16 M_e x Q along the ray's unit vector, inward, electricity 15
times gravity (the physicist's series F ratio; nature's 2.3 x 10^39 is
beyond the bounded integers, the proportions are the contents'). The
proton is a fixed measured event at c releasing on the shell of the 2616
primitive directions with 1016 <= |D|^2 <= 1032 (the physicist's fan: the
in-plane orbit at r <= 16 reads the lines with |c| <= 1 of a fan of
|D| = 32), one ray per direction every 10 intervals (`release` [1, 18360]:
`by_clock(age, 1836, 18360)`). The electron is a free measured event at
(c + r, c, c) with the tangential momentum [0, p, 0], `span` [1, 1, 3]
(the body on the Nodes z = c - 1, c, c + 1: it reads the flux of three
planes of the fan, the grain of one Node averaged; the physicist measured
0 to 8 rays per shell around a mean of 4 at one Node), `phase_by_momentum`
true with the world's `action` h, its table the default (`read`: the push
taken, the rays go on), its `directions` the four in-plane headings +-X,
+-Y on which it releases one ray per direction every 10 intervals with its
phase (the same `release` key: its content equals the proton's so that
both release at the world's one rate; with the proton fixed the ratio of
the contents enters nothing, the push per unit of content and the step
per unit of content cancelling). Its rays carry its phase and no content
(a free release costs nothing: the orbit does not decay) and leave through
the four side faces, whose face detectors record the square of the
coherent pointer of what leaves each interval and whose `click` lines
carry every ray's phase, Node and tick: the far-face `wave` detector, no
measured event added to the GameBoard.

## The derivation, before the runs (GAMEBOARD readings of the design)

The flux the fan's lines deliver to the body at radius r on the ring of
the plane z = c is E_body(r) entries per shell, the sum over its three
Nodes of the entries per Node counted from the engine's own flight lines
(`nature_beam.flight_table`, the Bresenham lines the walk takes), averaged
around the ring. The push per interval is F = 16 M_e Q E_body(r) / 10; with
the width S the speed is v = p / (Q S M_e + p), and a circular orbit needs
p v / r = F, so with n = p / M_e and A = 16 Q E_body(r) r / 10

    n^2 / (Q S + n) = A,  n = (A + sqrt(A^2 + 4 Q S A)) / 2,  T = 2 pi r / v.

S = 45120 makes v = 0.06 on the reference orbit r = 8 (the physicist's
speed of series F). The turn by momentum turns the phase by |p_axis| N / h
per Link stepped on an axis, so over one orbit of a circle of radius r
stepped on the GameBoard the phase turns by (N / h) x sum over the Links of
|p_axis| = (N / h) x 4 p r (the Manhattan weighting of the path, 4 r
against the circle's 2 pi r), and closes on itself when

    4 p(r) r = j h,  j whole:

de Broglie's condition in the GameBoard's metric. With p proportional to
1 / sqrt(r) under a 1 / r^2 push the closing radii are proportional to
j^2, Bohr's ladder. The action is fixed so that j = 2 exactly on the
reference orbit: h = 16 p(8) = 5414584320. The fan's ring flux falls as
about r^-1.83 between r = 8 and 18 and is not smooth at r >= 13 (the
lines of a finite fan), so j = 3 falls between the GameBoard radii 15 and
16; both are run.

| r | E_body (entries per shell) | p (label units) | v | T | lumps per orbit (degrees each) | j = 4 p r / h | kind | GameBoard | intervals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 183.33 | 640000560 | 0.1077 | 117 | 12 (30.9) | 0.946 | closing (j = 1 within 0.1) | 33^3 | 3000 |
| 4 | 56.25 | 495197450 | 0.0854 | 294 | 29 (12.2) | 1.463 | between | 37^3 | 3000 |
| 6 | 23.60 | 389235874 | 0.0684 | 551 | 55 (6.5) | 1.725 | between | 41^3 | 3000 |
| 8 | 13.50 | 338411520 | 0.0600 | 838 | 84 (4.3) | 2.000 | closing (by construction) | 45^3 | 4200 |
| 12 | 6.59 | 288249497 | 0.0516 | 1462 | 146 (2.5) | 2.555 | between | 53^3 | 7400 |
| 15 | 4.29 | 259251483 | 0.0466 | 2022 | 202 (1.8) | 2.873 | between (j = 3 within 0.13) | 59^3 | 10200 |
| 16 | 4.50 | 274747992 | 0.0493 | 2040 | 204 (1.8) | 3.248 | between | 61^3 | 10300 |

## The criteria, pinned before the runs

- A record check (fails the tool): every run completed, the books balanced
  at every tick.
- **The orbit** (GAMEBOARD): closed when at the closing of the angle (the
  first tick at which the angle about the proton, unwrapped, reaches 2 pi)
  the electron is within r / 4 of its start; T within 15 % of the
  derivation; the phase's turn per orbit, the fraction of a circle beyond
  whole circles, measured from the body's phase at successive closings
  against the design's j - floor(j).
- **The coherent record** (DETECTOR, `tools/bohr_readings.py`): the clicks
  of the electron's rays on each side face, assigned to the turn in which
  the ray was released (the click's tick less the flight time of its
  heading from the centre's plane to the face, the engine's own
  `manhattan_steps`), summed per turn through the engine's own
  `coherent_pointer` into x_t; the cumulative pointer X_T = sum x_t, its
  square R_T the cumulative coherent record, and the coherence ratio
  C(T) = R_T / sum |x_t|^2, which is T when the phase closes every turn
  and stays about 1 or below when it does not. Expected: at a closing
  radius C(T) >= T / 2 after T >= 2 turns and the log-log slope of R_T
  against T near 2; between two whole j, C(T) < 2 and the slope at most
  about 1; the closing radii in the ratio of j^2. Fewer than two closed
  turns: no coherence reading, the finding is the orbit.

## The worlds

`r<r>.json` for r in 2, 4, 6, 8, 12, 15, 16 (the model ids
`rays-bohr-r<r>-space-v1`). Run them in parallel and read the records:

```bash
python examples/events/bohr/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 4 --out artifacts/bohr examples/events/bohr/r*.json
PYTHONPATH=src python tools/bohr_readings.py artifacts/bohr
```

Each run takes 20 to 90 s (the proton's 262 rays per interval); the
records are a few hundred megabytes per world.

## What was measured (2026-09-20)

No orbit closed well enough for the coherence reading and the finding is
registered as such: every electron was bound for one to three turns and
then thrown out at a close pass; at r = 8 (the reference, j = 2) the two
turns had the right mean radius (8.11, 7.95) and a period 14 % short of
the derivation (722, 736 against 838), returned 5 and 4 Links off the
start, wandered from r = 3 to 28, and the phase's turn per orbit measured
0.234 of a circle beyond whole circles where the design says 0; the
coherence over those two turns was C(2) = 0.84 (outside; expected at
least 1.0). Nothing was tuned; the numbers are in the register.
